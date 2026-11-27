"""The weizhena adapter: the report's inline citations, or the exclusion.

The arm writes structured field JSON and a generated report. When the report
carries inline URL citations with a passage, the adapter builds the ledger from
them; the run's actual `webfetch` snapshot still has to support the quote. When
the report has no such citation, the adapter records why the ledger cannot be
populated and names the URLs the field JSON does carry, if any.
"""

from __future__ import annotations

import json
from pathlib import Path

from contract import build_receipt, report_entries, validate_report, write_json


def source_urls(value: object) -> list[str]:
    urls: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() == "url" and isinstance(item, str) and item:
                urls.append(item)
            else:
                urls.extend(source_urls(item))
    elif isinstance(value, list):
        for item in value:
            urls.extend(source_urls(item))
    return urls


def convert(fixture: Path, task: dict, out: Path, meta: dict) -> str:
    report = (fixture / "report.md").read_text()
    entries = report_entries(report)
    if entries:
        validate_report(report, entries)
        (out / "report.md").write_text(report)
        write_json(out / "sources.json", {"sources": entries})
        write_json(out / "receipt.json", build_receipt("weizhena", task["key"], meta))
        return "valid"
    results = sorted((fixture / "results").rglob("*.json"))
    urls: list[str] = []
    for path in results:
        urls.extend(source_urls(json.loads(path.read_text())))
    reason = (
        "The result JSON carries source URLs but the report cites no quote or locator; "
        "the ledger cannot be populated."
        if urls
        else "The field JSON and the report carry no source URL, verbatim quote or locator; "
        "the ledger cannot be populated."
    )
    write_json(
        out / "exclusion.json",
        {
            "arm": "weizhena",
            "task": task["key"],
            "status": "excluded",
            "reason": reason,
            "evidence": (
                f"results/ carries {len(results)} JSON file(s) with {len(urls)} source URL(s); "
                f"report.md is {len(report)} chars and cites {report.count('http')} URL(s) without "
                "a per-source quote and locator."
            ),
        },
    )
    return "excluded"
