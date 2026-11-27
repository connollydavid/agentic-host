"""The kanatami adapter: worker result sets to the contract.

The skill's final report cites URLs, and the workers return structured raw
data with `url` and `full_text`. The adapter resolves each cited URL to its
worker result, takes the first sentence of the fetched text as the quote and
records the worker and paragraph as the locator.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from contract import ContractError, build_receipt, write_json

URL = re.compile(r"https?://[^\s)\]>\"']+")


def first_sentence(text: str) -> str:
    return re.split(r"(?<=[.!?])\s+", text.strip(), maxsplit=1)[0].strip()


def convert(fixture: Path, task: dict, out: Path, meta: dict) -> str:
    report = (fixture / "report.md").read_text()
    cited = list(dict.fromkeys(url.rstrip(".,;:") for url in URL.findall(report)))
    if not cited:
        raise ContractError("the report cites no URL")
    workers = json.loads((fixture / "workers.json").read_text()).get("workers", [])
    found: dict[str, tuple[str, int, dict]] = {}
    for worker in workers:
        for index, result in enumerate(worker.get("results", []), 1):
            found.setdefault(result.get("url"), (worker["id"], index, result))
    entries = []
    for url in cited:
        if url not in found:
            raise ContractError(f"the report cites {url} with no worker result")
        worker_id, index, result = found[url]
        quote = first_sentence(result.get("full_text") or result.get("snippet") or "")
        if not quote:
            raise ContractError(f"{url} carries no passage")
        entries.append(
            {
                "url": url,
                "quote": quote,
                "locator": f"worker {worker_id} result {index} full_text paragraph 1",
            }
        )
    (out / "report.md").write_text(report)
    write_json(out / "sources.json", {"sources": entries})
    write_json(out / "receipt.json", build_receipt("kanatami", task["key"], meta))
    return "valid"
