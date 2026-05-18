> **Snapshot only — do not manage this file.** This document is a human-readable rendering of
> [`intake_schema.json`](intake_schema.json). It is generated for reference purposes and is not kept
> in sync automatically. For authoritative schema definitions, refer to `intake_schema.json` directly.

# GreenLight Intake Schema

**Version:** 1.0.0
**Last updated:** 2026-05-12
**Framework version target:** 1.0.0

Structured intake question schema served to the client via the Angular + Syncfusion UI. Drives section-by-section streaming of responses into the GreenLight agent. Question count: 32 (4 engagement metadata + 28 dimension questions, ~4–5 per dimension). A subset is tagged `deterministic: true` with `demo_signal` hooks — these drive the agent's working-demo recommendation alongside the readiness report.

> **UI notes:** Sections render top-to-bottom. Branching is supported per the `branching` attribute on each question. Each section ends with a single submit that streams responses to the orchestrator.

---

## Section 0 — About Your Organization (`engagement_metadata`)

| ID | Question | Type | Required | Options | Maps To |
| --- | --- | --- | --- | --- | --- |
| EM-001 | What is your organization's legal name? | text | Yes | — | `engagement_metadata.company_name` |
| EM-002 | Approximate employee count? | select | Yes | `< 200` / `200–500` / `500–1,000` / `1,000–2,000` / `> 2,000` | `engagement_metadata.employee_count_band` |
| EM-003 | Approximate annual revenue (USD)? | select | Yes | `< $50M` / `$50M–$200M` / `$200M–$500M` / `$500M–$1B` / `> $1B` | `engagement_metadata.revenue_band` |
| EM-004 | Primary industry? | select | Yes | Industrial Distribution / Wholesale · Manufacturing · Financial Services · Healthcare / Life Sciences · Retail / E-commerce · Professional Services · Technology · Other | `engagement_metadata.industry` |
| EM-005 | Your role at the organization? | text | Yes | — | `engagement_metadata.respondent_role` |

---

## Section 1 — Strategy & Use Case Portfolio (`strategy_use_case_portfolio`)

| ID | Question | Type | Required | Options (anchor 1→5) | Sub-criteria | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| S1-001 | Does your executive team have a documented AI strategy? | select | Yes | No formal discussion yet · Informal conversations only · Documented strategy drafted · Documented strategy reviewed at leadership cadence · AI strategy is integrated into corporate strategy | `executive_sponsorship` | |
| S1-002 | Who is the highest-level executive actively sponsoring AI initiatives? | select | Yes | No active sponsor · Director / VP level · C-suite · CEO / Owner | `executive_sponsorship` | |
| S1-003 | Have you identified specific AI use cases tied to business outcomes? | multi-select | No | Customer service automation · Sales / quoting assistance · Inventory / demand forecasting · Pricing optimization · Field service support · Document / email triage · Marketing / content generation · Other · None identified | `use_case_portfolio` | `deterministic` — `demo_signal: use_case_intent` |
| S1-004 | How do you prioritize where to invest first? | text | No | — | `prioritization_framework` | |
| S1-005 | Are AI initiatives tied to a quantified business case (revenue, cost, risk)? | select | Yes | No · Informally · Documented business cases for some · All initiatives have business cases · Outcomes tracked closed-loop against business cases | `value_articulation` | |

---

## Section 2 — Data Foundation (`data_foundation`)

| ID | Question | Type | Required | Options (anchor 1→5) | Sub-criteria | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| D1-001 | Do you maintain a catalog of your data assets (where data lives, who owns it)? | select | Yes | No catalog · Partial catalogs per system · Catalog for top systems · Enterprise catalog with owners + SLAs · Continuously catalogued with lineage | `data_inventory` | |
| D1-002 | How confident are you in the quality (completeness, accuracy, freshness) of your core operational data? | select | Yes | Quality is unknown · Anecdotally known issues · Monitored for critical domains · Quality dashboards per domain · Enforced SLOs per domain | `data_quality` | |
| D1-003 | How does an engineering or analytics team typically access data they need? | text | Yes | — | `data_accessibility` | |
| D1-004 | How well-integrated are your core systems (ERP, CRM, operational tools)? | select | Yes | Siloed; mostly manual · Point-to-point integrations exist but are brittle · Documented integrations between core systems · Centrally governed integration platform · Integration is a platform capability | `data_integration` | |
| D1-005 | Roughly how many active SKUs / customer records / transactions per month flow through your core systems? | text | No | — | `data_inventory` | `deterministic` — `demo_signal: sku_volume_high` |

---

## Section 3 — Technology & Infrastructure (`technology_infrastructure`)

