"""The plan/0113 run contract: one task in; a report, a source ledger and a receipt out.

The contract is deliberately small. A task file names the question; a draw
returns a Markdown report and a source ledger whose entries carry the URL, the
verbatim quote and the locator; the receipt records the pinned harness, the
pinned model, the search provider, the budget and the config digests.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

CAPS = {
    "prompt_tokens": 200000,
    "completion_tokens": 50000,
    "tool_calls": 60,
    "wall_seconds": 10800,
}

HEX = re.compile(r"^[0-9a-f]{64}$")
URL = re.compile(r"^https?://\S+$")
CITED = re.compile(r"https?://[^\s<>\"']+")


def normalize_url(url: str) -> str:
    """Strip trailing punctuation and only unbalanced closing brackets.

    A balanced ``(...)`` inside a URL is part of the URL; a closing bracket
    that is the report's punctuation is not. A markdown link whose text is a
    URL (``[https://a](https://b)``) contributes its target, not its text.
    """
    if "](" in url:
        url = url.rsplit("](", 1)[-1]
    url = url.rstrip(".,;:")
    for opener, closer in (("(", ")"), ("[", "]"), ("{", "}")):
        while url.endswith(closer) and url.count(opener) < url.count(closer):
            url = url[:-1]
    return url


class ContractError(Exception):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def load_task(path: Path) -> dict:
    task = json.loads(path.read_text())
    if not isinstance(task.get("key"), str) or not task["key"]:
        raise ContractError("task.key must be a non-empty string")
    kind = task.get("kind")
    if kind == "known-answer":
        source = task.get("source")
        if not isinstance(source, dict) or not source.get("benchmark"):
            raise ContractError("a known-answer task needs a source.benchmark")
        if "question" in task:
            raise ContractError("a known-answer task must not embed the question")
    else:
        if not isinstance(task.get("question"), str) or not task["question"].strip():
            raise ContractError("task.question must be a non-empty string")
    cover = task.get("must_cover", [])
    if not isinstance(cover, list):
        raise ContractError("task.must_cover must be a list")
    for item in cover:
        if not isinstance(item, dict) or not isinstance(item.get("entity"), str) or not item["entity"]:
            raise ContractError("each must_cover item needs a non-empty entity")
    return task


def validate_sources(sources: object) -> list[dict]:
    if not isinstance(sources, dict) or not isinstance(sources.get("sources"), list):
        raise ContractError("sources.json must be an object with a sources list")
    entries = sources["sources"]
    if not entries:
        raise ContractError("sources.json carries no sources")
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            raise ContractError(f"source {index} is not an object")
        url = entry.get("url")
        quote = entry.get("quote")
        locator = entry.get("locator")
        if not isinstance(url, str) or not URL.match(url):
            raise ContractError(f"source {index} has no http(s) URL")
        if not isinstance(quote, str) or not quote.strip():
            raise ContractError(f"source {index} has no verbatim quote")
        if not isinstance(locator, str) or not locator.strip():
            raise ContractError(f"source {index} has no locator")
        if "id" in entry and (not isinstance(entry["id"], str) or not entry["id"].strip()):
            raise ContractError(f"source {index} has an empty id")
    return entries


def validate_report(report: str, sources: list[dict]) -> None:
    if not report.strip():
        raise ContractError("report.md is empty")
    for index, entry in enumerate(sources, 1):
        key = entry.get("id") or entry["url"]
        if key not in report:
            raise ContractError(f"report.md does not cite source {index} ({key})")
    ledger = {normalize_url(entry["url"]) for entry in sources}
    report_urls = {normalize_url(match) for match in CITED.findall(report)}
    missing = sorted(report_urls - ledger)
    if missing:
        raise ContractError(f"report.md cites URL(s) absent from the ledger: {', '.join(missing)}")


def build_receipt(arm: str, task_key: str, meta: dict, status: str = "dry-run", used: dict | None = None) -> dict:
    return {
        "task": task_key,
        "arm": arm,
        "status": meta.get("status", status),
        "harness": meta["harness"],
        "model": meta["model"],
        "search_provider": meta["search_provider"],
        "budget": {
            "caps": meta["caps"],
            "used": used
            or {"prompt_tokens": 0, "completion_tokens": 0, "tool_calls": 0, "wall_seconds": 0},
        },
        "config_digests": meta["digests"],
    }


def validate_receipt(receipt: object, arm: str, task_key: str, meta: dict, status: str = "dry-run") -> None:
    if not isinstance(receipt, dict):
        raise ContractError("receipt.json is not an object")
    if receipt.get("arm") != arm or receipt.get("task") != task_key:
        raise ContractError("receipt names another arm or task")
    if receipt.get("status") != status:
        raise ContractError(f"receipt status is {receipt.get('status')!r}, expected {status!r}")
    if receipt.get("harness") != meta["harness"]:
        raise ContractError("receipt harness does not match the pin")
    if receipt.get("model") != meta["model"]:
        raise ContractError("receipt model does not match the pin")
    if not isinstance(receipt.get("search_provider"), str) or not receipt["search_provider"].strip():
        raise ContractError("receipt has no search provider")
    budget = receipt.get("budget")
    if not isinstance(budget, dict) or budget.get("caps") != meta["caps"]:
        raise ContractError("receipt budget caps do not match the contract")
    used = budget.get("used")
    if not isinstance(used, dict) or set(used) != set(meta["caps"]):
        raise ContractError("receipt budget used has the wrong keys")
    for key, value in used.items():
        if not isinstance(value, (int, float)) or value < 0:
            raise ContractError(f"receipt budget used.{key} is not a non-negative number")
    digests = receipt.get("config_digests")
    if not isinstance(digests, dict) or not digests:
        raise ContractError("receipt has no config digests")
    for key, value in digests.items():
        if not isinstance(value, str) or not HEX.match(value):
            raise ContractError(f"receipt config digest {key!r} is not sha256")
    if digests != meta["digests"]:
        raise ContractError("receipt config digests do not match the files")


def validate_fetch_log(path: Path) -> list[dict]:
    if not path.is_file():
        raise ContractError("a live draw needs fetch-log.jsonl")
    entries = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as error:
            raise ContractError(f"fetch-log line {number} is not JSON: {error}") from error
        if not isinstance(entry, dict):
            raise ContractError(f"fetch-log line {number} is not an object")
        url = entry.get("url")
        status = entry.get("status")
        snapshot = entry.get("snapshot")
        if not isinstance(url, str) or not URL.match(url):
            raise ContractError(f"fetch-log line {number} has no http(s) URL")
        if not isinstance(status, int):
            raise ContractError(f"fetch-log line {number} has no integer status")
        if not isinstance(snapshot, str) or not snapshot.strip():
            raise ContractError(f"fetch-log line {number} has no snapshot")
        if not (path.parent / snapshot).is_file():
            raise ContractError(f"fetch-log line {number} snapshot is missing: {snapshot}")
        entries.append(entry)
    if not entries:
        raise ContractError("fetch-log.jsonl carries no fetches")
    return entries


def validate_output(out: Path, arm: str, task_key: str, meta: dict) -> dict:
    report = (out / "report.md").read_text()
    sources = validate_sources(json.loads((out / "sources.json").read_text()))
    validate_report(report, sources)
    receipt = json.loads((out / "receipt.json").read_text())
    status = receipt.get("status")
    validate_receipt(receipt, arm, task_key, meta, status=status)
    if status == "live":
        log = validate_fetch_log(out / "fetch-log.jsonl")
        logged = {entry["url"] for entry in log}
        phantom = sorted(entry["url"] for entry in sources if entry["url"] not in logged)
        if phantom:
            raise ContractError("phantom source(s) absent from the fetch log: " + ", ".join(phantom))
    return {"report_chars": len(report), "sources": len(sources), "digests": len(receipt["config_digests"])}


def validate_exclusion(out: Path, arm: str, task_key: str) -> dict:
    exclusion = json.loads((out / "exclusion.json").read_text())
    if exclusion.get("arm") != arm or exclusion.get("task") != task_key:
        raise ContractError("exclusion names another arm or task")
    if exclusion.get("status") != "excluded":
        raise ContractError("exclusion status is not 'excluded'")
    for key in ("reason", "evidence"):
        if not isinstance(exclusion.get(key), str) or not exclusion[key].strip():
            raise ContractError(f"exclusion has no {key}")
    return exclusion
