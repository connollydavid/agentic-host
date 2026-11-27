#!/usr/bin/env python3
"""Score every selection draw with the blind judge.

Run after the draws and before `round.py`. The task question for a known-answer
task comes from the frozen selection set through `run.task_question`; the house
question is in the task file. The judge writes `judge.json` beside each draw;
`round.py` reads it. A draw with no report or ledger is skipped and contributes
0.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
sys.path.insert(0, str(HARNESS / "selection"))
sys.path.insert(0, str(HARNESS / "tasks"))

import judge  # noqa: E402
import run  # noqa: E402


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draws", default=str(HARNESS / "selection" / "draws-redo"))
    args = parser.parse_args(argv)
    root = Path(args.draws)
    tasks = {task["key"]: task for task in json.loads(run.TASKS.read_text())["tasks"]}
    scored = 0
    skipped = 0
    cost = 0.0
    for path in sorted(root.glob("*/*/score.json")):
        draw = path.parent
        summary = json.loads(path.read_text())
        task = tasks.get(summary["task"])
        if task is None:
            print(f"skip {draw}: task {summary['task']} is not in the selection set", file=sys.stderr)
            skipped += 1
            continue
        if not (draw / "report.md").is_file() or not (draw / "sources.json").is_file():
            print(f"skip {draw}: no report or ledger", file=sys.stderr)
            skipped += 1
            continue
        question = run.task_question(task)
        entities = [item["entity"] for item in task.get("must_cover", [])]
        report = (draw / "report.md").read_text()
        ledger = json.loads((draw / "sources.json").read_text())
        result = judge.judge(question, entities, report, ledger)
        result["task"] = summary["task"]
        (draw / "judge.json").write_text(json.dumps(result, indent=2) + "\n")
        cost += float(result.get("cost_usd") or 0)
        scored += 1
        print(
            f"{summary['arm']:9s} {summary['task'].split('/', 1)[-1]:28s} "
            f"judge={'valid' if result['valid'] else 'void ':5s} "
            f"score={result.get('score', 0)}/8 cost=${result.get('cost_usd', 0):.3f}"
            + (f"  ({result.get('reason')})" if not result["valid"] else "")
        )
    print(f"judge: {scored} draw(s) scored, {skipped} skipped, ${cost:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
