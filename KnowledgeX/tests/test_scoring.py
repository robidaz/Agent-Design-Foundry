"""Scoring band-assignment unit tests — no network calls."""

from __future__ import annotations

from knowledgex.scoring import (
    AgreementJudgment,
    CoverageJudgment,
    assign_band,
    chunk_similarity_signal,
)
from knowledgex.schemas import RetrievedChunk


def _rc(chunk_id: str, sim: float, source: str = "a.md") -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=chunk_id,
        source_doc=source,
        doc_type="spec_sheet",
        chunk_text="…",
        similarity_score=sim,
        bm25_score=0.1,
        rrf_score=0.02,
    )


def test_similarity_top3_mean():
    chunks = [_rc("a-1", 0.90), _rc("a-2", 0.80), _rc("a-3", 0.70), _rc("a-4", 0.40)]
    assert abs(chunk_similarity_signal(chunks) - 0.80) < 1e-9


def test_conflict_overrides_everything():
    band = assign_band(
        similarity=0.95,
        coverage=CoverageJudgment("strong", [], ""),
        agreement=AgreementJudgment("conflict", [("a", "b")], ""),
        high_sim=0.78,
    )
    assert band == "CONFLICT"


def test_insufficient_coverage_to_low():
    band = assign_band(
        similarity=0.90,
        coverage=CoverageJudgment("insufficient", ["x"], ""),
        agreement=AgreementJudgment("agree", [], ""),
        high_sim=0.78,
    )
    assert band == "LOW"


def test_high_requires_all_three():
    band = assign_band(
        similarity=0.85,
        coverage=CoverageJudgment("strong", [], ""),
        agreement=AgreementJudgment("agree", [], ""),
        high_sim=0.78,
    )
    assert band == "HIGH"


def test_medium_when_one_signal_marginal():
    # strong coverage + agree + similarity below high_sim → MEDIUM
    band = assign_band(
        similarity=0.70,
        coverage=CoverageJudgment("strong", [], ""),
        agreement=AgreementJudgment("agree", [], ""),
        high_sim=0.78,
    )
    assert band == "MEDIUM"

    # adequate coverage → MEDIUM regardless of other signals
    band = assign_band(
        similarity=0.95,
        coverage=CoverageJudgment("adequate", ["bracket interpolation"], ""),
        agreement=AgreementJudgment("agree", [], ""),
        high_sim=0.78,
    )
    assert band == "MEDIUM"

    # strong coverage + independent agreement → MEDIUM
    band = assign_band(
        similarity=0.95,
        coverage=CoverageJudgment("strong", [], ""),
        agreement=AgreementJudgment("independent", [], ""),
        high_sim=0.78,
    )
    assert band == "MEDIUM"
