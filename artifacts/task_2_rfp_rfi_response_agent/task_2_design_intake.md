# Task 2 — RFP / RFI Response Drafting Agent

## Context

Dynamix responds to a high volume of customer RFPs and RFIs. Sales engineers and product specialists spend substantial time pulling answers from prior responses, technical documentation, partner enablement material, and internal SME knowledge. The work is repetitive, but accuracy is non-negotiable — wrong answers in an RFP create both legal and credibility risk.

## Assumptions
- PoC uses a single synthetic RFP/RFI of ~15–25 questions covering all required edge cases: multi-source, no-source, conflicting-source, and standard-case questions
- RFP input arrives as a pre-structured markdown or JSON question list; upstream conversion from raw PDF/Word is out of scope for this agent
- Synthetic knowledge base (KB) contains 8 fictional markdown source documents — 3 prior RFP responses, 2 spec sheets, 2 partner-enablement docs, 1 internal SME FAQ — including at least one engineered conflict pair (e.g., differing SLA figures across two prior responses)
- KB documents are pre-approved and curated; agent has no write access and is not responsible for provenance validation or KB updates
- KB ingestion is a one-shot manual operation via a documented Python script loading into a local pgvector store; chunking is heading-aware for structured docs and paragraph-level for unstructured, targeting ~300–500 token chunks; a single embedding model is used for both ingestion and query, documented and configurable
- Retrieval is hybrid (semantic vector + BM25-style keyword) at k=5, filtered by relevance score, to handle acronyms, model numbers, and product names that fail pure semantic search
- Per-question confidence is a composite of chunk similarity, Claude-judged coverage, and source agreement; three bands drive routing: HIGH (draft committed), MEDIUM (draft + SME-review flag), LOW / NO-SOURCE / CONFLICT (no draft; escalated to SME with retrieval evidence)
- Every drafted answer cites source document + chunk; when sources conflict, both versions are surfaced and cited — the agent does not pick a winner; the SME resolves
- Output is a per-question response artifact (status + draft + citations + confidence band) rendered via Jinja to markdown/PDF; the SME (sales engineer or product specialist) is the sole party that finalizes responses and is referred to as "user" throughout the design
- Abstention is the default when retrieval support is insufficient — LOW/NO-SOURCE/CONFLICT items present retrieval evidence first (no fabricated draft) to avoid anchoring bias; "I don't know" is preferred over a hallucinated answer
- English only; no DMS integration (KB lives as repo files); no auto-submission to customers

## Requirements
- Ingest a structured RFP/RFI question list and produce a draft response per question
- Retrieve relevant context from a curated KB across multiple document types using hybrid semantic + keyword retrieval
- Confidence-score each draft answer into HIGH / MEDIUM / LOW / NO-SOURCE / CONFLICT bands based on similarity, coverage, and source agreement
- Cite source document + chunk for every drafted answer; multi-source answers cite all contributing chunks
- Detect when retrieved sources disagree on a question and surface the conflict rather than picking a winner
- Detect when no source supports a question and route to the SME with the original question plus best-effort retrieval context — no fabricated draft
- Route LOW / NO-SOURCE / CONFLICT items to an SME escalation queue, each with full retrieval evidence attached
- Produce a per-question response artifact the SME can review and edit — status, draft (if applicable), citations, confidence band
- Expose audit/observability — for every drafted question the SME can inspect which chunks were retrieved and why
- KB ingestion is reproducible: a documented Python script generates the embeddings index from source files
- Failure-mode analysis covers retrieval failure, hallucination prevention, conflicting/sparse-source handling, and prompt-injection risk in user-supplied questions
- Prioritize correctness over coverage — abstention is the preferred behavior when evidence is weak

## Scope Exclusions
- Full document parsing for every RFP format (PDF, Word, Excel layout extraction)
- Multi-language support
- Real DMS / SharePoint / Confluence integration
- KB content authoring, curation, or approval workflow
- Auto-submission to customer
- Closed-loop learning from SME edits (KB does not update based on draft review at PoC scope)
- Cross-RFP analytics or historical response reuse beyond the static KB

## Proposed Deliverables

- Draft response document with per-question status (drafted / escalated / conflict), draft text (when applicable), citations, and confidence band
- SME escalation queue listing all LOW / NO-SOURCE / CONFLICT items with their retrieval evidence
- Failure-mode analysis covering retrieval breakdown, hallucination prevention, abstention behavior, and prompt-injection considerations
- Working prototype: KB ingestion script, retrieval/generation pipeline, and an end-to-end run against the synthetic RFP
