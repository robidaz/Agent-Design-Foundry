# Task 1 — Quote / BOM Generation Agent

|                    |                                            |
| ------------------ | ------------------------------------------ |
| **Profile tested** | Builder — end-to-end agent design          |
| **Deliverable**    | Design doc + prototype OR annotated mockup |

## Context

Dynamix sources from 200+ vendors and distributors — Arrow, TD Synnex, Ingram Micro, and others. Sales engineers spend significant time manually building Bills of Materials for customer requirements: pulling SKUs across catalogs, validating availability and lead times, calculating margin against vendor cost, and assembling alternatives at different price/performance tiers. Quote turnaround time is one of the levers we use to compete; today, it is slower than it should be.

## Problem

Design an AI-augmented agent that converts a customer technical requirement into a multi-vendor BOM. The agent should select SKUs across distributor catalogs, propose alternatives, surface availability and lead-time risks, and produce a quote-ready output with margin transparency for the sales engineer to review and edit.

## Scope

- Limit to 3–4 representative product categories (e.g., enterprise networking, server compute, storage, security).
- Use synthetic catalog data. Real distributor APIs are not required.
- Focus on agent design, decision logic, data flow, and human checkpoints.
- Out of scope: full pricing engine, contract pricing, customer portal UI.

## Deliverables

- A design doc (≤8 pages) covering problem framing, architecture, agent decision logic, data sources, edge cases (out-of-stock, EOL SKUs, multi-vendor optimization), human checkpoints, and cost/latency reasoning.
- Either a working prototype demonstrating the core flow on synthetic data, OR a clickable mockup with annotated data flow. State which you chose and why.
- A short risks-and-failure-modes section: where the agent breaks, where the sales engineer must override, where wrong outputs would cost us money.

## What We Are Looking For

How you decompose an ambiguous request into a workable agent flow, how you handle the messy real-world edge cases that distinguish a demo from a production-worthy design, and whether your output is something a sales engineer could actually trust and edit. Your supply-chain background should help here.
