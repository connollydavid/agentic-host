#!/usr/bin/env python3
"""The plan/0113 rubric controls.

A clean house draw scores full, a planted phantom citation voids, a planted
wrong answer misses its key, and a receipt on a foreign model is refused.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
sys.path.insert(0, str(HARNESS / "contract"))
sys.path.insert(0, str(HARNESS / "tasks"))

import contract  # noqa: E402
import rubric  # noqa: E402
import schema  # noqa: E402

TASKS = HARNESS / "tasks" / "selection.json"
DATASET = Path("/tmp/opencode/simpleqa.csv")
SCRATCH = Path("/tmp/opencode/plan0113/probes/rubric")
NULL_CONFIG = HARNESS / "contract" / "fixtures" / "null" / "arm_config.json"
PASSES: list[str] = []


class ProbeFailure(Exception):
    pass


def fail(message: str) -> None:
    raise ProbeFailure(message)


def note(message: str) -> None:
    PASSES.append(message)
    print(f"PASS {message}", flush=True)


def task_from_set(key: str) -> dict:
    document = json.loads(TASKS.read_text())
    return next(task for task in document["tasks"] if task["key"] == key)


def receipt_for(task: dict) -> dict:
    meta = {
        "harness": rubric.pin_harness(),
        "model": rubric.pin_model(),
        "search_provider": "exa",
        "caps": contract.CAPS,
        "digests": {
            "task": schema.task_digest(task),
            "harness_pin": schema.sha256_file(HARNESS / "pin.env"),
            "model_pin": schema.sha256_file(HARNESS / "model-pin" / "model-pin.json"),
            "arm_config": schema.sha256_file(NULL_CONFIG),
        },
    }
    return contract.build_receipt("null", task["key"], meta)


def run(draw: Path, task: dict) -> dict:
    task_file = draw / "task.json"
    contract.write_json(task_file, task)
    result = subprocess.run(
        [
            sys.executable,
            str(HERE / "rubric.py"),
            "--draw",
            str(draw),
            "--task",
            str(task_file),
            "--dataset",
            str(DATASET),
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        fail(f"rubric output is not JSON: {result.stdout!r} {result.stderr!r}")


def main() -> int:
    if not DATASET.exists():
        DATASET.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(schema.DATASET_URL, DATASET)
    if schema.sha256_file(DATASET) != schema.DATASET_SHA256:
        fail("the SimpleQA dataset does not match the frozen digest")

    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir(parents=True, exist_ok=True)

    house = task_from_set("selection/house-path-crates")
    known = task_from_set("selection/simpleqa-0000")

    clean = SCRATCH / "clean-house"
    shutil.copytree(HERE / "fixtures" / "clean-house", clean)
    contract.write_json(clean / "receipt.json", receipt_for(house))
    clean_result = run(clean, house)
    if clean_result.get("status") != "scored":
        fail(f"the clean draw was void: {clean_result}")
    if clean_result["score"] != clean_result["max"] or clean_result["max"] != 16:
        fail(f"the clean draw did not score full: {clean_result}")
    if not clean_result.get("citation_pass"):
        fail(f"the clean draw missed the frozen citation threshold: {clean_result}")
    note(f"clean house draw scores full: {clean_result['score']}/{clean_result['max']}")

    phantom = SCRATCH / "phantom"
    shutil.copytree(clean, phantom)
    sources = json.loads((phantom / "sources.json").read_text())
    sources["sources"].append(
        {
            "url": "https://invented.example/claim",
            "quote": "The contract is optional.",
            "locator": "Phantom page, first paragraph",
        }
    )
    contract.write_json(phantom / "sources.json", sources)
    with (phantom / "report.md").open("a") as handle:
        handle.write("\nA phantom source says the contract is optional [https://invented.example/claim].\n")
    phantom_result = run(phantom, house)
    if phantom_result.get("status") != "void" or "phantom" not in phantom_result.get("reason", ""):
        fail(f"the phantom citation did not void the draw: {phantom_result}")
    note(f"planted phantom citation voids: {phantom_result['reason']}")

    foreign = SCRATCH / "foreign-model"
    shutil.copytree(clean, foreign)
    receipt = json.loads((foreign / "receipt.json").read_text())
    receipt["model"]["route"] = "qwen3.8-27b"
    receipt["model"]["backend"] = "openai/qwen3.8-27b"
    contract.write_json(foreign / "receipt.json", receipt)
    foreign_result = run(foreign, house)
    if foreign_result.get("status") != "void" or "model" not in foreign_result.get("reason", ""):
        fail(f"the foreign model was not refused: {foreign_result}")
    note(f"foreign-model draw is refused: {foreign_result['reason']}")

    wrong = SCRATCH / "wrong-answer"
    shutil.copytree(HERE / "fixtures" / "wrong-known-answer", wrong)
    contract.write_json(wrong / "receipt.json", receipt_for(known))
    wrong_result = run(wrong, known)
    if wrong_result.get("status") != "scored":
        fail(f"the wrong-answer draw was unexpectedly void: {wrong_result}")
    if wrong_result["components"]["known_answer"] != 0:
        fail(f"the planted wrong answer still scored its key: {wrong_result}")
    if wrong_result["score"] >= wrong_result["max"]:
        fail(f"the planted wrong answer scored full: {wrong_result}")
    note(
        f"planted wrong answer misses its key: known_answer=0, "
        f"score {wrong_result['score']}/{wrong_result['max']}"
    )

    unsupported = SCRATCH / "unsupported-quote"
    shutil.copytree(clean, unsupported)
    sources = json.loads((unsupported / "sources.json").read_text())
    sources["sources"][0]["quote"] = "A sentence that does not appear in the snapshot."
    contract.write_json(unsupported / "sources.json", sources)
    unsupported_result = run(unsupported, house)
    if unsupported_result.get("status") != "scored":
        fail(f"the unsupported quote was unexpectedly void: {unsupported_result}")
    if unsupported_result.get("citation_pass") is not False or unsupported_result["components"]["citation_support"] != 0:
        fail(f"the unsupported quote still met the citation threshold: {unsupported_result}")
    note(
        f"planted unsupported quote misses the frozen threshold: "
        f"citation_support=0, score {unsupported_result['score']}/{unsupported_result['max']}"
    )

    print(f"rubric-probe: {len(PASSES)} checks passed", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProbeFailure as error:
        print(f"FAIL {error}", file=sys.stderr, flush=True)
        raise SystemExit(1)
