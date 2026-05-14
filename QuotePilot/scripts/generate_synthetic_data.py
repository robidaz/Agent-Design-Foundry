"""
generate_synthetic_data.py — QuotePilot synthetic catalog generator

Outputs:
  assets/catalog.json            — clean JSON, 50 vendors, 2-4 SKUs each, 4 categories
  assets/catalog_exceptions.txt — exception log with data paths for all special cases

Special cases injected at fixed vendor IDs for repeatability:
  VEN-006  networking-switch      EXPIRED effective_date
  VEN-012  network-security       EXPIRED effective_date
  VEN-017  wireless-access-point  EXPIRED effective_date
  VEN-022  structured-cabling     EXPIRED effective_date
  VEN-023  networking-switch      BAD DATA — lead_time_days wrong type (string)
  VEN-024  structured-cabling     BAD DATA — missing margin_pct, unit_cost null

Run: python scripts/generate_synthetic_data.py
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

SEED = 42
random.seed(SEED)

ASSETS_DIR = Path(__file__).parent.parent / "assets"
CATALOG_PATH = ASSETS_DIR / "catalog.json"
EXCEPTIONS_PATH = ASSETS_DIR / "catalog_exceptions.txt"

SOURCE_LAST_UPDATED = "2026-05-01"
QUERY_DATE = date(2026, 5, 11)
STALE_THRESHOLD_DAYS = 90

# ---------------------------------------------------------------------------
# Product templates per category
# ---------------------------------------------------------------------------

PRODUCTS: dict[str, list[dict]] = {
    "networking-switch": [
        {"desc": "48-port PoE+ managed switch, 740W, stackable", "cost": (800, 5000), "margin": (14, 26)},
        {"desc": "24-port PoE+ managed switch, 370W, fixed uplinks", "cost": (500, 2500), "margin": (14, 24)},
        {"desc": "48-port 10GbE aggregation switch, 4x40G uplinks", "cost": (4000, 14000), "margin": (20, 28)},
        {"desc": "8-port PoE+ unmanaged switch, desktop, budget tier", "cost": (150, 450), "margin": (11, 16)},
    ],
    "network-security": [
        {"desc": "NGFW, branch tier, 1-5Gbps App-ID throughput", "cost": (600, 4000), "margin": (18, 28)},
        {"desc": "NGFW, enterprise edge, 6-15Gbps throughput, SD-WAN", "cost": (4000, 16000), "margin": (22, 30)},
        {"desc": "UTM appliance, SMB, all-in-one threat prevention", "cost": (400, 2000), "margin": (16, 24)},
        {"desc": "IDS/IPS inline sensor, 10Gbps inspection throughput", "cost": (3000, 10000), "margin": (20, 27)},
    ],
    "wireless-access-point": [
        {"desc": "Wi-Fi 6E tri-band indoor AP, 6GHz, 4x4 MU-MIMO", "cost": (400, 1200), "margin": (12, 30)},
        {"desc": "Wi-Fi 6 dual-band indoor AP, 2x2 MU-MIMO, ceiling mount", "cost": (150, 600), "margin": (12, 28)},
        {"desc": "Wi-Fi 6 outdoor AP, IP67, PoE-powered", "cost": (300, 1400), "margin": (14, 28)},
        {"desc": "Wi-Fi 7 indoor AP, 9Gbps aggregate, cloud-managed", "cost": (180, 1200), "margin": (12, 30)},
    ],
    "structured-cabling": [
        {"desc": "Cat6A UTP patch cable 3ft, 25-pack", "cost": (80, 200), "margin": (13, 20)},
        {"desc": "48-port Cat6A patch panel, 2U, angled", "cost": (350, 700), "margin": (15, 21)},
        {"desc": "Cat6A U/UTP bulk cable, CMR-rated, 1000ft spool", "cost": (400, 950), "margin": (13, 19)},
        {"desc": "Cat6A keystone jack, toolless, 25-pack", "cost": (100, 250), "margin": (15, 22)},
    ],
}

CATEGORIES = list(PRODUCTS.keys())

VENDOR_NAMES = [
    "Cisco Systems", "Juniper Networks", "Aruba Networks (HPE)", "Arista Networks",
    "Netgear ProAV", "Extreme Networks", "Palo Alto Networks", "Fortinet",
    "Check Point Software", "WatchGuard Technologies", "Cisco (Security Division)", "SonicWall",
    "Cisco Meraki", "Aruba Networks (HPE) — Wireless", "Ubiquiti UniFi", "Ruckus Networks",
    "TP-Link Omada", "CommScope", "Panduit", "Belden",
    "Legrand", "CablePro Supply", "D-Link Enterprise", "Vertiv",
    "Arrow Electronics", "Avnet", "TD Synnex", "Ingram Micro",
    "CDW", "SHI International", "Lenovo Networking", "Dell Networking",
    "Zyxel Networks", "Sophos", "Barracuda Networks", "Trellix (FireEye)",
    "Broadcom (Brocade)", "Moxa Technologies", "Lantronix", "Transition Networks",
    "Black Box Corporation", "Tripp Lite", "APC by Schneider", "Eaton",
    "Crestron Electronics", "Axis Communications", "Hanwha Vision", "Viavi Solutions",
    "IDEAL Networks", "Fluke Networks",
]

VENDOR_CATEGORY_AFFINITY: dict[int, list[str]] = {
    1:  ["networking-switch"],
    2:  ["networking-switch"],
    3:  ["networking-switch", "wireless-access-point"],
    4:  ["networking-switch"],
    5:  ["networking-switch"],
    6:  ["networking-switch"],
    7:  ["network-security"],
    8:  ["network-security"],
    9:  ["network-security"],
    10: ["network-security"],
    11: ["network-security"],
    12: ["network-security"],
    13: ["wireless-access-point"],
    14: ["wireless-access-point"],
    15: ["wireless-access-point"],
    16: ["wireless-access-point"],
    17: ["wireless-access-point"],
    18: ["structured-cabling"],
    19: ["structured-cabling"],
    20: ["structured-cabling"],
    21: ["structured-cabling"],
    22: ["structured-cabling"],
    23: ["networking-switch"],
    24: ["structured-cabling"],
}
for i in range(25, 51):
    VENDOR_CATEGORY_AFFINITY[i] = CATEGORIES

# ---------------------------------------------------------------------------
# Exception log
# ---------------------------------------------------------------------------

@dataclass
class ExceptionEntry:
    kind: str           # "EXPIRED" | "BAD DATA"
    vendor_id: str
    vendor_name: str
    path: str           # JSON path string, e.g. vendors[5].effective_date
    field_name: str
    value: str
    expected: str | None = None
    detail: str = ""
    action: str = ""

_exceptions: list[ExceptionEntry] = []

def log_exception(entry: ExceptionEntry) -> None:
    _exceptions.append(entry)

# ---------------------------------------------------------------------------
# Data generation
# ---------------------------------------------------------------------------

def fresh_date() -> str:
    days_ago = random.randint(5, STALE_THRESHOLD_DAYS - 1)
    return (QUERY_DATE - timedelta(days=days_ago)).isoformat()


def expired_date() -> str:
    days_ago = random.randint(STALE_THRESHOLD_DAYS + 30, 450)
    return (QUERY_DATE - timedelta(days=days_ago)).isoformat()


def make_sku(vendor_id: int, category: str, index: int) -> str:
    prefix = {"networking-switch": "SW", "network-security": "SEC",
               "wireless-access-point": "AP", "structured-cabling": "CAB"}[category]
    return f"V{vendor_id:03d}-{prefix}-{index:04d}"


def make_product(vendor_id: int, category: str, index: int) -> dict:
    template = random.choice(PRODUCTS[category])
    cost_lo, cost_hi = template["cost"]
    margin_lo, margin_hi = template["margin"]
    return {
        "sku": make_sku(vendor_id, category, index),
        "category": category,
        "description": template["desc"],
        "availability": random.random() > 0.15,
        "lead_time_days": random.choice([2, 3, 4, 5, 7, 10, 14, 21, 28]),
        "unit_cost": round(random.uniform(cost_lo, cost_hi), 2),
        "margin_pct": round(random.uniform(margin_lo, margin_hi), 1),
    }


def make_vendor(vid: int) -> dict:
    categories = VENDOR_CATEGORY_AFFINITY.get(vid, CATEGORIES)
    num_products = random.randint(2, 4)
    products = [
        make_product(vid, categories[i % len(categories)], i + 1)
        for i in range(num_products)
    ]
    return {
        "vendor_id": f"VEN-{vid:03d}",
        "vendor_name": VENDOR_NAMES[vid - 1],
        "effective_date": fresh_date(),
        "products": products,
    }


def inject_expired(vendor: dict, vendor_idx: int, category: str) -> dict:
    ed = expired_date()
    vendor["effective_date"] = ed
    days_old = (QUERY_DATE - date.fromisoformat(ed)).days
    log_exception(ExceptionEntry(
        kind="EXPIRED",
        vendor_id=vendor["vendor_id"],
        vendor_name=vendor["vendor_name"],
        path=f"vendors[{vendor_idx}].effective_date",
        field_name="effective_date",
        value=f'"{ed}"',
        detail=(
            f"Date is {days_old} days old; exceeds {STALE_THRESHOLD_DAYS}-day freshness threshold "
            f"(cutoff: {(QUERY_DATE - timedelta(days=STALE_THRESHOLD_DAYS)).isoformat()}). "
            f"Primary category: {category}."
        ),
        action="Agent must surface a stale-data warning to the SE before including any SKU from this vendor in a BOM draft.",
    ))
    return vendor


def inject_bad_type(vendor: dict, vendor_idx: int) -> dict:
    if vendor["products"]:
        vendor["products"][0]["lead_time_days"] = "21 days"
        sku = vendor["products"][0]["sku"]
        log_exception(ExceptionEntry(
            kind="BAD DATA",
            vendor_id=vendor["vendor_id"],
            vendor_name=vendor["vendor_name"],
            path=f"vendors[{vendor_idx}].products[0].lead_time_days",
            field_name="lead_time_days",
            value='"21 days"',
            expected="integer",
            detail=f"SKU {sku}: lead_time_days received as string; agent cannot apply lead-time threshold comparison.",
            action="Flag and skip this SKU. Do not include in BOM draft without SE-explicit override.",
        ))
    return vendor


def inject_missing_fields(vendor: dict, vendor_idx: int) -> dict:
    if vendor["products"]:
        p = vendor["products"][0]
        p.pop("margin_pct", None)
        p["unit_cost"] = None
        sku = p["sku"]
        log_exception(ExceptionEntry(
            kind="BAD DATA",
            vendor_id=vendor["vendor_id"],
            vendor_name=vendor["vendor_name"],
            path=f"vendors[{vendor_idx}].products[0]",
            field_name="unit_cost, margin_pct",
            value="unit_cost=null; margin_pct=<missing>",
            expected="number, number",
            detail=f"SKU {sku}: unit_cost is null and margin_pct attribute is absent. Incomplete pricing record.",
            action="Flag and skip this SKU. Do not include in BOM draft without SE-explicit override.",
        ))
    return vendor


def build_catalog() -> dict:
    vendors = []
    for vid in range(1, 51):
        vendor = make_vendor(vid)
        idx = vid - 1  # 0-based index for path references

        if vid == 6:
            vendor = inject_expired(vendor, idx, "networking-switch")
        elif vid == 12:
            vendor = inject_expired(vendor, idx, "network-security")
        elif vid == 17:
            vendor = inject_expired(vendor, idx, "wireless-access-point")
        elif vid == 22:
            vendor = inject_expired(vendor, idx, "structured-cabling")
        elif vid == 23:
            vendor = inject_bad_type(vendor, idx)
        elif vid == 24:
            vendor = inject_missing_fields(vendor, idx)

        vendors.append(vendor)

    return {
        "source_metadata": {
            "source": "vendor-catalog",
            "last_updated": SOURCE_LAST_UPDATED,
        },
        "vendors": vendors,
    }

# ---------------------------------------------------------------------------
# Exception log writer
# ---------------------------------------------------------------------------

def write_exceptions(path: Path) -> None:
    divider = "─" * 60
    lines: list[str] = [
        "QuotePilot Catalog Exception Log",
        f"Generated:   {date.today().isoformat()}",
        f"Source file: {CATALOG_PATH.name}",
        f"Query date:  {QUERY_DATE.isoformat()}",
        f"Freshness threshold: {STALE_THRESHOLD_DAYS} days",
        "",
        f"Total exceptions: {len(_exceptions)}",
        "",
    ]

    by_kind: dict[str, list[ExceptionEntry]] = {}
    for e in _exceptions:
        by_kind.setdefault(e.kind, []).append(e)

    for kind, entries in by_kind.items():
        lines += [divider, kind, divider, ""]
        for e in entries:
            lines.append(f"[{e.vendor_id}] {e.vendor_name}")
            lines.append(f"  Path:     {e.path}")
            lines.append(f"  Field:    {e.field_name}")
            lines.append(f"  Value:    {e.value}")
            if e.expected:
                lines.append(f"  Expected: {e.expected}")
            lines.append(f"  Detail:   {e.detail}")
            lines.append(f"  Action:   {e.action}")
            lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    catalog = build_catalog()

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    with CATALOG_PATH.open("w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
    print(f"Wrote catalog      → {CATALOG_PATH}")

    write_exceptions(EXCEPTIONS_PATH)
    print(f"Wrote exceptions   → {EXCEPTIONS_PATH}")
    print(f"Total exceptions:    {len(_exceptions)}")


if __name__ == "__main__":
    main()
