"""Jinja2 rendering: markdown + PDF (via WeasyPrint).

Per engagement we emit four artifacts:
  - rfp_<engagement_id>.json   — raw RFPResponseArtifact
  - rfp_<engagement_id>.md     — full SME-review document, markdown
  - rfp_<engagement_id>.pdf    — same content, PDF (WeasyPrint)
  - escalation_<engagement_id>.md — escalation queue, markdown only

Mirrors QuotePilot/scripts/render_bom.py rendering conventions.
"""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

from knowledgex.schemas import RFPResponseArtifact

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

_TPL_RFP_MD = "rfp_response.md.jinja"
_TPL_RFP_HTML = "rfp_response.html.jinja"
_TPL_ESCALATION_MD = "escalation_queue.md.jinja"


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html", "jinja"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_markdown(artifact: RFPResponseArtifact) -> str:
    return _env().get_template(_TPL_RFP_MD).render(artifact=artifact)


def render_html(artifact: RFPResponseArtifact) -> str:
    return _env().get_template(_TPL_RFP_HTML).render(artifact=artifact)


def render_escalation_markdown(artifact: RFPResponseArtifact) -> str:
    return _env().get_template(_TPL_ESCALATION_MD).render(artifact=artifact)


def render_all(artifact: RFPResponseArtifact, out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    eid = artifact.engagement_id

    paths: dict[str, Path] = {}

    # Raw JSON
    json_path = out_dir / f"rfp_{eid}.json"
    json_path.write_text(artifact.model_dump_json(indent=2), encoding="utf-8")
    paths["json"] = json_path

    # Markdown
    md_path = out_dir / f"rfp_{eid}.md"
    md_path.write_text(render_markdown(artifact), encoding="utf-8")
    paths["md"] = md_path

    # PDF
    pdf_path = out_dir / f"rfp_{eid}.pdf"
    html_str = render_html(artifact)
    HTML(string=html_str, base_url=str(TEMPLATES_DIR)).write_pdf(str(pdf_path))
    paths["pdf"] = pdf_path

    # Escalation queue (only if non-empty)
    if artifact.escalation_queue:
        esc_path = out_dir / f"escalation_{eid}.md"
        esc_path.write_text(render_escalation_markdown(artifact), encoding="utf-8")
        paths["escalation_md"] = esc_path

    return paths
