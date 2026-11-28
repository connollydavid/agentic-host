"""The samber adapter: the report's inline citations to the contract.

The researcher's report carries inline `[passage](url)` citations. The adapter
builds the ledger from those citations and gives each a paragraph locator. A
citation still needs a fetched page in the run's log: a report that cites a
URL the run never fetched is a phantom source, and the adapter records the
exclusion with the count and the first missing URLs instead of passing a
ledger the rubric must void. When the report carries no inline citation, the
adapter records the exclusion the contract's ledger requirement forces.
"""

from __future__ import annotations

from pathlib import Path

from contract import (
    build_receipt,
    canonical_url,
    report_entries,
    validate_report,
    write_json,
)


def convert(fixture: Path, task: dict, out: Path, meta: dict) -> str:
    report = (fixture / "report.md").read_text()
    entries = report_entries(report)
    fetched = {canonical_url(url) for url in meta.get("fetches") or []}
    missing = [entry["url"] for entry in entries if canonical_url(entry["url"]) not in fetched]
    if entries and not missing:
        validate_report(report, entries)
        (out / "report.md").write_text(report)
        write_json(out / "sources.json", {"sources": entries})
        write_json(out / "receipt.json", build_receipt("samber", task["key"], meta))
        return "valid"
    notes = sorted((fixture / "notes").rglob("*.md"))
    if entries:
        reason = (
            f"The report cites {len(entries)} source URL(s), but the run fetched "
            f"{len(entries) - len(missing)} of them; the ledger cannot carry a quote "
            "for a page the run never fetched."
        )
        evidence = (
            f"report.md cites {len(entries)} URL(s); the fetch log carries {len(fetched)} URL(s). "
            f"Missing snapshots: {', '.join(missing[:6])}."
        )
    else:
        reason = (
            "The report carries no inline URL citation with a passage and locator, and the "
            "claim notes carry URL, access and confidence without a verbatim quote or "
            "locator; the ledger cannot be populated."
        )
        evidence = (
            f"report.md is {len(report)} chars with {report.count('http')} URL occurrence(s) "
            f"and no report paragraph citation; {len(notes)} claim note(s) carry URL, accessed "
            "and confidence."
        )
    write_json(
        out / "exclusion.json",
        {
            "arm": "samber",
            "task": task["key"],
            "status": "excluded",
            "reason": reason,
            "evidence": evidence,
        },
    )
    return "excluded"
