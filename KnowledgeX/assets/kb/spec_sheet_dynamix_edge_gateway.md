---
source_doc: spec_sheet_dynamix_edge_gateway.md
doc_type: spec_sheet
approval_status: approved
product: Dynamix Edge Gateway
release_line: 4400 / 2200
---

# Dynamix Edge Gateway — Specification Sheet (4400 / 2200 series)

The Dynamix Edge Gateway is the on-site collection and aggregation appliance in the Dynamix product family. Two hardware tiers are currently shipping: the **4400 series** for high-throughput sites and the **2200 series** for smaller deployments.

## Throughput

| Series | Sustained ingest (events/sec) | Peak ingest (events/sec) | Median payload size |
| ------ | ----------------------------- | ------------------------ | ------------------- |
| 4400 | 80,000 | 120,000 (≤ 60 seconds) | 1.2 KB |
| 2200 | 20,000 | 35,000 (≤ 60 seconds) | 1.2 KB |

Throughput figures are validated in customer environments and certified against the median payload size shown. Smaller payloads scale slightly higher; larger payloads (≥ 4 KB) trend lower in proportion to payload size.

## Connectivity

| Series | 1 GbE ports | 10 GbE uplinks | PoE+ subset | Out-of-band management |
| ------ | ----------- | -------------- | ----------- | ---------------------- |
| 4400 | 24 | 4 | 12 | 1 × dedicated RJ-45 |
| 2200 | 8 | 2 | 4 | 1 × dedicated RJ-45 |

PoE++ is not supported in the current generation; the roadmap entry for PoE++ is tracked but no shipping date is published. Both appliances support 802.1Q VLAN segmentation and LACP link aggregation on the 10 GbE uplinks.

## Physical and Environmental

| Series | Form factor | Power draw (typ.) | Operating temperature | MTBF (h) |
| ------ | ----------- | ----------------- | --------------------- | -------- |
| 4400 | 1U | 280 W | 0 °C to 40 °C | 250,000 |
| 2200 | 1U short-depth | 95 W | 0 °C to 45 °C | 280,000 |

Both appliances are NEBS Level 3 certified. Fanless variants of the 2200 series are available for environments with strict acoustic requirements.

## Upstream Bandwidth

A single 4400 series appliance under sustained peak load consumes approximately 95 Mbps of upstream bandwidth to the Core Platform tier after on-device deduplication and compression. The 2200 series consumes approximately 25 Mbps under equivalent peak utilisation. Customers operating constrained WAN links may configure aggressive batching with the documented latency trade-off.

## Lead Time

Both appliances ship from stock within 5 business days of purchase order acknowledgement under standard demand. Lead times during quarterly close periods may extend to 10 business days.
