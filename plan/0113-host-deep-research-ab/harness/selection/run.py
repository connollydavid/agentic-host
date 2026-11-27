#!/usr/bin/env python3
"""The plan/0113 selection driver: the frozen 30-draw round.

One draw is one arm, one selection task, one pinned OpenCode run. The driver
builds the arm's scratch root, writes the provider and the per-arm config,
runs the pinned binary non-interactively, reads the contract files and the
fetch log, and scores the draw with the mechanical rubric. The draws are
committed evidence; the round report pools them and applies the frozen lock.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
ARMS = HARNESS.parent / "arms"
BIN = HARNESS / ".prefix" / "opencode"
TASKS = HARNESS / "tasks" / "selection.json"
DATASET = Path("/tmp/opencode/simpleqa.csv")
SCRATCH = Path("/tmp/opencode/plan0113/selection")
DRAWS = HERE / "draws"
PIN_ENV = HARNESS / "pin.env"
MODEL_PIN = HARNESS / "model-pin" / "model-pin.json"

sys.path.insert(0, str(HARNESS / "contract"))
sys.path.insert(0, str(HARNESS / "tasks"))
sys.path.insert(0, str(HARNESS / "rubric"))

import contract  # noqa: E402
import rubric  # noqa: E402
import schema  # noqa: E402

ARM_NAMES = ["null", "weizhena", "hffmnnj", "kanatami", "samber"]
TASK_KEYS = [
    "selection/simpleqa-0000",
    "selection/simpleqa-0002",
    "selection/simpleqa-1000",
    "selection/house-path-crates",
    "selection/house-rg-ast-grep",
    "selection/house-host-lint-docs",
]
ARM_LINES = {
    "weizhena": "Use the installed Weizhena research skills: run the research-deep workflow over the question, then satisfy the contract below.",
    "hffmnnj": "Use the installed hffmnnj deep-research plugin and its library: run its workflow over the question, then satisfy the contract below.",
    "kanatami": "Use the installed web-search-deep skill: follow its protocol over the question, then satisfy the contract below.",
    "samber": "Use the installed deep-research skill: follow its workflow over the question, then satisfy the contract below.",
}
WINDOWS_PATH = re.compile(r"[^A-Za-z0-9._/-]+")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def read_pin_env() -> dict[str, str]:
    values = {}
    for line in PIN_ENV.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value.strip().strip('"')
    return values


def task_question(task: dict) -> str:
    if task["kind"] == "house":
        return task["question"]
    if not DATASET.exists():
        DATASET.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(schema.DATASET_URL, DATASET)
    if schema.sha256_file(DATASET) != schema.DATASET_SHA256:
        raise SystemExit("the SimpleQA dataset does not match the frozen digest")
    rows = list(csv.DictReader(DATASET.open(newline="", encoding="utf-8")))
    return rows[task["source"]["row"]]["problem"]


def prompt_for(arm: str, task: dict) -> str:
    question = task_question(task)
    if arm == "null":
        frozen = (HARNESS / "contract" / "prompts" / "null.md").read_text()
        return f"{frozen}\n\nQuestion: {question}\n"
    contract_text = f"""{ARM_LINES[arm]}

Produce these files in the current working directory:
- report.md: a Markdown report. Put the source URL or your arm's citation id beside every cited sentence.
- sources.json: {{"sources": [{{"url": "https://...", "quote": "<verbatim passage>", "locator": "<section or paragraph>"}}]}}.
- fetch-log.jsonl: one line per page fetched: {{"url": "https://...", "status": 200, "snapshot": "snapshots/<file>.txt"}}; save the fetched page text under snapshots/.
Do not write receipt.json; the harness writes it. Cite only pages you fetched, copy every quote from the fetched page, and do not change the model, provider or configuration.

