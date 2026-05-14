"""One-shot KB ingestion.

Chunks every markdown file in assets/kb/, embeds each chunk with voyage-3,
and loads the kb_chunks table in pgvector. Idempotent: bootstraps the DDL
and truncates the table before re-inserting.

Usage:
    python scripts/ingest_kb.py
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

from knowledgex import db
from knowledgex.chunking import Chunk, chunk_markdown
from knowledgex.config import load_config
from knowledgex.embeddings import embed_batch

ROOT = Path(__file__).resolve().parent.parent
KB_DIR = ROOT / "assets" / "kb"

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _read_doc_type(text: str, fallback: str) -> str:
    """Extract `doc_type:` from front-matter; fall back to filename prefix."""
    m = _FRONTMATTER_RE.match(text)
    if m:
        for line in m.group(1).splitlines():
            if line.startswith("doc_type:"):
                return line.split(":", 1)[1].strip()
    return fallback


def _fallback_doc_type(filename: str) -> str:
    if filename.startswith("prior_rfp_response_"):
        return "prior_rfp_response"
    if filename.startswith("spec_sheet_"):
        return "spec_sheet"
    if filename.startswith("partner_enablement_"):
        return "partner_enablement"
    if filename.startswith("sme_faq"):
        return "sme_faq"
    raise ValueError(f"Cannot derive doc_type for {filename}")


def _chunk_all(cfg) -> list[Chunk]:
    out: list[Chunk] = []
    md_files = sorted(KB_DIR.glob("*.md"))
    if not md_files:
        print(f"No markdown files found in {KB_DIR}", file=sys.stderr)
        sys.exit(1)
    for path in md_files:
        text = path.read_text(encoding="utf-8")
        doc_type = _read_doc_type(text, _fallback_doc_type(path.name))
        chunks = chunk_markdown(
            source_doc=path.name,
            doc_type=doc_type,
            text=text,
            target_tokens=cfg.chunking.target_tokens,
            overlap_tokens=cfg.chunking.overlap_tokens,
        )
        out.extend(chunks)
        print(f"  chunked {path.name}: {len(chunks)} chunks")
    return out


def _embed_all(chunks: list[Chunk], model_name: str) -> list[list[float]]:
    print(f"Embedding {len(chunks)} chunks with {model_name}…")
    t0 = time.time()
    vectors = embed_batch([c.chunk_text for c in chunks], input_type="document")
    print(f"  embedded in {time.time() - t0:.1f}s")
    return vectors


def _insert_all(chunks: list[Chunk], vectors: list[list[float]], model_name: str) -> None:
    assert len(chunks) == len(vectors), "embedding count mismatch"
    rows = [
        (c.chunk_id, c.source_doc, c.doc_type, c.chunk_text, c.token_count, vec, model_name)
        for c, vec in zip(chunks, vectors)
    ]
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO kb_chunks
                    (chunk_id, source_doc, doc_type, chunk_text, token_count, embedding, embedding_model)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                rows,
            )
        conn.commit()


def main() -> None:
    cfg = load_config()
    print("Bootstrapping pgvector schema…")
    db.bootstrap()
    print("Truncating kb_chunks for re-ingestion…")
    db.truncate_chunks()

    chunks = _chunk_all(cfg)
    print(f"Total chunks: {len(chunks)}")

    vectors = _embed_all(chunks, cfg.models.embedding_model)
    _insert_all(chunks, vectors, cfg.models.embedding_model)

    final = db.chunk_count()
    print(f"Loaded {final} chunks into kb_chunks. Done.")


if __name__ == "__main__":
    main()
