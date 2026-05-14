"""RFP question-list parser. Accepts markdown or JSON.

Markdown format (per question, in any order; only `**Question:**` is required):

    ## Q-001
    **Section:** Security
    **Question:** What encryption-at-rest algorithm does Core Platform use?
    <!-- expected_band: HIGH -->

JSON format:

    {
      "engagement_id": "ENG-001",
      "questions": [
        {"id": "Q-001", "section": "Security", "text": "…", "expected_band": "HIGH"}
      ]
    }

`expected_band` is optional and only used by the fixture-verification path.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from knowledgex.schemas import ConfidenceBand, QuestionInput

_VALID_BANDS: tuple[ConfidenceBand, ...] = ("HIGH", "MEDIUM", "LOW", "NO_SOURCE", "CONFLICT")

# Markdown patterns
_Q_HEADER_RE = re.compile(r"^##\s+(Q-[A-Za-z0-9_-]+)\s*$", re.MULTILINE)
_SECTION_RE = re.compile(r"^\*\*Section:\*\*\s*(.+?)\s*$", re.MULTILINE)
_QUESTION_RE = re.compile(r"^\*\*Question:\*\*\s*(.+?)\s*$", re.MULTILINE)
_EXPECTED_RE = re.compile(r"<!--\s*expected_band:\s*([A-Z_]+)\s*-->")


class ParseError(ValueError):
    """Raised for malformed or empty question lists."""


def _split_md_blocks(text: str) -> list[tuple[str, str]]:
    """Return [(question_id, block_text)] split at level-2 headings."""
    matches = list(_Q_HEADER_RE.finditer(text))
    if not matches:
        return []
    blocks: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        qid = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks.append((qid, text[start:end]))
    return blocks


def _parse_markdown(text: str) -> list[QuestionInput]:
    blocks = _split_md_blocks(text)
    if not blocks:
        raise ParseError("No questions found in markdown input (no '## Q-…' headers).")
    out: list[QuestionInput] = []
    for qid, body in blocks:
        qm = _QUESTION_RE.search(body)
        if not qm:
            raise ParseError(f"{qid}: missing **Question:** line")
        sm = _SECTION_RE.search(body)
        em = _EXPECTED_RE.search(body)
        expected: ConfidenceBand | None = None
        if em:
            tag = em.group(1)
            if tag in _VALID_BANDS:
                expected = tag  # type: ignore[assignment]
        out.append(
            QuestionInput(
                id=qid,
                text=qm.group(1).strip(),
                section=sm.group(1).strip() if sm else None,
                expected_band=expected,
            )
        )
    return out


def _parse_json(text: str) -> list[QuestionInput]:
    data = json.loads(text)
    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ParseError("JSON input must contain non-empty 'questions' list.")
    out: list[QuestionInput] = []
    for q in questions:
        if not isinstance(q, dict):
            raise ParseError(f"Question entries must be objects, got {type(q).__name__}.")
        if "id" not in q or "text" not in q:
            raise ParseError(f"Question missing required 'id' or 'text': {q!r}")
        eb = q.get("expected_band")
        out.append(
            QuestionInput(
                id=str(q["id"]),
                text=str(q["text"]).strip(),
                section=q.get("section"),
                expected_band=eb if eb in _VALID_BANDS else None,
            )
        )
    return out


def parse(path: Path) -> list[QuestionInput]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        questions = _parse_json(raw)
    elif path.suffix.lower() in (".md", ".markdown"):
        questions = _parse_markdown(raw)
    else:
        raise ParseError(f"Unsupported question-list extension: {path.suffix}")
    if not questions:
        raise ParseError(f"No questions parsed from {path}")
    ids = [q.id for q in questions]
    if len(set(ids)) != len(ids):
        raise ParseError("Duplicate question ids in input.")
    return questions
