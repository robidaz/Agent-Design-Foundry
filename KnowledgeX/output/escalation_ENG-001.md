# SME Escalation Queue — ENG-001

**Generated:** 2026-05-12 21:23 UTC
**Items to resolve:** 10

The questions below have no committed draft. Each item carries the retrieval evidence the agent had at the time of escalation. Please provide a definitive answer, supply an additional source, or mark the item unanswerable.

---

## Q-021 — CONFLICT

**Question:** What is the Recovery Time Objective for a regional outage event?

**Conflicting versions retrieved (please select an authoritative version or supply a new source):**

- The spec sheet for the 2025.x release line documents two RTOs depending on recovery profile: 4 hours for a single-region restore under the Standard profile (asynchronous replication), and 90 minutes for in-region failover under the High-Availability profile (synchronous multi-AZ replication) [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001]. Neither figure is described as applying to a cross-region (regional outage) scenario specifically.
- The Deployment Playbook documents a third, distinct RTO for the Multi-Region Topology: for a region-out scenario, the standard published RTO is 8 hours (with RPO of 15 minutes), using asynchronous replication from a primary HA region to a secondary follower cluster; this target is described as customer-configurable [partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-000].
- The 2025 Q1 prior RFP response (2024.x release line, standard deployment) documents the RTO for a single-region restore as 4 hours using the documented runbook, with no separate cross-region or regional-outage RTO cited [prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000]. This conflicts with the Deployment Playbook&#39;s 8-hour cross-region RTO figure [partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-000], as it is unclear whether the Q1 response&#39;s 4-hour figure was intended to cover or exclude a regional outage scenario.

**Retrieval evidence:**
- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001` (similarity 0.68)- `partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-000` (similarity 0.60)- `prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000` (similarity 0.59)
---
## Q-022 — LOW

**Question:** What real-time streaming ingest mechanism does Core Platform expose?

**Escalation reason:** The retrieved chunks describe the Core Platform&#39;s REST API, Webhooks, and SDKs as integration surfaces, but none of these are real-time streaming ingest mechanisms, and no chunk mentions any streaming protocol (e.g., Kafka, WebSockets, SSE, gRPC streaming) for ingest. The question cannot be answered without speculating beyond what is documented.
**Retrieval evidence:**
- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000` (similarity 0.62)- `partner_enablement_integration_guide.md#partner-enablement-integration-guide-chunk-000` (similarity 0.61)- `sme_faq_internal.md#sme-faq-internal-chunk-000` (similarity 0.59)- `prior_rfp_response_2024_q4.md#prior-rfp-response-2024-q4-chunk-000` (similarity 0.58)- `sme_faq_internal.md#sme-faq-internal-chunk-001` (similarity 0.58)
---
## Q-023 — LOW

**Question:** What is the step-by-step procedure to provision customer-managed keys in production?

