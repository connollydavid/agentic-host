"""The hffmnnj adapter: library notes to the contract.

The plugin's report note cites finding notes by id. Each finding carries a
source with `url` and `quote`; the evidence contract puts the locator in the
note body. The adapter resolves each cited note id, reads the source record,
takes the `locator:` line from the body and writes the ledger.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from contract import ContractError, build_receipt, write_json

NOTE = re.compile(r"\[(rn_[A-Za-z0-9]+)\]")
LOCATOR = re.compile(r"(?im)^locator:\s*(.+)$")


def read_note(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ContractError(f"{path.name} has no JSON front matter")
    rest = text[len("---\n"):]
    if "\n---\n" not in rest:
        raise ContractError(f"{path.name} has no closing front-matter fence")
    front, body = rest.split("\n---\n", 1)
    return json.loads(front), body


def convert(fixture: Path, task: dict, out: Path, meta: dict) -> str:
    report = (fixture / "report.md").read_text()
    ids = list(dict.fromkeys(NOTE.findall(report)))
    if not ids:
        raise ContractError("the report cites no note id")
    entries = []
    for note_id in ids:
        note, body = read_note(fixture / "notes" / f"{note_id}.md")
        locator = LOCATOR.search(body)
        if not locator:
            raise ContractError(f"{note_id} carries no locator in its body")
        sources = note.get("sources") or []
        if not sources:
            raise ContractError(f"{note_id} carries no source record")
        for source in sources:
            if not source.get("quote"):
                raise ContractError(f"{note_id} has a source without a verbatim quote")
            entries.append(
                {
                    "id": note_id,
                    "url": source["url"],
                    "quote": source["quote"],
                    "locator": locator.group(1).strip(),
                }
            )
    (out / "report.md").write_text(report)
    write_json(out / "sources.json", {"sources": entries})
    write_json(out / "receipt.json", build_receipt("hffmnnj", task["key"], meta))
    return "valid"
