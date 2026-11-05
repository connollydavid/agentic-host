#!/usr/bin/env python3
"""The plan/0106 draw harness: prompt arms over the continuation body, Fen as the subject.

The plan/0088 kit shape, adapted to the rope channel: draws saved unedited to
samples/<state>-<arm>-<n>.md, the think block stripped only for scoring. Credentials
arrive via the environment: FEN_ENDPOINT (required for live draws; the direct LAN
endpoint needs no token, the WAN edge needs the bearer in FEN_TOKEN). No explicit
sampling params are sent by default: the server's thinking recipe is the deployment
envelope. Selection rounds are exploratory; the confirmation protocol is pre-declared
in the plan README's design gates, never improvised here.
"""
import json, os, pathlib, sys, urllib.request

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from rubric import score, strip_think  # noqa: E402

ENDPOINT = os.environ.get("FEN_ENDPOINT", "")
TOKEN = os.environ.get("FEN_TOKEN", "ignored-by-direct-endpoint")
MODEL = os.environ.get("FEN_MODEL", "qwen3.5-4b")
DRAWS = int(os.environ.get("FEN_DRAWS", "3"))
MAX_TOKENS = min(int(os.environ.get("FEN_MAX_TOKENS", "8192")), 8192)

DOCTRINE = (
    "\n\nWork the NEXT line. If it is a command, run it as printed. If it says work a "
    "task, start that task. Never invent a command or a flag. NEEDS YOU non-none means "
    "ask the operator and nothing else runs. Record each done task with the tasks verb. "
    "Then re-orient with goal show."
)

EXEMPLAR = (
    "\n\nA correct reply runs the NEXT line's work, records the receipt, and re-orients:\n"
    "ACTION:\n"
    "$ <the verify or work the NEXT line names>\n"
    "$ host-lifecycle tasks --record <the task key> --disposition done .\n"
    "$ host-lifecycle goal show ."
)

ARMS = {
    "A": lambda e: f"{e}\n\nWork the NEXT line.",
    "B": lambda e: f"{e}{DOCTRINE}",
    "C": lambda e: f"{e}{DOCTRINE}{EXEMPLAR}",
    "D": lambda e: f"{e}\n\nNever invent a command or a flag.{DOCTRINE}",
}

# The plan/0110 arms (round 2): the belt's own text, byte-faithful to
# software/host-loop/main/index.ts (the REMINDER constant with its
# "[host-loop reminder]\n" wrapper, the context hook's payload). R0 is the
# shipped default, the incumbent continuation shape (arm B's construction,
# the doctrine without the belt); R1 is R0 with the belt riding at the tail,
# the position the hook splices to. FEN_ARMS selects a subset so a round
# runs its protocol's arms without re-drawing the recorded ones.
REMINDER = "\n".join([
    "Record each done task with the exact command, passing the verify output:",
    "ACTION: $ host-lifecycle tasks --record <the task key> --disposition done --evidence <the verify output> .",
    "Never invent a command or a flag; never hand-edit a state file.",
    "NEEDS YOU non-none means ask the operator and run nothing.",
])
ARMS["R0"] = lambda e: f"{e}{DOCTRINE}"
ARMS["R1"] = lambda e: f"{e}{DOCTRINE}\n\n[host-loop reminder]\n{REMINDER}"


def ask(prompt: str) -> str:
    body = json.dumps({"model": MODEL,
                       "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": MAX_TOKENS,
                       "stream": False}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={
        "Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        d = json.load(r)
    return d["choices"][0]["message"].get("content") or ""


def main():
    if not ENDPOINT:
        sys.exit("refusing: FEN_ENDPOINT is required for live draws (the dry run is rubric.py on the controls)")
    emission_file = sys.argv[1] if len(sys.argv) > 1 else "emission.txt"
    state = sys.argv[2] if len(sys.argv) > 2 else "ready-frontier"
    emission = pathlib.Path(emission_file).read_text(encoding="utf-8", errors="replace")
    out = HERE / "samples"
    out.mkdir(exist_ok=True)
    table = []
    # FEN_INTERLEAVE=1 draws round-robin (the plan/0100 protocol: fixed arm order
    # entangles with within-round drift); the default keeps the arm-serial shape.
    only = [a.strip() for a in os.environ.get("FEN_ARMS", "").split(",") if a.strip()]
    arm_names = only or sorted(ARMS)
    if os.environ.get("FEN_INTERLEAVE") == "1":
        schedule = [(arm, n) for n in range(1, DRAWS + 1) for arm in arm_names]
    else:
        schedule = [(arm, n) for arm in arm_names for n in range(1, DRAWS + 1)]
    for arm, n in schedule:
        build = ARMS[arm]
        raw = ask(build(emission))
        path = out / f"{state}-{arm}-{n}.txt"
        path.write_text(raw, encoding="utf-8")
        checks, invented = score(emission, raw, state)
        total = sum(checks.values())
        table.append((state, arm, n, total, ",".join(sorted(set(invented)))))
        print(f"{state} {arm} draw {n}: {total}/6"
              + (f" invented: {table[-1][4]}" if table[-1][4] else ""), flush=True)
    print("\nstate arm n score")
    for row in table:
        print(" ".join(str(x) for x in row))


if __name__ == "__main__":
    main()
