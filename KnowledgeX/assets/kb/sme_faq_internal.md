---
source_doc: sme_faq_internal.md
doc_type: sme_faq
approval_status: approved
audience: internal_sme
---

# Internal SME FAQ

A working document maintained by the Dynamix solutions-engineering team. Captures questions that recur across customer engagements but do not fit cleanly into the spec sheets or partner-enablement material. Reviewed monthly; questions may be promoted to other documents once they stabilise.

## Roadmap and Release Cadence

**Q: When does the next major release ship?**
The 2026.x release line is targeted for general availability in Q3 2026. Specific features (PoE++ on Edge Gateway, regional active-active failover for Core Platform, additional language coverage for the admin console) are tracked on the internal roadmap board; commitments to specific customers should be routed through product management.

**Q: How long are LTS releases supported?**
Long-term support releases receive security patches for 36 months from general availability and critical-defect fixes for 24 months. The 2024.x release line is the current LTS; 2025.x will be designated LTS at general availability of 2026.x.

## Pricing and Commercial

**Q: How is the platform priced?**
Pricing is per-active-user with tier discounts at 1,000, 5,000, and 25,000 active users. The Edge Gateway appliances are priced per-unit and are sold separately from the Core Platform subscription. Specific customer pricing should be routed through commercial operations; this FAQ does not publish list prices.

**Q: Is there a freemium or trial tier?**
A 30-day evaluation tier is available with full functionality and a 500-active-user cap. Evaluations are provisioned by the solutions-engineering team on request.

## Support Tiers

**Q: What support tiers are offered?**
Three support tiers are published: Standard (business-hours email, 1-business-day response), Premium (24×7 email + phone, 4-hour response on production-impact issues), and Mission-Critical (24×7 with a 30-minute response target, named technical account manager, and quarterly health reviews). All Enterprise-tier subscriptions include Premium support by default.

## Operational Questions

**Q: Can the Core Platform be air-gapped?**
Air-gapped deployments are supported with a separately licensed offline-update bundle that customers stage internally. Air-gap deployments forfeit several telemetry-driven features (anomaly detection model updates, hosted health monitoring) and are recommended only when regulatory or policy requirements make connectivity infeasible.

**Q: What's our position on backwards compatibility?**
Database schema and on-disk format changes are forward-only within a major release line; downgrade is not supported. API surfaces follow a two-major-release deprecation policy: a deprecated endpoint remains available for two major releases after the deprecation announcement.

---

*This FAQ is deliberately scoped to operational and commercial questions that recur in engagements. It does not address regulatory authorisations, compliance attestations, or non-English-language coverage; those are tracked separately and should be sourced from the compliance team rather than this document.*
