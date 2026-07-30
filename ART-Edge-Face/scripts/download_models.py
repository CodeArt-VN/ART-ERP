#!/usr/bin/env python3
"""Download YuNet ONNX into models/ (recognition IR must be supplied by ART ML pack)."""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"

YUNET_URL = (
    "https://github.com/opencv/opencv_zoo/raw/main/models/"
    "face_detection_yunet/face_detection_yunet_2023mar.onnx"
)


def main() -> int:
    MODELS.mkdir(parents=True, exist_ok=True)
    dest = MODELS / "face-detection-yunet-2023mar.onnx"
    if dest.exists():
        print(f"Already present: {dest}")
    else:
        print(f"Downloading YuNet → {dest}")
        try:
            urllib.request.urlretrieve(YUNET_URL, dest)
        except Exception as exc:
            print(f"Download failed: {exc}", file=sys.stderr)
            return 1
        print("OK")

    rec = MODELS / "mobilefacenet-arcface.xml"
    if not rec.exists():
        print(
            "NOTE: Place MobileFaceNet OpenVINO IR as "
            "models/mobilefacenet-arcface.xml (+ .bin). "
            "Not auto-downloaded (license / internal pack)."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
