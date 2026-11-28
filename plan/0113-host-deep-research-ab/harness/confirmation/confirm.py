#!/usr/bin/env python3
"""The plan/0113 confirmation: the locked arm against null on fresh-2.

The confirmation is the first read of the fresh-2 sealed set. `--check` reads
only the sealed ciphertext digest and the recorded set metadata; it never
decrypts. A run requires the operator-held `--key`, decrypts to memory,
validates the set digest, and runs two fresh draws per task per arm for the
locked arm and `null` in a recorded random order within each task block. It
then judges every valid draw with the pinned Opus 5.5 judge and prints the
verdict from the frozen criteria: a 1.0-point margin, an 8-of-16 per-task
floor, zero phantom sources, no foreign-model reply, every draw valid or a
recorded harness-break re-run, and the judge's model, route and validity gate
passed. A void is a gate, not a measured zero.
"""

from __future__ import annotations

import argparse
import json
import random
import secrets
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
sys.path.insert(0, str(HARNESS / "selection"))
sys.path.insert(0, str(HARNESS / "tasks"))
sys.path.insert(0, str(HARNESS / "rubric"))
sys.path.insert(0, str(HARNESS / "judge"))

import judge  # noqa: E402
import rubric  # noqa: E402
import run  # noqa: E402
import schema  # noqa: E402

SEALED = HARNESS / "tasks" / "held-out-fresh2.json.enc"
SETS = HARNESS / "tasks" / "sets-fresh2.json"
SELECTION = HARNESS / "tasks" / "selection.json"
DRAWS = HERE / "draws-fresh2"
SCRATCH = Path("/tmp/opencode/plan0113/confirmation-fresh2")
ROUND = HARNESS / "selection" / "round-redo.json"
JUDGE_VALIDITY = HARNESS / "judge" / "validity.json"
DRAWS_PER_TASK = 2
MARGIN = 1.0
FLOOR = 8.0


def fail(message: str) -> None:
    raise SystemExit(message)


def check(sealed: Path, sets: Path) -> None:
    if not sealed.is_file():
        fail(f"the sealed fresh-2 set is absent at {sealed}")
    if not sets.is_file():
        fail(f"the fresh-2 set record is absent at {sets}")
    record = json.loads(sets.read_text())
    held = record.get("held_out") or {}
    if not held.get("sealed"):
        fail("the fresh-2 set record does not declare the set sealed")
    if schema.sha256_file(sealed) != held.get("ciphertext_sha256"):
        fail("the fresh-2 ciphertext digest does not match the record")
    if sealed.read_bytes()[:8] != b"Salted__":
        fail("the fresh-2 file is not an OpenSSL ciphertext")
    plaintext = sealed.with_suffix(".json")
    if plaintext.exists():
        fail(f"the fresh-2 plaintext is present at {plaintext}; the set is burned")
    selection = schema.load_set(SELECTION)
    if selection["set_digest"] != (record.get("selection") or {}).get("set_digest"):
        fail("the selection digest does not match the fresh-2 record")
    print(
        f"ok fresh-2 sealed: {held.get('tasks')} tasks "
        f"({held.get('known_answer')} known-answer, {held.get('house')} house), "
        f"ciphertext {held.get('ciphertext_sha256')}"
    )
    print(f"ok selection unchanged: {selection['tasks']} tasks, digest {selection['set_digest']}")
    print("ok --check read only the seal; no key was read and no plaintext was written")


def locked_arm() -> str:
    if not ROUND.is_file():
        fail("the selection round has not written round-redo.json; the confirmation waits")
    record = json.loads(ROUND.read_text())
    arm = record.get("locked")
    if record.get("decision") != "LOCKED" or not isinstance(arm, str) or not arm:
        fail("round-redo.json records no locked arm")
    if arm == "null" or arm not in run.ADAPTERS:
        fail(f"round-redo.json names {arm!r}, which is not a candidate arm")
    return arm


