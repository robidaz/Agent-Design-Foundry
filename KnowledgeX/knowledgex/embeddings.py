"""Local sentence-transformers embedding client. BAAI/bge-large-en-v1.5, 1024-dim.

Runs entirely on CPU. The model is loaded once per process (~2s) and cached.

BGE-v1.5 has an asymmetric query/document convention: queries are prefixed
with a fixed instruction, documents are passed raw. This mirrors the
`input_type="document" | "query"` parameter Voyage exposes.

References: https://huggingface.co/BAAI/bge-large-en-v1.5#frequently-asked-questions
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from knowledgex.config import load_config

InputType = Literal["document", "query"]

_BATCH_SIZE = 32
_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


@lru_cache(maxsize=1)
def _model():
    # Imported lazily so test environments without torch can still import
    # this module for type checking.
    from sentence_transformers import SentenceTransformer

    cfg = load_config()
    return SentenceTransformer(cfg.models.embedding_model, device="cpu")


def embed_batch(texts: list[str], *, input_type: InputType) -> list[list[float]]:
    if not texts:
        return []
    inputs = [(_QUERY_PREFIX + t if input_type == "query" else t) for t in texts]
    arr = _model().encode(
        inputs,
        batch_size=_BATCH_SIZE,
        normalize_embeddings=True,   # cosine-distance-ready vectors
        show_progress_bar=False,
        convert_to_numpy=True,
    )
    return [vec.tolist() for vec in arr]


def embed_one(text: str, *, input_type: InputType) -> list[float]:
    return embed_batch([text], input_type=input_type)[0]
