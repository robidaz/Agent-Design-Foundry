"""Band → status mapping; QuestionArtifact assembly.

NOTE: stub — implementation arrives in Phase 8.
"""

from __future__ import annotations

from knowledgex.schemas import ConfidenceBand, QuestionStatus

BAND_TO_STATUS: dict[ConfidenceBand, QuestionStatus] = {
    "HIGH": "drafted",
    "MEDIUM": "drafted_flagged",
    "LOW": "escalated",
    "NO_SOURCE": "no_source",
    "CONFLICT": "conflict",
}


def status_for(band: ConfidenceBand) -> QuestionStatus:
    return BAND_TO_STATUS[band]
