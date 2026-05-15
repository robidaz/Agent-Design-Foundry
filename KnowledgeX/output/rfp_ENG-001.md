# RFP / RFI Response — ENG-001

**Generated:** 2026-05-12 21:23 UTC
**Status:** Draft — requires SME review before customer delivery.
## Summary

| Band | Count |
| ---- | ----- |
| HIGH | 6 |
| MEDIUM (SME review) | 14 |
| LOW (escalated) | 2 |
| NO-SOURCE (escalated) | 5 |
| CONFLICT (escalated) | 3 |
| **Total questions** | **30** |

**Escalation queue:** 10 item(s) routed to SME (see end of document and `escalation_ENG-001.md`).
---

## Per-Question Responses

### Q-001 — HIGH
**Question:** What encryption algorithm protects data at rest in Dynamix Core Platform?
**Draft answer:**

Data at rest in Dynamix Core Platform is protected by AES-256-GCM, the default cipher applied to all data on disk, including primary database storage, snapshot archives, and audit logs [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000]. The 2025.x release line additionally introduced support for customer-managed keys via HSM integration (PKCS#11 and KMIP), while earlier releases supported only platform-managed keys [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000][prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-001].
**Citations:**
- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000` (similarity 0.76)- `prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-001` (similarity 0.72)
---
### Q-002 — HIGH
**Question:** Which identity-federation protocols does Core Platform support?
**Draft answer:**

Dynamix Core Platform supports two identity-federation protocols for enterprise integration: **SAML 2.0**, available on all 2024.x and 2025.x releases, and **OIDC (OpenID Connect)**, available on 2025.x and later [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000]. Both protocols use the same group-to-role mapping mechanism — SAML via attribute statements and OIDC via standard claims — configured through the platform admin console [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000][prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-000].
**Citations:**
- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000` (similarity 0.75)- `prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-000` (similarity 0.67)
---
### Q-003 — MEDIUM · REVIEW
**Question:** What is the default audit log retention period for Core Platform?
**Draft answer:**

The default audit log retention period for Dynamix Core Platform is **365 days** [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000][prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000]. Retention is configurable from 90 days up to 2,555 days (seven years) to meet long-horizon regulatory record-keeping requirements [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000][prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000]. Audit log entries are append-only, immutable once written, and integrity-signed using the platform key hierarchy [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000].
**Citations:**
- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000` (similarity 0.67)- `prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000` (similarity 0.67)
---
### Q-004 — HIGH
**Question:** What is the typical power draw of the Edge Gateway 4400 appliance?
**Draft answer:**

The Edge Gateway 4400 series has a typical power draw of **280 W** [spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-001]. The appliance ships in a 1U form factor and is rated for an operating temperature range of 0 °C to 40 °C [spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-001].
**Citations:**
- `spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-001` (similarity 0.71)
---
### Q-005 — HIGH
**Question:** How many 10 GbE uplinks does the Edge Gateway 4400 ship with?
**Draft answer:**

The Edge Gateway 4400 ships with 4 × 10 GbE uplinks [spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-000][prior_rfp_response_2024_q4.md#prior-rfp-response-2024-q4-chunk-000]. Both the 4400 and 2200 series support LACP link aggregation on these 10 GbE uplinks [spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-000].
**Citations:**
- `spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-000` (similarity 0.73)- `prior_rfp_response_2024_q4.md#prior-rfp-response-2024-q4-chunk-000` (similarity 0.74)
---
### Q-006 — MEDIUM · REVIEW
**Question:** What minimum TLS version does Core Platform require on its interfaces?
**Draft answer:**

Dynamix Core Platform requires a minimum of TLS 1.2 on all platform-internal and external interfaces [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000]. TLS 1.3 is supported and is the negotiated default when both peers support it [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000]. The REST API integration surface likewise operates over TLS 1.2 or higher [partner_enablement_integration_guide.md#partner-enablement-integration-guide-chunk-000]. When provisioned with `--security-profile=fips`, the platform enforces TLS 1.2 with FIPS-approved cipher suites for all data in transit [prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000].
**Citations:**
- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000` (similarity 0.70)- `partner_enablement_integration_guide.md#partner-enablement-integration-guide-chunk-000` (similarity 0.65)- `prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000` (similarity 0.63)
---
### Q-007 — MEDIUM · REVIEW
**Question:** What sustained request-rate ceiling applies to Standard-tier API tokens?
**Draft answer:**

Standard-tier API tokens are subject to a sustained request-rate ceiling of **200 requests per second per token**, with a burst allowance of 500 requests per second for periods of up to 10 seconds [partner_enablement_integration_guide.md#partner-enablement-integration-guide-chunk-001]. When the limit is exceeded, the platform returns HTTP 429 with a `Retry-After` header indicating how long to wait before retrying [partner_enablement_integration_guide.md#partner-enablement-integration-guide-chunk-001].
**Citations:**
- `partner_enablement_integration_guide.md#partner-enablement-integration-guide-chunk-001` (similarity 0.68)
---
### Q-008 — HIGH
**Question:** What is the standard lead time for Edge Gateway appliance shipment?
**Draft answer:**

Edge Gateway appliances (both the 4400 and 2200 series) ship from stock within 5 business days of purchase order acknowledgement under standard demand [spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-001][prior_rfp_response_2024_q4.md#prior-rfp-response-2024-q4-chunk-001]. During quarterly close periods, lead times may extend to 10 business days [spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-001]. On-site commissioning takes approximately one engineer-day per appliance, including network integration and initial telemetry validation [prior_rfp_response_2024_q4.md#prior-rfp-response-2024-q4-chunk-001].
**Citations:**
- `spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-001` (similarity 0.66)- `prior_rfp_response_2024_q4.md#prior-rfp-response-2024-q4-chunk-001` (similarity 0.81)
---
### Q-009 — MEDIUM · REVIEW
**Question:** What operating temperature range is the Edge Gateway 4400 certified for?
**Draft answer:**

The Dynamix Edge Gateway 4400 series is certified for an operating temperature range of **0 °C to 40 °C** [spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-001]. Note that the 2200 series has a slightly wider upper bound (0 °C to 45 °C), so deployments in warmer environments should account for this difference [spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-001]. Both appliances are NEBS Level 3 certified [spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-001].
**Citations:**
- `spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-001` (similarity 0.70)
---
### Q-010 — MEDIUM · REVIEW
**Question:** What support tiers does Dynamix offer for the platform?
**Draft answer:**

Dynamix offers three published support tiers for the platform [sme_faq_internal.md#sme-faq-internal-chunk-001]:

- **Standard** — business-hours email support with a 1-business-day response target.
- **Premium** — 24×7 email and phone support with a 4-hour response target on production-impact issues.
- **Mission-Critical** — 24×7 support with a 30-minute response target, a named Technical Account Manager, and quarterly health reviews.

All Enterprise-tier subscriptions include Premium support by default [sme_faq_internal.md#sme-faq-internal-chunk-001].
**Citations:**
- `sme_faq_internal.md#sme-faq-internal-chunk-001` (similarity 0.69)
---
### Q-011 — MEDIUM · REVIEW
**Question:** What is the published pricing model for the Core Platform?
**Draft answer:**

The Core Platform is priced on a per-active-user basis, with tier discounts applying at 1,000, 5,000, and 25,000 active users [sme_faq_internal.md#sme-faq-internal-chunk-000]. Edge Gateway appliances are priced per-unit and sold separately from the Core Platform subscription [sme_faq_internal.md#sme-faq-internal-chunk-000]. A 30-day evaluation tier is available with full functionality and a 500-active-user cap, provisioned by the solutions-engineering team on request [sme_faq_internal.md#sme-faq-internal-chunk-000]. Specific list prices are not published in this document and should be routed through commercial operations [sme_faq_internal.md#sme-faq-internal-chunk-000].
**Citations:**
- `sme_faq_internal.md#sme-faq-internal-chunk-000` (similarity 0.67)
---
### Q-012 — HIGH
**Question:** How long does a typical single-site Core Platform deployment take?
**Draft answer:**

A typical single-site Core Platform deployment takes **5 – 10 engineer-days** from infrastructure-ready to validated go-live [partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-001]. This timeline covers the full provisioning sequence: infrastructure setup, Core Platform installation, identity federation configuration, optional HSM key configuration, post-install validation, and handoff to the customer&#39;s operations team with a runbook [partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-001].
**Citations:**
- `partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-001` (similarity 0.76)
---
### Q-013 — MEDIUM · REVIEW
**Question:** For a tenant with approximately 4,500 active users, what HA deployment footprint should we expect?
**Draft answer:**

For a tenant with approximately 4,500 active users, the recommended High-Availability footprint is a 3-node-per-AZ deployment totalling 9 nodes across three availability zones [partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-000]. This aligns with the sizing table that places the 500–5,000 active-user range in a 3–9 core node HA topology, with 2–6 edge gateways typically provisioned alongside [partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-001]. A prior engagement with a similarly sized (~4,500 employee) healthcare payer was delivered using this HA profile [prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-000]. A typical HA deployment runs 15–25 engineer-days from infrastructure-ready to validated go-live [partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-001].
**Citations:**
- `partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-000` (similarity 0.66)- `partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-001` (similarity 0.70)- `prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-000` (similarity 0.66)
---
### Q-014 — MEDIUM · REVIEW
**Question:** Does the platform support hardware security modules for customer-managed key storage?
**Draft answer:**

Yes, the Dynamix Core Platform supports hardware security modules (HSMs) for customer-managed key storage. The 2025.x release introduced HSM integration via both PKCS#11 and KMIP protocols, enabling customer-managed keys alongside the default AES-256-GCM encryption at rest [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000]. This capability is confirmed in a prior production engagement where customer-managed keys via HSM integration were used exclusively [prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-001]. Note that HSM integration is only available on the 2025.x release line; earlier releases supported platform-managed keys only [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000].
**Citations:**
- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000` (similarity 0.67)- `prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-001` (similarity 0.62)
---
### Q-015 — MEDIUM · REVIEW
**Question:** What runtime languages are supported by the official SDKs?
**Draft answer:**

The official Dynamix Core Platform SDKs are published for Python, Java, and TypeScript [partner_enablement_integration_guide.md#partner-enablement-integration-guide-chunk-000]. These client libraries wrap the REST surface and additionally provide idempotency-key handling, paginated iterators, and retry policy [partner_enablement_integration_guide.md#partner-enablement-integration-guide-chunk-000].
**Citations:**
- `partner_enablement_integration_guide.md#partner-enablement-integration-guide-chunk-000` (similarity 0.62)
---
### Q-016 — MEDIUM · REVIEW
**Question:** What&#39;s the upper bound on platform-supported dataset size at the Enterprise tier?
**Draft answer:**

The platform-supported maximum dataset size at the Enterprise tier is 500 TB [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001].
**Citations:**
- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001` (similarity 0.64)
---
### Q-017 — MEDIUM · REVIEW
**Question:** Can the Core Platform be deployed on Windows Server?
**Draft answer:**

Windows Server is not a supported platform for Dynamix Core Platform in the 2025.x release line [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001]. Supported platforms are Linux x86_64 (RHEL 8/9, Ubuntu 22.04 LTS) and ARM64 (RHEL 9 only) [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001]. Windows-side integration is available through the SDK, with guidance covered in the partner-enablement documentation [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001].
**Citations:**
- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001` (similarity 0.58)
---
### Q-018 — MEDIUM · REVIEW
**Question:** What is the longest retention period available for audit log entries?
**Draft answer:**

The longest available retention period for audit log entries is 2,555 days (seven years) [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000][prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000]. The default retention is 365 days, with the configurable range spanning from 90 days up to the 2,555-day maximum [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000]. Audit log entries are immutable once written and integrity-signed using the platform key hierarchy [prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000][spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000].
**Citations:**
- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000` (similarity 0.55)- `prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000` (similarity 0.59)
---
### Q-019 — MEDIUM · REVIEW
**Question:** How long after a REST endpoint is deprecated does it remain available?
**Draft answer:**

Deprecated REST endpoints remain available for two major releases after the deprecation announcement, following the platform&#39;s API deprecation policy [sme_faq_internal.md#sme-faq-internal-chunk-001].
**Citations:**
- `sme_faq_internal.md#sme-faq-internal-chunk-001` (similarity 0.62)
---
### Q-020 — MEDIUM · REVIEW
**Question:** How many Core nodes are required for a 12,000-active-user Enterprise deployment?
**Draft answer:**

A 12,000-active-user Enterprise deployment falls within the 5,000–25,000 active-user range, for which the recommended topology is High-Availability with a 5-node-per-AZ configuration, totalling **15 Core nodes** [partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-000]. This is confirmed in the sizing table, which lists 15 Core nodes for the 5,000–25,000 active-user bracket under the HA (5-per-AZ) topology [partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-001]. This configuration is also noted as the topology certified for Enterprise tier operating limits [partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-000].
**Citations:**
- `partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-000` (similarity 0.70)- `partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-001` (similarity 0.70)
---
### Q-021 — CONFLICT
**Question:** What is the Recovery Time Objective for a regional outage event?
**Conflicting versions (SME must resolve):**

- The spec sheet for the 2025.x release line documents two RTOs depending on recovery profile: 4 hours for a single-region restore under the Standard profile (asynchronous replication), and 90 minutes for in-region failover under the High-Availability profile (synchronous multi-AZ replication) [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001]. Neither figure is described as applying to a cross-region (regional outage) scenario specifically.
- The Deployment Playbook documents a third, distinct RTO for the Multi-Region Topology: for a region-out scenario, the standard published RTO is 8 hours (with RPO of 15 minutes), using asynchronous replication from a primary HA region to a secondary follower cluster; this target is described as customer-configurable [partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-000].
- The 2025 Q1 prior RFP response (2024.x release line, standard deployment) documents the RTO for a single-region restore as 4 hours using the documented runbook, with no separate cross-region or regional-outage RTO cited [prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000]. This conflicts with the Deployment Playbook&#39;s 8-hour cross-region RTO figure [partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-000], as it is unclear whether the Q1 response&#39;s 4-hour figure was intended to cover or exclude a regional outage scenario.

**Citations:**
- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001` (similarity 0.68)- `partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-000` (similarity 0.60)- `prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000` (similarity 0.59)
---
### Q-022 — LOW
**Question:** What real-time streaming ingest mechanism does Core Platform expose?
**No draft — escalated.**
*Reason:* The retrieved chunks describe the Core Platform&#39;s REST API, Webhooks, and SDKs as integration surfaces, but none of these are real-time streaming ingest mechanisms, and no chunk mentions any streaming protocol (e.g., Kafka, WebSockets, SSE, gRPC streaming) for ingest. The question cannot be answered without speculating beyond what is documented.
**Citations:**
- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000` (similarity 0.62)- `partner_enablement_integration_guide.md#partner-enablement-integration-guide-chunk-000` (similarity 0.61)- `sme_faq_internal.md#sme-faq-internal-chunk-000` (similarity 0.59)- `prior_rfp_response_2024_q4.md#prior-rfp-response-2024-q4-chunk-000` (similarity 0.58)- `sme_faq_internal.md#sme-faq-internal-chunk-001` (similarity 0.58)
---
### Q-023 — LOW
**Question:** What is the step-by-step procedure to provision customer-managed keys in production?
**No draft — escalated.**
*Reason:* The retrieved chunks acknowledge that customer-managed key (CMK) support via HSM integration (PKCS#11 and KMIP) exists in the 2025.x release and mention it as a step in the general provisioning sequence (&#34;Apply customer-managed key configuration (HSM) if required&#34;), but none of the chunks provide the actual step-by-step procedure for provisioning CMKs. Drafting a procedural answer from these chunks would require speculation about the specific configuration steps.
**Citations:**
- `partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-001` (similarity 0.64)- `prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000` (similarity 0.63)- `prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-000` (similarity 0.62)- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000` (similarity 0.61)- `sme_faq_internal.md#sme-faq-internal-chunk-000` (similarity 0.60)
---
### Q-024 — NO_SOURCE
**Question:** What is the mean-time-to-repair for an Edge Gateway hardware failure?
**No draft — escalated.**
*Reason:* None of the retrieved chunks contain any information about MTTR or repair/recovery timelines for Edge Gateway hardware failures. The chunks cover throughput specs, connectivity, deployment timelines, sizing guidance, and commercial terms — none of which address hardware failure repair metrics.
---
### Q-025 — NO_SOURCE
**Question:** Is Dynamix Core Platform FedRAMP Moderate authorized?
**No draft — escalated.**
*Reason:* None of the retrieved chunks mention FedRAMP at any level (Moderate, Low, or High), nor any FedRAMP authorization, in-process status, or agency ATO. The chunks cover related security controls (AES-256, FIPS 140-2, TLS, audit logging) but these are general security capabilities, not FedRAMP authorization data — exactly as in Example D. Drafting an affirmative or negative FedRAMP answer from these chunks would require speculation.
---
### Q-026 — NO_SOURCE
**Question:** Does the platform comply with the HIPAA Privacy Rule for protected health information?
**No draft — escalated.**
*Reason:* None of the retrieved chunks address HIPAA Privacy Rule compliance, PHI handling, or any HIPAA-related attestation. The chunks cover encryption, audit logging, identity federation, recovery profiles, and API integration — general security controls that are adjacent but do not constitute or document HIPAA compliance. Notably, the SME FAQ explicitly states it does not address regulatory authorisations or compliance attestations, and directs such questions to the compliance team.
---
### Q-027 — NO_SOURCE
**Question:** What languages does the admin console UI support?
**No draft — escalated.**
*Reason:* No KB chunks above the retrieval relevance threshold for this question.
---
### Q-028 — NO_SOURCE
**Question:** Is the platform SOC 2 Type II certified?
**No draft — escalated.**
*Reason:* None of the retrieved chunks mention SOC 2 Type II at all. The chunks cover encryption, identity federation, audit logging, recovery profiles, and support tiers — none of which address SOC 2 certification. The internal FAQ explicitly notes it does not cover compliance attestations and directs those questions to the compliance team.
---
### Q-029 — CONFLICT
**Question:** What is the documented Recovery Point Objective for the Core Platform?
**Conflicting versions (SME must resolve):**

- Under the 2024.x standard deployment profile, with asynchronous replication and snapshots running on a 15-minute cadence, the documented RPO for Dynamix Core Platform is 15 minutes [prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000]. The accompanying RTO is 4 hours for a single-region restore [prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000].
- Under the 2025.x High-Availability profile, which uses synchronous replication between availability zones [prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-000], the documented RPO for Dynamix Core Platform is 5 minutes, with an RTO of 90 minutes for an in-region failover [prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-000].
- The 2025.x release line spec sheet documents two co-existing recovery profiles for Dynamix Core Platform: (1) the Standard profile with asynchronous replication carries an RPO of 15 minutes and RTO of 4 hours single-region, and (2) the High-Availability profile with synchronous multi-AZ replication carries an RPO of 5 minutes and RTO of 90 minutes in-region failover [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001]. The spec sheet notes the recovery profile is selected at deployment time and is not switchable in place [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001].

**Citations:**
- `prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000` (similarity 0.65)- `prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-000` (similarity 0.63)- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001` (similarity 0.68)
---
### Q-030 — CONFLICT
**Question:** What is the certified sustained ingest rate of the Edge Gateway 4400 series?
**Conflicting versions (SME must resolve):**

- The published spec sheet certifies the Edge Gateway 4400 series at a sustained ingest rate of 80,000 events per second, validated against a median payload size of 1.2 KB [spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-000].
- In a 2024 Q4 customer engagement (discrete manufacturing, mixed shop-floor telemetry payload profile with a median of ~2.0 KB, larger than the spec-sheet median), the Edge Gateway 4400 series sustained ingest was confirmed at 60,000 events per second per appliance via a one-week on-site validation [prior_rfp_response_2024_q4.md#prior-rfp-response-2024-q4-chunk-000].

**Citations:**
- `spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-000` (similarity 0.74)- `prior_rfp_response_2024_q4.md#prior-rfp-response-2024-q4-chunk-000` (similarity 0.74)
---

## Reviewer Checklist

- [ ] Every HIGH draft has at least one citation and the citation maps to a real KB chunk.
- [ ] Every MEDIUM draft's uncertainty note is reviewed and confirmed.
- [ ] Every LOW / NO-SOURCE / CONFLICT item is addressed in the escalation queue.
- [ ] No customer-confidential information was added to the draft from outside the KB.