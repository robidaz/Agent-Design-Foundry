# QuotePilot Agent — Test Cases

---

## TC-01 — Green Path: Standard 3-Tier BOM

**User request:**

>We're quoting a mid-size corporate office expansion for a client adding 150 desks to their existing campus. They need 24-port managed PoE switches for the new floor, a next-generation firewall to handle increased perimeter traffic, and Cat6A structured cabling to support the buildout. Budget is flexible but the client prefers not to overspend on switching. Please generate a full 3-tier BOM.

**Expected behavior:** Agent reads `rulesets.yaml` and `pc_def.json`, maps all three phrases to recognized categories (`networking-switch`, `network-security`, `structured-cabling`), queries `catalog.json`, selects one SKU per tier per category satisfying all five rules, emits `QuotePilot/output/bom_REQ-*.json`, renders a PDF, and returns a clean summary with `requires_human_review: false`.

---

## TC-02 — Stale Vendor Warning (VEN-012 / SonicWall, rule-002)

**User request:**

> "Quote an NGFW solution for a regional branch office with around 75 concurrent users. The client's IT team specifically asked whether SonicWall has any options in the mid-range tier — they've used SonicWall before and want to see it as one of the options if possible. Include two other vendors as alternatives across the remaining tiers. Lead time is not a concern for this engagement."

**Expected behavior:** Agent surfaces a `data_freshness_warnings` entry for VEN-012 (SonicWall, 340 days stale per rule-002) and sets `requires_human_review: true`. It still includes the SonicWall SKU in the requested tier but annotates the stale-data flag and notes the age prominently in the BOM output. The remaining tiers are filled from available, fresher vendors.

---

## TC-03 — Bad-Data Skip + Alternative Provided (VEN-023 / D-Link, rule-005 + rule-001)

**User request:**

> "We need a 24-port access switch for a small retail branch — price sensitivity is high, so budget tier is the priority. I've heard D-Link Enterprise has a competitive SKU in this range. If D-Link doesn't work out for any reason, I'd still like to see the next best budget-tier alternative so the client has something to move forward with."

**Expected behavior:** Agent detects VEN-023 / V023-SW-0001 has `lead_time_days` as a string (`"21 days"`) — an invalid type that makes the rule-001 threshold comparison impossible. It logs V023-SW-0001 as a bad-data skip, populates `gap_markers`, and falls back to the next qualifying budget-tier switch SKU. The BOM notes the D-Link skip with the specific bad-field (`lead_time_days`), confirms an alternative was selected, and explains the substitution in the justification.

---

## TC-04A — Unknown Terminology → SE Registration → No BOM (Single Session)

**Request 1:**

> "We need to quote out a full FlexNode bundle for a new warehouse site. The client is on a 90-day deployment window and wants all three tiers. FlexNode is what our solutions team internally calls our standard combo of an access switch plus wireless coverage — we use that term on all our warehouse deals."

**Expected behavior after Request 1:** Agent cannot resolve "FlexNode bundle" against any category in `pc_def.json` and stops before querying the catalog. It returns a clarification request explaining that `FlexNode` is not a recognized category and asks the SE to confirm the constituent product categories.

---

**Request 2:**

> "Got it — FlexNode maps to networking-switch plus wireless-access-point. Please register that in pc_def.json so the team can use it going forward. The client's needs have changed, so no quote is needed today."

**Expected behavior after Request 2:** Agent reads `pc_def.json`, confirms `FlexNode` is not already present, and proposes a precise before/after diff showing the new entry to be added (with `FlexNode` as a keyword or alias mapping to `networking-switch` and `wireless-access-point`). Agent pauses and waits for explicit SE grant ("approve" / "grant" / equivalent). On grant, agent applies the edit via `Edit` tool and confirms the registration. No BOM JSON is written and `render_bom.py` is not invoked, as no quote was requested.

---

## TC-04B — Registered Terminology Resolves in New Session

**Pre-requisite:** New session started after TC-04A. `pc_def.json` now contains the `FlexNode` entry registered by the SE; no in-session context from TC-04A carries over.

**Request 1:**

> "We need to quote out a full FlexNode bundle for a new warehouse site. The client is on a 90-day deployment window and wants all three tiers. FlexNode is what our solutions team internally calls our standard combo of an access switch plus wireless coverage — we use that term on all our warehouse deals."

**Expected behavior:** Agent reads the updated `pc_def.json`, resolves "FlexNode bundle" to `networking-switch` + `wireless-access-point`, and proceeds through the full BOM pipeline without requesting clarification. It queries the catalog for both categories, applies rules rule-001 through rule-005, selects one SKU per tier per category, emits `QuotePilot/output/bom_REQ-*.json`, renders a PDF via `render_bom.py`, and returns the standard summary with paths and any warnings or abstentions.

---

## TC-05 — Incomplete Pricing Skip + Tier Abstention Notification (VEN-024 / Vertiv, rule-005)

**User request:**

> "We're putting together a structured cabling BOM for a data center pre-wire job. The client wants to see all three tiers — budget through premium. I recall seeing a Vertiv cabling option that might be a good fit for one of the mid-range slots; include it if the data supports it. Delivery timeline is flexible."

**Expected behavior:** Agent identifies VEN-024 / V024-CAB-0001 — `unit_cost` is null and `margin_pct` is absent — and skips it per rule-005. If that skip leaves a tier slot empty for `structured-cabling` and no other candidate exists, the agent abstains for that tier, populates `abstention_reason`, and notifies the SE that the slot cannot be filled from current catalog data. `requires_human_review` is set to `true`. The agent does not fabricate a substitute SKU or relax the pricing constraint to fill the gap.
