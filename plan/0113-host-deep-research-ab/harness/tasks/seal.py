#!/usr/bin/env python3
"""Seal an operator-supplied fresh held-out set with an operator-held key.

The plaintext set lives outside the repository and is never committed. The
script validates it, encrypts it with `openssl enc -aes-256-cbc -pbkdf2`, writes
the ciphertext and a `sets-*.json` record carrying both digests, and deletes
the plaintext unless `--keep-plaintext` is given. It never creates a key: the
operator supplies it, and the confirmation takes `--key` explicitly.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
REPO = HERE.parents[3]
sys.path.insert(0, str(HERE))

import schema  # noqa: E402

DEFAULT_SELECTION = HERE / "selection.json"
DEFAULT_SETS = HERE / "sets.json"


def fail(message: str) -> None:
    raise SystemExit(message)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", required=True, help="the plaintext held-out set, outside the repository")
    parser.add_argument("--key", required=True, help="the operator-held key file")
    parser.add_argument("--sealed", required=True, help="the ciphertext path, usually under tasks/")
    parser.add_argument("--sets", required=True, help="the set record to write")
    parser.add_argument("--selection", default=str(DEFAULT_SELECTION))
    parser.add_argument("--benchmark", default=str(DEFAULT_SETS))
    parser.add_argument("--keep-plaintext", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    plaintext = Path(args.set).resolve()
    key = Path(args.key).resolve()
    sealed = Path(args.sealed).resolve()
    sets = Path(args.sets).resolve()
    if REPO in plaintext.parents:
        fail(f"the plaintext set is inside the repository at {plaintext}; author it under /tmp")
    if not plaintext.is_file():
        fail(f"the plaintext set is absent at {plaintext}")
    if not key.is_file():
        fail(f"the operator-held key is absent at {key}")
    if not args.force and (sealed.exists() or sets.exists()):
        fail(f"a sealed set or record already exists at {sealed} or {sets}; pass --force to replace it")

    document = json.loads(plaintext.read_text())
    summary = schema.validate_set(document)
    if summary["set"] != "held-out":
        fail("the supplied set is not a held-out set")
    selection = schema.load_set(Path(args.selection))
    benchmark = json.loads(Path(args.benchmark).read_text())
    sealed.parent.mkdir(parents=True, exist_ok=True)
    temporary = sealed.with_suffix(sealed.suffix + ".tmp")
    completed = subprocess.run(
        [
            "openssl",
            "enc",
            "-aes-256-cbc",
            "-pbkdf2",
            "-salt",
            "-in",
            str(plaintext),
            "-out",
            str(temporary),
            "-pass",
            f"file:{key}",
        ],
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        temporary.unlink(missing_ok=True)
        fail(f"openssl could not seal the set: {completed.stderr[-500:]}")
    temporary.replace(sealed)
    ciphertext = schema.sha256_file(sealed)
    if not args.keep_plaintext:
        plaintext.unlink()
        if plaintext.exists():
            fail(f"the plaintext was not deleted at {plaintext}")
    record = {
        "frozen": date.today().isoformat(),
        "before_first_draw": True,
        "benchmark": benchmark["benchmark"],
        "selection": {
            "path": Path(args.selection).name,
            "set_digest": selection["set_digest"],
            "tasks": selection["tasks"],
            "known_answer": selection["known_answer"],
            "house": selection["house"],
        },
        "held_out": {
            "path": sealed.name,
            "plaintext_set_digest": summary["set_digest"],
            "ciphertext_sha256": ciphertext,
            "tasks": summary["tasks"],
            "known_answer": summary["known_answer"],
            "house": summary["house"],
            "sealed": True,
            "fresh": True,
            "key": "operator-held",
        },
    }
    sets.write_text(json.dumps(record, indent=2) + "\n")
    print(
        f"ok sealed: {summary['tasks']} tasks "
        f"({summary['known_answer']} known-answer, {summary['house']} house)"
    )
    print(f"ok plaintext set digest: {summary['set_digest']}")
    print(f"ok ciphertext: {ciphertext}")
    print(f"ok plaintext {'kept at ' + str(plaintext) if args.keep_plaintext else 'deleted'}")
    print(f"ok record: {sets}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
