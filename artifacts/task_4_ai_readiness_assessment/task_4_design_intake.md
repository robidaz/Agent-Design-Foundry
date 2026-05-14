# Task 4 — AI Readiness Assessment Framework for the Services Practice

## Context

Dynamix is building an AI services practice to help mid-market organizations adopt AI in a structured way. The first engagement run with most clients is an AI readiness assessment — a discovery conversation that produces a recommendation: where the client should start, what they need to fix first, and what ROI looks like at 12, 24, and 36 months. Today this is a manual interview-and-deliverable process that needs to scale without losing rigor.

## Assumptions
- Target client profile: 200–2,000 employees, $50M–$1B revenue, mixed digital maturity; framework is industry-agnostic at the dimension level
- Sample report is built against a single fictional mid-market client: a regional industrial distributor
- Discovery agent uses a hybrid UX — client completes a structured intake (~25–35 questions across dimensions via a Jinja-rendered form), then the agent conducts a targeted follow-up chat loop only for dimensions where confidence is low or evidence is thin
- Framework defines 6 readiness dimensions scored on a 1–5 maturity rubric (Initial → Developing → Defined → Managed → Optimized): Strategy & Use Case Portfolio, Data Foundation, Technology & Infrastructure, People & Skills, Process & Operations, Governance & Risk Readiness; each carries 4–6 sub-criteria; composite is a weighted sum with weights configurable by Dynamix without code change
- Roadmap output is structured at 12/24/36-month horizons with recommended initiatives per horizon
- Agent declares "enough information" when all dimensions are scored above a configurable confidence threshold, or a per-dimension follow-up cap (proposed: 3 questions) is reached — unresolved dimensions are flagged for the consultant
- Draft report is always reviewed by a Dynamix consultant before client delivery; consultant owns final calibration, narrative additions, ROI sanity-check, and any overrides; consultant is referred to as "user," the assessed organization as "client"
- Productization assumes a fixed-scope, fixed-price engagement (proposed: 2-week sprint) with a templated deliverable and consultant-led readout
- Synthetic discovery responses are hand-authored to exercise the full scoring range, surface at least one UNKNOWN, trigger at least one consultant escalation, and include clearly labeled illustrative ROI projections
- Agent has no write access to the framework definition or scoring rubric — those are versioned and governed by Dynamix; historical benchmarking and longitudinal re-use across engagements are deferred to a future iteration
- Agent does not recommend specific vendors, products, or implementation partners — reserved for downstream services engagements
- No real client data; no CRM integration; no live consultant deployment at PoC scope

## Requirements
- Framework deliverable defines: dimensions, sub-criteria per dimension, the 1–5 scoring rubric with anchors per maturity level, composite weighting, methodology, and rationale per dimension
- Discovery agent ingests structured intake responses, scores them against the rubric, and identifies dimensions requiring follow-up
- Discovery agent conducts a targeted follow-up conversation per gap dimension, capped per the assumption above; the transcript is preserved alongside the report for the consultant's review
- Agent reports a completeness gate — an explicit declaration that it has enough information, or which dimensions remain underspecified and why
- Agent produces a draft readiness report including:
  - per-dimension score with supporting evidence
  - composite readiness tier
  - 12/24/36-month roadmap traceable to scores
  - confidence indicators per dimension and sub-criterion
  - explicit list of consultant-review gaps
- Output is Jinja-rendered markdown → PDF; the consultant can edit the markdown before final delivery
- Agent must surface confidence per scored dimension and explicitly flag UNKNOWN / low-confidence findings rather than fabricate
- Agent must abstain on a dimension when the discovery data cannot support a defensible score
- Framework definition (dimensions, weights, rubric anchors) is configurable so Dynamix can tune the framework without code changes
- Productization brief covers:
  - target ICP
  - fixed-scope engagement structure (intake → agent draft → consultant review → readout)
  - pricing model
  - repeatability levers (what is reusable across engagements, what is bespoke per engagement)
  - the AI-vs-human split per workflow step
- Sample report demonstrates: passing scores in some dimensions, low scores in others, at least one UNKNOWN, an explicit consultant escalation, and a roadmap that follows from the scores
- AI-vs-human split is documented for every workflow step in the design

## Scope Exclusions
- Certification programs (per definition)
- Partner enablement (per definition)
- Deep technical implementation playbooks (per definition)
- Real client data, real CRM integration, multi-tenant deployment
- Vendor / product / partner recommendations
- Historical assessment database / longitudinal benchmarking
- Live consultant tooling (collaboration UI, in-app review workflow)

## Proposed Deliverables

- Framework definition document covering dimensions, sub-criteria, scoring rubric with anchors, methodology, and rationale per dimension
- Sample readiness report on the fictional regional industrial distributor, with concrete dimension scores, composite tier, and a full 12/24/36-month roadmap
- Discovery agent design covering intake schema, follow-up flow, completeness gate, consultant handoff, and AI-vs-human split
- Productization brief covering engagement structure, ICP, repeatability levers, and pricing model
- Either a thin prototype demonstrating the agent loop on synthetic intake data, OR an annotated mockup of the same flow (state which and why, per the Task 1 pattern)
