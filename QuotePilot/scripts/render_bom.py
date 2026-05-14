"""
render_bom.py — Render a BOM PDF from structured data using the Jinja template.

Output filename is derived automatically from the BOM's request_id, stripping the date
and appending _internal or _external. REQ-2026-0511-003 → bom_REQ-003_internal.pdf.

Usage:
  python scripts/render_bom.py                          # sample BOM, internal draft
  python scripts/render_bom.py path/to/bom.json         # internal draft, auto-named
  python scripts/render_bom.py path/to/bom.json --external   # external, auto-named
  python scripts/render_bom.py --external               # sample BOM, external

Schema follows BOMOutput / BOMLineItem from quote_pilot_design_spec.md §6.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "output"

TEMPLATE_INTERNAL = "bom_template.html.jinja"
TEMPLATE_EXTERNAL = "bom_template_external.html.jinja"


def render_pdf(bom: dict, out_path: Path, *, external: bool = False) -> None:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html", "jinja"]),
    )
    template_name = TEMPLATE_EXTERNAL if external else TEMPLATE_INTERNAL
    html_str = env.get_template(template_name).render(
        bom=bom,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_str, base_url=str(TEMPLATES_DIR)).write_pdf(str(out_path))
    variant = "external" if external else "internal draft"
    print(f"Wrote BOM PDF ({variant}) → {out_path}")


SAMPLE_BOM = {
    "request_id": "REQ-001",
    "user_request": (
        "Need 48-port PoE switches and an enterprise firewall for a 200-person office. "
        "Budget is flexible but prefer not to overspend on switching. 3-year refresh window."
    ),
    "tiers": [
        {
            "tier": "budget",
            "sku": "V005-SW-0001",
            "vendor_id": "VEN-005",
            "vendor_name": "Netgear ProAV",
            "category": "networking-switch",
            "availability": True,
            "lead_time_days": 5,
            "unit_cost": 425.00,
            "margin_pct": 14.5,
            "catalog_effective_date": "2026-04-12",
            "evidence": [
                "catalog: VEN-005 / V005-SW-0001",
                "ruleset clause: rule-001 (lead-time-threshold)",
            ],
            "gap_markers": [],
        },
        {
            "tier": "balanced",
            "sku": "V002-SW-0001",
            "vendor_id": "VEN-002",
            "vendor_name": "Juniper Networks",
            "category": "networking-switch",
            "availability": True,
            "lead_time_days": 14,
            "unit_cost": 1850.00,
            "margin_pct": 19.2,
            "catalog_effective_date": "2026-03-28",
            "evidence": [
                "catalog: VEN-002 / V002-SW-0001",
                "ruleset clause: rule-004 (margin-floor)",
            ],
            "gap_markers": [],
        },
        {
            "tier": "premium",
            "sku": "V006-SW-0001",
            "vendor_id": "VEN-006",
            "vendor_name": "Extreme Networks",
            "category": "networking-switch",
            "availability": False,
            "lead_time_days": None,
            "unit_cost": 9200.00,
            "margin_pct": 24.8,
            "catalog_effective_date": "2025-08-04",
            "evidence": [
                "catalog: VEN-006 / V006-SW-0001",
            ],
            "gap_markers": ["lead_time_days"],
        },
    ],
    "justification": {
        "budget": {
            "summary": "Low-cost, in-stock 48-port managed switch with the shortest lead time in the set.",
            "bullets": [
                "V005-SW-0001 from Netgear ProAV at $425.00",
                "Lead time: 5 days — rule-001 compliant (threshold 21 days)",
                "Margin: 14.5% — below 15% floor; rule-004 flag, SE acknowledgment required",
                "Trade-off vs. balanced: lower cost but margin flag requires override",
            ],
        },
        "balanced": {
            "summary": "Juniper switch delivers higher performance headroom and margin well above the floor within the lead-time threshold.",
            "bullets": [
                "V002-SW-0001 from Juniper Networks at $1,850.00",
                "Lead time: 14 days — rule-001 compliant",
                "Margin: 19.2% — rule-004 compliant",
                "Trade-off vs. budget: $1,425 higher cost, but clears margin floor without SE override",
            ],
        },
        "premium": {
            "summary": "Extreme Networks aggregation switch offers the highest performance but is currently unavailable with a missing lead-time field.",
            "bullets": [
                "V006-SW-0001 from Extreme Networks at $9,200.00",
                "Lead time: MISSING — gap marker; rule-001 cannot be evaluated",
                "Margin: 24.8% — rule-004 compliant",
                "Availability: Unavailable — rule-003 triggered; no available alternative found",
                "SE review required before commit; stale effective_date (2025-08-04, rule-002)",
            ],
        },
    },
    "soft_recommendation": (
        "Recommend the Balanced tier: meets all ruleset constraints, in-stock, and 19.2% "
        "margin clears the 15% floor with room to negotiate."
    ),
    "data_freshness_warnings": [
        "VEN-006 (Extreme Networks): effective_date 2025-08-04 is 280 days old; "
        "exceeds 60-day freshness threshold per rule-002.",
    ],
    "requires_human_review": True,
    "abstention_reason": None,
}


def derive_out_path(bom: dict, external: bool) -> Path:
    """REQ-003 → output/bom_REQ-003_internal.pdf"""
    request_id = bom.get("request_id", "REQ-000")
    parts = request_id.split("-")
    slug = f"{parts[0]}-{parts[-1]}"
    variant = "external" if external else "internal"
    return OUTPUT_DIR / f"bom_{slug}_{variant}.pdf"


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    external = "--external" in sys.argv

    if args:
        bom_path = Path(args[0])
        bom = json.loads(bom_path.read_text(encoding="utf-8"))
    else:
        bom = SAMPLE_BOM

    out_path = derive_out_path(bom, external)
    render_pdf(bom, out_path, external=external)


if __name__ == "__main__":
    main()
