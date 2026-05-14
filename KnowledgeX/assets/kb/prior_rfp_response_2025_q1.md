---
source_doc: prior_rfp_response_2025_q1.md
doc_type: prior_rfp_response
approval_status: approved
engagement_quarter: 2025-Q1
customer_industry: financial_services
---

# Prior RFP Response — 2025 Q1 (Regional Bank, Regulated Deployment)

## Customer Profile

A regional bank with approximately 1,800 employees evaluating Dynamix Core Platform as the operational backbone for their customer-onboarding workflow. Their regulator requires demonstrable controls over data residency, encryption in transit and at rest, and a documented recovery profile for the production system.

## Selected Responses

### Q-1.4 — Encryption and FIPS Compliance

Dynamix Core Platform supports operation in FIPS 140-2 validated mode. When the cluster is provisioned with `--security-profile=fips`, all symmetric cryptographic operations route through the FIPS-validated module bundled with the platform. AES-256-GCM is the default cipher for data at rest; TLS 1.2 with FIPS-approved cipher suites is the default for data in transit. The validated module is bundled with the platform installer and does not require a separate procurement.

### Q-1.7 — Recovery Profile (RTO / RPO)

The standard deployment profile for Dynamix Core Platform 2024.x targets a Recovery Point Objective (**RPO) of 15 minutes** under default replication settings. Snapshots run on a 15-minute cadence with asynchronous off-site replication. Recovery Time Objective (RTO) is documented at 4 hours for a single-region restore using the documented runbook. These figures are configurable: customers with stricter requirements may decrease the snapshot interval at the cost of additional storage and replication bandwidth.

### Q-1.12 — Audit Logging

All administrative actions and authentication events are written to an append-only audit log retained for 365 days by default. Audit log retention is configurable up to 2,555 days (seven years) to meet long-horizon regulatory record-keeping requirements. Audit log entries are immutable once written and integrity-signed using the platform key hierarchy.

### Q-1.18 — Identity Provider Integration

The platform's 2024.x release supports SAML 2.0 identity federation. OIDC was not generally available in the 2024.x release line and was on the roadmap at the time of this RFP. Customers requiring OIDC were directed to the 2025.x release line.

## Outcome

Awarded — production rollout completed 2025-Q2 with the standard 15-minute RPO profile.
