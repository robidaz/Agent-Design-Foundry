"""Synthetic KB documents are committed directly to assets/kb/.

The 8 KB documents are hand-authored and version-controlled so that ingestion
results are deterministic across runs (the band-distribution verification in
test_cases.md depends on this). Re-running a Claude-based generator would
re-introduce drift in the engineered seeds.

Engineered properties (must be preserved if any doc is rewritten):

  prior_rfp_response_2025_q1.md   — RPO=15 minutes (2024.x standard)
  prior_rfp_response_2025_q3.md   — RPO=5  minutes (2025.x HA)   ← CONFLICT vs q1
  spec_sheet_dynamix_core_platform.md — documents BOTH 15-min and 5-min
                                        as separate profiles (resolves the
                                        conflict by *naming* the profile)
  spec_sheet_dynamix_core_platform.md — SAML + OIDC; AES-256-GCM at rest
                                        (HIGH-band canonical authority)
  sme_faq_internal.md             — DELIBERATELY silent on FedRAMP, HIPAA,
                                    non-English locales, and on-prem air-gap
                                    specifics (NO_SOURCE seeds for fixture)

If a doc must be rewritten, preserve the seeds above or update
assets/questions/sample_30q.md to match the new ground truth.

This script exists as documentation; it is not invoked by the pipeline.
"""

from __future__ import annotations

import sys


def main() -> None:
    print(
        "KB documents are committed under assets/kb/. "
        "See this file's docstring for the engineered seeds that must be preserved."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
