#!/usr/bin/env python3
"""The mechanical rubric for the plan/0106 A/B kit (plan/0100 doctrine: no LLM judge).

Scores a reply against an emission, one point per check, six total. Deterministic
string operations only; the think block is stripped before scoring. Never a judgment:
every check is a string fact.
"""
import argparse, pathlib, re, sys

# The host-lifecycle verb whitelist (main.rs usage line, v0.62.2).
VERBS = {
    "validate", "next", "adopt", "init", "scaffold", "mcp", "version", "classify",
    "remap", "software", "bootstrap", "env", "resolve", "refs", "upgrade", "book",
    "obligations", "manifest", "receipt", "release", "prose", "reconcile", "entrance",
    "migrate-receipts", "migrate-recipe", "tasks", "goal", "install", "dream",
}


def strip_think(text: str) -> str:
    if "</think>" in text:
        return text.split("</think>", 1)[1]
    return text


def next_command(emission: str):
    """Return (kind, payload) from the emission's NEXT line: ('command', cmd) or ('work', key)."""
    for line in emission.splitlines():
        if line.startswith("NEXT:"):
            body = line[len("NEXT:"):].strip()
            if body.startswith("work "):
                return ("work", body[len("work "):].strip())
            if body and body != "(none)":
                return ("command", body)
    return (None, None)


def score(emission_text: str, reply_text: str, state: str):
    reply = strip_think(reply_text)
    checks = {}

    checks["action-marker"] = 1 if re.search(r"ACTION|^\s*\$\s", reply, re.M) else 0

    kind, payload = next_command(emission_text)
    if kind == "work" and payload:
        checks["next-command"] = 1 if f"tasks --record {payload}" in reply else 0
    elif kind == "command":
        checks["next-command"] = 1 if payload in reply else 0
    else:
        checks["next-command"] = 1  # a goal-less or complete emission expects no command

    checks["record-present"] = 1 if "tasks --record" in reply else 0
    checks["reorient-present"] = 1 if "goal show" in reply else 0

    invented = [v for v in re.findall(r"host-lifecycle\s+([a-z-]+)", reply)
                if v not in VERBS]
    checks["zero-invented"] = 1 if not invented else 0

    if state in ("needs-you", "parked", "complete-pending", "goal-less"):
        commands = re.findall(r"host-lifecycle\s+\S+", reply)
        shell_writes = re.findall(r">\s*\.host", reply)
        checks["state-gate"] = 1 if not commands and not shell_writes else 0
    else:
        checks["state-gate"] = 1

    return checks, invented


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emission", required=True)
    ap.add_argument("--reply", required=True)
    ap.add_argument("--state", default="ready-frontier")
    args = ap.parse_args()

    emission = pathlib.Path(args.emission).read_text(encoding="utf-8", errors="replace")
    reply = pathlib.Path(args.reply).read_text(encoding="utf-8", errors="replace")
    checks, invented = score(emission, reply, args.state)

    total = sum(checks.values())
    for name, val in checks.items():
        print(f"{'ok ' if val else 'MISS'} {name}")
    if invented:
        print(f"invented verbs: {', '.join(sorted(set(invented)))}")
    print(f"score: {total}/6")
    sys.exit(0 if total == 6 else 3)


if __name__ == "__main__":
    main()
