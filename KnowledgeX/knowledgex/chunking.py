"""Markdown-aware, token-bounded chunker with overlap.

Splits on markdown heading boundaries first (H1–H3), then sentence boundaries
inside oversized sections. Token counts use tiktoken cl100k_base as a proxy
for the voyage-3 tokenizer (not publicly exposed; close enough for chunk
budgeting at PoC scale).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import tiktoken

_ENC = tiktoken.get_encoding("cl100k_base")

# Match a markdown heading line, capture the text. Up to H3 only — H4+
# headings are kept inside the parent chunk to avoid over-fragmentation.
_HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$", re.MULTILINE)

# Crude sentence split: full stop, question, or exclamation followed by space.
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")

# YAML front-matter at the top of a markdown doc — stripped before chunking.
_FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)


@dataclass
class Chunk:
    chunk_id: str
    source_doc: str
    doc_type: str
    chunk_text: str
    token_count: int


def _token_count(text: str) -> int:
    return len(_ENC.encode(text))


def _strip_frontmatter(text: str) -> str:
    return _FRONTMATTER_RE.sub("", text, count=1)


def _split_on_headings(text: str) -> list[str]:
    """Split a markdown doc into sections at H1–H3 boundaries.

    Each returned section begins with its heading line (or is the lead-in
    paragraph before the first heading, if any).
    """
    positions = [m.start() for m in _HEADING_RE.finditer(text)]
    if not positions:
        return [text.strip()] if text.strip() else []

    sections: list[str] = []
    if positions[0] > 0:
        lead = text[: positions[0]].strip()
        if lead:
            sections.append(lead)
    for i, start in enumerate(positions):
        end = positions[i + 1] if i + 1 < len(positions) else len(text)
        section = text[start:end].strip()
        if section:
            sections.append(section)
    return sections


def _split_long_section(section: str, target: int, overlap: int) -> list[str]:
    """Split a single section that exceeds target tokens, with overlap."""
    sentences = _SENTENCE_SPLIT_RE.split(section)
    chunks: list[str] = []
    buf: list[str] = []
    buf_tokens = 0

    for sent in sentences:
        st = _token_count(sent)
        if buf_tokens + st > target and buf:
            chunks.append(" ".join(buf).strip())
            # Build the overlap tail by walking back through buf until we have
            # ≈ overlap tokens of context.
            tail: list[str] = []
            tail_tokens = 0
            for s in reversed(buf):
                tail.insert(0, s)
                tail_tokens += _token_count(s)
                if tail_tokens >= overlap:
                    break
            buf = tail
            buf_tokens = tail_tokens
        buf.append(sent)
        buf_tokens += st

    if buf:
        chunks.append(" ".join(buf).strip())
    return [c for c in chunks if c]


def chunk_markdown(
    *,
    source_doc: str,
    doc_type: str,
    text: str,
    target_tokens: int,
    overlap_tokens: int,
) -> list[Chunk]:
    body = _strip_frontmatter(text)
    sections = _split_on_headings(body)

    # Pack sections into chunks no larger than target_tokens. Sections that
    # exceed target by themselves get sub-split with overlap.
    fragments: list[str] = []
    buf: list[str] = []
    buf_tokens = 0
    for section in sections:
        st = _token_count(section)
        if st > target_tokens:
            if buf:
                fragments.append("\n\n".join(buf))
                buf, buf_tokens = [], 0
            fragments.extend(_split_long_section(section, target_tokens, overlap_tokens))
            continue
        if buf_tokens + st > target_tokens and buf:
            fragments.append("\n\n".join(buf))
            buf, buf_tokens = [], 0
        buf.append(section)
        buf_tokens += st
    if buf:
        fragments.append("\n\n".join(buf))

    slug = Path(source_doc).stem.replace("_", "-")
    chunks: list[Chunk] = []
    for idx, frag in enumerate(fragments):
        text_clean = frag.strip()
        if not text_clean:
            continue
        chunks.append(
            Chunk(
                chunk_id=f"{slug}-chunk-{idx:03d}",
                source_doc=source_doc,
                doc_type=doc_type,
                chunk_text=text_clean,
                token_count=_token_count(text_clean),
            )
        )
    return chunks
