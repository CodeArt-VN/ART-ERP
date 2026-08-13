"""Face detection via OpenVINO (YuNet / DBFace IR)."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

log = logging.getLogger("edge_face.detection")


@dataclass
class FaceBox:
    x1: int
    y1: int
    x2: int
    y2: int
    score: float

    def clip(self, w: int, h: int) -> "FaceBox":
        return FaceBox(
            x1=max(0, min(self.x1, w - 1)),
            y1=max(0, min(self.y1, h - 1)),
            x2=max(0, min(self.x2, w)),
            y2=max(0, min(self.y2, h)),
            score=self.score,
        )

    @property
    def area(self) -> int:
        return max(0, self.x2 - self.x1) * max(0, self.y2 - self.y1)


class FaceDetector:
    """Prefer OpenCV YuNet (OpenVINO backend) — light enough for i3+UHD."""

    def __init__(
        self,
        model_path: str | Path,
        score_threshold: float = 0.6,
        nms_threshold: float = 0.3,
        input_size: tuple[int, int] = (320, 320),
        device: str = "GPU",
    ):
        self.model_path = Path(model_path)
        self.score_threshold = score_threshold
        self.nms_threshold = nms_threshold
        self.input_size = input_size
        self.device = device
        self._detector = None
        self._ov_compiled = None
        self._backend = "none"

    def load(self) -> None:
        if not self.model_path.exists():
            raise FileNotFoundError(f"Detection model not found: {self.model_path}")

        # YuNet ONNX / OpenCV FaceDetectorYN
        if self.model_path.suffix.lower() in {".onnx", ".xml"} or "yunet" in self.model_path.name.lower():
            try:
                self._detector = cv2.FaceDetectorYN.create(
                    str(self.model_path),
                    "",
                    self.input_size,
                    self.score_threshold,
                    self.nms_threshold,
                    5000,
                )
                # OpenCV may route to OpenVINO DNN when available.
                self._backend = "opencv_yunet"
                log.info("YuNet loaded via OpenCV FaceDetectorYN (%s)", self.model_path.name)
                return
            except Exception as exc:
                log.warning("FaceDetectorYN failed (%s); trying OpenVINO IR", exc)

        self._load_openvino_ir()

    def _load_openvino_ir(self) -> None:
        from openvino import Core

        core = Core()
        model = core.read_model(str(self.model_path))
        devices = core.available_devices
        target = self.device if self.device in devices else ("GPU" if "GPU" in devices else "CPU")
        self._ov_compiled = core.compile_model(model, target)
        self._backend = f"openvino:{target}"
        log.info("Detection IR compiled on %s", target)

    def detect(self, frame_bgr: np.ndarray) -> list[FaceBox]:
        if self._detector is None and self._ov_compiled is None:
            self.load()

        h, w = frame_bgr.shape[:2]
        if self._detector is not None:
            self._detector.setInputSize((w, h))
            _, faces = self._detector.detect(frame_bgr)
            boxes: list[FaceBox] = []
            if faces is None:
                return boxes
            for row in faces:
                x, y, bw, bh, score = row[:5]
                box = FaceBox(
                    x1=int(x),
                    y1=int(y),
                    x2=int(x + bw),
                    y2=int(y + bh),
                    score=float(score),
                ).clip(w, h)
                if box.area > 0 and box.score >= self.score_threshold:
                    boxes.append(box)
            return boxes

        return self._detect_ov(frame_bgr)

    def _detect_ov(self, frame_bgr: np.ndarray) -> list[FaceBox]:
        """Generic IR path — expects NMS already in graph or post-process hooks.

        Field builds should prefer YuNet ONNX for predictable boxes.
        """
        assert self._ov_compiled is not None
        h, w = frame_bgr.shape[:2]
        iw, ih = self.input_size
        resized = cv2.resize(frame_bgr, (iw, ih))
        blob = resized.transpose(2, 0, 1)[np.newaxis].astype(np.float32)
        out = self._ov_compiled([blob])
        # Without model-specific decode we return empty — keep POS safe.
        log.debug("Raw OV detection outputs: %s", list(out.keys()) if hasattr(out, "keys") else type(out))
        _ = (h, w)
        return []

    def crop(self, frame_bgr: np.ndarray, box: FaceBox, margin: float = 0.15) -> np.ndarray:
        h, w = frame_bgr.shape[:2]
        bw, bh = box.x2 - box.x1, box.y2 - box.y1
        mx, my = int(bw * margin), int(bh * margin)
        x1, y1 = max(0, box.x1 - mx), max(0, box.y1 - my)
        x2, y2 = min(w, box.x2 + mx), min(h, box.y2 + my)
        return frame_bgr[y1:y2, x1:x2]
