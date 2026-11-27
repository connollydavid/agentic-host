#!/usr/bin/env python3
"""Aggregate the plan/0113 selection draws and apply the frozen lock.

The round is 30 draws: five arms (null plus four candidates) on six selection
tasks. A draw's score is the rubric's score when the contract is valid; a void
draw scores zero. The lock is the highest suite-fit among the candidate arms
within 1.0 point of the best candidate's pooled score, then fewer tokens, then
name order.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
TASKS = HARNESS / "tasks" / "selection.json"
DRAWS = HERE / "draws"
ARMS = ["null", "weizhena", "hffmnnj", "kanatami", "samber"]
CANDIDATES = ["weizhena", "hffmnnj", "kanatami", "samber"]
BAND = 1.0
MAX = 16.0


def main() -> int:
    document = json.loads(TASKS.read_text())
    keys = [task["key"] for task in document["tasks"]]
    draws: list[dict] = []
    missing: list[str] = []
    for arm in ARMS:
        for key in keys:
            path = DRAWS / arm / key.split("/", 1)[1] / "score.json"
            if not path.is_file():
                missing.append(f"{arm}/{key.split('/', 1)[1]}")
                continue
            draws.append(json.loads(path.read_text()))
    if missing:
        print(f"selection: {len(missing)} draw(s) missing: {', '.join(missing)}", file=sys.stderr)
        return 1

    by_arm: dict[str, list[dict]] = {arm: [] for arm in ARMS}
    for draw in draws:
        by_arm[draw["arm"]].append(draw)
    pooled = {arm: sum(draw["score"] for draw in by_arm[arm]) / len(keys) for arm in ARMS}
    tokens = {
        arm: sum(draw["prompt_tokens"] + draw["completion_tokens"] for draw in by_arm[arm])
        for arm in ARMS
    }
    valid = {arm: sum(1 for draw in by_arm[arm] if draw["valid"]) for arm in ARMS}

    best = max(CANDIDATES, key=lambda arm: pooled[arm])
    band_arms = [arm for arm in CANDIDATES if pooled[best] - pooled[arm] <= BAND + 1e-9]
    suite: dict[str, dict] = {}
    for arm in ARMS:
        if arm == "null":
            suite[arm] = {
                "model": True,
                "ledger": all(draw["contract_ok"] for draw in by_arm[arm]),
                "snapshots": all(draw["contract_ok"] for draw in by_arm[arm]),
                "artifacts": True,
                "one_command": True,
                "vendored": True,
            }
        else:
            suite[arm] = {
                "model": True,
                "ledger": all(draw["contract_ok"] for draw in by_arm[arm]),
                "snapshots": all(draw["contract_ok"] for draw in by_arm[arm]),
                "artifacts": True,
                "one_command": True,
                "vendored": True,
            }
        suite[arm]["score"] = sum(1 for value in suite[arm].values() if value is True)

    ranked = sorted(band_arms, key=lambda arm: (-suite[arm]["score"], tokens[arm], arm))
    locked = ranked[0]

    result = {
        "round": "selection",
        "draws": len(draws),
        "tasks": len(keys),
        "arms": ARMS,
        "max": MAX,
        "band": BAND,
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
                "valid": draw["valid"],
                "score": draw["score"],
                "max": draw["rubric"].get("max"),
                "contract_ok": draw["contract_ok"],
                "contract_reason": draw["contract_reason"],
                "wall_seconds": draw["wall_seconds"],
            }
            for draw in draws
        ],
    }
    (HERE / "round.json").write_text(json.dumps(result, indent=2) + "\n")

    print(f"{'arm':10s} {'pooled':>7s} {'valid':>5s} {'tokens':>9s} {'suite':>5s}")
    for arm in ARMS:
        print(f"{arm:10s} {pooled[arm]:7.2f} {valid[arm]:5d} {tokens[arm]:9d} {suite[arm]['score']:5d}")
    print(f"best candidate: {best} ({pooled[best]:.2f}); band arms: {', '.join(band_arms)}")
    print(f"locked: {locked} (suite {suite[locked]['score']}, tokens {tokens[locked]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
