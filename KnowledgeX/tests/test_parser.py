"""Parser unit tests — markdown + JSON parity, malformed input."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from knowledgex.parser import ParseError, parse


def test_markdown_parses_with_expected_band(tmp_path: Path):
    md = tmp_path / "q.md"
    md.write_text(
        "## Q-001\n"
        "**Section:** Security\n"
        "**Question:** What algorithm is used at rest?\n"
        "<!-- expected_band: HIGH -->\n"
        "\n"
        "## Q-002\n"
        "**Question:** Anything else?\n",
        encoding="utf-8",
    )
    qs = parse(md)
    assert len(qs) == 2
    assert qs[0].id == "Q-001"
    assert qs[0].expected_band == "HIGH"
    assert qs[0].section == "Security"
    assert qs[1].expected_band is None


def test_json_parses(tmp_path: Path):
    js = tmp_path / "q.json"
    js.write_text(
        json.dumps(
            {
                "engagement_id": "ENG-T",
                "questions": [
                    {"id": "Q-001", "section": "S", "text": "x?", "expected_band": "HIGH"},
                    {"id": "Q-002", "text": "y?"},
                ],
            }
        ),
        encoding="utf-8",
    )
    qs = parse(js)
    assert qs[0].id == "Q-001"
    assert qs[0].expected_band == "HIGH"
    assert qs[1].expected_band is None


def test_md_and_json_produce_same_ids(tmp_path: Path):
    md = tmp_path / "q.md"
    md.write_text("## Q-A\n**Question:** a?\n\n## Q-B\n**Question:** b?\n", encoding="utf-8")
    js = tmp_path / "q.json"
    js.write_text(
        json.dumps({"questions": [{"id": "Q-A", "text": "a?"}, {"id": "Q-B", "text": "b?"}]}),
        encoding="utf-8",
    )
    assert [q.id for q in parse(md)] == [q.id for q in parse(js)]


def test_rejects_missing_question_line(tmp_path: Path):
    md = tmp_path / "q.md"
    md.write_text("## Q-001\n**Section:** S\n", encoding="utf-8")
    with pytest.raises(ParseError):
        parse(md)


def test_rejects_duplicate_ids(tmp_path: Path):
    md = tmp_path / "q.md"
    md.write_text(
        "## Q-001\n**Question:** a?\n\n## Q-001\n**Question:** b?\n",
        encoding="utf-8",
    )
    with pytest.raises(ParseError):
        parse(md)


def test_rejects_unknown_extension(tmp_path: Path):
    f = tmp_path / "q.txt"
    f.write_text("anything", encoding="utf-8")
    with pytest.raises(ParseError):
        parse(f)
