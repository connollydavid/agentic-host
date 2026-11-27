"""The null arm's adapter: the built-in web tools under the frozen prompt.

The null arm returns the Markdown report and the source ledger directly; the
adapter checks the shape, copies them and writes the receipt.
"""

from __future__ import annotations

import json
from pathlib import Path

from contract import build_receipt, validate_report, validate_sources, write_json


def convert(fixture: Path, task: dict, out: Path, meta: dict) -> str:
    report = (fixture / "report.md").read_text()
    sources = json.loads((fixture / "sources.json").read_text())
    entries = validate_sources(sources)
    validate_report(report, entries)
    (out / "report.md").write_text(report)
    write_json(out / "sources.json", {"sources": entries})
    write_json(out / "receipt.json", build_receipt("null", task["key"], meta))
    return "valid"
