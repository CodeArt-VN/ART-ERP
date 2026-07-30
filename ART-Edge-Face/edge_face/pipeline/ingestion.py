"""RTSP sub-stream ingestion with ROI crop and FPS throttle."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Iterator

import cv2
import numpy as np

from edge_face.config import CameraConfig, RoiConfig

log = logging.getLogger("edge_face.ingestion")


@dataclass
class FramePacket:
    camera_id: str
    frame_bgr: np.ndarray
    captured_at: float
    full_shape: tuple[int, int, int]


def apply_roi(frame: np.ndarray, roi: RoiConfig) -> np.ndarray:
    h, w = frame.shape[:2]
    x0 = int(roi.x * w)
    y0 = int(roi.y * h)
    x1 = int((roi.x + roi.w) * w)
    y1 = int((roi.y + roi.h) * h)
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(w, x1), min(h, y1)
    if x1 <= x0 or y1 <= y0:
        return frame
    return frame[y0:y1, x0:x1]


class CameraIngestor:
    """Pull sub-stream only; never touch NVR main stream / recording path."""

    def __init__(self, camera: CameraConfig, reconnect_delay: float = 3.0):
        self.camera = camera
        self.reconnect_delay = reconnect_delay
        self._cap: cv2.VideoCapture | None = None
        self._next_ts = 0.0
        self._min_interval = 1.0 / max(1, camera.fps_target)

    def open(self) -> bool:
        self.close()
        # Prefer FFMPEG; CAP_PROP_BUFFERSIZE reduces latency / RAM on POS.
        cap = cv2.VideoCapture(self.camera.rtsp_url, cv2.CAP_FFMPEG)
        try:
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        except Exception:
            pass
        if not cap.isOpened():
            log.warning("Cannot open RTSP %s", self.camera.camera_id)
            cap.release()
            return False
        self._cap = cap
        log.info("Opened camera %s", self.camera.camera_id)
        return True

    def close(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    def read(self) -> FramePacket | None:
        now = time.monotonic()
        if now < self._next_ts:
            return None
        if self._cap is None and not self.open():
            time.sleep(self.reconnect_delay)
            return None

        assert self._cap is not None
        ok, frame = self._cap.read()
        if not ok or frame is None:
            log.warning("Read failed %s — reconnecting", self.camera.camera_id)
            self.close()
            time.sleep(self.reconnect_delay)
            return None

        self._next_ts = now + self._min_interval
        cropped = apply_roi(frame, self.camera.roi)
        return FramePacket(
            camera_id=self.camera.camera_id,
            frame_bgr=cropped,
            captured_at=time.time(),
            full_shape=frame.shape,
        )

    def frames(self) -> Iterator[FramePacket]:
        while True:
            packet = self.read()
            if packet is not None:
                yield packet
            else:
                time.sleep(0.01)
