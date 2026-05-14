"""Sample question fixtures are committed directly to assets/questions/.

The 30-question fixture (`sample_30q.md` and `sample_30q.json`) is hand-
authored to exercise all five confidence bands against the engineered seeds
in the KB. The band distribution (HIGH=12, MEDIUM=8, LOW=4, NO_SOURCE=4,
CONFLICT=2) is the contract that `test_cases.md` verifies.

Regenerating the fixture by an automated process would re-introduce drift
between the question topics and the KB content; both must move together.
This script exists as documentation.
"""

from __future__ import annotations

import sys


def main() -> None:
    print(
        "Question fixtures are committed under assets/questions/. "
        "See test_cases.md for the expected band distribution."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