**Escalation reason:** The retrieved chunks acknowledge that customer-managed key (CMK) support via HSM integration (PKCS#11 and KMIP) exists in the 2025.x release and mention it as a step in the general provisioning sequence (&#34;Apply customer-managed key configuration (HSM) if required&#34;), but none of the chunks provide the actual step-by-step procedure for provisioning CMKs. Drafting a procedural answer from these chunks would require speculation about the specific configuration steps.
**Retrieval evidence:**
- `partner_enablement_deployment_playbook.md#partner-enablement-deployment-playbook-chunk-001` (similarity 0.64)- `prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000` (similarity 0.63)- `prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-000` (similarity 0.62)- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-000` (similarity 0.61)- `sme_faq_internal.md#sme-faq-internal-chunk-000` (similarity 0.60)
---
## Q-024 — NO_SOURCE

**Question:** What is the mean-time-to-repair for an Edge Gateway hardware failure?

**Escalation reason:** None of the retrieved chunks contain any information about MTTR or repair/recovery timelines for Edge Gateway hardware failures. The chunks cover throughput specs, connectivity, deployment timelines, sizing guidance, and commercial terms — none of which address hardware failure repair metrics.
**Retrieval evidence:** none above the relevance threshold.
---
## Q-025 — NO_SOURCE

**Question:** Is Dynamix Core Platform FedRAMP Moderate authorized?

**Escalation reason:** None of the retrieved chunks mention FedRAMP at any level (Moderate, Low, or High), nor any FedRAMP authorization, in-process status, or agency ATO. The chunks cover related security controls (AES-256, FIPS 140-2, TLS, audit logging) but these are general security capabilities, not FedRAMP authorization data — exactly as in Example D. Drafting an affirmative or negative FedRAMP answer from these chunks would require speculation.
**Retrieval evidence:** none above the relevance threshold.
---
## Q-026 — NO_SOURCE

**Question:** Does the platform comply with the HIPAA Privacy Rule for protected health information?

**Escalation reason:** None of the retrieved chunks address HIPAA Privacy Rule compliance, PHI handling, or any HIPAA-related attestation. The chunks cover encryption, audit logging, identity federation, recovery profiles, and API integration — general security controls that are adjacent but do not constitute or document HIPAA compliance. Notably, the SME FAQ explicitly states it does not address regulatory authorisations or compliance attestations, and directs such questions to the compliance team.
**Retrieval evidence:** none above the relevance threshold.
---
## Q-027 — NO_SOURCE

**Question:** What languages does the admin console UI support?

**Escalation reason:** No KB chunks above the retrieval relevance threshold for this question.
**Retrieval evidence:** none above the relevance threshold.
---
## Q-028 — NO_SOURCE

**Question:** Is the platform SOC 2 Type II certified?

**Escalation reason:** None of the retrieved chunks mention SOC 2 Type II at all. The chunks cover encryption, identity federation, audit logging, recovery profiles, and support tiers — none of which address SOC 2 certification. The internal FAQ explicitly notes it does not cover compliance attestations and directs those questions to the compliance team.
**Retrieval evidence:** none above the relevance threshold.
---
## Q-029 — CONFLICT

**Question:** What is the documented Recovery Point Objective for the Core Platform?

**Conflicting versions retrieved (please select an authoritative version or supply a new source):**

- Under the 2024.x standard deployment profile, with asynchronous replication and snapshots running on a 15-minute cadence, the documented RPO for Dynamix Core Platform is 15 minutes [prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000]. The accompanying RTO is 4 hours for a single-region restore [prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000].
- Under the 2025.x High-Availability profile, which uses synchronous replication between availability zones [prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-000], the documented RPO for Dynamix Core Platform is 5 minutes, with an RTO of 90 minutes for an in-region failover [prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-000].
- The 2025.x release line spec sheet documents two co-existing recovery profiles for Dynamix Core Platform: (1) the Standard profile with asynchronous replication carries an RPO of 15 minutes and RTO of 4 hours single-region, and (2) the High-Availability profile with synchronous multi-AZ replication carries an RPO of 5 minutes and RTO of 90 minutes in-region failover [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001]. The spec sheet notes the recovery profile is selected at deployment time and is not switchable in place [spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001].

**Retrieval evidence:**
- `prior_rfp_response_2025_q1.md#prior-rfp-response-2025-q1-chunk-000` (similarity 0.65)- `prior_rfp_response_2025_q3.md#prior-rfp-response-2025-q3-chunk-000` (similarity 0.63)- `spec_sheet_dynamix_core_platform.md#spec-sheet-dynamix-core-platform-chunk-001` (similarity 0.68)
---
## Q-030 — CONFLICT

**Question:** What is the certified sustained ingest rate of the Edge Gateway 4400 series?

**Conflicting versions retrieved (please select an authoritative version or supply a new source):**

- The published spec sheet certifies the Edge Gateway 4400 series at a sustained ingest rate of 80,000 events per second, validated against a median payload size of 1.2 KB [spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-000].
- In a 2024 Q4 customer engagement (discrete manufacturing, mixed shop-floor telemetry payload profile with a median of ~2.0 KB, larger than the spec-sheet median), the Edge Gateway 4400 series sustained ingest was confirmed at 60,000 events per second per appliance via a one-week on-site validation [prior_rfp_response_2024_q4.md#prior-rfp-response-2024-q4-chunk-000].

**Retrieval evidence:**
- `spec_sheet_dynamix_edge_gateway.md#spec-sheet-dynamix-edge-gateway-chunk-000` (similarity 0.74)- `prior_rfp_response_2024_q4.md#prior-rfp-response-2024-q4-chunk-000` (similarity 0.74)
---
