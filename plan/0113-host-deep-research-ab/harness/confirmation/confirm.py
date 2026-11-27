#!/usr/bin/env python3
"""The plan/0113 confirmation: the locked arm against null on the fresh held-out set.

The confirmation is the first read of the fresh sealed set. It decrypts
`tasks/held-out-fresh.json.enc` with the operator-held key, validates the five
tasks, runs two fresh draws per task per arm for the locked arm and `null`, and
prints the verdict from the frozen criteria: a 1.0-point margin, an 8-of-16
per-task floor, zero phantom sources and no foreign-model receipt.
"""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
sys.path.insert(0, str(HARNESS / "selection"))
sys.path.insert(0, str(HARNESS / "tasks"))
sys.path.insert(0, str(HARNESS / "rubric"))

import rubric  # noqa: E402
import run  # noqa: E402
import schema  # noqa: E402

SEALED = HARNESS / "tasks" / "held-out-fresh.json.enc"
SETS = HARNESS / "tasks" / "sets-fresh.json"
KEY = Path("/tmp/opencode/plan0113/held-out-fresh.key")
PLAIN = Path("/tmp/opencode/plan0113/confirmation/held-out-fresh.json")
DRAWS = HERE / "draws-fresh"
SCRATCH = Path("/tmp/opencode/plan0113/confirmation-fresh")
ROUND = HARNESS / "selection" / "round-redo.json"
DRAWS_PER_TASK = 2
MARGIN = 1.0
FLOOR = 8.0


def locked_arm() -> str:
    if ROUND.is_file():
        record = json.loads(ROUND.read_text())
        if isinstance(record.get("locked"), str):
            return record["locked"]
    return "weizhena"


ARMS = [locked_arm(), "null"]


def load_held_out() -> list[dict]:
    if not PLAIN.exists():
        if not KEY.is_file():
            raise SystemExit(f"the held-out key is absent at {KEY}; the operator holds it")
        PLAIN.parent.mkdir(parents=True, exist_ok=True)
        schema.decrypt(SEALED, KEY, PLAIN)
    summary = schema.load_set(PLAIN)
    expected = json.loads(SETS.read_text())["held_out"]["plaintext_set_digest"]
    if summary["set_digest"] != expected:
        raise SystemExit("the decrypted held-out set digest does not match sets.json")
    print(
        f"ok held-out decrypted: {summary['tasks']} tasks "
        f"({summary['known_answer']} known-answer, {summary['house']} house), "
        f"digest {summary['set_digest']}"
    )
    return summary["document"]["tasks"]


def draw_summary(arm: str, task: dict, suffix: str) -> dict:
    path = DRAWS / arm / (task["key"].split("/", 1)[1] + suffix) / "score.json"
    return json.loads(path.read_text())


def task_mean(arm: str, task: dict) -> float:
    return sum(draw_summary(arm, task, f"-d{n}")["score"] for n in range(1, DRAWS_PER_TASK + 1)) / DRAWS_PER_TASK


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--parallel", type=int, default=2)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    tasks = load_held_out()
    if args.check:
        for task in tasks:
            print(f"held-out task: {task['key']} ({task['kind']})")
        return 0

    run.DRAWS = DRAWS
    run.SCRATCH = SCRATCH
    for task in tasks:
        with ThreadPoolExecutor(max_workers=args.parallel) as pool:
            futures = {
                pool.submit(run.safe_run_draw, arm, task, args.force, f"-d{n}"): (arm, n)
                for arm in ARMS
                for n in range(1, DRAWS_PER_TASK + 1)
            }
            for future in as_completed(futures):
                arm, n = futures[future]
                try:
                    summary = future.result()
                except Exception as error:  # noqa: BLE001
                    raise SystemExit(f"confirmation draw crashed for {arm} d{n}: {error}")
                print(
                    f"{arm:8s} {task['key'].split('/', 1)[1]:26s} d{n} "
                    f"{'valid' if summary['valid'] else 'void ':5s} {summary['score']}/{summary['rubric'].get('max', '-')} "
                    f"contract={'ok' if summary['contract_ok'] else 'no'} wall={summary['wall_seconds']}s"
                    + (f"  ({summary['contract_reason']})" if summary["contract_reason"] else ""),
                    flush=True,
                )

    per_task = {}
    draws = []
    for task in tasks:
        key = task["key"].split("/", 1)[1]
        per_task[task["key"]] = {
            arm: task_mean(arm, task) for arm in ARMS
        }
        for arm in ARMS:
            for n in range(1, DRAWS_PER_TASK + 1):
                draws.append(draw_summary(arm, task, f"-d{n}"))
    pooled = {arm: sum(per_task[key][arm] for key in per_task) / len(per_task) for arm in ARMS}
    margin = pooled["weizhena"] - pooled["null"]
    phantom = sum(
        1 for draw in draws if str((draw.get("rubric") or {}).get("reason", "")).startswith("phantom source")
    )
    foreign = 0
    pinned = rubric.pin_model()
    for task in tasks:
        for arm in ARMS:
            for n in range(1, DRAWS_PER_TASK + 1):
                receipt_path = DRAWS / arm / (task["key"].split("/", 1)[1] + f"-d{n}") / "receipt.json"
                if not receipt_path.is_file():
                    foreign += 1
                    continue
                receipt = json.loads(receipt_path.read_text())
                if receipt.get("model") != pinned:
                    foreign += 1
    criteria = {
        "margin": margin >= MARGIN,
        "floor": all(per_task[task["key"]]["weizhena"] >= FLOOR for task in tasks),
        "phantom": phantom == 0,
        "foreign": foreign == 0,
    }
    missed = [name for name, passed in criteria.items() if not passed]
    verdict = "SHIP" if not missed else "NO-SHIP"
    result = {
        "verdict": verdict,
        "locked": ARMS[0],
        "control": "null",
        "draws": len(draws),
        "draws_per_task": DRAWS_PER_TASK,
        "per_task": per_task,
        "pooled": pooled,
        "margin": margin,
        "margin_required": MARGIN,
        "floor": FLOOR,
        "phantom": phantom,
        "foreign": foreign,
        "criteria": criteria,
        "missed": missed,
        "draws_detail": [
            {
                "arm": draw["arm"],
                "task": draw["task"],
                "valid": draw["valid"],
                "score": draw["score"],
                "contract_ok": draw["contract_ok"],
                "contract_reason": draw["contract_reason"],
            }
            for draw in draws
        ],
    }
    (HERE / "verdict.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"pooled: weizhena {pooled['weizhena']:.2f}, null {pooled['null']:.2f}; margin {margin:.2f}")
    print(f"floor: {criteria['floor']}; phantom {phantom}; foreign receipts {foreign}")
    print(f"verdict: {verdict}" + (f" (missed: {', '.join(missed)})" if missed else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
