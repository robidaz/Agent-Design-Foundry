"""Pydantic round-trip on a hand-built artifact."""

from __future__ import annotations

from datetime import datetime

from knowledgex.schemas import (
    Citation,
    QuestionArtifact,
    RFPResponseArtifact,
)


def test_artifact_roundtrip():
    q = QuestionArtifact(
        question_id="Q-001",
        question_text="What encryption-at-rest does Core Platform use?",
        status="drafted",
        confidence_band="HIGH",
        draft_text="AES-256-GCM.",
        citations=[
            Citation(
                source_doc="spec_sheet_dynamix_core_platform.md",
                chunk_id="spec-core-chunk-003",
                similarity_score=0.89,
            )
        ],
    )
    art = RFPResponseArtifact(
        engagement_id="ENG-001",
        generated_at=datetime(2026, 5, 12, 12, 0, 0),
        questions=[q],
        escalation_queue=[],
    )

    payload = art.model_dump_json()
    restored = RFPResponseArtifact.model_validate_json(payload)
    assert restored.questions[0].confidence_band == "HIGH"
    assert restored.band_counts()["HIGH"] == 1
    assert restored.requires_human_review is True
