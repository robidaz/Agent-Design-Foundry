"""Re-render an existing RFPResponseArtifact JSON to markdown + PDF.

Useful when iterating on templates without re-running the full pipeline.

Usage:
    python scripts/render_response.py output/rfp_ENG-001.json [--out output/]
"""

from __future__ import annotations

import sys
from pathlib import Path

from knowledgex.render import render_all
from knowledgex.schemas import RFPResponseArtifact

ROOT = Path(__file__).resolve().parent.parent


def _parse_args(argv: list[str]) -> tuple[Path, Path]:
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    in_path = Path(args[0]).resolve()
    out_dir = ROOT / "output"
    if "--out" in argv:
        i = argv.index("--out")
        if i + 1 < len(argv):
            out_dir = Path(argv[i + 1]).resolve()
    return in_path, out_dir


def main() -> None:
    in_path, out_dir = _parse_args(sys.argv[1:])
    artifact = RFPResponseArtifact.model_validate_json(in_path.read_text(encoding="utf-8"))
    paths = render_all(artifact, out_dir)
    for kind, p in paths.items():
        print(f"  {kind:>14} → {p}")


if __name__ == "__main__":
    main()
