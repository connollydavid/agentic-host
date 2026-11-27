#!/usr/bin/env python3
"""The plan/0113 model pre-flight: the named strata route and the draw's replies.

`model-preflight.py` with no arguments fetches the router's `/model/info`
record and refuses unless the named route still resolves to the pinned
deployment, backend and limits. `--record PATH` reads a saved record instead
(for the probe's drift fixtures). `--replies PATH` checks a draw's reply
ledger, one JSON object per line with `provider` and `model`; one foreign
reply voids the draw.

The route name is strata's `qwen3.8-flash-next`; it resolves through the
`qwen*` wildcard entry, whose deployment id is the pin. The legacy
`qwen3.6-27b` name is foreign.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PIN = json.loads((HERE / "model-pin.json").read_text())


def void(message: str) -> None:
    print(f"VOID {message}", file=sys.stderr, flush=True)
    raise SystemExit(1)


def fetch_record() -> dict:
    url = PIN["route_url"]
    bearer = os.environ.get(PIN["bearer_env"], "")
    if not bearer:
        void(f"route: {PIN['bearer_env']} is unset; cannot read {url}")
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {bearer}"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def check_route(record: dict) -> None:
    entry_name = PIN.get("route_entry", PIN["route"])
    entries = [entry for entry in record.get("data", []) if entry.get("model_name") == entry_name]
    if len(entries) != 1:
        void(f"route: expected one entry {entry_name!r} for {PIN['route']!r}, found {len(entries)}")
    entry = entries[0]
    info = entry.get("model_info") or {}
    params = entry.get("litellm_params") or {}
    checks = (
        ("deployment id", info.get("id"), PIN["deployment_id"]),
        ("backend", params.get("model"), PIN["backend"]),
        ("max input tokens", info.get("max_input_tokens"), PIN["max_input_tokens"]),
        ("max output tokens", info.get("max_output_tokens"), PIN["max_output_tokens"]),
    )
    for label, got, pinned in checks:
        if got != pinned:
            void(f"route: {label} is {got!r}, pinned {pinned!r} for {PIN['route']!r}")
    print(
        f"model-preflight: ok route={PIN['route']} via={entry_name} "
        f"deployment={PIN['deployment_id']} backend={PIN['backend']} "
        f"limits={PIN['max_input_tokens']}/{PIN['max_output_tokens']}"
    )


def check_replies(path: Path) -> None:
    lines = [line for line in path.read_text().splitlines() if line.strip()]
    if not lines:
        void(f"replies: {path} carries no replies; a draw with no replies is not a pass")
    for number, line in enumerate(lines, 1):
        try:
            reply = json.loads(line)
        except json.JSONDecodeError as error:
            void(f"replies: line {number} is not JSON: {error}")
        provider = reply.get("provider")
        model = reply.get("model")
        if provider != PIN["provider"] or model != PIN["route"]:
            void(
                f"replies: line {number} carries provider={provider!r} model={model!r}, "
                f"pinned {PIN['provider']}/{PIN['route']}"
            )
    print(f"model-preflight: ok replies={len(lines)} all {PIN['provider']}/{PIN['route']}")


def main(argv: list[str]) -> int:
    record: Path | None = None
    replies: Path | None = None
    index = 0
    while index < len(argv):
        argument = argv[index]
        if argument == "--record" and index + 1 < len(argv):
            record = Path(argv[index + 1])
            index += 2
        elif argument == "--replies" and index + 1 < len(argv):
            replies = Path(argv[index + 1])
            index += 2
        else:
            print("usage: model-preflight.py [--record PATH] [--replies PATH]", file=sys.stderr)
            return 2
    if replies is not None:
        check_replies(replies)
        return 0
    check_route(json.loads(record.read_text()) if record else fetch_record())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
