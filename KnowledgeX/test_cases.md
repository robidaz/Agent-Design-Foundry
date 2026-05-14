# KnowledgeX Test Cases

Verification checklist for the 30-question fixture (`assets/questions/sample_30q.md`). Every question carries an inline `<!-- expected_band: ... -->` annotation; after running `scripts/run_agent.py`, the actual `confidence_band` in `output/rfp_ENG-001.json` should match.

## Expected Band Distribution

| Band | Count | Driven by |
| ---- | ----- | --------- |
| HIGH | 12 | Single authoritative source, strong coverage, sources agree |
| MEDIUM | 8 | Partial / marginal signal on one of coverage, similarity, or agreement |
| LOW | 3 | Chunks retrieved but coverage judged insufficient |
| NO-SOURCE | 4 | No relevant chunks (empty retrieval or `has_relevant_information: false`) |
| CONFLICT | 3 | Two sources disagree on the same point |

## Per-Band Spot Checks

| Case | Topic | Expected behavior |
| ---- | ----- | ----------------- |
| HIGH | Encryption-at-rest algorithm (Core Platform) | Draft committed; citations include `spec_sheet_dynamix_core_platform.md` |
| MEDIUM | HA deployment topology for 5K-user tenant | Draft + REVIEW flag; citations include `partner_enablement_deployment_playbook.md` |
| LOW | Step-by-step key-provisioning procedure (Q-023) | No draft; `escalation_reason` mentions insufficient coverage; citations present |
| NO-SOURCE | FedRAMP Moderate authorization (Q-025) | No draft; escalation_reason references no relevant information in retrieved chunks |
| CONFLICT | Documented platform RPO (Q-029) | `conflict_versions` contains 15-min and 5-min; both cited (Q1 vs Q3 prior RFP) |
| CONFLICT | Regional-outage RTO (Q-021) | `conflict_versions` contains 4h/90min/8h values from different deployment profiles |

## Cross-cutting Checks

- `output/escalation_ENG-001.md` contains exactly 10 items (3 LOW + 4 NO-SOURCE + 3 CONFLICT).
- `output/rfp_ENG-001.pdf` renders cleanly via WeasyPrint (no template errors).
- `RFPResponseArtifact.requires_human_review` is always `True`.
- No draft contains a claim without a citation in `cited_chunk_ids`.

## Mechanical Pass/Fail

```bash
python -c "
import json, re
from pathlib import Path
art = json.loads(Path('output/rfp_ENG-001.json').read_text())
expected = {}
for line in Path('assets/questions/sample_30q.md').read_text().splitlines():
    m = re.search(r'## (Q-\d+).*', line)
    if m: last = m.group(1)
    m = re.search(r'expected_band: (\w+)', line)
    if m: expected[last] = m.group(1)
pass_n = sum(1 for q in art['questions'] if expected.get(q['question_id']) == q['confidence_band'])
print(f'{pass_n} / {len(art[\"questions\"])} questions match expected band')
"
```
