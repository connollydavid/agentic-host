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
import sqlite3
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

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
MODEL_PREFLIGHT = HARNESS / "model-pin" / "model-preflight.py"

sys.path.insert(0, str(HARNESS / "contract"))
sys.path.insert(0, str(HARNESS / "tasks"))
sys.path.insert(0, str(HARNESS / "rubric"))

import contract  # noqa: E402
import rubric  # noqa: E402
import schema  # noqa: E402
from adapters import hffmnnj, kanatami, null as null_adapter, samber, weizhena  # noqa: E402

ARM_NAMES = ["null", "weizhena", "hffmnnj", "kanatami", "samber"]
ADAPTERS = {
    "null": null_adapter,
    "weizhena": weizhena,
    "hffmnnj": hffmnnj,
    "kanatami": kanatami,
    "samber": samber,
}
TASK_KEYS = [
    "selection/simpleqa-0000",
    "selection/simpleqa-0002",
    "selection/simpleqa-1000",
    "selection/house-path-crates",
    "selection/house-rg-ast-grep",
    "selection/house-host-lint-docs",
]
ARM_LINES = {
    "weizhena": (
        "Use the installed Weizhena research skills: run the research-deep workflow over the question. "
        "Write your output in the current working directory. "
        "Do not ask clarifying questions; proceed with stated assumptions."
    ),
    "hffmnnj": (
        "Use the installed hffmnnj deep-research plugin and its library: run its workflow over the question. "
        "Write your output in the current working directory. "
        "Do not ask clarifying questions; proceed with stated assumptions."
    ),
    "kanatami": (
        "Use the installed web-search-deep skill: follow its protocol over the question. "
        "Write your output in the current working directory. "
        "Do not ask clarifying questions; proceed with stated assumptions."
    ),
    "samber": (
        "Use the installed deep-research skill: follow its workflow over the question. "
        "Write your output in the current working directory. "
        "Do not ask clarifying questions; proceed with stated assumptions."
    ),
}
WINDOWS_PATH = re.compile(r"[^A-Za-z0-9._/-]+")
SEARCH_PROVIDER = "exa"
SEARCH_ENGINES = ("duckduckgo.com", "google.com", "bing.com", "search.yahoo.com")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def read_replies(root: Path) -> list[dict]:
    """Read every assistant reply's provider/model from the scratch OpenCode DB."""
    db = root / "data" / "opencode" / "opencode.db"
    if not db.is_file():
        return []
    connection = None
    try:
        connection = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        rows = connection.execute(
            "SELECT json_extract(data, '$.model.providerID'), "
            "json_extract(data, '$.model.id') FROM session_message WHERE type = 'assistant'"
        ).fetchall()
    except sqlite3.Error:
        return []
    finally:
        if connection is not None:
            connection.close()
    return [
        {"provider": provider, "model": model}
        for provider, model in rows
        if isinstance(provider, str) and isinstance(model, str)
    ]


def is_search_engine(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == engine or host.endswith("." + engine) for engine in SEARCH_ENGINES)


def provider_gate(measured: str, foreign_fetches: list[str], arm: str) -> str | None:
    """The scoped one-provider rule.

    The null arm is the measured search control: a search-engine fetch or a
    provider other than Exa voids it. A research arm may carry its own native
    search route; that route is recorded in the receipt, not judged against the
    null's provider.
    """
    if arm != "null":
        return None
    if foreign_fetches:
        return "search-engine fetch is a foreign provider: " + ", ".join(foreign_fetches[:3])
    if measured not in (SEARCH_PROVIDER, "none"):
        return f"foreign search provider {measured}; expected {SEARCH_PROVIDER}"
    return None


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
    return f"{ARM_LINES[arm]}\n\nQuestion: {question}\n"


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
        "websearch": {"provider": SEARCH_PROVIDER},
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


