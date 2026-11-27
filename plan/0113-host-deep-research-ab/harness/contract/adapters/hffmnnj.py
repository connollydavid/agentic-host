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

NOTE = re.compile(r"\b(rn_[A-Za-z0-9]+)\b")
LOCATOR = re.compile(r"(?im)^locator:\s*(.+)$")
QUOTE = re.compile(r"(?im)^quote:\s*(.+)$")
EVIDENCE = re.compile(r"(?ims)^##\s+Evidence\s*\n+(.+?)(?=\n##\s|\Z)")


def read_note(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ContractError(f"{path.name} has no JSON front matter")
    rest = text[len("---\n"):]
    if "\n---\n" not in rest:
        raise ContractError(f"{path.name} has no closing front-matter fence")
    front, body = rest.split("\n---\n", 1)
    return json.loads(front), body


def quote_for(source: dict, body: str) -> str:
    if isinstance(source.get("quote"), str) and source["quote"].strip():
        return source["quote"].strip()
    line = QUOTE.search(body)
    if line and line.group(1).strip():
        return line.group(1).strip()
    evidence = EVIDENCE.search(body)
    if evidence:
        paragraph = evidence.group(1).strip().split("\n\n", 1)[0].strip()
        if paragraph:
            return paragraph
    return ""


def convert(fixture: Path, task: dict, out: Path, meta: dict) -> str:
    report = (fixture / "report.md").read_text()
    if "<tool_call>" in report or "<function=" in report:
        raise ContractError(
            "the run emitted pseudo tool calls; the plugin tools were not invoked, "
            "so this is a harness break, not an arm exclusion"
        )
    ids = list(dict.fromkeys(NOTE.findall(report)))
    if not ids:
        notes = list(fixture.rglob("rn_*.md"))
        write_json(
            out / "exclusion.json",
            {
                "arm": "hffmnnj",
                "task": task["key"],
                "status": "excluded",
                "reason": (
                    "The native report cites no library note id; this run answered directly instead of "
                    "saving the finding and source notes, so the note-based ledger cannot be populated."
                ),
                "evidence": (
                    f"report.md is {len(report)} chars and cites {report.count('http')} URL(s), with no "
                    f"[rn_...] citation; the library holds {len(notes)} note(s). The plugin's report shape "
                    "cites note ids, and each note carries the source record."
                ),
            },
        )
        return "excluded"
    notes: dict[str, Path] = {}
    for path in fixture.rglob("rn_*.md"):
        note, _ = read_note(path)
        notes[str(note.get("id") or path.stem)] = path
    entries = []
    for note_id in ids:
        path = notes.get(note_id)
        if path is None:
            raise ContractError(f"the report cites {note_id} with no saved note")
        note, body = read_note(path)
        locator = LOCATOR.search(body)
        location = locator.group(1).strip() if locator else str(note.get("title") or note_id)
        sources = note.get("sources") or []
        if not sources:
            raise ContractError(f"{note_id} carries no source record")
        for source in sources:
            quote = quote_for(source, body)
            if not source.get("url") or not quote:
                raise ContractError(f"{note_id} has a source without a URL and a quote")
            entries.append(
                {
                    "id": note_id,
                    "url": source["url"],
                    "quote": quote,
                    "locator": location,
                }
            )
    (out / "report.md").write_text(report)
    write_json(out / "sources.json", {"sources": entries})
    write_json(out / "receipt.json", build_receipt("hffmnnj", task["key"], meta))
    return "valid"
