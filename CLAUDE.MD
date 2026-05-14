# AI Engineering & Design Documentation Instructions

## Purpose

This repository exists to design, document, prototype, and demonstrate production-minded AI solutions inspired by the Dynamix Group AI Engineer Candidate Exercise.

The goal is not to build flashy demos or autonomous AI systems. The goal is to create defensible, explainable, operationally realistic AI workflows that solve real business problems.

Focus on:

* Clear thinking under ambiguity
* Strong operational judgment
* Human oversight
* Explainability
* Maintainability
* Enterprise readiness
* Practical scope control

Prefer a smaller believable system over a larger unrealistic one.

---

# Core Principles

## Human-In-The-Loop Is Mandatory

Every workflow MUST include:

* Human approval checkpoints
* Confidence visibility
* Escalation paths
* Failure handling
* Manual override capability

The AI system assists operators. It does not replace accountability.

Humans remain responsible for:

* Final approvals
* Customer-facing communication
* Financial decisions
* Vendor relationships
* Compliance-sensitive actions

---

## Explainability Over Black Boxes

All recommendations should:

* Show supporting evidence
* Show reasoning
* Show source attribution
* Expose confidence indicators
* Explain tradeoffs

Avoid opaque workflows where AI silently makes decisions.

If the output impacts:

* Revenue
* Margin
* Customer trust
* Vendor relationships
* Legal exposure

Then the reasoning must be inspectable.

---

## “I Don’t Know” Is A Valid Outcome

The system must support:

* Low-confidence responses
* Missing-data scenarios
* Conflicting-source handling
* Escalation to SMEs

Never force an answer when the evidence is weak.

Escalation is preferable to hallucination.

---

## Scope Aggressively

Design the smallest credible solution.

Prefer:

* Narrow workflows
* Explicit assumptions
* Well-defined boundaries
* Strong operational controls

Avoid:

* Autonomous-agent fantasies
* Unbounded orchestration
* Multi-agent complexity without justification
* Over-engineered platforms

The objective is judgment, not maximum complexity.

---

# Technical Standards

## Preferred Technology Stack

### Backend & Processing

Use:

* Python

Preferred libraries:

* pandas
* pydantic
* sqlalchemy
* fastapi
* pgvector

Use orchestration frameworks sparingly and only when justified.

---

### Frontend

Use:

* Angular
* Syncfusion

Frontend UX should prioritize:

* Explainability
* Data density
* Review workflows
* Editable outputs
* Audit visibility

Avoid gimmicky AI-chat-only interfaces unless clearly justified.

---

### Database

Use:

* PostgreSQL
* pgvector where embeddings are needed

Prefer:

* Structured relational schemas
* Explicit audit/history tables
* Strong typing

Avoid hiding business logic only inside prompts.

---

### AI Models

Preferred provider:

* Anthropic Claude

Claude should be used for:

* Reasoning
* Structured extraction
* Summarization
* RAG answer synthesis
* Draft generation
* Classification

AI workflows should:

* Prefer structured outputs
* Be traceable
* Support observability
* Minimize hallucination risk

---

### Templating

Use:

* Jinja2

Use Jinja for:

* Report generation
* Markdown generation
* Email drafting
* Proposal formatting
* RFP responses

---

### Documentation

Use:

* Markdown
* Mermaid diagrams

Documentation should be:

* AI-readable
* Human-readable
* Concise
* Structured
* Operationally focused

---

# Mermaid Diagram Standards

Mermaid is the default diagramming format.

Preferred diagram types:

* flowchart
* sequenceDiagram
* stateDiagram-v2
* entityRelationshipDiagram

Use Mermaid for:

* System architecture
* Agent workflows
* Human approval flows
* Retrieval flows
* Escalation paths
* State transitions
* Integration boundaries
* Data movement

Diagrams should:

* Prioritize clarity over completeness
* Explicitly show human checkpoints
* Explicitly show AI decision points
* Be modular and readable in raw markdown

Avoid:

* Massive all-in-one diagrams
* Decorative styling
* Excessive visual complexity

---

# Design Documentation Standards

Design documents should generally include:

1. Problem Framing
2. Scope Definition
3. Assumptions
4. Constraints
5. Architecture Overview
6. Data Flow
7. Decision Logic
8. Human Checkpoints
9. Failure Modes
10. Governance & Security
11. Cost & Latency Considerations
12. Future Improvements

Keep design docs concise.

Prefer a sharp 4–6 page document over a bloated 12-page document.

---

# AI Workflow Standards

## Retrieval-Augmented Generation (RAG)

RAG systems should include:

* Source attribution
* Retrieval transparency
* Chunking strategy explanation
* Confidence scoring
* SME escalation paths

The system must handle:

* Conflicting sources
* Missing sources
* Partial answers
* Retrieval failure

Avoid citation-free generation.

---

## Agent Design

Agents should behave like:

* Assistants
* Analysts
* Recommenders
* Workflow accelerators

NOT:

* Autonomous employees
* Independent decision makers
* Unsupervised operators

Every design should clearly answer:

* What does the human approve?
* What can fail?
* What triggers escalation?
* What would financially damage the business?
* How is confidence communicated?

---

# Data Standards

## Structured Data First

Prefer:

* Explicit schemas
* Strong typing
* Relational modeling
* Traceable lineage

Avoid:

* Prompt-only business logic
* Freeform JSON blobs for critical entities

---

## Synthetic Data Requirements

All prototypes should use fictional or synthetic data only.

Synthetic datasets should intentionally include:

* Missing data
* Conflicting information
* Ambiguous scenarios
* Invalid states
* Edge cases

---

# Code Generation Standards

Generated code should be:

* Readable
* Modular
* Production-minded
* Explicitly structured

Include:

* Validation
* Error handling
* Logging
* Configuration separation

Avoid:

* Clever abstractions without value
* Massive single-file implementations
* Hidden side effects

---

# Template Standards

A set of extension templates will be provided separately and should be treated as canonical starting points.

Generated documentation must:

* Preserve template structure
* Populate all required sections
* Clearly identify unknown information
* Explicitly identify assumptions

Never fabricate enterprise details.

If information is unavailable, explicitly mark it as:

* TODO
* UNKNOWN
* ASSUMPTION
* REQUIRES SME INPUT

---

# Scope

Only consider files within this repository (`design-docs/`) when providing assistance. Do not read, reference, or pull context from files outside this directory unless explicitly instructed.

---

# Repository Expectations

Suggested structure:

```text
repo/
├── documentation/
├── frontend/
├── backend/
├── prompts/
├── templates/
├── scripts/
└── prototypes/
```

---

# Final Principle

A believable AI system beats an impressive fake one.

Design for the system that a skeptical enterprise operator would actually approve for production.
