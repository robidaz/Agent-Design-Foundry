"""Pydantic schemas for the RFP/RFI Response Agent.

Mirrors §6 (Structured Output Schema) and Appendix A (KB Chunk Schema) of the
design spec at knowledgex_design_spec.md.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

DocType = Literal["prior_rfp_response", "spec_sheet", "partner_enablement", "sme_faq"]

ConfidenceBand = Literal["HIGH", "MEDIUM", "LOW", "NO_SOURCE", "CONFLICT"]

QuestionStatus = Literal[
    "drafted",          # HIGH band: committed draft
    "drafted_flagged",  # MEDIUM band: draft + SME review flag
    "escalated",        # LOW band: no draft, escalated with evidence
    "conflict",         # CONFLICT: both versions surfaced, no winner
    "no_source",        # NO_SOURCE: no chunks above relevance threshold
]


class Citation(BaseModel):
    source_doc: str
    chunk_id: str
    similarity_score: float


class KBChunk(BaseModel):
    """Appendix A — KB Chunk Schema. Persisted row in pgvector `kb_chunks`."""

    chunk_id: str
    source_doc: str
    doc_type: DocType
    approval_status: Literal["approved"] = "approved"
    chunk_text: str
    token_count: int
    embedding: list[float]
    embedding_model: str
    ingested_at: Optional[datetime] = None


class RetrievedChunk(BaseModel):
    """A KB chunk returned from hybrid retrieval, with scoring metadata."""

    chunk_id: str
    source_doc: str
    doc_type: DocType
    chunk_text: str
    similarity_score: float
    bm25_score: float
    rrf_score: float


class QuestionInput(BaseModel):
    """A single parsed question from the RFP question list."""

    id: str
    text: str
    section: Optional[str] = None
    expected_band: Optional[ConfidenceBand] = None  # set only by fixtures via inline comment


class QuestionArtifact(BaseModel):
    question_id: str
    question_text: str
    status: QuestionStatus
    confidence_band: ConfidenceBand
    draft_text: Optional[str] = None
    citations: list[Citation] = Field(default_factory=list)
    conflict_versions: Optional[list[str]] = None
    escalation_reason: Optional[str] = None


class RFPResponseArtifact(BaseModel):
    engagement_id: str
    generated_at: datetime
    questions: list[QuestionArtifact]
    escalation_queue: list[QuestionArtifact]
    requires_human_review: bool = True

    def band_counts(self) -> dict[str, int]:
        counts = {b: 0 for b in ("HIGH", "MEDIUM", "LOW", "NO_SOURCE", "CONFLICT")}
        for q in self.questions:
            counts[q.confidence_band] += 1
        return counts
