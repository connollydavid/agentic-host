#!/usr/bin/env python3
"""The plan/0113 search-provider probe.

The first selection round set `OPENCODE_ENABLE_EXA=1` but never selected a
provider, so a non-interactive draw cancelled the provider form and the model
fell back to `webfetch` on DuckDuckGo. This probe pins the provider in the
per-draw config, runs one live `websearch` call under the pinned harness, and
records the provider the tool actually called. It also proves the controls: a
receipt naming another provider is void, and a search-engine fetch is foreign.

The probe writes `probe.json` and `evidence/` beside this file. The evidence is
committed; the scratch root under `/tmp/opencode/plan0113/search-provider/` is
not.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
BIN = HARNESS / ".prefix" / "opencode"
PIN_ENV = HARNESS / "pin.env"
MODEL_PIN = HARNESS / "model-pin" / "model-pin.json"
SCRATCH = Path("/tmp/opencode/plan0113/search-provider")
EVIDENCE = HERE / "evidence"
RECEIPT = HERE / "probe.json"

PROVIDER = "exa"
SEARCH_ENGINES = ("duckduckgo.com", "google.com", "bing.com", "search.yahoo.com")
QUERY = "OpenCode web search provider Exa"
PROMPT = (
    "Call the websearch tool exactly once with the query "
    f'"{QUERY}". Do not use webfetch or any other tool. After the tool returns, '
    "reply with the provider field from the tool metadata and nothing else."
)


def read_pin_env() -> dict[str, str]:
    values: dict[str, str] = {}
    for line in PIN_ENV.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value.strip().strip('"')
    return values


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def config_text() -> str:
    model = json.loads(MODEL_PIN.read_text())
    return (
        json.dumps(
            {
                "$schema": "https://opencode.ai/config.json",
                "model": f"{model['provider']}/{model['route']}",
                "provider": {
                    model["provider"]: {
                        "npm": "@ai-sdk/openai-compatible",
                        "name": model["provider"],
                        "options": {
                            "baseURL": "https://api.d07yx58.net/v1",
                            "apiKey": "{env:ROPE_BEARER}",
                        },
                        "models": {
                            model["route"]: {
                                "name": "Qwen3.8-Flash-Next (strata)",
                                "limit": {
                                    "context": model["max_input_tokens"],
                                    "input": model["max_input_tokens"],
                                    "output": model["max_output_tokens"],
                                },
                            }
                        },
                    }
                },
                "websearch": {"provider": PROVIDER},
                "lsp": False,
                "plugins": [],
            },
            indent=2,
        )
        + "\n"
    )


def parse_events(text: str) -> dict:
    websearch: list[dict] = []
    fetches: list[str] = []
    text_parts: list[str] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        part = event.get("part") or {}
        if event.get("type") == "text":
            text_parts.append(part.get("text") or "")
            continue
        if event.get("type") != "tool_use":
            continue
        state = part.get("state") or {}
        if part.get("tool") == "websearch" and state.get("status") == "completed":
            metadata = (state.get("metadata") or {}).get("metadata") or {}
            output = state.get("output") or ""
            url = re.search(r"## \[[^\]]*\]\((https?://[^)]+)\)", output)
            websearch.append(
                {
                    "provider": metadata.get("provider"),
                    "query": (state.get("input") or {}).get("query"),
                    "results": output.count("## ["),
                    "first_url": url.group(1) if url else None,
                    "event": event,
                }
            )
        if part.get("tool") == "webfetch" and state.get("status") == "completed":
            url = ((state.get("input") or {}).get("url") or "").strip()
            if url:
                fetches.append(url)
    return {
        "websearch": websearch,
        "fetches": fetches,
        "text": "\n".join(part for part in text_parts if part).strip(),
    }


def provider_of(receipt: dict, measured: str) -> None:
    if receipt.get("search_provider") != measured:
        raise ValueError(
            f"receipt names {receipt.get('search_provider')!r}; the tool called {measured!r}"
        )


def is_search_engine(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == engine or host.endswith("." + engine) for engine in SEARCH_ENGINES)


def main() -> int:
    if not BIN.is_file():
        raise SystemExit("the pinned binary is missing; run harness/install.sh")
    if not os.environ.get("ROPE_BEARER"):
        raise SystemExit("ROPE_BEARER is unset")
    pin = read_pin_env()
    model = json.loads(MODEL_PIN.read_text())
    root = SCRATCH / "run"
    if root.exists():
        shutil.rmtree(root)
    for part in ("home", "config/opencode", "data", "cache", "state", "work"):
        (root / part).mkdir(parents=True, exist_ok=True)
    config = config_text()
    (root / "config" / "opencode" / "opencode.json").write_text(config)

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
        "ROPE_BEARER": os.environ["ROPE_BEARER"],
    }
    started = time.time()
    completed = subprocess.run(
        [str(BIN), "run", "--format", "json", "--auto", PROMPT],
        cwd=root / "work",
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
    )
    wall = round(time.time() - started, 1)
    parsed = parse_events(completed.stdout)
    if not parsed["websearch"]:
        print(completed.stderr[-2000:], file=sys.stderr)
        raise SystemExit("the probe made no completed websearch call")
    call = parsed["websearch"][0]
    measured = call["provider"]
    if measured != PROVIDER:
        raise SystemExit(f"the tool called {measured!r}, expected {PROVIDER!r}")
    if not call["results"]:
        raise SystemExit("the websearch call returned no results")
    fetches = parsed["fetches"]
    foreign = [url for url in fetches if is_search_engine(url)]
    if foreign:
        raise SystemExit("the probe fetched a search engine: " + ", ".join(foreign))

    # Controls: the gates must reject a receipt that names another provider and
    # a draw that reaches a search engine through webfetch.
    controls = {"foreign_receipt": False, "foreign_fetch": False, "clean_receipt": False}
    try:
        provider_of({"search_provider": "parallel"}, measured)
    except ValueError:
        controls["foreign_receipt"] = True
    controls["foreign_fetch"] = is_search_engine("https://html.duckduckgo.com/html/?q=probe")
    provider_of({"search_provider": measured}, measured)
    controls["clean_receipt"] = True
    if not all(controls.values()):
        raise SystemExit(f"a control failed: {controls}")

    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "events.jsonl").write_text(completed.stdout)
    (EVIDENCE / "websearch-event.json").write_text(
        json.dumps(call["event"], indent=2, ensure_ascii=False) + "\n"
    )
    receipt = {
        "probe": "search-provider",
        "status": "pass",
        "recorded": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "harness": {
            "tag": pin["OPENCODE_TAG"],
            "binary_sha256": pin["OPENCODE_BINARY_SHA256"],
        },
        "model": {
            "provider": model["provider"],
            "route": model["route"],
            "deployment_id": model["deployment_id"],
            "backend": model["backend"],
        },
        "config": {
            "websearch": {"provider": PROVIDER},
            "env": ["OPENCODE_ENABLE_EXA=1"],
            "sha256": sha256_text(config),
        },
        "query": QUERY,
        "provider": measured,
        "websearch_calls": len(parsed["websearch"]),
        "results": call["results"],
        "first_url": call["first_url"],
        "wall_seconds": wall,
        "exit_code": completed.returncode,
        "events_sha256": sha256_file(EVIDENCE / "events.jsonl"),
        "controls": controls,
        "defect": {
            "selection_event_log": "/tmp/opencode/plan0113/selection/null-house-host-lint-docs/events.jsonl",
            "websearch_error": "Web search cancelled",
            "fallback_url": "https://html.duckduckgo.com/html/?q=%22host-lint%22+VOCABULARY.md+docs+lane",
            "cause": "the draw enabled Exa but selected no provider, so the non-interactive form was cancelled",
        },
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(
        f"PASS search-provider: {measured} returned {call['results']} result(s) "
        f"for {QUERY!r} in {wall}s; controls {controls}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
