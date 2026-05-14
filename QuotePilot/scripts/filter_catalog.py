"""
filter_catalog.py — Pre-filter catalog.json to qualifying candidates for requested categories.

Reads thresholds live from rulesets.yaml so filter behavior tracks any SE-approved rule changes.

Hard-excludes rule-005 violations (null unit_cost or missing margin_pct).
Soft-annotates rule-001 (lead time), rule-002 (data freshness), rule-003 (availability),
rule-004 (margin floor) so the agent sees pre-computed flags instead of re-deriving them.

For single-category queries this typically cuts candidate count by 60–70%. For broad
multi-category queries the primary savings are rule pre-annotation and eliminating the
separate rulesets.yaml read — the agent reasons over pre-labelled rows instead of applying
rules mentally across the full catalog.

Usage:
  .venv/bin/python QuotePilot/scripts/filter_catalog.py <cat1> [<cat2> ...] [--out path.json]

Output is written to --out path (default: QuotePilot/output/catalog_filtered.json).
The agent reads this file instead of catalog.json + rulesets.yaml.
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
CATALOG_PATH = ROOT / "assets" / "catalog.json"
RULESETS_PATH = ROOT / "assets" / "rulesets.yaml"
DEFAULT_OUT = ROOT / "output" / "catalog_filtered.json"


def load_thresholds() -> dict:
    data = yaml.safe_load(RULESETS_PATH.read_text(encoding="utf-8"))
    thresholds: dict = {}
    for rule in data.get("rules", []):
        rid = rule["id"]
        val = rule["condition"].get("value")
        if rid == "rule-001" and val is not None:
            thresholds["lead_time_days"] = int(val)
        elif rid == "rule-002" and val is not None:
            thresholds["freshness_days"] = int(val)
        elif rid == "rule-004" and val is not None:
            thresholds["margin_pct_floor"] = float(val)
    return thresholds


def age_days(date_str: str) -> int:
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (date.today() - d).days


def filter_catalog(categories: list[str], thresholds: dict) -> dict:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    cat_set = set(categories)

    lead_limit = thresholds["lead_time_days"]
    fresh_limit = thresholds["freshness_days"]
    margin_floor = thresholds["margin_pct_floor"]

    candidates: list[dict] = []
    excluded: list[dict] = []
    total_skus = 0

    for vendor in catalog.get("vendors", []):
        vendor_id = vendor["vendor_id"]
        vendor_name = vendor["vendor_name"]
        effective_date = vendor.get("effective_date", "")
        vendor_age = age_days(effective_date) if effective_date else None

        for product in vendor.get("products", []):
            total_skus += 1
            category = product.get("category", "")

            if category not in cat_set:
                continue

            sku = product["sku"]
            unit_cost = product.get("unit_cost")
            margin_pct = product.get("margin_pct")
            lead_time = product.get("lead_time_days")
            availability = product.get("availability", False)

            # rule-005: hard block — missing pricing data
            missing_fields = []
            if unit_cost is None:
                missing_fields.append("unit_cost")
            if margin_pct is None:
                missing_fields.append("margin_pct")
            # Also catch bad-type lead_time (e.g. "21 days" string)
            if lead_time is not None and not isinstance(lead_time, (int, float)):
                missing_fields.append(f"lead_time_days (bad type: {lead_time!r})")
                lead_time = None

            if missing_fields:
                excluded.append({
                    "vendor_id": vendor_id,
                    "vendor_name": vendor_name,
                    "sku": sku,
                    "category": category,
                    "rule": "rule-005",
                    "reason": f"missing or null: {', '.join(missing_fields)}",
                })
                continue

            # Soft rule annotations
            rules_fired: list[str] = []

            if vendor_age is not None and vendor_age > fresh_limit:
                rules_fired.append(
                    f"rule-002 (stale: {vendor_age}d old, threshold {fresh_limit}d)"
                )

            if not availability:
                rules_fired.append("rule-003 (availability: false)")

            if lead_time is not None and lead_time > lead_limit:
                rules_fired.append(
                    f"rule-001 (lead_time {lead_time}d exceeds {lead_limit}d threshold)"
                )

            if margin_pct < margin_floor:
                rules_fired.append(
                    f"rule-004 (margin {margin_pct}% below {margin_floor}% floor)"
                )

            candidates.append({
                "vendor_id": vendor_id,
                "vendor_name": vendor_name,
                "effective_date": effective_date,
                "sku": sku,
                "category": category,
                "description": product.get("description", ""),
                "availability": availability,
                "lead_time_days": lead_time,
                "unit_cost": unit_cost,
                "margin_pct": margin_pct,
                "rules_fired": rules_fired,
            })

    return {
        "filter_generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "categories_requested": categories,
        "thresholds_applied": thresholds,
        "summary": {
            "total_vendors_scanned": len(catalog.get("vendors", [])),
            "total_skus_scanned": total_skus,
            "candidates_returned": len(candidates),
            "excluded_rule005": len(excluded),
        },
        "candidates": candidates,
        "excluded_rule005": excluded,
    }


def main() -> None:
    raw_args = sys.argv[1:]
    out_path = DEFAULT_OUT
    categories: list[str] = []

    i = 0
    while i < len(raw_args):
        if raw_args[i] == "--out" and i + 1 < len(raw_args):
            out_path = Path(raw_args[i + 1])
            i += 2
        else:
            categories.append(raw_args[i])
            i += 1

    if not categories:
        print("Usage: filter_catalog.py <category1> [<category2> ...] [--out path.json]", file=sys.stderr)
        sys.exit(1)

    thresholds = load_thresholds()
    result = filter_catalog(categories, thresholds)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    s = result["summary"]
    print(
        f"Filtered catalog: {s['total_skus_scanned']} SKUs scanned → "
        f"{s['candidates_returned']} candidates, "
        f"{s['excluded_rule005']} excluded (rule-005). "
        f"Written to {out_path}"
    )


if __name__ == "__main__":
    main()
