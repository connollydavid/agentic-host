"""The plan/0113 task-set schema, digest and seal.

The selection set and the held-out set are JSON documents of tasks. A
known-answer task references a SimpleQA row by the dataset's digest and row
index; a house task carries its question and must-cover list. Every task
carries its own digest, and each set carries a digest over its task list. The
held-out set is stored encrypted; only its plaintext and ciphertext digests are
tracked until confirmation.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

BENCHMARK = "simpleqa"
DATASET_URL = "https://openaipublic.blob.core.windows.net/simple-evals/simple_qa_test_set.csv"
DATASET_SHA256 = "feee3f7e7db3617e94e8fcf1977b756ec420ef8568f4e0fcbbe0e92e9d5fc032"
HEX = 64


class TaskError(Exception):
    pass


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest_value(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def task_digest(task: dict) -> str:
    body = {key: value for key, value in task.items() if key != "digest"}
    return digest_value(body)


def set_digest(tasks: list[dict]) -> str:
    return digest_value(tasks)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TaskError(message)


def validate_task(task: object) -> str:
    require(isinstance(task, dict), "a task is not an object")
    key = task.get("key")
    require(isinstance(key, str) and key, "task.key is missing")
    kind = task.get("kind")
    require(kind in ("known-answer", "house"), f"{key}: kind must be known-answer or house")
    stored = task.get("digest")
    require(isinstance(stored, str) and len(stored) == HEX, f"{key}: digest is missing")
    require(task_digest(task) == stored, f"{key}: digest does not match the task body")
    if kind == "known-answer":
        source = task.get("source")
        require(isinstance(source, dict), f"{key}: known-answer needs a source")
        require(source.get("benchmark") == BENCHMARK, f"{key}: benchmark must be {BENCHMARK}")
        require(source.get("dataset_url") == DATASET_URL, f"{key}: wrong dataset URL")
        require(source.get("dataset_sha256") == DATASET_SHA256, f"{key}: wrong dataset digest")
        row = source.get("row")
        require(isinstance(row, int) and row >= 0, f"{key}: row must be a non-negative integer")
        require("question" not in task, f"{key}: known-answer must not embed the question")
        require(task.get("must_cover", []) == [], f"{key}: known-answer must not carry must_cover")
    else:
        question = task.get("question")
        require(isinstance(question, str) and question.strip(), f"{key}: house needs a question")
        cover = task.get("must_cover")
        require(isinstance(cover, list) and cover, f"{key}: house needs a must_cover list")
        for item in cover:
            require(isinstance(item, dict), f"{key}: must_cover item is not an object")
            entity = item.get("entity")
            require(isinstance(entity, str) and entity, f"{key}: must_cover entity is empty")
            aliases = item.get("aliases")
            require(isinstance(aliases, list), f"{key}: must_cover aliases is not a list")
            require(all(isinstance(alias, str) and alias for alias in aliases), f"{key}: empty alias")
    return key


def validate_set(document: object) -> dict:
    require(isinstance(document, dict), "set document is not an object")
    name = document.get("set")
    require(name in ("selection", "held-out"), "set must be selection or held-out")
    tasks = document.get("tasks")
    require(isinstance(tasks, list) and tasks, "set has no tasks")
    keys = [validate_task(task) for task in tasks]
    require(len(keys) == len(set(keys)), "task keys are not unique")
    return {
        "set": name,
        "tasks": len(tasks),
        "known_answer": sum(1 for task in tasks if task["kind"] == "known-answer"),
        "house": sum(1 for task in tasks if task["kind"] == "house"),
        "set_digest": set_digest(tasks),
    }


def load_set(path: Path) -> dict:
    document = json.loads(path.read_text())
    summary = validate_set(document)
    summary["document"] = document
    return summary


def check(selection: Path, sealed: Path, sets: Path) -> None:
    record = json.loads(sets.read_text())
    chosen = load_set(selection)
    require(record["selection"]["set_digest"] == chosen["set_digest"], "selection digest does not match sets.json")
    require(record["selection"]["tasks"] == chosen["tasks"], "selection task count does not match sets.json")
    require(sha256_file(sealed) == record["held_out"]["ciphertext_sha256"], "held-out ciphertext digest does not match sets.json")
    require(sealed.read_bytes()[:8] == b"Salted__", "held-out file is not an OpenSSL ciphertext")
    plaintext = sealed.with_suffix(".json")
    require(not plaintext.exists(), f"the held-out plaintext is present at {plaintext}")
    benchmark = record["benchmark"]
    require(benchmark["name"] == BENCHMARK, "sets.json names another benchmark")
    require(benchmark["dataset_sha256"] == DATASET_SHA256, "sets.json carries another dataset digest")
    print(f"ok selection: {chosen['tasks']} tasks, {chosen['known_answer']} known-answer, {chosen['house']} house")
    print(f"ok selection digest: {chosen['set_digest']}")
    print(f"ok held-out: {record['held_out']['tasks']} tasks sealed, ciphertext {record['held_out']['ciphertext_sha256']}")
    print(f"ok held-out plaintext digest recorded: {record['held_out']['plaintext_set_digest']}")
    print("ok frozen before the first draw (sets.json recorded before the selection round)")


def decrypt(sealed: Path, key: Path, out: Path) -> None:
    subprocess.run(
        [
            "openssl",
            "enc",
            "-d",
            "-aes-256-cbc",
            "-pbkdf2",
            "-in",
            str(sealed),
            "-out",
            str(out),
            "-pass",
            f"file:{key}",
        ],
        check=True,
    )
    summary = load_set(out)
    print(f"ok held-out decrypted: {summary['tasks']} tasks, digest {summary['set_digest']}")


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[0] == "validate":
        summary = load_set(Path(argv[1]))
        print(
            f"ok {summary['set']}: {summary['tasks']} tasks "
            f"({summary['known_answer']} known-answer, {summary['house']} house), "
            f"digest {summary['set_digest']}"
        )
        return 0
    if len(argv) == 4 and argv[0] == "check":
        check(Path(argv[1]), Path(argv[2]), Path(argv[3]))
        return 0
    if len(argv) == 4 and argv[0] == "decrypt":
        decrypt(Path(argv[1]), Path(argv[2]), Path(argv[3]))
        return 0
    print("usage: schema.py validate <set.json>", file=sys.stderr)
    print("       schema.py check <selection.json> <held-out.json.enc> <sets.json>", file=sys.stderr)
    print("       schema.py decrypt <held-out.json.enc> <key> <out.json>", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
