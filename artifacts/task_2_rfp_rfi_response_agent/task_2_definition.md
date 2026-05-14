# Task 2 — RFP / RFI Response Drafting Agent

| | |
|---|---|
| **Profile tested** | Architect — RAG and knowledge systems |
| **Deliverable** | Design doc + working RAG prototype |

## Context

Dynamix responds to a high volume of customer RFPs and RFIs. Sales engineers and product specialists spend substantial time pulling answers from prior responses, technical documentation, partner enablement material, and internal SME knowledge. The work is repetitive, but accuracy is non-negotiable — wrong answers in an RFP create both legal and credibility risk.

## Problem

Design an AI agent that ingests a customer RFP/RFI and produces a draft response by retrieving and adapting content from a knowledge base of prior responses and reference material. The agent must flag questions where it has low confidence or no source material — those go to a human SME, not into the draft.

## Scope

- Synthetic RFP and a small fictional knowledge base (5–10 source documents) you create.
- Demonstrate handling of: questions that span multiple sources, questions with no good source, and questions where sources disagree.
- Out of scope: full document parsing for every RFP format, multi-language support, integration with a real DMS.

## Deliverables

- A design doc (≤8 pages) covering ingestion, chunking and embedding strategy, retrieval strategy, generation prompting, confidence scoring, citation and source attribution, and the SME escalation handoff.
- A working prototype demonstrating the retrieval-and-generation flow on the synthetic RFP and knowledge base.
- A failure-mode analysis: where retrieval breaks down, how hallucinations are prevented, and how you handle the "I don't know" case.

## What We Are Looking For

Quality of retrieval design, judgment on when not to answer, rigor of source attribution, and how cleanly the agent hands off to a human when it should not be answering. The "I don't know" case is as important as the answers.
