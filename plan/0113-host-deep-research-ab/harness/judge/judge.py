#!/usr/bin/env python3
"""The plan/0113 blind judge: completeness and creativity on the report.

The judge is Opus 5.5 through the host's `claude` CLI (`--model opus`, which
resolves to `claude-opus-5-5`). It sees the question, the must-cover list, the
report and the source ledger, never the arm. Its scores are 0-4 for
completeness and 0-4 for creativity; the sum is the judge score (0-8).

The judge is optional until its validity gate passes: a clean report must
outrank a broken one, and a malformed reply must be rejected. When the gate
fails, `judge.json` records `valid: false` and the mechanical rubric alone
scores.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
ROUTE = "claude-agent/opus"
EXPECTED_MODEL = "claude-opus-5-5"
CLAUDE = "claude"

PROMPT = """You are a blind judge for a deep-research A/B. You score the report, not the arm.

Score completeness from 0 to 4: does the report answer the question and name every must-cover entity, with support from the source ledger? 0 means it misses the question or most entities; 4 means it answers fully and every entity is supported.

Score creativity from 0 to 4: does the report synthesize across sources, compare alternatives, and add an insight a list of facts would not? 0 means a generic or copied answer; 4 means a genuinely useful synthesis.

Do not reward length, token count or confident tone. Do not infer the arm. Return ONLY a JSON object:
{{"completeness": <0-4>, "creativity": <0-4>, "rationale": "<one paragraph>"}}

Question:
{question}

Must-cover entities:
{entities}

Report:
{report}

Source ledger:
{ledger}
"""


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("the judge reply carries no JSON object")
    value = json.loads(text[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("the judge reply is not a JSON object")
    return value


def validate_reply(value: dict) -> dict:
    for key in ("completeness", "creativity"):
        score = value.get(key)
        if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 4:
            raise ValueError(f"judge {key} is not an integer 0-4: {score!r}")
    rationale = value.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        raise ValueError("judge rationale is empty")
    return {
        "completeness": value["completeness"],
        "creativity": value["creativity"],
        "score": value["completeness"] + value["creativity"],
        "rationale": rationale.strip(),
    }


def run_claude(prompt: str) -> tuple[dict, dict]:
    last: Exception | None = None
    for attempt in range(3):
        try:
            completed = subprocess.run(
                [CLAUDE, "-p", "--model", "opus", "--output-format", "json", prompt],
                capture_output=True,
                text=True,
                timeout=180,
            )
            if completed.returncode != 0:
                raise ValueError(f"claude exited {completed.returncode}: {completed.stderr[-500:]}")
            envelope = json.loads(completed.stdout)
            if envelope.get("is_error"):
                raise ValueError(f"claude returned an error: {envelope.get('result')}")
            return envelope, envelope.get("modelUsage") or {}
        except (ValueError, json.JSONDecodeError, subprocess.SubprocessError) as error:
            last = error
            if attempt < 2:
                time.sleep(2)
    raise ValueError(f"claude failed after 3 attempts: {last}")


def judge(question: str, entities: list[str], report: str, ledger: dict) -> dict:
    prompt = PROMPT.format(
        question=question,
        entities="\n".join(f"- {entity}" for entity in entities) or "- (none; score the answer)",
        report=report,
        ledger=json.dumps(ledger, indent=2, ensure_ascii=False),
    )
    try:
        envelope, usage = run_claude(prompt)
        reply = extract_json(envelope.get("result") or "")
        scored = validate_reply(reply)
        model = next(iter(usage), EXPECTED_MODEL)
        if model != EXPECTED_MODEL:
            raise ValueError(f"judge model {model!r} is not {EXPECTED_MODEL!r}")
        return {
            "valid": True,
            "route": ROUTE,
            "model": model,
            "prompt_sha256": sha256_text(prompt),
            "reply_sha256": sha256_text(json.dumps(reply, sort_keys=True)),
            "cost_usd": envelope.get("total_cost_usd"),
            **scored,
        }
    except (ValueError, json.JSONDecodeError, subprocess.SubprocessError) as error:
        return {
            "valid": False,
            "route": ROUTE,
            "reason": str(error),
            "prompt_sha256": sha256_text(prompt),
        }


def load_draw(draw: Path, task_path: Path, question: str | None) -> tuple[dict, str, list[str], str, dict]:
    task = json.loads(task_path.read_text())
    report = (draw / "report.md").read_text()
    ledger = json.loads((draw / "sources.json").read_text())
    entities = [item["entity"] for item in task.get("must_cover", [])]
    if not question:
        question = task.get("question") or task["key"]
    return task, question, entities, report, ledger


def validity() -> int:
    samples = HERE / "validity"
    checks: dict[str, dict] = {}
    passed = True
    for name in ("clean", "broken"):
        task_path = samples / f"{name}.task.json"
        task = json.loads(task_path.read_text())
        report = (samples / f"{name}.report.md").read_text()
        ledger = json.loads((samples / f"{name}.sources.json").read_text())
        result = judge(task["question"], [item["entity"] for item in task["must_cover"]], report, ledger)
        checks[name] = result
        print(f"{'PASS' if result['valid'] else 'FAIL'} validity {name}: {json.dumps(result, ensure_ascii=False)}")
        passed = passed and result["valid"]
    if checks["clean"].get("valid") and checks["broken"].get("valid"):
        passed = passed and checks["clean"]["score"] > checks["broken"]["score"]
    else:
        passed = False
    try:
        validate_reply({"completeness": 5, "creativity": "high", "rationale": ""})
        malformed = False
    except ValueError:
        malformed = True
    print(f"{'PASS' if malformed else 'FAIL'} validity malformed reply is rejected")
    passed = passed and malformed
    record = {
        "recorded": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "route": ROUTE,
        "expected_model": EXPECTED_MODEL,
        "clean": checks["clean"],
        "broken": checks["broken"],
        "malformed_rejected": malformed,
        "passed": passed,
    }
    (HERE / "validity.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"judge validity: {'passed' if passed else 'FAILED'}")
    return 0 if passed else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draw")
    parser.add_argument("--task")
    parser.add_argument("--question")
    parser.add_argument("--out")
    parser.add_argument("--validity", action="store_true")
    args = parser.parse_args(argv)
    if args.validity:
        return validity()
    if not args.draw or not args.task:
        parser.error("--draw and --task are required unless --validity")
    draw = Path(args.draw)
    task_path = Path(args.task)
    task, question, entities, report, ledger = load_draw(draw, task_path, args.question)
    result = judge(question, entities, report, ledger)
    result["task"] = task["key"]
    out = Path(args.out) if args.out else draw / "judge.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
