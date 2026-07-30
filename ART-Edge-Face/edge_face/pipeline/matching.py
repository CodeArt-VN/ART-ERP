"""Local gallery matching — FAISS IndexFlatIP (cosine on L2-normalized vectors)."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np

log = logging.getLogger("edge_face.matching")


@dataclass(frozen=True)
class MatchResult:
    user_id: str
    score: float
    display_name: str | None = None


class VectorGallery:
    """RAM-resident gallery for ~100–500 identities; match < 1ms."""

    def __init__(self, embedding_dim: int = 128, backend: str = "faiss"):
        self.embedding_dim = embedding_dim
        self.backend = backend
        self.user_ids: list[str] = []
        self.display_names: list[str | None] = []
        self._vectors: np.ndarray | None = None
        self._index = None

    @property
    def size(self) -> int:
        return len(self.user_ids)

    def clear(self) -> None:
        self.user_ids.clear()
        self.display_names.clear()
        self._vectors = None
        self._index = None

    def load_from_json(self, path: str | Path) -> int:
        p = Path(path)
        if not p.exists():
            log.warning("Gallery file missing: %s — starting empty", p)
            self.clear()
            return 0
        with p.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
        entries = payload.get("identities", payload if isinstance(payload, list) else [])
        ids: list[str] = []
        names: list[str | None] = []
        vecs: list[np.ndarray] = []
        for item in entries:
            emb = np.asarray(item["embedding"], dtype=np.float32).reshape(-1)
            if emb.shape[0] != self.embedding_dim:
                continue
            norm = float(np.linalg.norm(emb))
            if norm > 0:
                emb = emb / norm
            ids.append(str(item["user_id"]))
            names.append(item.get("display_name"))
            vecs.append(emb)
        self.user_ids = ids
        self.display_names = names
        self._vectors = np.vstack(vecs).astype(np.float32) if vecs else None
        self._rebuild_index()
        log.info("Gallery loaded: %s identities from %s", self.size, p.name)
        return self.size

    def load_entries(self, entries: list[dict]) -> int:
        ids: list[str] = []
        names: list[str | None] = []
        vecs: list[np.ndarray] = []
        for item in entries:
            emb = np.asarray(item["embedding"], dtype=np.float32).reshape(-1)
            if emb.shape[0] != self.embedding_dim:
                continue
            norm = float(np.linalg.norm(emb))
            if norm > 0:
                emb = emb / norm
            ids.append(str(item["user_id"]))
            names.append(item.get("display_name"))
            vecs.append(emb)
        self.user_ids = ids
        self.display_names = names
        self._vectors = np.vstack(vecs).astype(np.float32) if vecs else None
        self._rebuild_index()
        return self.size

    def _rebuild_index(self) -> None:
        self._index = None
        if self._vectors is None or self.size == 0:
            return
        if self.backend == "faiss":
            try:
                import faiss

                index = faiss.IndexFlatIP(self.embedding_dim)
                index.add(self._vectors)
                self._index = index
                return
            except Exception as exc:
                log.warning("FAISS unavailable (%s) — numpy fallback", exc)
        # numpy cosine via matmul (vectors already L2-normalized)

    def match(self, embedding: np.ndarray, threshold: float, top_k: int = 1) -> MatchResult | None:
        if self.size == 0 or self._vectors is None:
            return None
        q = embedding.astype(np.float32).reshape(1, -1)
        if self._index is not None:
            scores, idxs = self._index.search(q, min(top_k, self.size))
            best_i = int(idxs[0][0])
            best_s = float(scores[0][0])
        else:
            sims = (self._vectors @ q.T).reshape(-1)
            best_i = int(np.argmax(sims))
            best_s = float(sims[best_i])
        if best_s < threshold or best_i < 0:
            return None
        return MatchResult(
            user_id=self.user_ids[best_i],
            score=best_s,
            display_name=self.display_names[best_i],
        )
