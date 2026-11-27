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
        if SOURCE_KEYS & {str(key).lower() for key in value}:
            return True
        return any(source_like(item) for item in value.values())
    if isinstance(value, list):
        return any(source_like(item) for item in value)
    return False


def convert(fixture: Path, task: dict, out: Path, meta: dict) -> str:
    results = sorted((fixture / "results").glob("*.json"))
    for path in results:
        if source_like(json.loads(path.read_text())):
            raise ContractError(f"{path.name} now carries a source record; re-examine the exclusion")
    report = (fixture / "report.md").read_text()
    if "http://" in report or "https://" in report:
        raise ContractError("the report now carries a URL; re-examine the exclusion")
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
                "results/Item.json holds field values only; report.md carries no URL; the research-deep "
                "output requirements define JSON fields, an uncertain array and a validation script, not a "
                "source record."
            ),
        },
    )
    return "excluded"
