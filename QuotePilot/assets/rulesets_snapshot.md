> **Snapshot only — do not manage this file.** This document is a human-readable rendering of
> [`rulesets.yaml`](rulesets.yaml). It is generated for reference purposes and is not kept in sync
> automatically. For authoritative rule definitions, refer to `rulesets.yaml` directly.

# QuotePilot Rulesets

**Version:** 1.0
**Last updated:** 2026-05-11
**Authored by:** SE

Evaluation rules applied by the QuotePilot agent before including any SKU in a BOM draft. The agent reads this document at the start of every session before querying the catalog. Rules may be updated by the SE; the agent may propose amendments only with explicit per-session write authorization.

---

## Rules

| ID | Name | Applies To | Condition | Severity | Agent Action |
| --- | --- | --- | --- | --- | --- |
| rule-001 | Lead Time Threshold | `product.lead_time_days` | `> 21 days` | warn | Search for an alternative SKU in the same category and tier with `lead_time_days <= 21`. If a qualifying alternative exists, prefer it and note the substitution in the BOM justification. If no alternative exists, include the original SKU and surface the lead-time breach to the SE with the exact value and nearest available alternative (if any). |
| rule-002 | Vendor Data Freshness | `vendor.effective_date` | `> 60 days` before query date | warn | Before including any SKU from this vendor in the BOM, surface a stale-data warning to the SE including `vendor_id`, `vendor_name`, `effective_date`, and days since last update. Do not block inclusion — the SE may choose to proceed — but the warning must appear in BOM output regardless of the SE's decision. |
| rule-003 | SKU Availability Gate | `product.availability` | `== false` | warn | Deprioritize unavailable SKUs. First attempt to satisfy the requirement using an available SKU in the same category and tier. If no available alternative exists, include the unavailable SKU as the sole candidate labeled "UNAVAILABLE — no in-stock alternative found." SE must acknowledge before quote is finalized. |
| rule-004 | Margin Floor | `product.margin_pct` | `< 15.0%` | flag | Do not automatically include the SKU. Surface it to the SE with the exact `margin_pct` value and a note that it falls below the 15% floor. If the SE explicitly approves inclusion within the session, proceed and annotate the BOM line with "SE-approved below-margin exception." Otherwise, prefer the next qualifying SKU that meets the floor. |
| rule-005 | Incomplete Pricing Data | `product.unit_cost`, `product.margin_pct` | `unit_cost == null` or `margin_pct` missing | block | Skip this SKU entirely — do not include it in any BOM tier. Log the `sku_id`, `vendor_id`, and the specific missing/null fields as a bad-data entry. If the skipped SKU was the only candidate for a required BOM slot, surface the gap to the SE and request guidance — do not leave the slot empty without notification. |
