#!/usr/bin/env python3
"""Aggregate the plan/0113 selection draws and apply the lock.

The pooled selection score is the mechanical rubric (0-16) plus the blind judge
(0-8), a 24-point maximum. The band is 1.5 points. Within the band the lock
goes to the highest suite-fit, then the judge score, then name order. The token
count is recorded, never a tie-break.

The first round's `round.json` is historical. The corrected round writes a new
file: `python3 round.py --draws draws-redo --out round-redo.json`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
TASKS = HARNESS / "tasks" / "selection.json"
DRAWS = HERE / "draws"
ARMS = ["null", "weizhena", "hffmnnj", "kanatami", "samber"]
CANDIDATES = ["weizhena", "hffmnnj", "kanatami", "samber"]
BAND = 1.5
MECHANICAL_MAX = 16.0
MAX = 24.0


def judge_score(path: Path) -> tuple[int, bool]:
    record = path / "judge.json"
    if not record.is_file():
        return 0, False
    try:
        value = json.loads(record.read_text())
    except json.JSONDecodeError:
        return 0, False
    if not value.get("valid"):
        return 0, False
    score = value.get("score")
    if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 8:
        return 0, False
    return score, True


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draws", default=str(DRAWS))
    parser.add_argument("--out", default=str(HERE / "round.json"))
    args = parser.parse_args(argv)
    draws_root = Path(args.draws)
    document = json.loads(TASKS.read_text())
    keys = [task["key"] for task in document["tasks"]]
    draws: list[dict] = []
    missing: list[str] = []
    for arm in ARMS:
        for key in keys:
            draw = draws_root / arm / key.split("/", 1)[1]
            path = draw / "score.json"
            if not path.is_file():
                missing.append(f"{arm}/{key.split('/', 1)[1]}")
                continue
            record = json.loads(path.read_text())
            record["_judge"], record["_judge_valid"] = judge_score(draw)
            draws.append(record)
    if missing:
        print(f"selection: {len(missing)} draw(s) missing: {', '.join(missing)}", file=sys.stderr)
        return 1

    by_arm: dict[str, list[dict]] = {arm: [] for arm in ARMS}
    for draw in draws:
        by_arm[draw["arm"]].append(draw)
    mechanical = {arm: sum(draw["score"] for draw in by_arm[arm]) / len(keys) for arm in ARMS}
    judge = {arm: sum(draw["_judge"] for draw in by_arm[arm]) / len(keys) for arm in ARMS}
    pooled = {arm: mechanical[arm] + judge[arm] for arm in ARMS}
    tokens = {
        arm: sum(draw["prompt_tokens"] + draw["completion_tokens"] for draw in by_arm[arm])
        for arm in ARMS
    }
    valid = {arm: sum(1 for draw in by_arm[arm] if draw["valid"]) for arm in ARMS}
    judged = {arm: sum(1 for draw in by_arm[arm] if draw["_judge_valid"]) for arm in ARMS}

    best = max(CANDIDATES, key=lambda arm: pooled[arm])
    band_arms = [arm for arm in CANDIDATES if pooled[best] - pooled[arm] <= BAND + 1e-9]
    suite: dict[str, dict] = {}
    for arm in ARMS:
        suite[arm] = {
            "model": True,
            "ledger": all(draw["contract_ok"] for draw in by_arm[arm]),
            "snapshots": all(draw["contract_ok"] for draw in by_arm[arm]),
            "artifacts": True,
            "one_command": True,
            "vendored": True,
        }
        suite[arm]["score"] = sum(1 for value in suite[arm].values() if value is True)

    ranked = sorted(band_arms, key=lambda arm: (-suite[arm]["score"], -judge[arm], arm))
    locked = ranked[0]

    result = {
        "round": "selection-redo",
        "draws": len(draws),
        "tasks": len(keys),
        "arms": ARMS,
        "mechanical_max": MECHANICAL_MAX,
        "judge_max": 8.0,
        "max": MAX,
        "band": BAND,
        "mechanical": mechanical,
        "judge": judge,
        "judged": judged,
        "pooled": pooled,
        "valid": valid,
        "tokens": tokens,
        "best_candidate": best,
        "band_arms": band_arms,
        "suite_fit": suite,
        "locked": locked,
        "draws_detail": [
            {
                "arm": draw["arm"],
                "task": draw["task"],
                "draw": draw.get("draw"),
                "valid": draw["valid"],
                "excluded": draw.get("excluded", False),
                "adapter": draw.get("adapter_result"),
                "mechanical": draw["score"],
                "judge": draw["_judge"],
                "judge_valid": draw["_judge_valid"],
                "pooled": draw["score"] + draw["_judge"],
                "max": draw["rubric"].get("max"),
                "contract_ok": draw["contract_ok"],
                "contract_reason": draw["contract_reason"],
                "wall_seconds": draw["wall_seconds"],
            }
            for draw in draws
        ],
    }
    Path(args.out).write_text(json.dumps(result, indent=2) + "\n")

    print(f"{'arm':10s} {'mech':>6s} {'judge':>6s} {'pooled':>7s} {'valid':>5s} {'tokens':>9s} {'suite':>5s}")
    for arm in ARMS:
        print(
            f"{arm:10s} {mechanical[arm]:6.2f} {judge[arm]:6.2f} {pooled[arm]:7.2f} "
            f"{valid[arm]:5d} {tokens[arm]:9d} {suite[arm]['score']:5d}"
        )
    print(f"best candidate: {best} ({pooled[best]:.2f}); band arms: {', '.join(band_arms)}")
    print(f"locked: {locked} (suite {suite[locked]['score']}, judge {judge[locked]:.2f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
