---
source_doc: partner_enablement_deployment_playbook.md
doc_type: partner_enablement
approval_status: approved
audience: deployment_partners
---

# Deployment Playbook — Dynamix Core Platform

This playbook captures the reference deployment topologies that partner field engineers use when sizing and provisioning Dynamix Core Platform installations. It is the authoritative source for topology recommendations and standard sizing.

## Reference Topologies

### Single-Site Topology

Used for customers with a single data centre and no cross-region availability requirement. The Core Platform runs in a 3-node cluster with local quorum. Standard recovery profile applies (RPO 15 minutes, RTO 4 hours). Targets up to 5,000 concurrent active users and 50 TB of primary data.

### High-Availability Topology

Used for customers requiring in-region resilience. Spans three availability zones with synchronous replication. Quorum is maintained across zones; loss of a single AZ does not interrupt service. This topology pairs with the High-Availability recovery profile (RPO 5 minutes, RTO 90 minutes in-region failover). Recommended for tenants of any size with regulatory or operational continuity requirements.

For tenants in the 1,000 – 5,000 active-user range, a 3-node-per-AZ deployment (9 nodes total) is the standard footprint. For tenants in the 5,000 – 25,000 active-user range, a 5-node-per-AZ deployment (15 nodes total) is recommended and is the configuration certified for the Enterprise tier operating limits.

### Multi-Region Topology

Used for customers with explicit cross-region recovery requirements or data residency constraints that span regions. A primary region runs the High-Availability topology; a secondary region runs a smaller follower cluster receiving asynchronous replication. Cross-region RPO and RTO are customer-configurable; the standard published targets are RPO 15 minutes and RTO 8 hours for a region-out scenario.

## Sizing Guidance

| Active users | Recommended topology | Core nodes | Edge gateways (typical) |
| ------------ | -------------------- | ---------- | ----------------------- |
| ≤ 500 | Single-Site | 3 | 0 – 2 |
| 500 – 5,000 | Single-Site or HA | 3 – 9 | 2 – 6 |
| 5,000 – 25,000 | HA (5-per-AZ) | 15 | 6 – 18 |
| ≥ 25,000 | Multi-Region | 15 + follower | per-site |

## Provisioning Sequence

1. Provision infrastructure (compute, storage, networking) per the topology sizing.
2. Install the Core Platform via the documented installer.
3. Configure identity federation (SAML or OIDC) against the customer's IdP.
4. Apply customer-managed key configuration (HSM) if required.
5. Run the post-install validation suite documented in the partner portal.
6. Hand-off to the customer's operations team with the runbook attached.

A typical single-site deployment takes 5 – 10 engineer-days from infrastructure-ready to validated go-live. A High-Availability deployment takes 15 – 25 engineer-days. Multi-region deployments are scoped per engagement.
