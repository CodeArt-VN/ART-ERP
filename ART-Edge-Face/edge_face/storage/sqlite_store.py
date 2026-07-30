"""SQLite offline event cache + pending sync queue."""

from __future__ import annotations

import json
import logging
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

log = logging.getLogger("edge_face.storage")


@dataclass(frozen=True)
class FaceEvent:
    branch_id: str
    event_type: str
    timestamp: float
    score: float
    camera_id: str
    user_id: str | None = None
    unknown_face_id: str | None = None
    display_name: str | None = None
    meta: dict[str, Any] | None = None

    def to_payload(self) -> dict[str, Any]:
        return {
            "branch_id": self.branch_id,
            "event_type": self.event_type,
            "user_id": self.user_id,
            "unknown_face_id": self.unknown_face_id,
            "timestamp": self.timestamp,
            "score": round(float(self.score), 4),
            "camera_id": self.camera_id,
            "display_name": self.display_name,
            "meta": self.meta or {},
        }


class EventStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS face_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    branch_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    user_id TEXT,
                    unknown_face_id TEXT,
                    ts REAL NOT NULL,
                    score REAL NOT NULL,
                    camera_id TEXT NOT NULL,
                    display_name TEXT,
                    payload_json TEXT NOT NULL,
                    synced INTEGER NOT NULL DEFAULT 0,
                    created_at REAL NOT NULL,
                    synced_at REAL
                );
                CREATE INDEX IF NOT EXISTS idx_face_events_synced
                    ON face_events(synced, id);
                CREATE TABLE IF NOT EXISTS dedupe (
                    camera_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    last_ts REAL NOT NULL,
                    PRIMARY KEY (camera_id, user_id)
                );
                """
            )

    def should_emit(self, camera_id: str, user_id: str, ts: float, window_seconds: int) -> bool:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT last_ts FROM dedupe WHERE camera_id=? AND user_id=?",
                (camera_id, user_id),
            ).fetchone()
            if row and (ts - float(row["last_ts"])) < window_seconds:
                return False
            conn.execute(
                """
                INSERT INTO dedupe(camera_id, user_id, last_ts) VALUES(?,?,?)
                ON CONFLICT(camera_id, user_id) DO UPDATE SET last_ts=excluded.last_ts
                """,
                (camera_id, user_id, ts),
            )
            return True

    def enqueue(self, event: FaceEvent, synced: bool = False) -> int:
        payload = json.dumps(event.to_payload(), ensure_ascii=False)
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO face_events(
                    branch_id, event_type, user_id, unknown_face_id,
                    ts, score, camera_id, display_name,
                    payload_json, synced, created_at, synced_at
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    event.branch_id,
                    event.event_type,
                    event.user_id,
                    event.unknown_face_id,
                    event.timestamp,
                    event.score,
                    event.camera_id,
                    event.display_name,
                    payload,
                    1 if synced else 0,
                    time.time(),
                    time.time() if synced else None,
                ),
            )
            return int(cur.lastrowid)

    def pending(self, limit: int = 50) -> list[tuple[int, dict[str, Any]]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, payload_json FROM face_events
                WHERE synced=0 ORDER BY id ASC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [(int(r["id"]), json.loads(r["payload_json"])) for r in rows]

    def mark_synced(self, ids: list[int]) -> None:
        if not ids:
            return
        now = time.time()
        with self._connect() as conn:
            conn.executemany(
                "UPDATE face_events SET synced=1, synced_at=? WHERE id=?",
                [(now, i) for i in ids],
            )

    def pending_count(self) -> int:
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS c FROM face_events WHERE synced=0").fetchone()
            return int(row["c"])
