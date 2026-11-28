#!/usr/bin/env python3
"""The plan/0113 contract dry runs: one task through every arm's adapter.

Each arm's native output shape has a fixture under `fixtures/<arm>/`. The
adapter either maps it to a contract-valid report, source ledger and receipt,
or records why the arm's output cannot satisfy the ledger. The three controls
then show the validator is not a rubber stamp: an empty quote, a foreign model
receipt and a report that does not cite its ledger all fail.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from adapters import hffmnnj, kanatami, null, samber, weizhena  # noqa: E402
from contract import (  # noqa: E402
    CAPS,
    ContractError,
    load_task,
    sha256_file,
    validate_exclusion,
    validate_output,
    validate_receipt,
    validate_report,
    validate_sources,
)

HARNESS = HERE.parent
SCRATCH = Path("/tmp/opencode/plan0113/probes/contract")
TASK = HERE / "tasks" / "dry-run.json"
PIN_ENV = HARNESS / "pin.env"
MODEL_PIN = HARNESS / "model-pin" / "model-pin.json"

ADAPTERS = {
    "null": null,
    "hffmnnj": hffmnnj,
    "kanatami": kanatami,
    "weizhena": weizhena,
    "samber": samber,
}

PASSES: list[str] = []


class DryRunFailure(Exception):
    pass


def fail(message: str) -> None:
    raise DryRunFailure(message)


def note(message: str) -> None:
    PASSES.append(message)
    print(f"PASS {message}", flush=True)


def read_pin_env(path: Path) -> dict[str, str]:
    values = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value.strip().strip('"')
    return values


def meta_for(arm: str, arm_config: Path) -> dict:
    pin = read_pin_env(PIN_ENV)
    model = json.loads(MODEL_PIN.read_text())
    digests = {
        "task": sha256_file(TASK),
        "harness_pin": sha256_file(PIN_ENV),
        "model_pin": sha256_file(MODEL_PIN),
        "arm_config": sha256_file(arm_config),
    }
    if arm == "null":
        digests["prompt"] = sha256_file(HERE / "prompts" / "null.md")
    config = json.loads(arm_config.read_text())
    meta = {
        "harness": {
            "tag": pin["OPENCODE_TAG"],
            "binary_sha256": pin["OPENCODE_BINARY_SHA256"],
        },
        "model": {
            "provider": model["provider"],
            "route": model["route"],
            "deployment_id": model["deployment_id"],
            "backend": model["backend"],
            "max_input_tokens": model["max_input_tokens"],
            "max_output_tokens": model["max_output_tokens"],
        },
        "search_provider": config["search_provider"],
        "native_search": [],
        "caps": CAPS,
        "digests": digests,
    }
    if arm == "samber":
        meta["fetches"] = ["https://example.com/contract"]
    return meta


def expect_error(label: str, call) -> None:
    try:
        call()
    except ContractError:
        note(f"control: {label} is rejected")
        return
    fail(f"control: {label} passed the validator")


def main() -> int:
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    task = load_task(TASK)

    null_out = None
    null_meta = None
    for arm, adapter in ADAPTERS.items():
        fixture = HERE / "fixtures" / arm
        arm_config = fixture / "arm_config.json"
        meta = meta_for(arm, arm_config)
        out = SCRATCH / arm
        out.mkdir(parents=True, exist_ok=True)
        result = adapter.convert(fixture, task, out, meta)
        if result == "valid":
            detail = validate_output(out, arm, task["key"], meta)
            note(
                f"{arm}: valid output and receipt "
                f"(report {detail['report_chars']} chars, sources {detail['sources']}, "
                f"digests {detail['digests']})"
            )
            if arm == "null":
                null_out, null_meta = out, meta
        elif result == "excluded":
            exclusion = validate_exclusion(out, arm, task["key"])
            note(f"{arm}: excluded — {exclusion['reason']}")
        else:
            fail(f"{arm}: adapter returned {result!r}")

    assert null_out is not None and null_meta is not None
    receipt = json.loads((null_out / "receipt.json").read_text())
    sources = json.loads((null_out / "sources.json").read_text())
    expect_error("an empty quote", lambda: validate_sources({"sources": [{"url": "https://example.com/", "quote": " ", "locator": "x"}]}))
    foreign = json.loads(json.dumps(receipt))
    foreign["model"]["route"] = "qwen3.8-27b"
    expect_error("a foreign model receipt", lambda: validate_receipt(foreign, "null", task["key"], null_meta))
    expect_error("a report that cites no ledger source", lambda: validate_report("no citation here", sources["sources"]))

    print(f"contract-dryrun: {len(PASSES)} checks passed", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DryRunFailure as error:
        print(f"FAIL {error}", file=sys.stderr, flush=True)
        raise SystemExit(1)
