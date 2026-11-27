"""The weizhena exclusion: structured field JSON has no source record.

The arm writes one JSON file per item against `fields.yaml` and a report
generated from those fields. The adapter looks for a source URL, quote or
locator in either the JSON or the report; finding none, it records the
exclusion the contract's ledger requirement forces.
"""

from __future__ import annotations

import json
from pathlib import Path

from contract import ContractError, write_json

SOURCE_KEYS = {"url", "quote", "locator", "sources", "source", "citation"}


def source_like(value: object) -> bool:
    if isinstance(value, dict):
        keys = {str(key).lower() for key in value}
        if "url" in keys and ("quote" in keys or "locator" in keys):
            return True
        if SOURCE_KEYS & keys and any(source_like(item) for item in value.values()):
            return True
        return any(source_like(item) for item in value.values())
    if isinstance(value, list):
        return any(source_like(item) for item in value)
    return False


def convert(fixture: Path, task: dict, out: Path, meta: dict) -> str:
    results = sorted((fixture / "results").rglob("*.json"))
    for path in results:
        if source_like(json.loads(path.read_text())):
            raise ContractError(f"{path.name} now carries a source record; re-examine the exclusion")
    report = (fixture / "report.md").read_text()
    write_json(
        out / "exclusion.json",
        {
            "arm": "weizhena",
            "task": task["key"],
            "status": "excluded",
            "reason": (
                "The arm outputs structured field JSON against fields.yaml and a report generated from "
                "those fields; it carries no source URL, verbatim quote or locator, so the source ledger "
                "cannot be populated."
            ),
            "evidence": (
                f"results/ carries {len(results)} JSON file(s); none pairs a URL with a quote and locator. "
                f"report.md is {len(report)} chars and cites {report.count('http')} URL(s); a URL in the "
                "report is not a per-source quote record, so the ledger cannot be populated."
            ),
        },
    )
    return "excluded"
