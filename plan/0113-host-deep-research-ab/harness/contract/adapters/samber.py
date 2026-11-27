"""The samber exclusion: claim records carry no quote or locator.

The researcher returns a source URL, access date and confidence per claim; the
report cites the URL. The adapter looks for a verbatim quote or a locator in
the claim notes; finding neither, it records the exclusion.
"""

from __future__ import annotations

from pathlib import Path

from contract import ContractError, write_json


def convert(fixture: Path, task: dict, out: Path, meta: dict) -> str:
    notes = sorted((fixture / "notes").glob("*.md"))
    for path in notes:
        text = path.read_text()
        for field in ("quote:", "locator:"):
            if field in text.lower():
                raise ContractError(f"{path.name} now carries {field}; re-examine the exclusion")
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
                "notes/claim.md carries claim, url, accessed and confidence; the researcher reference "
                "returns URL, accessed date and confidence per claim; report.md cites the URL without a "
                "passage or locator."
            ),
        },
    )
    return "excluded"