def state_text(state: dict) -> str:
    """The fetched page text from a tool state.

    The live event stream carries ``state.output``; the scratch database's
    ``session_part`` rows carry the same page as ``state.content`` parts. Both
    shapes are real records; a missing one is not a fetched page.
    """
    content = state.get("content")
    if isinstance(content, list):
        text = "\n".join(
            part.get("text", "")
            for part in content
            if isinstance(part, dict) and isinstance(part.get("text"), str)
        )
        if text.strip():
            return text
    output = state.get("output")
    return output if isinstance(output, str) else ""


def read_fetches(root: Path) -> list[tuple[str, str]]:
    """Read every completed webfetch page from the scratch OpenCode DB."""
    db = root / "data" / "opencode" / "opencode.db"
    if not db.is_file():
        return []
    connection = None
    try:
        connection = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        rows = connection.execute(
            "SELECT data FROM session_part WHERE data LIKE '%\"name\":\"webfetch\"%'"
        ).fetchall()
    except sqlite3.Error:
        return []
    finally:
        if connection is not None:
            connection.close()
    fetches: list[tuple[str, str]] = []
    for (raw,) in rows:
        try:
            part = json.loads(raw)
        except json.JSONDecodeError:
            continue
        state = part.get("state") or {}
        if state.get("status") != "completed":
            continue
        url = (state.get("input") or {}).get("url")
        output = state_text(state)
        if isinstance(url, str) and output.strip():
            fetches.append((url, output))
    return fetches


def read_websearch(root: Path) -> list[dict]:
    """Read every websearch call's provider and query from the scratch DB."""
    db = root / "data" / "opencode" / "opencode.db"
    if not db.is_file():
        return []
    connection = None
    try:
        connection = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        rows = connection.execute(
            "SELECT data FROM session_part WHERE data LIKE '%\"name\":\"websearch\"%'"
        ).fetchall()
    except sqlite3.Error:
        return []
    finally:
        if connection is not None:
            connection.close()
    calls: list[dict] = []
    for (raw,) in rows:
        try:
            part = json.loads(raw)
        except json.JSONDecodeError:
            continue
        state = part.get("state") or {}
        metadata = state.get("metadata") or {}
        provider = metadata.get("provider") or (metadata.get("metadata") or {}).get("provider")
        calls.append(
            {
                "provider": provider,
                "query": (state.get("input") or {}).get("query"),
                "status": state.get("status"),
            }
        )
    return calls


def parse_events(path: Path) -> dict:
    text: list[str] = []
    fetches: list[tuple[str, str]] = []
    websearch: list[dict] = []
    prompt_tokens = 0
    completion_tokens = 0
    tool_calls = 0
    if not path.exists():
        return {
            "text": "",
            "fetches": fetches,
            "websearch": websearch,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "tool_calls": 0,
        }
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
                output = state_text(state)
                if url and output.strip():
                    fetches.append((url, output))
            if part.get("tool") == "websearch" and state.get("status") == "completed":
                metadata = state.get("metadata") or {}
                provider = metadata.get("provider") or (metadata.get("metadata") or {}).get("provider")
                websearch.append(
                    {
                        "provider": provider,
                        "query": (state.get("input") or {}).get("query"),
                    }
                )
    return {
        "text": "\n".join(part for part in text if part).strip(),
        "fetches": fetches,
        "websearch": websearch,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "tool_calls": tool_calls,
    }


def note_front_body(path: Path) -> tuple[dict, str]:
    text = path.read_text(errors="replace")
    if not text.startswith("---\n"):
        return {}, text
    rest = text[len("---\n"):]
    if "\n---\n" not in rest:
        return {}, text
    front, body = rest.split("\n---\n", 1)
    try:
        return json.loads(front), body
    except json.JSONDecodeError:
        return {}, body


def text_sources(text: str) -> list[tuple[str, str]]:
    """Pair each URL in the run text with the paragraph that carries it."""
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    for paragraph in paragraphs:
        for url in re.findall(r"https?://[^\s)\]>\"']+", paragraph):
            url = url.rstrip(".,;:")
            if url not in seen:
                seen.add(url)
                pairs.append((url, paragraph))
    return pairs


