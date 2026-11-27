"""The samber adapter: claim records to the contract, or the exclusion.

The researcher returns a source URL, access date and confidence per claim. When
a note also carries a `quote:` and a `locator:`, the adapter maps it to the
ledger. When the notes carry no such fields, the adapter records the exclusion
the contract's ledger requirement forces.
"""

from __future__ import annotations

import re
from pathlib import Path

from contract import ContractError, build_receipt, validate_report, validate_sources, write_json

URL = re.compile(r"(?im)^\s*url:\s*(\S+)\s*$")
QUOTE = re.compile(r"(?ims)^\s*quote:\s*(.+?)(?=\n\s*\w+:|\Z)")
LOCATOR = re.compile(r"(?im)^\s*locator:\s*(.+)$")


def read_claim(path: Path) -> dict:
    text = path.read_text()
    url = URL.search(text)
    quote = QUOTE.search(text)
    locator = LOCATOR.search(text)
    return {
        "path": path,
        "url": url.group(1).strip() if url else None,
        "quote": " ".join(quote.group(1).split()) if quote else None,
        "locator": locator.group(1).strip() if locator else None,
    }


def convert(fixture: Path, task: dict, out: Path, meta: dict) -> str:
    notes = sorted((fixture / "notes").rglob("*.md"))
    claims = [read_claim(path) for path in notes]
    report = (fixture / "report.md").read_text()
    if claims and all(claim["url"] and claim["quote"] and claim["locator"] for claim in claims):
        entries = [
            {"url": claim["url"], "quote": claim["quote"], "locator": claim["locator"]}
            for claim in claims
        ]
        sources = validate_sources({"sources": entries})
        validate_report(report, sources)
        (out / "report.md").write_text(report)
        write_json(out / "sources.json", {"sources": sources})
        write_json(out / "receipt.json", build_receipt("samber", task["key"], meta))
        return "valid"
    if any(claim["quote"] or claim["locator"] for claim in claims):
        raise ContractError("a claim note now carries a quote or locator; re-examine the exclusion")
    write_json(
        out / "exclusion.json",
        {
            "arm": "samber",
            "task": task["key"],
            "status": "excluded",
            "reason": (
                "The researcher's claim record carries the source URL, access date and confidence, but no "
                "verbatim quote or locator; the report cites the URL only, so the ledger's quote and "
                "locator cannot be populated."
            ),
            "evidence": (
                f"{len(claims)} claim note(s) carry URL, accessed and confidence; none carries a quote: "
                "and locator: pair; report.md cites the URL without a passage or locator."
            ),
        },
    )
    return "excluded"
