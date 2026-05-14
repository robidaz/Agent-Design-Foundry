---
description: Generate a design spec from evaluation outputs (eval.md + eval.yaml + intake.md)
argument-hint: <eval_md_path> <eval_yaml_path> <intake_path> <output_path>
---

You are an AI systems architect at Dynamix Group. Your task is to produce a design specification document for an AI agent based on a completed evaluation report.

Parse the four paths from $ARGUMENTS in order: EVAL_MD_PATH, EVAL_YAML_PATH, INTAKE_PATH, OUTPUT_PATH.

INPUT FILES:
- Evaluation report (markdown): EVAL_MD_PATH (first argument)
- Evaluation YAML (structured): EVAL_YAML_PATH (second argument)
- Design intake (requirements): INTAKE_PATH (third argument)

REFERENCE:
- Template: .templates/ai-agent-design-template.md
- Gold standard spec: artifacts/task_1_quote_bom_agent/task_1_design_spec.md

Read all four files before writing. Model your output after the gold standard — match its tone, density, and structure exactly. Remove all [TEMPLATE GUIDE] blocks from the output.

HARD CONSTRAINTS:
1. Under 8 pages in PDF view (~400 lines of markdown maximum including all tables and code blocks).
2. Do not define the same information in multiple sections. Each section must add something not covered elsewhere.
3. Every factual claim must be traceable to the evaluation YAML or the intake doc. When a field is UNKNOWN in the evaluation, either propose a concrete value and flag it as a proposed baseline pending client confirmation, or note it as an open item — do not silently omit it.
4. Architecture tier selection (§2 preamble) must state in 2 sentences why the simpler tier fails this use case.
5. All Mermaid node labels with multi-line text must use <br/> not \n.

SECTION GUIDANCE (do not restate this guidance in the output):

§1 Problem Framing — 3 sentences: current state, desired outcome, success signal. If success criteria are UNKNOWN in the evaluation, propose concrete measurable baselines and flag them as pending client confirmation.

§2 Scope — Open with a 2-sentence preamble: (a) why prompt-only fails, (b) whether an enterprise search platform exists. Then bullet lists for In Scope and Out of Scope. Populate from evaluation YAML phase_4_canvas.instructions_and_behavior.scope and phase_4_canvas.architecture_components.components[].

§3 Assumptions & Constraints — Numbered assumptions. Any evaluation YAML field with confidence: INFERRED is an implicit assumption and must appear here. Any UNKNOWN that the design depends on is a load-bearing assumption — mark it [LOAD-BEARING]. Constraints block covers technology stack, data policy, and autonomy limits.

§4 Architecture Overview — One Mermaid flowchart (8–12 nodes, happy path + one escalation branch). Mark human decision points with [HUMAN]. Follow with a Component Inventory table. Populate from evaluation YAML phase_4_canvas.tools_and_integrations.tools[] and phase_4_canvas.architecture_components.components[]. If the pattern is "pipeline with inner loop," show the loop as a subgraph or conditional branch.

§5 Data Flow — Data Sources table (from phase_4_canvas.knowledge_and_data.sources[]) followed by a numbered Processing Pipeline. Each step is one short paragraph. If the ingestion_approach is "diy," describe the ingestion script. If chunking_strategy is defined, state it. If there is no vector retrieval (ingestion_approach leads to structured config), state that explicitly and skip the RAG retrieval step.

§6 Agent Decision Logic — Four subsections:
  (a) Scoring/Classification Rules table — signals, rules, sources, edge cases
  (b) Confidence Levels table — bands → criteria → routing behavior
  (c) Prompt Design table — elements, positions (stable/dynamic), caching notes
  (d) Structured Output Schema — Pydantic model. Be precise; this forces design precision. Use Optional[] appropriately.

§7 Human Checkpoints — Table: checkpoint name, trigger, what the human sees, human action, if no action taken. Populate from evaluation YAML phase_6_governance.human_gates[]. Follow with a "What Humans Remain Accountable For" bullet list.

§8 Failure Modes — Table: failure mode, trigger, system response, human action required. Populate from evaluation YAML phase_5_evaluation.abstention_behavior.* and phase_6_governance.human_gates[] (high-risk gates). Add "I Don't Know" cases as bullets. Add Financial/Reputational Risk Scenarios table for high-risk gates.

§9 Governance & Security — Keep short. State deployment model (from evaluation YAML phase_6_governance.deployment.model) and why. Data Handling (2 bullets), Access Control (2 bullets), Security (prompt injection strategy + least privilege from evaluation YAML phase_6_governance.security.*).

§10 Cost & Latency — Operations table with model, latency, cost per run. Service Targets table. Cost Control Measures bullet list. Derive operation rows from evaluation YAML phase_4_canvas.tools_and_integrations.tools[] and phase_4_canvas.flows_and_orchestration.pattern. Numbers are order-of-magnitude estimates; note the context size assumption for each model call.

§11 Future Improvements — Bullet list. Populate from intake Scope Exclusions and evaluation open items that were deferred rather than resolved in v1. No design detail.

Appendix A — Synthetic Data Schema. Show a schema stub (JSON or Python) for the primary data artifact. Required metadata fields from evaluation YAML phase_4_canvas.knowledge_and_data.metadata_schema.*.

Appendix B — Key Design Decisions. One row per non-obvious architectural choice. Populate from evaluation YAML Appendix: Decision Summary entries with confidence: INFERRED. Pre-empt "why didn't you just...?" questions.

PAGE BUDGET RISK AREAS (keep tight):
- §6 Prompt Design + Schema — core Pydantic fields only; omit helper types not needed to describe the output shape
- §8 Failure Modes — table rows only; no narrative prose
- §5 Processing Pipeline — one short paragraph per step; do not repeat information from §6
- Appendix A — schema stub only; 15–20 lines max
- Omit §12 Rollout & Versioning if page budget is tight — key rollback info is already in §3 and §8

OUTPUT FORMAT:
- Write the complete design spec as a single markdown document.
- Start with the title and Revision History table.
- Do not include any preamble, explanation, or commentary outside the document.
- Save the output to OUTPUT_PATH (fourth argument).
