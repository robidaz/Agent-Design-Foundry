# QuotePilot — Quote BOM Agent

## Overview

QuotePilot is my take on **Task 1 — Quote BOM Agent**.

Beyond the design spec ([QuotePilot.md](QuotePilot.md)), I built a working agent that turns a Sales Engineer's (SE) curated requirements list into a 3-tier (budget / balanced / premium) multi-vendor BOM. The agent reads a synthetic 50-vendor catalog and an SE-maintained rulesets document, applies tier-specific evaluation rules around availability, lead time, and margin, and produces an internal draft BOM for the SE to review alongside an external customer-facing BOM that only renders *after* explicit SE confirmation.

The bigger design call I made between v0.1 and v0.2 was to split the BOM template in two (internal vs. external) and gate the external PDF on SE sign-off. I also added a deterministic Python catalog pre-filter step so the agent isn't asking Claude to scan all 50 vendors on every call; that kept token cost and latency predictable while letting the model focus its reasoning on the short list that actually qualifies.

The [output](output) folder contains generated BOMs for three sample requirement lists (`REQ-001`, `REQ-002`, `REQ-003`), each with the internal draft PDF, the external customer PDF, and the raw JSON artifact.

## Repository Structure

| Path                           | Description                                                                                                                                                                        |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [QuotePilot.md](QuotePilot.md) | Full design specification — architecture, data flow, agent decision logic, failure modes, governance, and cost/latency estimates.                                                  |
| [assets](assets)               | Synthetic source data the agent reads: `catalog.json` (50-vendor SKU catalog), `pc_def.json` (product category definitions), and `rulesets.yaml` (SE-maintained evaluation rules). |
| [scripts](scripts)             | CLI tools that support the pipeline: synthetic catalog generation, catalog pre-filtering, and BOM PDF rendering.                                                                   |
| [templates](templates)         | Jinja2 templates for rendering the internal draft BOM and the external customer-facing BOM.                                                                                        |
| [output](output)               | Generated BOM artifacts per request — internal PDF, external PDF, and raw JSON.                                                                                                    |
| [tests](tests)                 | Test fixtures and verification cases for the agent and its supporting scripts.                                                                                                     |
