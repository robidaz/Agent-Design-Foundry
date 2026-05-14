"""Claude drafting per band.

  HIGH / MEDIUM  → draft()
  CONFLICT       → draft_conflict()
  LOW / NO_SOURCE → never invoked (upstream routes them to the escalation queue)

Validation: any draft whose `cited_chunk_ids` is empty, or which references a
chunk id not present in the retrieved set, is rejected. Callers re-route a
rejected draft to LOW with a descriptive escalation reason.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from knowledgex import prompts
from knowledgex.claude_client import call_json
from knowledgex.schemas import ConfidenceBand, RetrievedChunk


@dataclass
class DraftResult:
    draft_text: str
    cited_chunk_ids: list[str]
    uncertainty_note: Optional[str]


class DraftValidationError(RuntimeError):
    """Raised when a draft fails citation validation."""


def _validate(result: DraftResult, retrieved_ids: set[str]) -> None:
    if not result.draft_text.strip():
        raise DraftValidationError("draft_text is empty")
    if not result.cited_chunk_ids:
        raise DraftValidationError("no citations in cited_chunk_ids")
    unknown = [cid for cid in result.cited_chunk_ids if cid not in retrieved_ids]
    if unknown:
        raise DraftValidationError(f"cited unknown chunk_ids: {unknown}")


def draft(
    question_text: str,
    chunks: list[RetrievedChunk],
    band: ConfidenceBand,
) -> DraftResult:
    if band not in ("HIGH", "MEDIUM"):
        raise ValueError(f"draft() is only valid for HIGH/MEDIUM bands, got {band}")
    raw = call_json(
        system_prefix=prompts.DRAFT_SYSTEM_PREFIX,
        user_text=prompts.build_draft_user(question_text, chunks, band),
        schema_name="draft_answer",
        schema=prompts.DRAFT_TOOL_SCHEMA,
    )
    result = DraftResult(
        draft_text=raw.get("draft_text", "") or "",
        cited_chunk_ids=list(raw.get("cited_chunk_ids") or []),
        uncertainty_note=raw.get("uncertainty_note") or None,
    )
    _validate(result, retrieved_ids={c.chunk_id for c in chunks})
    return result


def draft_conflict(
    question_text: str,
    chunks: list[RetrievedChunk],
    conflicting_pairs: list[tuple[str, str]],
) -> tuple[list[str], list[str]]:
    """Returns (versions, all_cited_chunk_ids). Never picks a winner."""
    raw = call_json(
        system_prefix=prompts.CONFLICT_DRAFT_SYSTEM_PREFIX,
        user_text=prompts.build_conflict_draft_user(question_text, chunks, conflicting_pairs),
        schema_name="conflict_draft",
        schema=prompts.CONFLICT_DRAFT_TOOL_SCHEMA,
    )
    versions = [v for v in (raw.get("versions") or []) if isinstance(v, str) and v.strip()]
    all_cited = list(raw.get("all_cited_chunk_ids") or [])
    if len(versions) < 2:
        raise DraftValidationError("conflict draft must produce ≥ 2 versions")
    return versions, all_cited
