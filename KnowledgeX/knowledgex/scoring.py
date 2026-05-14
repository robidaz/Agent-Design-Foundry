"""Composite confidence scoring → band assignment.

Signals:
  - chunk_similarity_signal — mean of top-3 cosine sims (Python, no API call)
  - coverage_signal         — one Claude call per question
  - agreement_signal        — Claude call whenever ≥ 2 chunks from distinct
                              source_docs are present (cosine pre-check is
                              skipped: conflicts often involve textually
                              similar chunks with different numbers, and the
                              pre-check would mis-classify those as "agree")

Band rules (precedence order):
  - agreement == "conflict"                    → CONFLICT
  - not coverage.has_relevant_information      → NO_SOURCE
    (chunks found by retrieval but none on-topic for the question)
  - coverage  == "insufficient"                → LOW
  - coverage  == "strong"              AND
    agreement in {"agree","independent"} AND
    sim >= cfg.high_sim                        → HIGH
  - else                                       → MEDIUM
  - NO_SOURCE is also set upstream in retrieval (empty result set).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from knowledgex import prompts
from knowledgex.claude_client import call_json
from knowledgex.config import load_config
from knowledgex.schemas import ConfidenceBand, RetrievedChunk


@dataclass
class CoverageJudgment:
    coverage: Literal["strong", "adequate", "insufficient"]
    has_relevant_information: bool
    missing_aspects: list[str]
    rationale: str


@dataclass
class AgreementJudgment:
    verdict: Literal["agree", "conflict", "independent"]
    conflicting_pairs: list[tuple[str, str]]
    rationale: str


@dataclass
class ScoreResult:
    similarity: float
    coverage: CoverageJudgment
    agreement: AgreementJudgment
    band: ConfidenceBand


def chunk_similarity_signal(chunks: list[RetrievedChunk]) -> float:
    if not chunks:
        return 0.0
    top3 = sorted((c.similarity_score for c in chunks), reverse=True)[:3]
    return sum(top3) / len(top3)


def coverage_signal(question_text: str, chunks: list[RetrievedChunk]) -> CoverageJudgment:
    raw = call_json(
        system_prefix=prompts.COVERAGE_SYSTEM_PREFIX,
        user_text=prompts.build_coverage_user(question_text, chunks),
        schema_name="coverage_judgment",
        schema=prompts.COVERAGE_TOOL_SCHEMA,
    )
    return CoverageJudgment(
        coverage=raw["coverage"],
        has_relevant_information=bool(raw.get("has_relevant_information", True)),
        missing_aspects=list(raw.get("missing_aspects") or []),
        rationale=raw.get("rationale", ""),
    )


def agreement_signal(question_text: str, chunks: list[RetrievedChunk]) -> AgreementJudgment:
    distinct_docs = {c.source_doc for c in chunks}
    if len(distinct_docs) < 2:
        # No cross-source conflict possible.
        return AgreementJudgment(
            verdict="independent",
            conflicting_pairs=[],
            rationale="Single source — no cross-document agreement check applicable.",
        )
    raw = call_json(
        system_prefix=prompts.AGREEMENT_SYSTEM_PREFIX,
        user_text=prompts.build_agreement_user(question_text, chunks),
        schema_name="agreement_judgment",
        schema=prompts.AGREEMENT_TOOL_SCHEMA,
    )
    pairs_raw = raw.get("conflicting_pairs") or []
    pairs: list[tuple[str, str]] = []
    for pair in pairs_raw:
        if isinstance(pair, (list, tuple)) and len(pair) == 2:
            pairs.append((str(pair[0]), str(pair[1])))
    return AgreementJudgment(
        verdict=raw["verdict"],
        conflicting_pairs=pairs,
        rationale=raw.get("rationale", ""),
    )


def assign_band(
    *,
    similarity: float,
    coverage: CoverageJudgment,
    agreement: AgreementJudgment,
    high_sim: float,
) -> ConfidenceBand:
    if agreement.verdict == "conflict":
        return "CONFLICT"
    if not coverage.has_relevant_information:
        return "NO_SOURCE"
    if coverage.coverage == "insufficient":
        return "LOW"
    if coverage.coverage == "strong" and agreement.verdict in {"agree", "independent"} and similarity >= high_sim:
        return "HIGH"
    return "MEDIUM"


def score(question_text: str, chunks: list[RetrievedChunk]) -> ScoreResult:
    cfg = load_config()
    sim = chunk_similarity_signal(chunks)
    coverage = coverage_signal(question_text, chunks)
    agreement = agreement_signal(question_text, chunks)
    band = assign_band(
        similarity=sim,
        coverage=coverage,
        agreement=agreement,
        high_sim=cfg.scoring.high_sim,
    )
    return ScoreResult(similarity=sim, coverage=coverage, agreement=agreement, band=band)
