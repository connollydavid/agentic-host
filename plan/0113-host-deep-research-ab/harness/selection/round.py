#!/usr/bin/env python3
"""Aggregate the plan/0113 redo selection and apply the lock.

The pooled selection score is the mechanical rubric (0-16) plus the blind judge
(0-8), a 24-point maximum. The band is 1.5 points. A candidate locks only when
it has at least four valid draws, all six draws judged, and a pooled score
above the null control; the tie-break is the six-row suite-fit evidence table,
then the judge score, then name order. The token count is recorded, never a
tie-break. An unresolved harness break refuses the round; a fully invalid
round records NO-SHIP instead of a lock.
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
SUITE = HERE / "suite-fit.json"
JUDGE_VALIDITY = HARNESS / "judge" / "validity.json"
ARMS = ["null", "weizhena", "hffmnnj", "kanatami", "samber"]
CANDIDATES = ["weizhena", "hffmnnj", "kanatami", "samber"]
BAND = 1.5
MECHANICAL_MAX = 16.0
MAX = 24.0
VALID_FLOOR = 4
JUDGED_FLOOR = 6
JUDGE_MODEL = "claude-opus-5-5"
JUDGE_ROUTE = "claude-agent/opus"
CRITERIA = ("model", "ledger", "snapshots", "artifacts", "one_command", "vendored")


def judge_score(draw: Path, record: dict) -> tuple[int, bool]:
    if not record.get("valid"):
        return 0, False
    path = draw / "judge.json"
    if not path.is_file():
        return 0, False
    if not JUDGE_VALIDITY.is_file() or not json.loads(JUDGE_VALIDITY.read_text()).get("passed"):
        return 0, False
    try:
        value = json.loads(path.read_text())
    except json.JSONDecodeError:
        return 0, False
    if not value.get("valid"):
        return 0, False
    if value.get("model") != JUDGE_MODEL or value.get("route") != JUDGE_ROUTE:
        return 0, False
    score = value.get("score")
    if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 8:
        return 0, False
    return score, True


def load_suite() -> dict:
    if not SUITE.is_file():
        raise SystemExit(f"selection: the six-row suite-fit table is missing at {SUITE}")
    table = json.loads(SUITE.read_text())
    suite: dict[str, dict] = {}
    for arm in ARMS:
        rows = (table.get("arms") or {}).get(arm) or {}
        result = {criterion: bool((rows.get(criterion) or {}).get("verdict")) for criterion in CRITERIA}
        result["score"] = sum(1 for value in result.values() if value is True)
        suite[arm] = result
    return suite


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draws", default=str(DRAWS))
    parser.add_argument("--out", default=str(HERE / "round-redo.json"))
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
            record["_judge"], record["_judge_valid"] = judge_score(draw, record)
            draws.append(record)
    if missing:
        print(f"selection: {len(missing)} draw(s) missing: {', '.join(missing)}", file=sys.stderr)
        return 1

    unresolved = [
        f"{draw['arm']}/{draw['task'].split('/', 1)[-1]}"
        for draw in draws
        if draw.get("break_class") == "harness" and not draw.get("valid")
    ]
    if unresolved:
        print(
            "selection: unresolved harness break(s): " + ", ".join(unresolved)
            + "; re-run them under the same task and config before the lock",
            file=sys.stderr,
        )
        return 1

    suite = load_suite()
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

    eligible = [
        arm
        for arm in CANDIDATES
        if valid[arm] >= VALID_FLOOR and judged[arm] >= JUDGED_FLOOR and pooled[arm] > pooled["null"]
    ]
    base = {
        "round": "selection-redo",
        "draws": len(draws),
        "tasks": len(keys),
        "arms": ARMS,
        "mechanical_max": MECHANICAL_MAX,
        "judge_max": 8.0,
        "max": MAX,
        "band": BAND,
        "valid_floor": VALID_FLOOR,
        "judged_floor": JUDGED_FLOOR,
        "mechanical": mechanical,
        "judge": judge,
        "judged": judged,
        "pooled": pooled,
        "valid": valid,
        "tokens": tokens,
        "eligible": eligible,
        "suite_fit": suite,
        "draws_detail": [
            {
                "arm": draw["arm"],
                "task": draw["task"],
                "draw": draw.get("draw"),
                "valid": draw.get("valid"),
                "excluded": draw.get("excluded", False),
                "adapter": draw.get("adapter_result"),
                "break_class": draw.get("break_class"),
                "rerun_of": draw.get("rerun_of"),
                "mechanical": draw["score"],
                "judge": draw["_judge"],
                "judge_valid": draw["_judge_valid"],
                "pooled": draw["score"] + draw["_judge"],
                "max": (draw.get("rubric") or {}).get("max"),
                "contract_ok": draw.get("contract_ok"),
                "contract_reason": draw.get("contract_reason"),
                "wall_seconds": draw.get("wall_seconds"),
            }
            for draw in draws
        ],
    }
    if not eligible:
        base["decision"] = "NO-SHIP"
        base["locked"] = None
        base["band_arms"] = []
        base["best_candidate"] = None
        Path(args.out).write_text(json.dumps(base, indent=2) + "\n")
        print("selection: NO-SHIP; no candidate clears the valid floor, the judge floor and the null")
        return 0

    best = max(eligible, key=lambda arm: pooled[arm])
    band_arms = [arm for arm in eligible if pooled[best] - pooled[arm] <= BAND + 1e-9]
    ranked = sorted(band_arms, key=lambda arm: (-suite[arm]["score"], -judge[arm], arm))
    locked = ranked[0]
    base["decision"] = "LOCKED"
    base["best_candidate"] = best
    base["band_arms"] = band_arms
    base["locked"] = locked
    Path(args.out).write_text(json.dumps(base, indent=2) + "\n")

    print(f"{'arm':10s} {'mech':>6s} {'judge':>6s} {'pooled':>7s} {'valid':>5s} {'judged':>6s} {'tokens':>9s} {'suite':>5s}")
    for arm in ARMS:
        print(
            f"{arm:10s} {mechanical[arm]:6.2f} {judge[arm]:6.2f} {pooled[arm]:7.2f} "
            f"{valid[arm]:5d} {judged[arm]:6d} {tokens[arm]:9d} {suite[arm]['score']:5d}"
        )
    print(f"eligible: {', '.join(eligible)}; best {best} ({pooled[best]:.2f}); band {', '.join(band_arms)}")
    print(f"locked: {locked} (suite {suite[locked]['score']}, judge {judge[locked]:.2f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