def prepare_native(arm: str, work: Path, root: Path, draw: Path, parsed: dict) -> Path:
    """Copy the arm's native output into the draw's `native/` audit surface.

    The adapters read this directory; the contract files they write stay in the
    draw root. The null arm already writes the contract, so its files are copied
    as-is. Each other arm's documented output shape is collected: the hffmnnj
    library notes, the kanatami workers, the weizhena result JSON, the samber
    research notes. A report file or the run's final text is the fallback.
    """
    native = draw / "native"
    native.mkdir(parents=True, exist_ok=True)
    if arm == "null":
        for name in ("report.md", "sources.json"):
            if (work / name).is_file():
                shutil.copyfile(work / name, native / name)
        return native
    if arm == "hffmnnj":
        candidates = [
            root / "data" / "opencode-deep-research" / "library" / "notes",
            root / "home" / ".local" / "share" / "opencode-deep-research" / "library" / "notes",
        ]
        library = next((path for path in candidates if path.is_dir()), None)
        if library is not None:
            shutil.copytree(library, native / "notes", dirs_exist_ok=True)
            reports = []
            for path in library.rglob("*.md"):
                front, body = note_front_body(path)
                if front.get("kind") == "report":
                    reports.append((path.stat().st_mtime, body))
            if reports:
                (native / "report.md").write_text(max(reports)[1])
    elif arm == "kanatami":
        if (work / "workers.json").is_file():
            shutil.copyfile(work / "workers.json", native / "workers.json")
        if (work / "final-report.md").is_file():
            shutil.copyfile(work / "final-report.md", native / "report.md")
    elif arm == "weizhena":
        for base in (work / "results", work / "research"):
            if base.is_dir():
                shutil.copytree(base, native / "results", dirs_exist_ok=True)
        for path in work.rglob("*.json"):
            if native in path.parents:
                continue
            target = native / "results" / path.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
    elif arm == "samber":
        for base in (work / "research", work / "notes"):
            if base.is_dir():
                shutil.copytree(base, native / "notes", dirs_exist_ok=True)

    if not (native / "report.md").exists():
        candidates = [path for path in work.rglob("*.md") if native not in path.parents]
        if candidates:
            report = min(candidates, key=lambda path: (len(path.parts), -path.stat().st_mtime))
            shutil.copyfile(report, native / "report.md")
        elif parsed["text"]:
            (native / "report.md").write_text(parsed["text"] + "\n")

    if arm == "kanatami" and not (work / "workers.json").is_file():
        text = parsed["text"]
        corpus = work / "research-corpus.md"
        if corpus.is_file():
            text = corpus.read_text() + "\n\n" + text
        report_file = work / "final-report.md"
        if report_file.is_file():
            text = report_file.read_text() + "\n\n" + text
        results = [{"url": url, "full_text": paragraph} for url, paragraph in text_sources(text)]
        contract.write_json(native / "workers.json", {"workers": [{"id": "run", "results": results}]})
    return native


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


