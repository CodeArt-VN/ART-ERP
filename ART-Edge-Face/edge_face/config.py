"""Load and validate edge_face config.json."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RoiConfig:
    x: float
    y: float
    w: float
    h: float

    def clamp(self) -> "RoiConfig":
        x = min(max(self.x, 0.0), 1.0)
        y = min(max(self.y, 0.0), 1.0)
        w = min(max(self.w, 0.0), 1.0 - x)
        h = min(max(self.h, 0.0), 1.0 - y)
        return RoiConfig(x=x, y=y, w=w, h=h)


@dataclass(frozen=True)
class CameraConfig:
    camera_id: str
    rtsp_url: str
    enabled: bool = True
    fps_target: int = 4
    roi: RoiConfig = field(default_factory=lambda: RoiConfig(0.0, 0.0, 1.0, 1.0))


@dataclass(frozen=True)
class DetectionModelConfig:
    name: str
    xml_path: str
    score_threshold: float = 0.6
    nms_threshold: float = 0.3
    input_size: tuple[int, int] = (320, 320)


@dataclass(frozen=True)
class RecognitionModelConfig:
    name: str
    xml_path: str
    embedding_dim: int = 128


@dataclass(frozen=True)
class ModelsConfig:
    detection: DetectionModelConfig
    recognition: RecognitionModelConfig
    device: str = "GPU"
    num_requests: int = 1


@dataclass(frozen=True)
class MatchingConfig:
    backend: str = "faiss"
    gallery_path: str = "data/gallery.json"
    metric: str = "cosine"
    top_k: int = 1


@dataclass(frozen=True)
class HqConfig:
    api_base_url: str
    webhook_path: str = "/edge/face-events"
    gallery_sync_path: str = "/edge/face-gallery"
    timeout_seconds: float = 5.0
    retry_max: int = 3
    api_key_env: str = "EDGE_FACE_API_KEY"

    @property
    def events_url(self) -> str:
        return self.api_base_url.rstrip("/") + self.webhook_path

    @property
    def gallery_url(self) -> str:
        return self.api_base_url.rstrip("/") + self.gallery_sync_path

    def api_key(self) -> str | None:
        return os.environ.get(self.api_key_env)


@dataclass(frozen=True)
class StorageConfig:
    sqlite_path: str = "data/edge_face.db"
    sync_batch_size: int = 50
    sync_interval_seconds: int = 30


@dataclass(frozen=True)
class ServiceConfig:
    poll_interval_ms: int = 50
    log_level: str = "INFO"
    log_dir: str = "logs"


@dataclass(frozen=True)
class AppConfig:
    branch_id: str
    confidence_threshold: float
    cameras: list[CameraConfig]
    models: ModelsConfig
    matching: MatchingConfig
    hq: HqConfig
    storage: StorageConfig
    service: ServiceConfig
    dedupe_window_seconds: int = 30
    config_path: Path | None = None

    @property
    def enabled_cameras(self) -> list[CameraConfig]:
        return [c for c in self.cameras if c.enabled][:3]


def _roi(raw: dict[str, Any] | None) -> RoiConfig:
    if not raw:
        return RoiConfig(0.0, 0.0, 1.0, 1.0)
    return RoiConfig(
        x=float(raw.get("x", 0.0)),
        y=float(raw.get("y", 0.0)),
        w=float(raw.get("w", 1.0)),
        h=float(raw.get("h", 1.0)),
    ).clamp()


def load_config(path: str | Path) -> AppConfig:
    cfg_path = Path(path).resolve()
    with cfg_path.open("r", encoding="utf-8") as fh:
        raw = json.load(fh)

    threshold = float(raw.get("confidence_threshold", 0.75))
    if threshold < 0.75:
        # Brief requires confidence >= 0.75; clamp to protect false accepts.
        threshold = 0.75

    cameras = [
        CameraConfig(
            camera_id=str(c["camera_id"]),
            rtsp_url=str(c["rtsp_url"]),
            enabled=bool(c.get("enabled", True)),
            fps_target=int(c.get("fps_target", 4)),
            roi=_roi(c.get("roi")),
        )
        for c in raw.get("cameras", [])
    ]
    if not cameras:
        raise ValueError("config.cameras must contain at least one camera")

    det = raw["models"]["detection"]
    rec = raw["models"]["recognition"]
    input_size = det.get("input_size", [320, 320])

    return AppConfig(
        branch_id=str(raw["branch_id"]),
        confidence_threshold=threshold,
        dedupe_window_seconds=int(raw.get("dedupe_window_seconds", 30)),
        cameras=cameras,
        models=ModelsConfig(
            detection=DetectionModelConfig(
                name=str(det.get("name", "yunet")),
                xml_path=str(det["xml_path"]),
                score_threshold=float(det.get("score_threshold", 0.6)),
                nms_threshold=float(det.get("nms_threshold", 0.3)),
                input_size=(int(input_size[0]), int(input_size[1])),
            ),
            recognition=RecognitionModelConfig(
                name=str(rec.get("name", "mobilefacenet")),
                xml_path=str(rec["xml_path"]),
                embedding_dim=int(rec.get("embedding_dim", 128)),
            ),
            device=str(raw["models"].get("device", "GPU")),
            num_requests=int(raw["models"].get("num_requests", 1)),
        ),
        matching=MatchingConfig(
            backend=str(raw.get("matching", {}).get("backend", "faiss")),
            gallery_path=str(raw.get("matching", {}).get("gallery_path", "data/gallery.json")),
            metric=str(raw.get("matching", {}).get("metric", "cosine")),
            top_k=int(raw.get("matching", {}).get("top_k", 1)),
        ),
        hq=HqConfig(
            api_base_url=str(raw["hq"]["api_base_url"]),
            webhook_path=str(raw["hq"].get("webhook_path", "/edge/face-events")),
            gallery_sync_path=str(raw["hq"].get("gallery_sync_path", "/edge/face-gallery")),
            timeout_seconds=float(raw["hq"].get("timeout_seconds", 5)),
            retry_max=int(raw["hq"].get("retry_max", 3)),
            api_key_env=str(raw["hq"].get("api_key_env", "EDGE_FACE_API_KEY")),
        ),
        storage=StorageConfig(
            sqlite_path=str(raw.get("storage", {}).get("sqlite_path", "data/edge_face.db")),
            sync_batch_size=int(raw.get("storage", {}).get("sync_batch_size", 50)),
            sync_interval_seconds=int(raw.get("storage", {}).get("sync_interval_seconds", 30)),
        ),
        service=ServiceConfig(
            poll_interval_ms=int(raw.get("service", {}).get("poll_interval_ms", 50)),
            log_level=str(raw.get("service", {}).get("log_level", "INFO")),
            log_dir=str(raw.get("service", {}).get("log_dir", "logs")),
        ),
        config_path=cfg_path,
    )


def resolve_path(base: Path | None, relative: str) -> Path:
    p = Path(relative)
    if p.is_absolute():
        return p
    root = base.parent if base else Path.cwd()
    return (root / p).resolve()
