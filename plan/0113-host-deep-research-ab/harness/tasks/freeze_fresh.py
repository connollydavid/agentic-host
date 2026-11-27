#!/usr/bin/env python3
"""Freeze and seal a fresh held-out set after the first set was read.

The first held-out set was decrypted at the failed confirmation, so it is
burned. This script builds a new five-task set (two SimpleQA rows and three
house tasks), validates it, seals it with a new key outside the repo, deletes
the plaintext, and writes `sets-fresh.json` with both digests. The old
`held-out.json.enc` and `sets.json` stay as history.

The key path is `/tmp/opencode/plan0113/held-out-fresh.key`; the operator holds
it, and the confirmation reads it.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
sys.path.insert(0, str(HERE))

import schema  # noqa: E402

KEY = Path("/tmp/opencode/plan0113/held-out-fresh.key")
PLAIN = HERE / "held-out-fresh.json"
SEALED = HERE / "held-out-fresh.json.enc"
SETS = HERE / "sets-fresh.json"
OLD_SETS = HERE / "sets.json"

TASKS = [
    {
        "key": "held-out-fresh/simpleqa-0010",
        "kind": "known-answer",
        "source": {
            "benchmark": schema.BENCHMARK,
            "dataset_url": schema.DATASET_URL,
            "dataset_sha256": schema.DATASET_SHA256,
            "row": 10,
        },
        "must_cover": [],
    },
    {
        "key": "held-out-fresh/simpleqa-0050",
        "kind": "known-answer",
        "source": {
            "benchmark": schema.BENCHMARK,
            "dataset_url": schema.DATASET_URL,
            "dataset_sha256": schema.DATASET_SHA256,
            "row": 50,
        },
        "must_cover": [],
    },
    {
        "key": "held-out-fresh/house-serde-simd",
        "kind": "house",
        "question": (
            "Compare serde_json and simd-json for parsing a 100 MB JSON stream in Rust. "
            "Name each license, the API difference, and the case where each wins."
        ),
        "must_cover": [
            {"entity": "serde_json", "aliases": ["serde json"]},
            {"entity": "simd-json", "aliases": ["simd json"]},
            {"entity": "license", "aliases": ["licence", "MIT", "Apache-2.0"]},
        ],
    },
    {
        "key": "held-out-fresh/house-nextest",
        "kind": "house",
        "question": (
            "Compare cargo-nextest and cargo test for a large Rust workspace. "
            "Name each license, the parallelism model, and one case where the standard runner wins."
        ),
        "must_cover": [
            {"entity": "cargo-nextest", "aliases": ["cargo nextest"]},
            {"entity": "cargo test", "aliases": ["cargo-test"]},
            {"entity": "license", "aliases": ["licence", "MIT", "Apache-2.0"]},
            {"entity": "parallelism", "aliases": ["parallel"]},
        ],
    },
    {
        "key": "held-out-fresh/house-verify-setup",
        "kind": "house",
        "question": (
            "What does host-lifecycle software --verify-setup check, and how does it differ from "
            "software --check? Name the artifacts each gate reads."
        ),
        "must_cover": [
            {"entity": "--verify-setup", "aliases": ["verify-setup"]},
            {"entity": "--check", "aliases": ["software --check"]},
            {"entity": "hooks", "aliases": ["commit hooks"]},
            {"entity": "worktrees", "aliases": ["worktree"]},
        ],
    },
]


def main() -> int:
    for task in TASKS:
        task["digest"] = schema.task_digest(task)
    document = {"set": "held-out", "tasks": TASKS}
    summary = schema.validate_set(document)
    PLAIN.write_text(json.dumps(document, indent=2) + "\n")

    if not KEY.is_file():
        KEY.parent.mkdir(parents=True, exist_ok=True)
        KEY.write_text(subprocess.run(["openssl", "rand", "-hex", "32"], capture_output=True, text=True, check=True).stdout)
        KEY.chmod(0o600)
    if SEALED.exists():
        SEALED.unlink()
    subprocess.run(
        [
            "openssl",
            "enc",
            "-aes-256-cbc",
            "-pbkdf2",
            "-salt",
            "-in",
            str(PLAIN),
            "-out",
            str(SEALED),
            "-pass",
            f"file:{KEY}",
        ],
        check=True,
    )
    ciphertext = schema.sha256_file(SEALED)
    PLAIN.unlink()
    if PLAIN.exists():
        raise SystemExit("the fresh held-out plaintext was not deleted")

    old = json.loads(OLD_SETS.read_text())
    record = {
        "frozen": date.today().isoformat(),
        "before_first_draw": True,
        "benchmark": old["benchmark"],
        "selection": old["selection"],
        "held_out": {
            "path": SEALED.name,
            "plaintext_set_digest": summary["set_digest"],
            "ciphertext_sha256": ciphertext,
            "tasks": summary["tasks"],
            "known_answer": summary["known_answer"],
            "house": summary["house"],
            "sealed": True,
            "fresh": True,
            "key_path": str(KEY),
            "replaces": "held-out.json.enc (read at the failed confirmation)",
        },
    }
    SETS.write_text(json.dumps(record, indent=2) + "\n")
    print(f"ok fresh held-out: {summary['tasks']} tasks "
          f"({summary['known_answer']} known-answer, {summary['house']} house)")
    print(f"ok plaintext set digest: {summary['set_digest']}")
    print(f"ok ciphertext: {ciphertext}")
    print(f"ok sealed: {SEALED.name}; plaintext deleted; key at {KEY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
