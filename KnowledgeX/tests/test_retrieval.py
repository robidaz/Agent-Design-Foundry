"""Retrieval module — pure-logic checks that don't need a live database.

The RRF SQL itself is verified end-to-end during Phase 11 by running the
agent against the 30-question fixture and confirming the band distribution.
"""

from __future__ import annotations

from knowledgex.schemas import RetrievedChunk


def test_retrieved_chunk_roundtrip():
    rc = RetrievedChunk(
        chunk_id="x-chunk-001",
        source_doc="x.md",
        doc_type="spec_sheet",
        chunk_text="hello",
        similarity_score=0.81,
        bm25_score=0.12,
        rrf_score=0.034,
    )
    assert rc.similarity_score == 0.81
    assert rc.doc_type == "spec_sheet"
