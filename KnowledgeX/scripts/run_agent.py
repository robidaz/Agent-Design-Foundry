"""End-to-end orchestrator.

Usage:
    python scripts/run_agent.py assets/questions/sample_30q.md \\
        --engagement-id ENG-001 --out output/

Per question: retrieve → score → route → (draft if HIGH/MEDIUM, draft_conflict
if CONFLICT) → assemble QuestionArtifact. Then build the RFPResponseArtifact
and call render.render_all() which writes JSON + MD + PDF + escalation_*.md.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from knowledgex import draft as draft_mod
from knowledgex import parser as q_parser
from knowledgex import retrieval
from knowledgex.render import render_all
from knowledgex.routing import status_for
from knowledgex.schemas import (
    Citation,
    ConfidenceBand,
    QuestionArtifact,
    QuestionInput,
    RFPResponseArtifact,
    RetrievedChunk,
)
from knowledgex.scoring import ScoreResult, score

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "output"

_ESCALATED_BANDS: tuple[ConfidenceBand, ...] = ("LOW", "NO_SOURCE", "CONFLICT")


def _parse_argv() -> tuple[Path, str, Path]:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("question_list", type=Path, help="Path to .md or .json question list.")
    p.add_argument("--engagement-id", default=None, help="Engagement ID; defaults to timestamp.")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output directory.")
    args = p.parse_args()
    engagement_id = args.engagement_id or f"ENG-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return args.question_list, engagement_id, args.out


def _citations_from_ids(
    cited_ids: list[str], chunks: list[RetrievedChunk]
) -> list[Citation]:
    by_id = {c.chunk_id: c for c in chunks}
    out: list[Citation] = []
    for cid in cited_ids:
        c = by_id.get(cid)
        if c is None:
            continue
        out.append(
            Citation(source_doc=c.source_doc, chunk_id=c.chunk_id, similarity_score=c.similarity_score)
        )
    return out


def _citations_from_chunks(chunks: list[RetrievedChunk]) -> list[Citation]:
    return [
        Citation(source_doc=c.source_doc, chunk_id=c.chunk_id, similarity_score=c.similarity_score)
        for c in chunks
    ]


def _no_source_artifact(q: QuestionInput, reason: str | None = None) -> QuestionArtifact:
    return QuestionArtifact(
        question_id=q.id,
        question_text=q.text,
        status="no_source",
        confidence_band="NO_SOURCE",
        draft_text=None,
        citations=[],
        conflict_versions=None,
        escalation_reason=reason or "No KB chunks above the retrieval relevance threshold for this question.",
    )


def _draft_or_route_to_low(
    q: QuestionInput,
    chunks: list[RetrievedChunk],
    sr: ScoreResult,
) -> QuestionArtifact:
    """HIGH / MEDIUM path. On draft validation failure, fall back to LOW."""
    try:
        result = draft_mod.draft(q.text, chunks, sr.band)
    except draft_mod.DraftValidationError as exc:
        return QuestionArtifact(
            question_id=q.id,
            question_text=q.text,
            status="escalated",
            confidence_band="LOW",
            draft_text=None,
            citations=_citations_from_chunks(chunks),
            conflict_versions=None,
            escalation_reason=f"Draft rejected on validation ({exc}); evidence retained for SME.",
        )
    return QuestionArtifact(
        question_id=q.id,
        question_text=q.text,
        status=status_for(sr.band),
        confidence_band=sr.band,
        draft_text=result.draft_text,
        citations=_citations_from_ids(result.cited_chunk_ids, chunks),
        conflict_versions=None,
        escalation_reason=result.uncertainty_note if sr.band == "MEDIUM" else None,
    )


def _conflict_artifact(
    q: QuestionInput,
    chunks: list[RetrievedChunk],
    sr: ScoreResult,
) -> QuestionArtifact:
    try:
        versions, cited_ids = draft_mod.draft_conflict(q.text, chunks, sr.agreement.conflicting_pairs)
    except draft_mod.DraftValidationError as exc:
        # Fall back to LOW with the conflict-detection rationale in the reason.
        return QuestionArtifact(
            question_id=q.id,
            question_text=q.text,
            status="escalated",
            confidence_band="LOW",
            draft_text=None,
            citations=_citations_from_chunks(chunks),
            conflict_versions=None,
            escalation_reason=f"Conflict draft failed validation ({exc}); raw evidence retained for SME.",
        )
    return QuestionArtifact(
        question_id=q.id,
        question_text=q.text,
        status="conflict",
        confidence_band="CONFLICT",
        draft_text=None,
        citations=_citations_from_ids(cited_ids, chunks),
        conflict_versions=versions,
        escalation_reason=sr.agreement.rationale or "Sources disagree; SME must select an authoritative version.",
    )


def _low_artifact(q: QuestionInput, chunks: list[RetrievedChunk], sr: ScoreResult) -> QuestionArtifact:
    return QuestionArtifact(
        question_id=q.id,
        question_text=q.text,
        status="escalated",
        confidence_band="LOW",
        draft_text=None,
        citations=_citations_from_chunks(chunks),
        conflict_versions=None,
        escalation_reason=sr.coverage.rationale or "Retrieved chunks judged insufficient to draft an answer.",
    )


def _process_question(q: QuestionInput) -> QuestionArtifact:
    chunks = retrieval.search(q.text)
    if not chunks:
        return _no_source_artifact(q)
    sr = score(q.text, chunks)
    if sr.band == "CONFLICT":
        return _conflict_artifact(q, chunks, sr)
    if sr.band == "NO_SOURCE":
        return _no_source_artifact(
            q,
            reason=sr.coverage.rationale or "Retrieved chunks contain no information relevant to this question.",
        )
    if sr.band == "LOW":
        return _low_artifact(q, chunks, sr)
    # HIGH or MEDIUM
    return _draft_or_route_to_low(q, chunks, sr)


def main() -> None:
    question_list_path, engagement_id, out_dir = _parse_argv()
    questions = q_parser.parse(question_list_path)
    print(f"Loaded {len(questions)} questions from {question_list_path}")
    print(f"Engagement: {engagement_id}")

    artifacts: list[QuestionArtifact] = []
    started = time.time()
    for idx, q in enumerate(questions, start=1):
        t0 = time.time()
        try:
            artifact = _process_question(q)
        except Exception as exc:
            print(f"  [{idx:>3}/{len(questions)}] {q.id}: ERROR {exc!r}", file=sys.stderr)
            raise
        elapsed = time.time() - t0
        print(
            f"  [{idx:>3}/{len(questions)}] {q.id}: {artifact.confidence_band:<9} "
            f"({elapsed:.1f}s)",
            flush=True,
        )
        artifacts.append(artifact)

    rfp = RFPResponseArtifact(
        engagement_id=engagement_id,
        generated_at=datetime.now(timezone.utc),
        questions=artifacts,
        escalation_queue=[a for a in artifacts if a.confidence_band in _ESCALATED_BANDS],
        requires_human_review=True,
    )

    paths = render_all(rfp, out_dir)
    print(f"\nTotal wall-clock: {time.time() - started:.1f}s")
    print(f"Band counts: {rfp.band_counts()}")
    print("Artifacts:")
    for kind, p in paths.items():
        print(f"  {kind:>14} → {p}")


if __name__ == "__main__":
    main()
