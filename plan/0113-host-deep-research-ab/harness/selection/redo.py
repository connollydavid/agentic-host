#!/usr/bin/env python3
"""Run the plan/0113 redo after the smoke gate: 30 draws, judge, lock.

The wrapper refuses to start unless the latest smoke record is a full PASS for
all five arms with the isolation probe. It runs the interleaved two-way draw
round, checks that every arm/task draw is present, judges the valid draws, and
applies `round.py`'s lock. A missing draw stops before the judge; a judge or
lock refusal is printed with its remedy.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
SMOKE = HARNESS / "smoke" / "smoke.json"
TASKS = HARNESS / "tasks" / "selection.json"
ARMS = ["null", "weizhena", "hffmnnj", "kanatami", "samber"]


def fail(message: str) -> None:
    raise SystemExit(f"redo: {message}")


def smoke_gate(path: Path) -> dict:
    if not path.is_file():
        fail(f"the smoke record is absent at {path}")
    record = json.loads(path.read_text())
    if not record.get("passed"):
        fail("the latest smoke record is not a PASS; fix it before a scored draw")
    if set(record.get("arms") or []) != set(ARMS):
        fail(f"the smoke record covers {record.get('arms')}, not all five arms")
    isolation = record.get("isolation") or {}
    if not isolation.get("passed"):
        fail("the smoke record has no passing isolation probe")
    task = (record.get("task") or {}).get("key")
    if task != "smoke/house-capital":
        fail(f"the smoke record names {task!r}, not the dedicated smoke task")
    return record


def score_paths(draws: Path) -> list[Path]:
    return sorted(draws.glob("*/*/score.json"))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", default=str(SMOKE))
    parser.add_argument("--draws", default=str(HERE / "draws-redo"))
    parser.add_argument("--parallel", type=int, default=2)
    parser.add_argument("--out", default=str(HERE / "round-redo.json"))
    parser.add_argument("--skip-draws", action="store_true", help="judge and lock recorded draws")
    args = parser.parse_args(argv)
    record = smoke_gate(Path(args.smoke))
    print(
        f"redo: smoke gate passed ({record.get('recorded')}), "
        f"isolation {len((record.get('isolation') or {}).get('output') or [])} checks",
        flush=True,
    )
    draws = Path(args.draws)
    if not args.skip_draws:
        command = [
            sys.executable,
            str(HERE / "run.py"),
            "--draws",
            str(draws),
            "--parallel",
            str(args.parallel),
            "--order",
            "interleaved",
        ]
        print("redo: " + " ".join(command), flush=True)
        completed = subprocess.run(command)
        if completed.returncode != 0:
            fail(f"the draw round exited {completed.returncode}")
    tasks = json.loads(TASKS.read_text())["tasks"]
    expected = {(arm, task["key"].split("/", 1)[1]) for arm in ARMS for task in tasks}
    present = {
        (path.parent.parent.name, path.parent.name)
        for path in score_paths(draws)
    }
    missing = sorted(expected - present)
    if missing:
        fail(
            f"{len(missing)} draw(s) missing: "
            + ", ".join(f"{arm}/{name}" for arm, name in missing[:12])
        )
    print(f"redo: {len(present)} of {len(expected)} draws recorded", flush=True)
    completed = subprocess.run(
        [sys.executable, str(HARNESS / "judge" / "judge_all.py"), "--draws", str(draws)]
    )
    if completed.returncode != 0:
        fail(f"the judge exited {completed.returncode}")
    completed = subprocess.run(
        [sys.executable, str(HERE / "round.py"), "--draws", str(draws), "--out", args.out]
    )
    if completed.returncode != 0:
        fail(f"the lock exited {completed.returncode}; the round is not locked")
    record = json.loads(Path(args.out).read_text())
    print(f"redo: decision {record.get('decision')}; locked {record.get('locked')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
