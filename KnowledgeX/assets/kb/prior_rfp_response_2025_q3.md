---
source_doc: prior_rfp_response_2025_q3.md
doc_type: prior_rfp_response
approval_status: approved
engagement_quarter: 2025-Q3
customer_industry: healthcare_payer
---

# Prior RFP Response — 2025 Q3 (Healthcare Payer, High-Availability Deployment)

## Customer Profile

A mid-sized healthcare payer (~4,500 employees) evaluating Dynamix Core Platform as the foundation for their claims-adjudication pipeline. The customer's operational continuity requirements are tighter than the standard banking profile and informed several configuration choices documented below.

## Selected Responses

### Q-3.2 — Identity Federation

Dynamix Core Platform supports **SAML 2.0** identity federation against the customer's enterprise identity provider. Group-to-role mapping is performed through SAML attribute statements; mappings are configured in the platform admin console and audited as part of the standard access-control export. OIDC is also supported in the 2025.x release line for customers that prefer it; both protocols use the same group-to-role mapping mechanism.

### Q-3.5 — Recovery Profile (RTO / RPO)

This deployment was configured using the **High-Availability profile available in the 2025.x release line**, which leverages synchronous replication between availability zones. Under this profile the documented Recovery Point Objective (**RPO) is 5 minutes** and the Recovery Time Objective is 90 minutes for an in-region failover. The High-Availability profile is the recommended configuration for customers with regulatory or operational continuity requirements that exceed the 2024.x standard 15-minute RPO baseline.

> Note: the 2024.x release line documented a 15-minute RPO under standard asynchronous replication. The figures cited here apply only to the 2025.x High-Availability profile and should not be generalised to other deployment configurations.

### Q-3.9 — Audit Logging

Audit logging follows the standard platform model: append-only, integrity-signed, retained 365 days by default and configurable up to seven years. Healthcare deployments typically configure retention at 2,555 days to align with their record-keeping policy.

### Q-3.14 — Encryption at Rest

AES-256-GCM is the default cipher for data at rest. The 2025.x release line introduced support for customer-managed keys via HSM integration; this engagement uses customer-managed keys exclusively.

## Outcome

Awarded — production rollout completed 2025-Q4 on the High-Availability profile.
