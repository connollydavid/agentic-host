#!/usr/bin/env python3
"""The plan/0113 mechanical rubric.

A draw is void if the receipt's model or harness is not the pin, if a cited URL
is absent from the run's fetch log, or if a cited URL has no ledger entry. A
scored draw is the sum of the applicable components: citation support (six),
known-answer correctness (four, known-answer tasks), must-cover recall (four,
tasks with a must-cover list), numerals (three, one lost per unsupported
numeral) and prose (three, one lost per host-lint prose match).
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
import unicodedata
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
sys.path.insert(0, str(HARNESS / "contract"))
sys.path.insert(0, str(HARNESS / "tasks"))

import contract  # noqa: E402
import schema  # noqa: E402

PIN_ENV = HARNESS / "pin.env"
MODEL_PIN = HARNESS / "model-pin" / "model-pin.json"
NUMERAL = re.compile(r"\d[\d,]*(?:\.\d+)?")
SENTENCE = re.compile(r"(?<=[.!?])\s+")
CITATION_PASS = 5.0


class RubricError(Exception):
    pass


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def pin_harness() -> dict:
    values = {}
    for line in PIN_ENV.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value.strip().strip('"')
    return {"tag": values["OPENCODE_TAG"], "binary_sha256": values["OPENCODE_BINARY_SHA256"]}


def pin_model() -> dict:
    model = json.loads(MODEL_PIN.read_text())
    return {
        key: model[key]
        for key in ("provider", "route", "deployment_id", "backend", "max_input_tokens", "max_output_tokens")
    }


def void(reason: str) -> dict:
    return {"status": "void", "reason": reason}


def dataset_answer(path: Path, row: int) -> str:
    if schema.sha256_file(path) != schema.DATASET_SHA256:
        raise RubricError("the dataset does not match the frozen digest")
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
    if row < 0 or row >= len(rows):
        raise RubricError(f"row {row} is outside the dataset")
    return rows[row]["answer"]


def fetch_snapshot(draw: Path, log: list[dict], url: str) -> str:
    wanted = contract.canonical_url(url)
    entry = next(
        (item for item in log if contract.canonical_url(item.get("url") or "") == wanted),
        None,
    )
    if entry is None:
        raise RubricError(f"no fetch-log entry for {url}")
    path = draw / str(entry.get("snapshot", ""))
    if not path.is_file():
        raise RubricError(f"the snapshot for {url} is missing at {path}")
    return normalize(path.read_text())


def score(draw: Path, task: dict, dataset: Path) -> dict:
    receipt = json.loads((draw / "receipt.json").read_text())
    if receipt.get("task") != task["key"]:
        return void("receipt names another task")
    if receipt.get("model") != pin_model():
        return void("receipt model is foreign to the pinned route")
    if receipt.get("harness") != pin_harness():
        return void("receipt harness is not the pinned binary")

    report = (draw / "report.md").read_text()
    try:
        sources = contract.validate_sources(json.loads((draw / "sources.json").read_text()))
        contract.validate_report(report, sources)
    except contract.ContractError as error:
        return void(f"contract: {error}")

    report_urls = {contract.canonical_url(match) for match in contract.citation_urls(report)}
    ledger_urls = {contract.canonical_url(entry["url"]) for entry in sources}
    if not report_urls <= ledger_urls:
        return void("the report cites a URL absent from the ledger")
    log = [json.loads(line) for line in (draw / "fetch-log.jsonl").read_text().splitlines() if line.strip()]
    logged = {contract.canonical_url(item.get("url") or "") for item in log}
    phantom = sorted((report_urls | ledger_urls) - logged)
    if phantom:
        return void("phantom source: " + ", ".join(phantom))

    snapshots = {entry["url"]: fetch_snapshot(draw, log, entry["url"]) for entry in sources}

    cited = []
    for sentence in SENTENCE.split(report):
        matches = [
            entry
            for entry in sources
            if entry["url"] in sentence or ("id" in entry and entry["id"] in sentence)
        ]
        if matches:
            cited.append((sentence, matches))
    if not cited:
        return void("the report has no cited sentence")
    supported = sum(
        1
        for _, matches in cited
        if all(normalize(entry["quote"]) in snapshots[entry["url"]] for entry in matches)
    )
    citation = 6 * supported / len(cited)

    known = None
    max_known = 0
    if task["kind"] == "known-answer":
        max_known = 4
        answer = dataset_answer(dataset, task["source"]["row"])
        known = 4 if normalize(answer) in normalize(report) else 0

    cover = None
    max_cover = 0
    if task.get("must_cover"):
        max_cover = 4
        matched = sum(
            1
            for item in task["must_cover"]
            if any(normalize(name) in normalize(report) for name in [item["entity"], *item.get("aliases", [])])
        )
        cover = 4 * matched / len(task["must_cover"])

    numerals = NUMERAL.findall(report)
    unsupported = [value for value in numerals if not any(value in snapshot for snapshot in snapshots.values())]
    numeral_points = max(0, 3 - len(unsupported))

    prose = subprocess.run(
        ["host-lint", "--prose", "--json", str(draw / "report.md")],
        capture_output=True,
        text=True,
        timeout=60,
    )
    try:
        prose_matches = json.loads(prose.stdout) if prose.stdout.strip() else []
    except json.JSONDecodeError:
        return void("the prose lane returned unreadable JSON")
    prose_points = max(0, 3 - len(prose_matches))

    maximum = 6 + max_known + max_cover + 3 + 3
    total = citation + (known or 0) + (cover or 0) + numeral_points + prose_points
    return {
        "status": "scored",
        "task": task["key"],
        "kind": task["kind"],
        "components": {
            "citation_support": citation,
            "known_answer": known,
            "must_cover": cover,
            "numerals": numeral_points,
            "prose": prose_points,
        },
        "max": maximum,
        "score": total,
        "citation_pass": citation >= CITATION_PASS,
        "notes": {
            "cited_sentences": len(cited),
            "supported_sentences": supported,
            "numerals": numerals,
            "unsupported_numerals": unsupported,
            "prose_matches": len(prose_matches),
        },
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draw", type=Path, required=True)
    parser.add_argument("--task", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    args = parser.parse_args(argv)
    task = json.loads(args.task.read_text())
    try:
        result = score(args.draw, task, args.dataset)
    except (RubricError, FileNotFoundError, json.JSONDecodeError) as error:
        result = void(str(error))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "scored" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