| ID | Question | Type | Required | Options (anchor 1→5) | Sub-criteria | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| T1-001 | Which best describes your cloud posture? | select | Yes | Primarily on-prem · Hybrid with ad-hoc cloud usage · Defined cloud strategy in motion · Cloud-native or well-governed hybrid · Platform-as-product across the business | `cloud_posture` | |
| T1-002 | Do your core systems (ERP, CRM, etc.) expose APIs that downstream systems can consume? | select | Yes | No APIs · A few one-off integrations exist · Documented APIs on key systems · Event-driven integration available · Integration is composable across the business | `integration_architecture` | |
| T1-003 | How confident are you that your security baseline (identity, encryption, audit) meets enterprise norms? | select | Yes | Weak / unknown · Standard but uninspected for AI · Meets enterprise norms; AI not specifically reviewed · Reviewed for AI workloads · Continuously validated for AI | `security_baseline` | |
| T1-004 | Do you have MLOps or AI platform tooling in use (model registry, versioning, monitoring)? | select | Yes | No · Experimental usage · Limited but in production · MLOps platform operating · Full-lifecycle MLOps with rollback | `mlops_tooling` | |

---

## Section 4 — People & Skills (`people_skills`)

| ID | Question | Type | Required | Options (anchor 1→5) | Sub-criteria | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| P1-001 | How would you characterize your leadership team's working understanding of AI? | select | Yes | Unfamiliar · Curious but uneven · Baseline-literate · Conversant in AI strategy · Shapes AI strategy directly | `ai_literacy_leadership` | |
| P1-002 | Do you have technical staff in-house who can deliver AI / ML / data engineering work? | select | Yes | None · 1–2 technically literate staff · Small but capable internal team · Multi-role internal team · Deep cross-functional capability | `technical_talent` | |
| P1-003 | How has the organization historically absorbed major process or tooling change? | text | Yes | — | `change_management_capacity` | |
| P1-004 | Do you offer formal training programs for business or technical staff on AI tooling? | select | Yes | No · Ad-hoc · Structured for key roles · Managed program · Continuous and outcome-linked | `training_programs` | |
| P1-005 | Do you currently work with external partners (services, vendors) on AI initiatives? | select | Yes | No · Opportunistically · Defined partner roster · Strategically selected partners · Curated and managed partner ecosystem | `partnership_strategy` | |

---

## Section 5 — Process & Operations (`process_operations`)

| ID | Question | Type | Required | Options (anchor 1→5) | Sub-criteria | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| O1-001 | Are your core business processes documented? | select | Yes | No · Partially · Documented for core flows · Governed and reviewed · Continuously optimized | `process_documentation` | |
| O1-002 | What automation do you have in place today (RPA, workflow tools, custom scripts)? | text | No | — | `automation_baseline` | `deterministic` — `demo_signal: manual_doc_processing` |
| O1-003 | Are operational KPIs measured and visible to the people running the work? | select | Yes | Unclear KPIs · Lagging KPIs in spreadsheets · KPIs visible to operators · KPIs in real-time dashboards · Real-time KPIs drive operations | `kpi_instrumentation` | |
| O1-004 | How are operator feedback or process issues captured today? | text | No | — | `feedback_loops` | |
| O1-005 | Where do you feel your team spends the most repetitive, manual time? | multi-select | No | Quoting / pricing · Inbound email triage · Document handling · Inventory adjustments · Field service dispatch · Reporting / spreadsheets · Other | `automation_baseline` | `deterministic` — `demo_signal: operational_pain_areas` |

---

## Section 6 — Governance & Risk Readiness (`governance_risk`)

| ID | Question | Type | Required | Options (anchor 1→5) | Sub-criteria | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| G1-001 | Do you have a documented internal policy governing AI use, data, and outputs? | select | Yes | No policy · Informal guidance only · Documented AI policy · Policy actively governed · Policy integrated with enterprise risk | `ai_policy_framework` | |
| G1-002 | How are AI-specific risks (bias, hallucination, IP, regulatory) assessed for a new use case? | text | No | — | `risk_assessment_capability` | |
| G1-003 | How aware is your organization of regulatory regimes that might apply to AI use in your sector? | select | Yes | Unaware · Partial awareness · Reviewed before launch · Continuously monitored · Proactively engaged | `compliance_posture` | |
| G1-004 | Are there controls in place to monitor, audit, or override outputs from any AI tools currently in use? | text | No | — | `model_oversight` | |
| G1-005 | Do you have AI-aware controls over third-party vendors (data handling, IP, model usage)? | select | Yes | No · Inherited from generic procurement · AI-aware controls in place · Reviewed at cadence · Continuously governed and audited | `vendor_governance` | |

---

## Completeness Rules

A dimension is marked complete when **all required questions are answered** AND **dimension confidence ≥ `settings.confidence_threshold`** OR **the follow-up cap per dimension is reached**.

**Required sections for full completion:**

| Section ID | Title |
| --- | --- |
| `engagement_metadata` | About Your Organization |
| `strategy_use_case_portfolio` | Strategy & Use Case Portfolio |
| `data_foundation` | Data Foundation |
| `technology_infrastructure` | Technology & Infrastructure |
| `people_skills` | People & Skills |
| `process_operations` | Process & Operations |
| `governance_risk` | Governance & Risk Readiness |
