#!/usr/bin/env python3
"""The search-provider gate test: no model call, no network.

The one-provider rule is a pure function in the selection driver. These checks
prove it rejects a search-engine fetch even when a `websearch` call also ran,
rejects a provider other than Exa, and accepts the measured provider or no
search at all.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
sys.path.insert(0, str(HARNESS / "selection"))

import run  # noqa: E402

CHECKS = [
    ("exa with no fetch", run.provider_gate("exa", []) is None),
    ("no search with no fetch", run.provider_gate("none", []) is None),
    (
        "exa plus a DuckDuckGo fetch",
        run.provider_gate("exa", ["https://html.duckduckgo.com/html/?q=probe"]) is not None,
    ),
    (
        "no search plus a DuckDuckGo fetch",
        run.provider_gate("none", ["https://html.duckduckgo.com/html/?q=probe"]) is not None,
    ),
    ("a foreign provider", run.provider_gate("parallel", []) is not None),
    ("a search-engine host", run.is_search_engine("https://html.duckduckgo.com/html/?q=x")),
    ("a normal page", not run.is_search_engine("https://example.com/page")),
    ("the draw config selects Exa", run.arm_config("null").get("websearch") == {"provider": "exa"}),
]


def main() -> int:
    failed = [name for name, ok in CHECKS if not ok]
    for name, ok in CHECKS:
        print(f"{'PASS' if ok else 'FAIL'} {name}")
    if failed:
        print(f"search-provider gate: {len(failed)} check(s) failed", file=sys.stderr)
        return 1
    print(f"search-provider gate: {len(CHECKS)} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
