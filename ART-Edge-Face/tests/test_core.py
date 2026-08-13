"""Unit tests — no camera / OpenVINO GPU required."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from edge_face.config import load_config
from edge_face.pipeline.ingestion import apply_roi
from edge_face.pipeline.matching import VectorGallery
from edge_face.pipeline.recognition import l2_normalize
from edge_face.storage.sqlite_store import EventStore, FaceEvent
from edge_face.sync.hq_client import SyncWorker


def _write_config(tmp: Path) -> Path:
    cfg = {
        "branch_id": "TEST-01",
        "confidence_threshold": 0.75,
        "cameras": [
            {
                "camera_id": "cam-1",
                "rtsp_url": "rtsp://example/stream",
                "enabled": True,
                "fps_target": 4,
                "roi": {"x": 0.1, "y": 0.1, "w": 0.5, "h": 0.5},
            }
        ],
        "models": {
            "detection": {"name": "yunet", "xml_path": "models/det.xml"},
            "recognition": {"name": "mobilefacenet", "xml_path": "models/rec.xml", "embedding_dim": 128},
            "device": "CPU",
        },
        "matching": {"backend": "numpy", "gallery_path": "data/gallery.json"},
        "hq": {"api_base_url": "http://127.0.0.1:9", "webhook_path": "/edge/face-events"},
        "storage": {"sqlite_path": str(tmp / "edge.db")},
        "service": {"log_level": "WARNING", "log_dir": str(tmp / "logs")},
    }
    path = tmp / "config.json"
    path.write_text(json.dumps(cfg), encoding="utf-8")
    return path


def test_load_config_clamps_threshold(tmp_path: Path):
    path = _write_config(tmp_path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["confidence_threshold"] = 0.5
    path.write_text(json.dumps(raw), encoding="utf-8")
    cfg = load_config(path)
    assert cfg.confidence_threshold == 0.75
    assert cfg.branch_id == "TEST-01"
    assert cfg.enabled_cameras[0].roi.w == pytest.approx(0.5)


def test_apply_roi_crop():
    from edge_face.config import RoiConfig

    frame = np.zeros((100, 200, 3), dtype=np.uint8)
    frame[10:60, 20:120] = 255
    crop = apply_roi(frame, RoiConfig(0.1, 0.1, 0.5, 0.5))
    assert crop.shape[0] == 50
    assert crop.shape[1] == 100


def test_gallery_match_cosine():
    dim = 128
    gallery = VectorGallery(embedding_dim=dim, backend="numpy")
    target = l2_normalize(np.random.randn(dim).astype(np.float32))
    other = l2_normalize(np.random.randn(dim).astype(np.float32))
    gallery.load_entries(
        [
            {"user_id": "U1", "display_name": "Alice", "embedding": target.tolist()},
            {"user_id": "U2", "display_name": "Bob", "embedding": other.tolist()},
        ]
    )
    hit = gallery.match(target, threshold=0.75)
    assert hit is not None
    assert hit.user_id == "U1"
    assert hit.score >= 0.99

    # Orthogonal-ish random vector should not meet a very high threshold reliably;
    # assert best-against-self still wins when querying target.
    hit2 = gallery.match(l2_normalize(target * 0.5 + other * 0.01), threshold=0.5)
    assert hit2 is not None
    assert hit2.user_id == "U1"


def test_event_store_offline_and_dedupe(tmp_path: Path):
    store = EventStore(tmp_path / "t.db")
    ev = FaceEvent("B1", "known_match", 1_000.0, 0.9, "cam-1", "U1", None, "Alice")
    assert store.should_emit("cam-1", "U1", 1_000.0, 30) is True
    assert store.should_emit("cam-1", "U1", 1_010.0, 30) is False
    assert store.should_emit("cam-1", "U1", 1_040.0, 30) is True
    store.enqueue(ev, synced=False)
    pending = store.pending(10)
    assert len(pending) == 1
    assert pending[0][1]["user_id"] == "U1"
    assert pending[0][1]["event_type"] == "known_match"
    store.mark_synced([pending[0][0]])
    assert store.pending_count() == 0


def test_sync_worker_queues_when_hq_down(tmp_path: Path, monkeypatch):
    store = EventStore(tmp_path / "t.db")

    class FakeClient:
        def post_event(self, payload):
            return False

    worker = SyncWorker(store, FakeClient())  # type: ignore[arg-type]
    worker.publish(FaceEvent("B1", "known_match", 1.0, 0.88, "cam-2", "U9"))
    assert store.pending_count() == 1


def test_face_event_payload_size():
    ev = FaceEvent(
        "HN-001",
        "unknown_face",
        1710000000.123,
        0.0,
        "cam-entrance-01",
        None,
        "UNK-0001",
        None,
        {"bbox": {"cx": 0.2, "cy": 0.4}},
    )
    payload = json.dumps(ev.to_payload())
    assert len(payload.encode("utf-8")) < 1024


def test_unknown_event_payload_has_null_user_id():
    ev = FaceEvent("B1", "unknown_face", 2.0, 0.0, "cam-1", None, "UNK-1")
    payload = ev.to_payload()
    assert payload["event_type"] == "unknown_face"
    assert payload["user_id"] is None
    assert payload["unknown_face_id"] == "UNK-1"
