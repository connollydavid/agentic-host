#!/usr/bin/env python3
"""The plan/0113 smoke gate: one draw per arm through the full pipeline.

The smoke runs before any scored selection draw. It checks the native prompt
(no wrapper postscript), the adapter dispatch, the measured search provider,
the fetch log, the receipt, the rubric and the isolation probe. The null must
produce the contract; every other arm must produce the contract or a recorded
exclusion. A void is a failure.

Usage:
  python3 run.py                 # all arms, serial
  python3 run.py --only null     # one arm
  python3 run.py --skip-probe    # skip the pinned-binary isolation probe
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
sys.path.insert(0, str(HARNESS / "selection"))
sys.path.insert(0, str(HARNESS / "tasks"))

import run  # noqa: E402
import schema  # noqa: E402

TASK = HERE / "task.json"
DRAWS = HERE / "draws"
SCRATCH = Path("/tmp/opencode/plan0113/smoke")
PROBE = HARNESS / "probe.py"
ARMS = ["null", "hffmnnj", "kanatami", "weizhena", "samber"]
RECORD = HERE / "smoke.json"


def isolation() -> dict:
    completed = subprocess.run(
        [sys.executable, str(PROBE)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    lines = [line for line in completed.stdout.splitlines() if line.startswith("PASS") or line.startswith("probe:")]
    return {
        "exit_code": completed.returncode,
        "passed": completed.returncode == 0,
        "output": lines,
        "stderr": completed.stderr[-1000:] if completed.returncode != 0 else "",
    }


def suspect_exclusion(arm: str, draw: Path) -> str | None:
    """An exclusion is a harness break when the native output already carries a source record."""
    native = draw / "native"
    if arm == "hffmnnj":
        for note in native.rglob("rn_*.md"):
            front, _ = run.note_front_body(note)
            if front.get("kind") != "finding":
                continue
            for source in front.get("sources") or []:
                if source.get("url") and source.get("quote"):
                    return "the hffmnnj native notes carry a source record; an exclusion is a harness break"
    if arm == "kanatami":
        workers = native / "workers.json"
        if workers.is_file():
            try:
                data = json.loads(workers.read_text())
            except json.JSONDecodeError:
                data = {}
            for worker in data.get("workers", []):
                for result in worker.get("results", []):
                    if result.get("url") and (result.get("full_text") or result.get("snippet")):
                        return "the kanatami workers carry a source record; an exclusion is a harness break"
    return None


def draw_gate(arm: str, summary: dict) -> list[str]:
    findings: list[str] = []
    prompt = (DRAWS / arm / summary["draw"] / "prompt.txt").read_text()
    if arm != "null" and "Produce these files" in prompt:
        findings.append("the wrapper postscript is still in the native prompt")
    if arm != "null" and run.ARM_LINES[arm].split(".")[0] not in prompt:
        findings.append("the native arm line is absent from the prompt")
    if summary["adapter"] != arm:
        findings.append(f"the receipt names adapter {summary['adapter']!r}")
    if summary["adapter_result"] not in ("valid", "excluded"):
        findings.append(f"adapter result is {summary['adapter_result']!r}")
    if summary["search_provider"] not in (run.SEARCH_PROVIDER, "none"):
        findings.append(f"foreign search provider {summary['search_provider']!r}")
    if summary["search_engine_fetches"]:
        findings.append("search-engine fetch: " + ", ".join(summary["search_engine_fetches"][:2]))
    if summary["adapter_result"] == "valid":
        draw = DRAWS / arm / summary["draw"]
        if not summary["valid"]:
            findings.append("the adapter said valid but the draw is not valid")
        if not (draw / "receipt.json").is_file():
            findings.append("a valid draw has no receipt")
        else:
            receipt = json.loads((draw / "receipt.json").read_text())
            if receipt.get("status") != "live":
                findings.append(f"receipt status is {receipt.get('status')!r}")
            if receipt.get("budget", {}).get("caps") != run.contract.CAPS:
                findings.append("receipt caps do not match the frozen budget")
        if not (draw / "fetch-log.jsonl").is_file():
            findings.append("a valid draw has no fetch log")
        if summary["rubric"].get("status") != "scored":
            findings.append("a valid draw has no scored rubric")
    if summary["adapter_result"] == "excluded":
        draw = DRAWS / arm / summary["draw"]
        if not (draw / "exclusion.json").is_file():
            findings.append("an excluded draw has no exclusion.json")
        if not summary["contract_reason"]:
            findings.append("an exclusion carries no reason")
        suspect = suspect_exclusion(arm, draw)
        if suspect:
            findings.append(suspect)
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append", choices=ARMS)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--reuse", action="store_true", help="re-process the recorded draw, no model run")
    parser.add_argument("--skip-probe", action="store_true")
    parser.add_argument("--record-only", action="store_true")
    args = parser.parse_args(argv)
    arms = args.only or ARMS
    task = json.loads(TASK.read_text())
    summary = schema.validate_set({"set": "selection", "tasks": [task]})
    print(f"smoke task: {task['key']} ({summary['tasks']} task, digest {summary['set_digest'][:12]}...)")

    probe = {"skipped": True}
    if not args.skip_probe:
        probe = isolation()
        print(f"isolation probe: {'passed' if probe['passed'] else 'FAILED'}")
        if not probe["passed"]:
            print(probe["output"][-3:], probe["stderr"], file=sys.stderr)

    run.DRAWS = DRAWS
    run.SCRATCH = SCRATCH
    results: dict[str, dict] = {}
    findings: dict[str, list[str]] = {}
    for arm in arms:
        if args.record_only:
            path = DRAWS / arm / f"{task['key'].split('/', 1)[1]}-smoke" / "score.json"
            if not path.is_file():
                findings[arm] = ["no smoke draw"]
                continue
            result = json.loads(path.read_text())
            results[arm] = result
            findings[arm] = draw_gate(arm, result)
            print(
                f"  {arm:9s} adapter={result['adapter_result']:8s} valid={result['valid']} "
                f"provider={result['search_provider']} score={result['score']}/{result['rubric'].get('max', '-')} "
                f"wall={result['wall_seconds']}s"
                + (f"  findings: {', '.join(findings[arm])}" if findings[arm] else ""),
                flush=True,
            )
            continue
        print(f"smoke: {arm}", flush=True)
        result = run.safe_run_draw(arm, task, force=args.force, suffix="-smoke", reuse=args.reuse)
        results[arm] = result
        findings[arm] = draw_gate(arm, result)
        print(
            f"  {arm:9s} adapter={result['adapter_result']:8s} valid={result['valid']} "
            f"provider={result['search_provider']} score={result['score']}/{result['rubric'].get('max', '-')} "
            f"wall={result['wall_seconds']}s"
            + (f"  findings: {', '.join(findings[arm])}" if findings[arm] else ""),
            flush=True,
        )

    passed = probe.get("passed", True) and all(not findings[arm] for arm in arms)
    if "null" in results and results["null"]["adapter_result"] != "valid":
        passed = False
        findings.setdefault("null", []).append("the null control did not produce the contract")
    record = {
        "recorded": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "task": task,
        "arms": arms,
        "isolation": probe,
        "draws": results,
        "findings": findings,
        "passed": passed,
    }
    RECORD.write_text(json.dumps(record, indent=2) + "\n")
    print(f"smoke: {'PASS' if passed else 'FAIL'} ({RECORD})")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
