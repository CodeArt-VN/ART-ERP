"""HQ / ERP NAS webhook client + offline catch-up sync."""

from __future__ import annotations

import logging
import time
from typing import Any

import requests

from edge_face.config import HqConfig
from edge_face.storage.sqlite_store import EventStore, FaceEvent

log = logging.getLogger("edge_face.sync")


class HqClient:
    def __init__(self, cfg: HqConfig):
        self.cfg = cfg
        self._session = requests.Session()
        key = cfg.api_key()
        if key:
            self._session.headers["Authorization"] = f"Bearer {key}"
        self._session.headers["Content-Type"] = "application/json"
        self._session.headers["User-Agent"] = "ART-Edge-Face/0.1"

    def post_event(self, payload: dict[str, Any]) -> bool:
        try:
            resp = self._session.post(
                self.cfg.events_url,
                json=payload,
                timeout=self.cfg.timeout_seconds,
            )
            if 200 <= resp.status_code < 300:
                return True
            log.warning("HQ event rejected HTTP %s: %s", resp.status_code, resp.text[:200])
            return False
        except requests.RequestException as exc:
            log.warning("HQ unreachable: %s", exc)
            return False

    def fetch_gallery(self, branch_id: str) -> list[dict[str, Any]] | None:
        try:
            resp = self._session.get(
                self.cfg.gallery_url,
                params={"branch_id": branch_id},
                timeout=self.cfg.timeout_seconds,
            )
            if resp.status_code != 200:
                log.warning("Gallery sync HTTP %s", resp.status_code)
                return None
            data = resp.json()
            if isinstance(data, dict):
                return list(data.get("identities", []))
            if isinstance(data, list):
                return data
            return None
        except requests.RequestException as exc:
            log.warning("Gallery fetch failed: %s", exc)
            return None


class SyncWorker:
    """Online: fire-and-forget JSON ~1KB. Offline: SQLite then catch-up."""

    def __init__(self, store: EventStore, client: HqClient, batch_size: int = 50):
        self.store = store
        self.client = client
        self.batch_size = batch_size
        self._last_flush = 0.0

    def publish(self, event: FaceEvent) -> None:
        payload = event.to_payload()
        ok = self.client.post_event(payload)
        self.store.enqueue(event, synced=ok)
        if not ok:
            log.info("Queued offline event user=%s cam=%s", event.user_id, event.camera_id)

    def flush_pending(self, force: bool = False, interval_seconds: int = 30) -> int:
        now = time.time()
        if not force and (now - self._last_flush) < interval_seconds:
            return 0
        self._last_flush = now
        pending = self.store.pending(self.batch_size)
        if not pending:
            return 0
        synced_ids: list[int] = []
        for event_id, payload in pending:
            if self.client.post_event(payload):
                synced_ids.append(event_id)
            else:
                break
        if synced_ids:
            self.store.mark_synced(synced_ids)
            log.info("Synced %s offline events to HQ", len(synced_ids))
        return len(synced_ids)