def run_draw(arm: str, task: dict, force: bool = False, suffix: str = "", reuse: bool = False) -> dict:
    name = task["key"].split("/", 1)[1] + suffix
    draw = DRAWS / arm / name
    if (draw / "score.json").exists() and not force and not reuse:
        return json.loads((draw / "score.json").read_text())
    root = SCRATCH / f"{arm}-{name}"
    events_path = root / "events.jsonl"
    if reuse:
        if not (draw / "score.json").is_file() or not events_path.is_file():
            raise RuntimeError(f"reuse: no recorded draw or event log at {draw}")
        previous = json.loads((draw / "score.json").read_text())
        work = root / "work"
        prompt = (draw / "prompt.txt").read_text()
        wall = float(previous.get("wall_seconds", 0))
        exit_code = previous.get("exit_code", 0)
        timed_out = bool(previous.get("timed_out", False))
        rerun_of = ""
    else:
        rerun_of = ""
        prior: dict = {}
        if draw.exists():
            if force:
                attempts = DRAWS / arm / "attempts"
                attempts.mkdir(parents=True, exist_ok=True)
                number = len(list(attempts.glob(f"{name}-*"))) + 1
                previous_draw = attempts / f"{name}-{number}"
                shutil.move(str(draw), str(previous_draw))
                rerun_of = str(previous_draw.relative_to(DRAWS))
                score_path = previous_draw / "score.json"
                if score_path.is_file():
                    try:
                        prior = json.loads(score_path.read_text())
                    except json.JSONDecodeError:
                        prior = {}
            else:
                shutil.rmtree(draw)
        draw.mkdir(parents=True, exist_ok=True)
        if rerun_of:
            contract.write_json(
                draw / "rerun.json",
                {
                    "previous": rerun_of,
                    "reason": prior.get("contract_reason") or prior.get("break_class") or "re-run",
                    "break_class": prior.get("break_class"),
                    "recorded": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                },
            )
        if root.exists():
            shutil.rmtree(root)
        work = prepare(arm, root)
        prompt = prompt_for(arm, task)
        (root / "prompt.txt").write_text(prompt)
        contract.write_json(root / "task.json", task)
        contract.write_json(work / "task.json", task)
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
        stderr_path = root / "stderr.log"
        timeout = contract.CAPS["wall_seconds"]
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
    parsed["fetches"].extend(read_fetches(root))
    websearch = read_websearch(root) or parsed["websearch"]
    parsed["websearch"] = websearch
    providers = sorted({call["provider"] for call in websearch if isinstance(call.get("provider"), str) and call["provider"]})
    measured_provider = providers[0] if len(providers) == 1 else (",".join(providers) if providers else "none")
    foreign_fetches = [url for url, _ in parsed["fetches"] if is_search_engine(url)]
    native_search = sorted(
        {
            (urlparse(url).hostname or "").lower()
            for url, _ in parsed["fetches"]
            if is_search_engine(url)
        }
    )
    replies = read_replies(root)
    replies_path = draw / "replies.jsonl"
    replies_path.write_text("".join(json.dumps(reply) + "\n" for reply in replies))
    preflight_reason = ""
    if MODEL_PREFLIGHT.is_file():
        preflight = subprocess.run(
            [sys.executable, str(MODEL_PREFLIGHT), "--replies", str(replies_path)],
            capture_output=True,
            text=True,
        )
        if preflight.returncode != 0:
            preflight_reason = preflight.stderr.strip() or "model pre-flight failed"

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
        "search_provider": measured_provider,
        "native_search": native_search,
        "status": "live",
        "caps": contract.CAPS,
        "fetches": sorted({url for url, _ in parsed["fetches"]}),
        "digests": {
            "task": schema.task_digest(task),
            "harness_pin": schema.sha256_file(PIN_ENV),
            "model_pin": schema.sha256_file(MODEL_PIN),
            "arm_config": schema.sha256_file(root / "config" / "opencode" / "opencode.json"),
            "prompt": sha256_text(prompt),
            "replies": schema.sha256_file(replies_path),
        },
    }

    native = prepare_native(arm, work, root, draw, parsed)
    adapter = ADAPTERS[arm]
    used = {
        "prompt_tokens": parsed["prompt_tokens"],
        "completion_tokens": parsed["completion_tokens"],
        "tool_calls": parsed["tool_calls"],
        "wall_seconds": round(wall, 1),
    }
    over = [key for key, cap in contract.CAPS.items() if used.get(key, 0) > cap]
    adapter_result = "void"
    adapter_reason = ""
    try:
        adapter_result = adapter.convert(native, task, draw, meta)
    except contract.ContractError as error:
        adapter_reason = str(error)
    merge_fetch_log(draw, parsed)
    contract.write_json(draw / "task.json", task)
    (draw / "prompt.txt").write_text(prompt)

    if adapter_result == "valid":
        contract.write_json(
            draw / "receipt.json",
            contract.build_receipt(
                arm,
                task["key"],
                meta,
                status="live",
                used=used,
            ),
        )

    provider_reason = provider_gate(measured_provider, foreign_fetches, arm)
    contract_ok = False
    contract_reason = ""
    excluded = False
    over_detail = [
        f"{key} {used[key]} > {contract.CAPS[key]}" for key in contract.CAPS if used.get(key, 0) > contract.CAPS[key]
    ]
    if timed_out and not any(item.startswith("wall_seconds") for item in over_detail):
        over_detail.append(
            f"wall_seconds {used['wall_seconds']} reached {contract.CAPS['wall_seconds']}"
        )
    budget_reason = "budget exhausted: " + ", ".join(over_detail) if over_detail else ""
    if timed_out or over:
        contract_reason = budget_reason
        result = {"status": "void", "reason": contract_reason}
    elif provider_reason:
        contract_reason = provider_reason
        result = {"status": "void", "reason": provider_reason}
    elif preflight_reason:
        contract_reason = preflight_reason
        result = {"status": "void", "reason": preflight_reason}
    elif adapter_result == "valid":
        try:
            contract.validate_output(draw, arm, task["key"], meta)
            contract_ok = True
            result = rubric.score(draw, task, DATASET)
        except contract.ContractError as error:
            contract_reason = str(error)
            result = {"status": "void", "reason": str(error)}
        except Exception as error:  # noqa: BLE001 - a rubric crash is a draw finding
            contract_reason = f"rubric error: {error}"
            result = {"status": "void", "reason": contract_reason}
    elif adapter_result == "excluded":
        try:
            exclusion = contract.validate_exclusion(draw, arm, task["key"])
            excluded = True
            contract_reason = exclusion["reason"]
            result = {"status": "excluded", "reason": exclusion["reason"], "max": 16}
        except contract.ContractError as error:
            contract_reason = str(error)
            result = {"status": "void", "reason": str(error)}
    else:
        contract_reason = adapter_reason or "the adapter produced no contract output"
        result = {"status": "void", "reason": contract_reason}
    valid = contract_ok and result.get("status") == "scored"
    score = result.get("score", 0) if valid else 0
    if timed_out or over:
        break_class = "budget"
    elif exit_code not in (0,):
        break_class = "harness"
    elif valid:
        break_class = "none"
    elif adapter_result == "excluded":
        break_class = "arm"
    else:
        reason = contract_reason.lower()
        arm_tokens = ("report.md cites", "the report cites", "phantom", "no worker result", "no fetched", "no url")
        harness_tokens = (
            "pseudo tool calls",
            "driver error",
            "budget exhausted",
            "foreign model reply",
            "model pre-flight",
            "replies:",
        )
        if any(token in reason for token in arm_tokens):
            break_class = "arm"
        elif any(token in reason for token in harness_tokens):
            break_class = "harness"
        else:
            break_class = "harness"
    native_files = sum(1 for path in native.rglob("*") if path.is_file()) if native.exists() else 0
    summary = {
        "arm": arm,
        "task": task["key"],
        "draw": name,
        "adapter": arm,
        "adapter_result": adapter_result,
        "excluded": excluded,
        "reused": reuse,
        "rerun_of": rerun_of,
        "break_class": break_class,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "wall_seconds": round(wall, 1),
        "prompt_tokens": parsed["prompt_tokens"],
        "completion_tokens": parsed["completion_tokens"],
        "tool_calls": parsed["tool_calls"],
        "search_provider": measured_provider,
        "native_search": native_search,
        "websearch_calls": len(parsed["websearch"]),
        "search_engine_fetches": foreign_fetches,
        "replies": len(replies),
        "model_preflight": preflight_reason or "ok",
        "native_files": native_files,
        "contract_ok": contract_ok,
        "contract_reason": contract_reason,
        "rubric": result,
        "valid": valid,
        "score": score,
    }
    contract.write_json(draw / "score.json", summary)
    return summary


