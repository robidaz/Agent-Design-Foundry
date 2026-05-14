---
source_doc: prior_rfp_response_2024_q4.md
doc_type: prior_rfp_response
approval_status: approved
engagement_quarter: 2024-Q4
customer_industry: manufacturing
---

# Prior RFP Response — 2024 Q4 (Manufacturing, Edge Deployment)

## Customer Profile

A discrete-manufacturing customer with 12 production sites evaluating the Dynamix Edge Gateway as the on-site data collection and aggregation tier for shop-floor telemetry. The Core Platform was already deployed in their central data centre; this RFP focused exclusively on the Edge tier.

## Selected Responses

### Q-4.1 — Edge Gateway Throughput

The Dynamix Edge Gateway 4400 series is rated for sustained ingest of up to **60,000 events per second per appliance** at this customer's mixed payload profile (median ~2.0 KB, larger than the spec-sheet median). Throughput was confirmed in a one-week customer-site validation against shop-floor telemetry. The 2200 series is rated at 20,000 events per second for smaller sites under the spec-sheet payload profile.

### Q-4.4 — Port Density and Connectivity

The Edge Gateway 4400 ships with 24 × 1 GbE ports and 4 × 10 GbE uplinks; the 2200 series ships with 8 × 1 GbE ports and 2 × 10 GbE uplinks. Both appliances support PoE+ on a subset of ports for downstream sensor power; PoE++ is not supported in the current generation.

### Q-4.8 — Bandwidth Profile for Upstream Replication

A single 4400 series appliance under peak load (80,000 EPS) consumes approximately 95 Mbps of upstream bandwidth to the Core Platform tier after on-device deduplication and compression. Customers with constrained WAN links may configure aggressive batching and accept higher end-to-end latency in exchange for lower bandwidth utilisation.

### Q-4.13 — Deployment Timelines

Edge Gateway appliances are stocked and ship within 5 business days of purchase order acknowledgement. On-site commissioning takes approximately one engineer-day per appliance including network integration and initial telemetry validation.

## Outcome

Awarded — 18-appliance rollout across the 12 production sites; rollout completed 2025-Q1.
