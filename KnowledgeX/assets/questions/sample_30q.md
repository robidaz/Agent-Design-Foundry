# Sample RFP Question List — 30 Questions

**Engagement ID:** ENG-001
**Customer:** Synthetic — used for KnowledgeX PoC verification

Each question carries an inline `<!-- expected_band: ... -->` annotation used
by the band-distribution check in `test_cases.md`. The annotations are
stripped by `knowledgex.parser.parse()` before retrieval.

Expected distribution: HIGH=12, MEDIUM=8, LOW=3, NO_SOURCE=4, CONFLICT=3.

---

## Q-001
**Section:** Security
**Question:** What encryption algorithm protects data at rest in Dynamix Core Platform?
<!-- expected_band: HIGH -->

## Q-002
**Section:** Identity
**Question:** Which identity-federation protocols does Core Platform support?
<!-- expected_band: HIGH -->

## Q-003
**Section:** Auditing
**Question:** What is the default audit log retention period for Core Platform?
<!-- expected_band: HIGH -->

## Q-004
**Section:** Hardware
**Question:** What is the typical power draw of the Edge Gateway 4400 appliance?
<!-- expected_band: HIGH -->

## Q-005
**Section:** Hardware
**Question:** How many 10 GbE uplinks does the Edge Gateway 4400 ship with?
<!-- expected_band: HIGH -->

## Q-006
**Section:** Security
**Question:** What minimum TLS version does Core Platform require on its interfaces?
<!-- expected_band: HIGH -->

## Q-007
**Section:** Integration
**Question:** What sustained request-rate ceiling applies to Standard-tier API tokens?
<!-- expected_band: HIGH -->

## Q-008
**Section:** Commercial
**Question:** What is the standard lead time for Edge Gateway appliance shipment?
<!-- expected_band: HIGH -->

## Q-009
**Section:** Hardware
**Question:** What operating temperature range is the Edge Gateway 4400 certified for?
<!-- expected_band: HIGH -->

## Q-010
**Section:** Support
**Question:** What support tiers does Dynamix offer for the platform?
<!-- expected_band: HIGH -->

## Q-011
**Section:** Commercial
**Question:** What is the published pricing model for the Core Platform?
<!-- expected_band: HIGH -->

## Q-012
**Section:** Deployment
**Question:** How long does a typical single-site Core Platform deployment take?
<!-- expected_band: HIGH -->

## Q-013
**Section:** Deployment
**Question:** For a tenant with approximately 4,500 active users, what HA deployment footprint should we expect?
<!-- expected_band: MEDIUM -->

## Q-014
**Section:** Security
**Question:** Does the platform support hardware security modules for customer-managed key storage?
<!-- expected_band: MEDIUM -->

## Q-015
**Section:** Integration
**Question:** What runtime languages are supported by the official SDKs?
<!-- expected_band: MEDIUM -->

## Q-016
**Section:** Operating Limits
**Question:** What's the upper bound on platform-supported dataset size at the Enterprise tier?
<!-- expected_band: MEDIUM -->

## Q-017
**Section:** Platform Support
**Question:** Can the Core Platform be deployed on Windows Server?
<!-- expected_band: MEDIUM -->

## Q-018
**Section:** Auditing
**Question:** What is the longest retention period available for audit log entries?
<!-- expected_band: MEDIUM -->

## Q-019
**Section:** Integration
**Question:** How long after a REST endpoint is deprecated does it remain available?
<!-- expected_band: MEDIUM -->

## Q-020
**Section:** Deployment
**Question:** How many Core nodes are required for a 12,000-active-user Enterprise deployment?
<!-- expected_band: MEDIUM -->

## Q-021
**Section:** Resilience
**Question:** What is the Recovery Time Objective for a regional outage event?
<!-- expected_band: CONFLICT -->

## Q-022
**Section:** Integration
**Question:** What real-time streaming ingest mechanism does Core Platform expose?
<!-- expected_band: LOW -->

## Q-023
**Section:** Security
**Question:** What is the step-by-step procedure to provision customer-managed keys in production?
<!-- expected_band: LOW -->

## Q-024
**Section:** Hardware
**Question:** What is the mean-time-to-repair for an Edge Gateway hardware failure?
<!-- expected_band: LOW -->

## Q-025
**Section:** Compliance
**Question:** Is Dynamix Core Platform FedRAMP Moderate authorized?
<!-- expected_band: NO_SOURCE -->

## Q-026
**Section:** Compliance
**Question:** Does the platform comply with the HIPAA Privacy Rule for protected health information?
<!-- expected_band: NO_SOURCE -->

## Q-027
**Section:** UX
**Question:** What languages does the admin console UI support?
<!-- expected_band: NO_SOURCE -->

## Q-028
**Section:** Compliance
**Question:** Is the platform SOC 2 Type II certified?
<!-- expected_band: NO_SOURCE -->

## Q-029
**Section:** Resilience
**Question:** What is the documented Recovery Point Objective for the Core Platform?
<!-- expected_band: CONFLICT -->

## Q-030
**Section:** Hardware
**Question:** What is the certified sustained ingest rate of the Edge Gateway 4400 series?
<!-- expected_band: CONFLICT -->