def safe_run_draw(arm: str, task: dict, force: bool = False, suffix: str = "", reuse: bool = False) -> dict:
    try:
        return run_draw(arm, task, force=force, suffix=suffix, reuse=reuse)
    except Exception as error:  # noqa: BLE001 - a driver crash is a draw finding
        name = task["key"].split("/", 1)[1] + suffix
        draw = DRAWS / arm / name
        draw.mkdir(parents=True, exist_ok=True)
        summary = {
            "arm": arm,
            "task": task["key"],
            "draw": name,
            "adapter": arm,
            "adapter_result": "void",
            "excluded": False,
            "reused": reuse,
            "rerun_of": "",
            "break_class": "harness",
            "exit_code": None,
            "timed_out": False,
            "wall_seconds": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "tool_calls": 0,
            "search_provider": "none",
            "native_search": [],
            "websearch_calls": 0,
            "search_engine_fetches": [],
            "replies": 0,
            "model_preflight": "harness",
            "native_files": 0,
            "contract_ok": False,
            "contract_reason": f"driver error: {error}",
            "rubric": {"status": "void", "reason": f"driver error: {error}"},
            "valid": False,
            "score": 0,
        }
        contract.write_json(draw / "score.json", summary)
        return summary


def main(argv: list[str]) -> int:
    global DRAWS, SCRATCH
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="arm, task name, or arm/task")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--parallel", type=int, default=2, help="draws in flight")
    parser.add_argument("--order", choices=("interleaved", "task"), default="interleaved")
    parser.add_argument("--draws", default=str(DRAWS))
    parser.add_argument("--scratch", default=str(SCRATCH))
    parser.add_argument("--reuse", action="store_true", help="re-process the recorded draw, no model run")
    args = parser.parse_args(argv)
    DRAWS = Path(args.draws)
    SCRATCH = Path(args.scratch)
    if not BIN.is_file():
        raise SystemExit("the pinned binary is missing; run harness/install.sh")
    if not os.environ.get("ROPE_BEARER"):
        raise SystemExit("ROPE_BEARER is unset")
    tasks = {task["key"]: task for task in json.loads(TASKS.read_text())["tasks"]}

    def report(summary: dict) -> None:
        print(
            f"{summary['arm']:9s} {summary['task'].split('/', 1).pop():24s} "
            f"{'valid' if summary['valid'] else 'void ':5s} "
            f"{summary['score']}/{summary['rubric'].get('max', '-')} "
            f"contract={'ok' if summary['contract_ok'] else 'no'} "
            f"provider={summary.get('search_provider', 'none')} "
            f"tokens={summary['prompt_tokens']}+{summary['completion_tokens']} "
            f"tools={summary['tool_calls']} wall={summary['wall_seconds']}s"
            + (f"  ({summary['contract_reason']})" if summary["contract_reason"] else ""),
            flush=True,
        )

    def run_jobs(jobs: list[tuple[str, dict]]) -> None:
        if args.parallel <= 1 or len(jobs) == 1:
            for arm, task in jobs:
                report(safe_run_draw(arm, task, force=args.force, reuse=args.reuse))
            return
        with ThreadPoolExecutor(max_workers=args.parallel) as pool:
            futures = {
                pool.submit(safe_run_draw, arm, task, args.force, "", args.reuse): (arm, task)
                for arm, task in jobs
            }
            for future in as_completed(futures):
                report(future.result())

    if args.only or args.order == "task":
        waves: list[list[tuple[str, dict]]] = []
        for key in TASK_KEYS:
            name = key.split("/", 1)[1]
            selected = []
            for arm in ARM_NAMES:
                if args.only:
                    selector = args.only
                    if "/" in selector:
                        wanted_arm, wanted_task = selector.split("/", 1)
                        if arm != wanted_arm or name != wanted_task:
                            continue
                    elif selector != arm and selector != name:
                        continue
                selected.append((arm, tasks[key]))
            if selected:
                waves.append(selected)
        for wave in waves:
            run_jobs(wave)
        return 0

    jobs: list[tuple[str, dict]] = []
    for step in range(len(ARM_NAMES)):
        for index, key in enumerate(TASK_KEYS):
            arm = ARM_NAMES[(step + index) % len(ARM_NAMES)]
            jobs.append((arm, tasks[key]))
    run_jobs(jobs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