def load_tasks(sealed: Path, sets: Path, key: Path) -> tuple[list[dict], dict, dict]:
    if not key.is_file():
        fail(f"the operator-held key is absent at {key}")
    completed = subprocess.run(
        [
            "openssl",
            "enc",
            "-d",
            "-aes-256-cbc",
            "-pbkdf2",
            "-in",
            str(sealed),
            "-pass",
            f"file:{key}",
        ],
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        fail(f"openssl could not decrypt the fresh-2 set: {completed.stderr[-500:]}")
    document = json.loads(completed.stdout)
    summary = schema.validate_set(document)
    record = json.loads(sets.read_text())
    held = record.get("held_out") or {}
    if summary["set_digest"] != held.get("plaintext_set_digest"):
        fail("the decrypted fresh-2 set digest does not match the record")
    if summary["tasks"] != held.get("tasks"):
        fail("the decrypted fresh-2 task count does not match the record")
    print(
        f"ok fresh-2 decrypted: {summary['tasks']} tasks "
        f"({summary['known_answer']} known-answer, {summary['house']} house), "
        f"digest {summary['set_digest']}"
    )
    return document["tasks"], summary, record


def draw_name(task: dict, n: int) -> str:
    return task["key"].split("/", 1)[1] + f"-d{n}"


def draw_path(arm: str, task: dict, n: int) -> Path:
    return DRAWS / arm / draw_name(task, n)


def draw_summary(arm: str, task: dict, n: int) -> dict:
    path = draw_path(arm, task, n) / "score.json"
    if not path.is_file():
        fail(f"the confirmation draw is missing at {path}")
    return json.loads(path.read_text())


def task_mean(arm: str, task: dict, draws: dict[tuple[str, str, int], dict]) -> float:
    return sum(draws[(arm, task["key"], n)]["score"] for n in range(1, DRAWS_PER_TASK + 1)) / DRAWS_PER_TASK


def valid_judge(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text())
    except json.JSONDecodeError:
        return None
    if not value.get("valid") or value.get("model") != judge.EXPECTED_MODEL or value.get("route") != judge.ROUTE:
        return None
    score = value.get("score")
    if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 8:
        return None
    return value


def judge_draws(draws: list[dict], tasks_by_key: dict[str, dict]) -> tuple[int, int, float, str]:
    if not JUDGE_VALIDITY.is_file() or not json.loads(JUDGE_VALIDITY.read_text()).get("passed"):
        return 0, 0, 0.0, "the judge validity gate has not passed"
    judged = 0
    invalid = 0
    cost = 0.0
    for draw in draws:
        if not draw["valid"]:
            continue
        path = DRAWS / draw["arm"] / draw["draw"] / "judge.json"
        record = valid_judge(path)
        if record is not None:
            judged += 1
            cost += float(record.get("cost_usd") or 0)
            continue
        task = tasks_by_key[draw["task"]]
        question = run.task_question(task)
        entities = [item["entity"] for item in task.get("must_cover", [])]
        report = (DRAWS / draw["arm"] / draw["draw"] / "report.md").read_text()
        ledger = json.loads((DRAWS / draw["arm"] / draw["draw"] / "sources.json").read_text())
        result = judge.judge(question, entities, report, ledger)
        result["task"] = draw["task"]
        path.write_text(json.dumps(result, indent=2) + "\n")
        if valid_judge(path) is not None:
            judged += 1
            cost += float(result.get("cost_usd") or 0)
        else:
            invalid += 1
    return judged, invalid, cost, ""


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="read the seal only; never decrypt")
    parser.add_argument("--key", help="the operator-held key; required for a draw run")
    parser.add_argument("--sealed", default=str(SEALED))
    parser.add_argument("--sets", default=str(SETS))
    parser.add_argument("--parallel", type=int, default=2)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    sealed = Path(args.sealed)
    sets = Path(args.sets)
    if args.check:
        check(sealed, sets)
        return 0
    if not args.key:
        parser.error("--key is required; the operator holds the fresh-2 key")
    tasks, _summary, record = load_tasks(sealed, sets, Path(args.key))
    arm = locked_arm()
    arms = [arm, "null"]
    if DRAWS.exists() and any(DRAWS.rglob("score.json")) and not args.force:
        fail(f"confirmation draws already exist under {DRAWS}; a re-run needs --force")
    run.DRAWS = DRAWS
    run.SCRATCH = SCRATCH
    rng = random.Random(secrets.randbits(64))
    order: list[dict] = []
    for task in tasks:
        jobs = [(a, n) for a in arms for n in range(1, DRAWS_PER_TASK + 1)]
        rng.shuffle(jobs)
        order.append(
            {
                "task": task["key"],
                "order": [f"{a}-d{n}" for a, n in jobs],
            }
        )
        with ThreadPoolExecutor(max_workers=args.parallel) as pool:
            futures = {
                pool.submit(run.safe_run_draw, a, task, args.force, f"-d{n}"): (a, n)
                for a, n in jobs
            }
            for future in as_completed(futures):
                a, n = futures[future]
                summary = future.result()
                print(
                    f"{a:8s} {task['key'].split('/', 1)[1]:28s} d{n} "
                    f"{'valid' if summary['valid'] else 'void ':5s} "
                    f"{summary['score']}/{summary['rubric'].get('max', '-')} "
                    f"wall={summary['wall_seconds']}s"
                    + (f"  ({summary['contract_reason']})" if summary["contract_reason"] else ""),
                    flush=True,
                )

    reruns: list[dict] = []
    for task in tasks:
        for a in arms:
            for n in range(1, DRAWS_PER_TASK + 1):
                first = draw_summary(a, task, n)
                if first["break_class"] != "harness" or first.get("rerun_of"):
                    continue
                print(f"remedy: {a} {task['key'].split('/', 1)[1]} d{n} is a harness break; re-running once", flush=True)
                second = run.safe_run_draw(a, task, force=True, suffix=f"-d{n}")
                reruns.append(
                    {
                        "arm": a,
                        "task": task["key"],
                        "draw": draw_name(task, n),
                        "previous": second.get("rerun_of"),
                        "first_break_class": first["break_class"],
                        "first_reason": first.get("contract_reason"),
                        "valid": second["valid"],
                        "reason": second.get("contract_reason"),
                    }
                )

    draws: list[dict] = []
    draws_by: dict[tuple[str, str, int], dict] = {}
    for task in tasks:
        for a in arms:
            for n in range(1, DRAWS_PER_TASK + 1):
                summary = draw_summary(a, task, n)
                draws.append(summary)
                draws_by[(a, task["key"], n)] = summary
    invalid = [draw for draw in draws if not draw["valid"]]
    per_task = {
        task["key"]: {a: task_mean(a, task, draws_by) for a in arms}
        for task in tasks
    }
    pooled = {a: sum(per_task[key][a] for key in per_task) / len(per_task) for a in arms}
    margin = pooled[arm] - pooled["null"]
    phantom = sum(
        1
        for draw in draws
        if str((draw.get("rubric") or {}).get("reason", "")).startswith("phantom source")
    )
    pinned = rubric.pin_model()
    foreign = 0
    for draw in draws:
        receipt_path = DRAWS / draw["arm"] / draw["draw"] / "receipt.json"
        if not receipt_path.is_file():
            foreign += 1
            continue
        receipt = json.loads(receipt_path.read_text())
        if receipt.get("model") != pinned or draw.get("model_preflight") != "ok":
            foreign += 1
    judged, judge_invalid, judge_cost, judge_reason = judge_draws(
        draws, {task["key"]: task for task in tasks}
    )
    valid_draws = sum(1 for draw in draws if draw["valid"])
    criteria = {
        "draws": not invalid,
        "margin": margin >= MARGIN,
        "floor": all(per_task[task["key"]][arm] >= FLOOR for task in tasks),
        "phantom": phantom == 0,
        "foreign": foreign == 0,
        "judge": judge_invalid == 0 and judged == valid_draws and not judge_reason,
    }
    missed = [name for name, passed in criteria.items() if not passed]
    verdict = "SHIP" if not missed else "NO-SHIP"
    result = {
        "verdict": verdict,
        "locked": arm,
        "control": "null",
        "draws": len(draws),
        "valid_draws": valid_draws,
        "draws_per_task": DRAWS_PER_TASK,
        "per_task": per_task,
        "pooled": pooled,
        "margin": margin,
        "margin_required": MARGIN,
        "floor": FLOOR,
        "phantom": phantom,
        "foreign": foreign,
        "invalid": [
            {
                "arm": draw["arm"],
                "task": draw["task"],
                "draw": draw["draw"],
                "break_class": draw.get("break_class"),
                "reason": draw.get("contract_reason"),
            }
            for draw in invalid
        ],
        "judge": {
            "validity": json.loads(JUDGE_VALIDITY.read_text()) if JUDGE_VALIDITY.is_file() else None,
            "judged": judged,
            "invalid": judge_invalid,
            "cost_usd": judge_cost,
            "reason": judge_reason,
        },
        "criteria": criteria,
        "missed": missed,
        "order": order,
        "reruns": reruns,
        "set": {
            "plaintext_set_digest": record["held_out"]["plaintext_set_digest"],
            "ciphertext_sha256": record["held_out"]["ciphertext_sha256"],
            "tasks": record["held_out"]["tasks"],
        },
        "draws_detail": [
            {
                "arm": draw["arm"],
                "task": draw["task"],
                "draw": draw["draw"],
                "valid": draw["valid"],
                "score": draw["score"],
                "break_class": draw.get("break_class"),
                "contract_ok": draw["contract_ok"],
                "contract_reason": draw["contract_reason"],
                "judge": (valid_judge(DRAWS / draw["arm"] / draw["draw"] / "judge.json") or {}).get("score"),
            }
            for draw in draws
        ],
    }
    (HERE / "verdict.json").write_text(json.dumps(result, indent=2) + "\n")
    print(
        f"pooled: {arm} {pooled[arm]:.2f}, null {pooled['null']:.2f}; "
        f"margin {margin:.2f} (required {MARGIN})"
    )
    print(
        f"draws: {valid_draws}/{len(draws)} valid; judged {judged}/{valid_draws}; "
        f"phantom {phantom}; foreign {foreign}; judge cost ${judge_cost:.2f}"
    )
    print(
        "criteria: " + ", ".join(f"{name}={'pass' if value else 'fail'}" for name, value in criteria.items())
    )
    print(f"verdict: {verdict}" + (f" (missed: {', '.join(missed)})" if missed else ""))
    return 0 if verdict == "SHIP" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
