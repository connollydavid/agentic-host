"""The samber adapter: the report's inline citations to the contract.

The researcher's report carries inline `[passage](url)` citations. The adapter
builds the ledger from those citations and gives each a paragraph locator; the
run's actual `webfetch` snapshot still has to support the quote. When the
report carries no inline citation, the adapter records the exclusion the
contract's ledger requirement forces.
"""

from __future__ import annotations

from pathlib import Path

from contract import build_receipt, report_entries, validate_report, write_json


def convert(fixture: Path, task: dict, out: Path, meta: dict) -> str:
    report = (fixture / "report.md").read_text()
    entries = report_entries(report)
    if entries:
        validate_report(report, entries)
        (out / "report.md").write_text(report)
        write_json(out / "sources.json", {"sources": entries})
        write_json(out / "receipt.json", build_receipt("samber", task["key"], meta))
        return "valid"
    notes = sorted((fixture / "notes").rglob("*.md"))
    write_json(
        out / "exclusion.json",
        {
            "arm": "samber",
            "task": task["key"],
            "status": "excluded",
            "reason": (
                "The report carries no inline URL citation with a passage and locator, and the "
                "claim notes carry URL, access and confidence without a verbatim quote or "
                "locator; the ledger cannot be populated."
            ),
            "evidence": (
                f"report.md is {len(report)} chars with {report.count('http')} URL occurrence(s) "
                f"and no report paragraph citation; {len(notes)} claim note(s) carry URL, accessed "
                "and confidence."
            ),
        },
    )
    return "excluded"