Question: {question}
"""
    return contract_text


def arm_config(arm: str) -> dict:
    config = {
        "$schema": "https://opencode.ai/config.json",
        "model": "api.d07yx58.net/qwen3.8-flash-next",
        "provider": {
            "api.d07yx58.net": {
                "npm": "@ai-sdk/openai-compatible",
                "name": "api.d07yx58.net",
                "options": {
                    "baseURL": "https://api.d07yx58.net/v1",
                    "apiKey": "{env:ROPE_BEARER}",
                },
                "models": {
                    "qwen3.8-flash-next": {
                        "name": "Qwen3.8-Flash-Next (strata)",
                        "limit": {"context": 500000, "input": 500000, "output": 524288},
                    }
                },
            }
        },
        "lsp": False,
        "plugins": [],
    }
    if arm == "hffmnnj":
        config["plugins"] = [f"file://{ARMS / 'hffmnnj'}"]
    return config


def override_agent(source: Path, destination: Path, write: bool = False) -> None:
    text = source.read_text()
    text = re.sub(r"(?m)^model:.*$", "model: api.d07yx58.net/qwen3.8-flash-next", text)
    if write:
        text = text.replace("write: false", "write: true")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text)


def prepare(arm: str, root: Path) -> Path:
    for part in ("home", "config/opencode", "data", "cache", "state", "work"):
        (root / part).mkdir(parents=True, exist_ok=True)
    contract.write_json(root / "config" / "opencode" / "opencode.json", arm_config(arm))
    skills = root / "config" / "opencode" / "skills"
    agents = root / "config" / "opencode" / "agents"
    if arm == "weizhena":
        for name in ("research", "research-deep", "research-report", "research-add-items", "research-add-fields"):
            shutil.copytree(ARMS / "weizhena" / "skills" / "research-en" / name, skills / name)
        override_agent(ARMS / "weizhena" / "agents" / "web-search-opencode.md", agents / "web-search.md", write=True)
    elif arm == "kanatami":
        shutil.copytree(ARMS / "kanatami", skills / "web-search-deep", ignore=shutil.ignore_patterns(".git", "__pycache__"))
        override_agent(ARMS / "kanatami" / "agents" / "web-search-worker.md", agents / "web-search-worker.md")
    elif arm == "samber":
        shutil.copytree(ARMS / "samber" / "skills" / "deep-research", skills / "deep-research")
    return root / "work"


def parse_events(path: Path) -> dict:
    text: list[str] = []
    fetches: list[tuple[str, str]] = []
    prompt_tokens = 0
    completion_tokens = 0
    tool_calls = 0
    if not path.exists():
        return {"text": "", "fetches": fetches, "prompt_tokens": 0, "completion_tokens": 0, "tool_calls": 0}
    for line in path.read_text(errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "text":
            text.append((event.get("part") or {}).get("text", ""))
        elif event.get("type") == "step_finish":
            tokens = (event.get("part") or {}).get("tokens") or {}
            prompt_tokens += int(tokens.get("input", 0) or 0)
            completion_tokens += int(tokens.get("output", 0) or 0)
        elif event.get("type") == "tool_use":
            tool_calls += 1
            part = event.get("part") or {}
            state = part.get("state") or {}
            if part.get("tool") == "webfetch" and state.get("status") == "completed":
                url = ((state.get("input") or {}).get("url") or "").strip()
                output = state.get("output") or ""
                if url:
                    fetches.append((url, output))
    return {
        "text": "\n".join(part for part in text if part).strip(),
        "fetches": fetches,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "tool_calls": tool_calls,
    }


def copy_agent_files(work: Path, draw: Path) -> dict:
    report = work / "report.md"
    sources = work / "sources.json"
    fetch_log = work / "fetch-log.jsonl"
    if report.is_file() and report.read_text().strip():
        shutil.copyfile(report, draw / "report.md")
    if sources.is_file():
        shutil.copyfile(sources, draw / "sources.json")
    if fetch_log.is_file():
        shutil.copyfile(fetch_log, draw / "fetch-log.jsonl")
    if (work / "snapshots").is_dir():
        shutil.copytree(work / "snapshots", draw / "snapshots", dirs_exist_ok=True)
    return {"report": report.is_file(), "sources": sources.is_file(), "fetch_log": fetch_log.is_file()}


def merge_fetch_log(draw: Path, parsed: dict) -> None:
    entries: list[dict] = []
    seen: set[str] = set()
    agent_log = draw / "fetch-log.jsonl"
    if agent_log.is_file():
        for line in agent_log.read_text().splitlines():
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            url = entry.get("url")
            snapshot = entry.get("snapshot")
            if not isinstance(url, str) or not isinstance(snapshot, str):
                continue
            source = draw / snapshot
            if not source.is_file():
                continue
            target = draw / "snapshots" / f"agent-{len(entries)}-{Path(snapshot).name}"
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            entries.append({"url": url, "status": entry.get("status", 200), "snapshot": str(target.relative_to(draw))})
            seen.add(url)
    for index, (url, output) in enumerate(parsed["fetches"], 1):
        if url in seen:
            continue
        target = draw / "snapshots" / f"main-{index}.txt"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output)
        entries.append({"url": url, "status": 200, "snapshot": str(target.relative_to(draw))})
        seen.add(url)
    with agent_log.open("w") as handle:
        for entry in entries:
            handle.write(json.dumps(entry) + "\n")


def run_draw(arm: str, task: dict, force: bool = False) -> dict:
    name = task["key"].split("/", 1)[1]
    draw = DRAWS / arm / name
    if (draw / "score.json").exists() and not force:
        return json.loads((draw / "score.json").read_text())
    if draw.exists():
        shutil.rmtree(draw)
    draw.mkdir(parents=True, exist_ok=True)
    root = SCRATCH / f"{arm}-{name}"
    if root.exists():
        shutil.rmtree(root)
    work = prepare(arm, root)
    prompt = prompt_for(arm, task)
    (root / "prompt.txt").write_text(prompt)
    contract.write_json(root / "task.json", task)
    env = {
        "HOME": str(root / "home"),
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "XDG_CONFIG_HOME": str(root / "config"),
        "XDG_DATA_HOME": str(root / "data"),
        "XDG_CACHE_HOME": str(root / "cache"),
        "XDG_STATE_HOME": str(root / "state"),
        "OPENCODE_DISABLE_AUTOUPDATE": "1",
        "OPENCODE_DISABLE_MODELS_FETCH": "1",
        "OPENCODE_ENABLE_EXA": "1",
        "ROPE_BEARER": os.environ.get("ROPE_BEARER", ""),
    }
    started = time.time()
    events_path = root / "events.jsonl"
    stderr_path = root / "stderr.log"
    timeout = 1800
    with events_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        try:
            completed = subprocess.run(
                [str(BIN), "run", "--format", "json", "--auto", prompt],
                cwd=work,
                env=env,
                stdout=stdout,
                stderr=stderr,
                timeout=timeout,
            )
            exit_code = completed.returncode
            timed_out = False
        except subprocess.TimeoutExpired:
            exit_code = 124
            timed_out = True
    wall = time.time() - started
    parsed = parse_events(events_path)
    files = copy_agent_files(work, draw)
    if not (draw / "report.md").exists() and parsed["text"]:
        (draw / "report.md").write_text(parsed["text"] + "\n")
    merge_fetch_log(draw, parsed)

    pin = read_pin_env()
    model = json.loads(MODEL_PIN.read_text())
    meta = {
        "harness": {"tag": pin["OPENCODE_TAG"], "binary_sha256": pin["OPENCODE_BINARY_SHA256"]},
        "model": {
            "provider": model["provider"],
            "route": model["route"],
            "deployment_id": model["deployment_id"],
            "backend": model["backend"],
            "max_input_tokens": model["max_input_tokens"],
            "max_output_tokens": model["max_output_tokens"],
        },
        "search_provider": "exa",
        "caps": contract.CAPS,
        "digests": {
            "task": schema.task_digest(task),
            "harness_pin": schema.sha256_file(PIN_ENV),
            "model_pin": schema.sha256_file(MODEL_PIN),
            "arm_config": schema.sha256_file(root / "config" / "opencode" / "opencode.json"),
            "prompt": sha256_text(prompt),
        },
    }
    receipt = contract.build_receipt(
        arm,
        task["key"],
        meta,
        status="live",
        used={
            "prompt_tokens": parsed["prompt_tokens"],
            "completion_tokens": parsed["completion_tokens"],
            "tool_calls": parsed["tool_calls"],
            "wall_seconds": round(wall, 1),
        },
    )
    contract.write_json(draw / "receipt.json", receipt)
    contract.write_json(draw / "task.json", task)
    (draw / "prompt.txt").write_text(prompt)

    contract_ok = False
    contract_reason = ""
    if not (draw / "sources.json").exists():
        contract_reason = "the draw wrote no sources.json"
    else:
        try:
            contract.validate_output(draw, arm, task["key"], meta)
            contract_ok = True
        except contract.ContractError as error:
            contract_reason = str(error)
    try:
        result = rubric.score(draw, task, DATASET)
    except Exception as error:  # noqa: BLE001 - a rubric crash is a draw finding
        result = {"status": "void", "reason": f"rubric error: {error}"}
    valid = contract_ok and result.get("status") == "scored"
    score = result.get("score", 0) if valid else 0
    summary = {
        "arm": arm,
        "task": task["key"],
        "exit_code": exit_code,
        "timed_out": timed_out,
        "wall_seconds": round(wall, 1),
        "prompt_tokens": parsed["prompt_tokens"],
        "completion_tokens": parsed["completion_tokens"],
        "tool_calls": parsed["tool_calls"],
        "agent_files": files,
        "contract_ok": contract_ok,
        "contract_reason": contract_reason,
        "rubric": result,
        "valid": valid,
        "score": score,
    }
    contract.write_json(draw / "score.json", summary)
    return summary


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="arm, task name, or arm/task")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    if not BIN.is_file():
        raise SystemExit("the pinned binary is missing; run harness/install.sh")
    if not os.environ.get("ROPE_BEARER"):
        raise SystemExit("ROPE_BEARER is unset")
    tasks = {task["key"]: task for task in json.loads(TASKS.read_text())["tasks"]}
    pairs = []
    for key in TASK_KEYS:
        name = key.split("/", 1)[1]
        for arm in ARM_NAMES:
            if args.only:
                selector = args.only
                if "/" in selector:
                    wanted_arm, wanted_task = selector.split("/", 1)
                    if arm != wanted_arm or name != wanted_task:
                        continue
                elif selector != arm and selector != name:
                    continue
            pairs.append((arm, tasks[key]))
    for arm, task in pairs:
        summary = run_draw(arm, task, force=args.force)
        print(
            f"{arm:9s} {task['key'].split('/', 1).pop():24s} "
            f"{'valid' if summary['valid'] else 'void ':5s} "
            f"{summary['score']}/{summary['rubric'].get('max', '-')} "
            f"contract={'ok' if summary['contract_ok'] else 'no'} "
            f"tokens={summary['prompt_tokens']}+{summary['completion_tokens']} "
            f"tools={summary['tool_calls']} wall={summary['wall_seconds']}s"
            + (f"  ({summary['contract_reason']})" if summary["contract_reason"] else ""),
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
