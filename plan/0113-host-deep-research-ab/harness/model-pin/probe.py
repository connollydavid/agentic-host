#!/usr/bin/env python3
"""The plan/0113 model probes: the named route, and the reply ledger's model ids.

The live route check reads the router's `/model/info` record and requires the
pinned named entry and deployment. The fixtures then prove the reply check
passes a clean ledger and voids one foreign model id, one foreign provider,
an empty ledger, a drifted deployment record and a missing named entry.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREFLIGHT = HERE / "model-preflight.py"
SCRATCH = Path(os.environ.get("PLAN0113_SCRATCH", "/tmp/opencode/plan0113/probes")) / "model-pin"

PASSES: list[str] = []


class ProbeFailure(Exception):
    pass


def fail(message: str) -> None:
    raise ProbeFailure(message)


def note(message: str) -> None:
    PASSES.append(message)
    print(f"PASS {message}", flush=True)


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, timeout=120)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def reply(provider: str, model: str) -> str:
    return json.dumps({"provider": provider, "model": model}) + "\n"


def record(deployment: str, backend: str, max_input: int, max_output: int) -> str:
    return json.dumps(
        {
            "data": [
                {
                    "model_name": "qwen3.6-27b",
                    "litellm_params": {"model": backend},
                    "model_info": {
                        "id": deployment,
                        "max_input_tokens": max_input,
                        "max_output_tokens": max_output,
                    },
                }
            ]
        }
    ) + "\n"


def check_live() -> None:
    if not os.environ.get("ROPE_BEARER"):
        fail("ROPE_BEARER is unset; the live route check cannot run")
    result = run([str(PREFLIGHT)])
    if result.returncode != 0:
        fail(f"the live route check refused: {result.stderr.strip()}")
    note(result.stdout.strip())


def check_replies(path: Path, expected_ok: bool, label: str) -> None:
    result = run([str(PREFLIGHT), "--replies", str(path)])
    if expected_ok and result.returncode != 0:
        fail(f"{label}: a clean ledger was voided: {result.stderr.strip()}")
    if not expected_ok and (result.returncode == 0 or "VOID" not in result.stderr):
        fail(f"{label}: a foreign ledger passed: rc={result.returncode} {result.stderr.strip()}")
    note(f"replies: {label} {'passes' if expected_ok else 'is void'}")


def check_record(path: Path, label: str) -> None:
    result = run([str(PREFLIGHT), "--record", str(path)])
    if result.returncode == 0 or "VOID" not in result.stderr:
        fail(f"{label}: a bad route record passed: rc={result.returncode} {result.stderr.strip()}")
    note(f"route: {label} is void")


def main() -> int:
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir(parents=True, exist_ok=True)

    pin = json.loads((HERE / "model-pin.json").read_text())
    clean = reply(pin["provider"], pin["route"]) + reply(pin["provider"], pin["route"])
    foreign_model = reply(pin["provider"], pin["route"]) + reply(pin["provider"], "qwen3.8-27b")
    foreign_provider = reply(pin["provider"], pin["route"]) + reply("other.provider", pin["route"])
    write(SCRATCH / "clean.jsonl", clean)
    write(SCRATCH / "foreign-model.jsonl", foreign_model)
    write(SCRATCH / "foreign-provider.jsonl", foreign_provider)
    write(SCRATCH / "empty.jsonl", "")
    write(
        SCRATCH / "drift-record.json",
        record("2f8863340f6db4763ff3bf04b236dde977d79042b87385862a462a4d6564d2ff", "openai/qwen3.8-27b", 262144, 32768),
    )
    write(SCRATCH / "missing-record.json", json.dumps({"data": []}) + "\n")

    check_live()
    check_replies(SCRATCH / "clean.jsonl", True, "two pinned replies")
    check_replies(SCRATCH / "foreign-model.jsonl", False, "one foreign model id")
    check_replies(SCRATCH / "foreign-provider.jsonl", False, "one foreign provider")
    check_replies(SCRATCH / "empty.jsonl", False, "an empty ledger")
    check_record(SCRATCH / "drift-record.json", "the cut's old deployment record")
    check_record(SCRATCH / "missing-record.json", "a missing named entry")

    print(f"model-probe: {len(PASSES)} checks passed", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProbeFailure as error:
        print(f"FAIL {error}", file=sys.stderr, flush=True)
        raise SystemExit(1)
