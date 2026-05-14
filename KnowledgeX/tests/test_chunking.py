"""Chunking unit tests — token budget, overlap, deterministic chunk_ids."""

from __future__ import annotations

from knowledgex.chunking import chunk_markdown


SAMPLE = """---
source_doc: sample.md
doc_type: spec_sheet
---

# Title

Lead-in paragraph that introduces the doc.

## Section A

Some content about section A. It has a couple of sentences. They are short.

## Section B

Section B content. Also short. With multiple sentences.
"""


def test_frontmatter_stripped():
    chunks = chunk_markdown(
        source_doc="sample.md",
        doc_type="spec_sheet",
        text=SAMPLE,
        target_tokens=400,
        overlap_tokens=50,
    )
    assert chunks, "expected at least one chunk"
    joined = " ".join(c.chunk_text for c in chunks)
    assert "doc_type" not in joined, "front-matter must be stripped"


def test_chunk_id_format_and_uniqueness():
    chunks = chunk_markdown(
        source_doc="sample.md",
        doc_type="spec_sheet",
        text=SAMPLE,
        target_tokens=400,
        overlap_tokens=50,
    )
    ids = [c.chunk_id for c in chunks]
    assert len(set(ids)) == len(ids), "chunk_ids must be unique"
    for cid in ids:
        assert cid.startswith("sample-chunk-"), cid


def test_token_counts_recorded():
    chunks = chunk_markdown(
        source_doc="sample.md",
        doc_type="spec_sheet",
        text=SAMPLE,
        target_tokens=400,
        overlap_tokens=50,
    )
    for c in chunks:
        assert c.token_count > 0


def test_long_section_subsplit():
    big_section = "## Big Section\n\n" + ("A short sentence. " * 200)
    chunks = chunk_markdown(
        source_doc="big.md",
        doc_type="spec_sheet",
        text=big_section,
        target_tokens=100,
        overlap_tokens=20,
    )
    assert len(chunks) > 1, "oversized section should sub-split"
    for c in chunks:
        # Loose upper bound: target plus one sentence of slack
        assert c.token_count <= 200
