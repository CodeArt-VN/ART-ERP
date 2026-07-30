"""End-to-end edge processing loop: ingest → detect → embed → match → sync."""

from __future__ import annotations

import logging
import signal
import threading
import time
from hashlib import sha1
from pathlib import Path

from edge_face.config import AppConfig, resolve_path
from edge_face.pipeline.detection import FaceDetector
from edge_face.pipeline.ingestion import CameraIngestor
from edge_face.pipeline.matching import VectorGallery
from edge_face.pipeline.recognition import FaceEmbedder
from edge_face.storage.sqlite_store import EventStore, FaceEvent
from edge_face.sync.hq_client import HqClient, SyncWorker

log = logging.getLogger("edge_face.pipeline")


class EdgePipeline:
    def __init__(self, config: AppConfig):
        self.config = config
        self._stop = threading.Event()
        self._ingestors: list[CameraIngestor] = []
        self._detector: FaceDetector | None = None
        self._embedder: FaceEmbedder | None = None
        self._gallery = VectorGallery(
            embedding_dim=config.models.recognition.embedding_dim,
            backend=config.matching.backend,
        )
        base = config.config_path
        self._store = EventStore(resolve_path(base, config.storage.sqlite_path))
        self._sync = SyncWorker(
            self._store,
            HqClient(config.hq),
            batch_size=config.storage.sync_batch_size,
        )

    def load_models(self) -> None:
        base = self.config.config_path
        det_path = resolve_path(base, self.config.models.detection.xml_path)
        rec_path = resolve_path(base, self.config.models.recognition.xml_path)
        self._detector = FaceDetector(
            model_path=det_path,
            score_threshold=self.config.models.detection.score_threshold,
            nms_threshold=self.config.models.detection.nms_threshold,
            input_size=self.config.models.detection.input_size,
            device=self.config.models.device,
        )
        self._embedder = FaceEmbedder(
            model_path=rec_path,
            embedding_dim=self.config.models.recognition.embedding_dim,
            device=self.config.models.device,
        )
        # Lazy-load on first frame to allow service start even if models copied later;
        # still fail-fast if paths missing when explicitly loading.
        if not det_path.exists() or not rec_path.exists():
            log.error(
                "Model files missing. Place OpenVINO IR/ONNX under models/. "
                "det=%s rec=%s",
                det_path,
                rec_path,
            )
            raise FileNotFoundError("Detection/recognition models not found")
        self._detector.load()
        self._embedder.load()

    def load_gallery(self) -> None:
        path = resolve_path(self.config.config_path, self.config.matching.gallery_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        loaded = self._gallery.load_from_json(path)
        if loaded == 0:
            remote = self._sync.client.fetch_gallery(self.config.branch_id)
            if remote:
                self._gallery.load_entries(remote)
                self._persist_gallery(path, remote)

    def _persist_gallery(self, path: Path, entries: list[dict]) -> None:
        import json

        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            json.dump({"identities": entries}, fh)
        log.info("Persisted gallery (%s) → %s", len(entries), path)

    def start_cameras(self) -> None:
        self._ingestors = [CameraIngestor(cam) for cam in self.config.enabled_cameras]
        for ing in self._ingestors:
            ing.open()

    def stop(self) -> None:
        self._stop.set()
        for ing in self._ingestors:
            ing.close()

    def request_stop(self, *_args) -> None:
        log.info("Stop signal received")
        self.stop()

    def _unknown_face_id(self, camera_id: str, embedding, captured_at: float) -> str:
        rounded = ",".join(f"{v:.3f}" for v in embedding[:16])
        raw = f"{self.config.branch_id}|{camera_id}|{int(captured_at)}|{rounded}"
        return "UNK-" + sha1(raw.encode("utf-8")).hexdigest()[:16].upper()

    def _bbox_meta(self, box, frame_bgr) -> dict:
        h, w = frame_bgr.shape[:2]
        return {
            "det_score": box.score,
            "bbox": {
                "x1": box.x1,
                "y1": box.y1,
                "x2": box.x2,
                "y2": box.y2,
                "cx": round((box.x1 + box.x2) / 2 / w, 4),
                "cy": round((box.y1 + box.y2) / 2 / h, 4),
            },
            "frame_size": {"width": w, "height": h},
        }

    def process_frame(self, camera_id: str, frame_bgr, captured_at: float) -> int:
        assert self._detector is not None and self._embedder is not None
        faces = self._detector.detect(frame_bgr)
        emitted = 0
        for box in faces:
            crop = self._detector.crop(frame_bgr, box)
            if crop.size == 0:
                continue
            emb = self._embedder.embed(crop)
            match = self._gallery.match(
                emb,
                threshold=self.config.confidence_threshold,
                top_k=self.config.matching.top_k,
            )
            if match is None:
                unknown_face_id = self._unknown_face_id(camera_id, emb, captured_at)
                if not self._store.should_emit(
                    camera_id,
                    unknown_face_id,
                    captured_at,
                    self.config.dedupe_window_seconds,
                ):
                    continue
                event = FaceEvent(
                    branch_id=self.config.branch_id,
                    event_type="unknown_face",
                    user_id=None,
                    unknown_face_id=unknown_face_id,
                    timestamp=captured_at,
                    score=0.0,
                    camera_id=camera_id,
                    display_name=None,
                    meta=self._bbox_meta(box, frame_bgr),
                )
                self._sync.publish(event)
                emitted += 1
                log.info(
                    "UNKNOWN branch=%s unknown_face_id=%s cam=%s",
                    self.config.branch_id,
                    unknown_face_id,
                    camera_id,
                )
                continue
            if not self._store.should_emit(
                camera_id,
                match.user_id,
                captured_at,
                self.config.dedupe_window_seconds,
            ):
                continue
            event = FaceEvent(
                branch_id=self.config.branch_id,
                event_type="known_match",
                user_id=match.user_id,
                timestamp=captured_at,
                score=match.score,
                camera_id=camera_id,
                unknown_face_id=None,
                display_name=match.display_name,
                meta=self._bbox_meta(box, frame_bgr),
            )
            self._sync.publish(event)
            emitted += 1
            log.info(
                "MATCH branch=%s user=%s score=%.3f cam=%s",
                self.config.branch_id,
                match.user_id,
                match.score,
                camera_id,
            )
        return emitted

    def run(self, load_models: bool = True) -> None:
        signal.signal(signal.SIGINT, self.request_stop)
        signal.signal(signal.SIGTERM, self.request_stop)

        if load_models:
            self.load_models()
        self.load_gallery()
        self.start_cameras()
        log.info(
            "Edge pipeline running branch=%s cameras=%s gallery=%s threshold=%.2f",
            self.config.branch_id,
            len(self._ingestors),
            self._gallery.size,
            self.config.confidence_threshold,
        )

        poll = max(1, self.config.service.poll_interval_ms) / 1000.0
        while not self._stop.is_set():
            for ing in self._ingestors:
                packet = ing.read()
                if packet is None:
                    continue
                try:
                    self.process_frame(packet.camera_id, packet.frame_bgr, packet.captured_at)
                except Exception:
                    log.exception("Frame processing error cam=%s", packet.camera_id)
            self._sync.flush_pending(
                interval_seconds=self.config.storage.sync_interval_seconds
            )
            time.sleep(poll)

        log.info("Edge pipeline stopped. pending_offline=%s", self._store.pending_count())
