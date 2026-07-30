"""Face embedding via OpenVINO MobileFaceNet / ArcFace-MobileNetV2."""

from __future__ import annotations

import logging
from pathlib import Path

import cv2
import numpy as np

log = logging.getLogger("edge_face.recognition")


def l2_normalize(vec: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    norm = float(np.linalg.norm(vec))
    if norm < eps:
        return vec.astype(np.float32)
    return (vec / norm).astype(np.float32)


class FaceEmbedder:
    def __init__(
        self,
        model_path: str | Path,
        embedding_dim: int = 128,
        device: str = "GPU",
        input_size: tuple[int, int] = (112, 112),
    ):
        self.model_path = Path(model_path)
        self.embedding_dim = embedding_dim
        self.device = device
        self.input_size = input_size
        self._compiled = None
        self._input_name: str | None = None
        self._output_name: str | None = None
        self._target_device = device

    def load(self) -> None:
        if not self.model_path.exists():
            raise FileNotFoundError(f"Recognition model not found: {self.model_path}")

        from openvino import Core

        core = Core()
        model = core.read_model(str(self.model_path))
        devices = core.available_devices
        target = self.device if self.device in devices else ("GPU" if "GPU" in devices else "CPU")
        self._target_device = target
        self._compiled = core.compile_model(model, target)
        self._input_name = self._compiled.inputs[0].get_any_name()
        self._output_name = self._compiled.outputs[0].get_any_name()
        log.info(
            "Recognition model %s compiled on %s (dim=%s)",
            self.model_path.name,
            target,
            self.embedding_dim,
        )

    def preprocess(self, face_bgr: np.ndarray) -> np.ndarray:
        if face_bgr.size == 0:
            raise ValueError("Empty face crop")
        rgb = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb, self.input_size, interpolation=cv2.INTER_LINEAR)
        # MobileFaceNet typically expects [-1, 1] or ImageNet norm; use centered float.
        blob = (resized.astype(np.float32) - 127.5) / 127.5
        return blob.transpose(2, 0, 1)[np.newaxis]

    def embed(self, face_bgr: np.ndarray) -> np.ndarray:
        if self._compiled is None:
            self.load()
        assert self._compiled is not None
        blob = self.preprocess(face_bgr)
        result = self._compiled([blob])
        # InferRequest-like mapping or list
        if isinstance(result, dict):
            key = self._output_name or next(iter(result))
            raw = np.asarray(result[key]).reshape(-1)
        else:
            raw = np.asarray(result[0]).reshape(-1)
        if raw.shape[0] != self.embedding_dim:
            log.warning(
                "Embedding dim mismatch: got %s expected %s — trunc/pad",
                raw.shape[0],
                self.embedding_dim,
            )
            out = np.zeros(self.embedding_dim, dtype=np.float32)
            n = min(self.embedding_dim, raw.shape[0])
            out[:n] = raw[:n]
            raw = out
        return l2_normalize(raw.astype(np.float32))
