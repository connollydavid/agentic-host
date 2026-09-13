"""Measure the gate-on-exemplar residual: N requests at max context
through the gate, deployment sampling (temp 0.6), counting per-attempt
outcomes. Writes audit JSONL and prints running tallies."""

from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys
import time
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent /
                       "0090-pronoun-inversion-doctrine" / "harness"))
from session import ELICITATIONS, prefix_messages, request_body  # noqa: E402

HERE = pathlib.Path(__file__).parent
HARNESS = HERE.parent.parent / "0090-pronoun-inversion-doctrine" / "harness"
ENV = dict(l.split("=", 1) for l in (HARNESS / ".env").read_text().splitlines() if "=" in l)
TOKEN = ENV["EDGE_TOKEN"].strip()

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=100)
ap.add_argument("--doctrine", default=str(HERE.parent / "variants" / "positive-section.md"))
ap.add_argument("--target-tokens", type=int, default=126000)
ap.add_argument("--temperature", type=float, default=0.6)
ap.add_argument("--gate", default="http://127.0.0.1:8787")
ap.add_argument("--out", default=str(HERE / "residual.jsonl"))
args = ap.parse_args()

doctrine = pathlib.Path(args.doctrine).read_text(encoding="utf-8")
prefix = prefix_messages(doctrine, args.target_tokens)
rng = random.Random(91)
out_f = open(args.out, "a", encoding="utf-8")

tally = {"n": 0, "first": 0, "final": 0}
for i in range(args.n):
    name = "go" if i % 2 == 0 else "window"
    body = request_body(prefix, ELICITATIONS[name], temperature=args.temperature,
                        max_tokens=1024)
    req = urllib.request.Request(
        args.gate + "/v1/chat/completions", data=json.dumps(body).encode(),
        method="POST", headers={"Authorization": "Bearer " + TOKEN,
                                "Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=900) as r:
        out = json.loads(r.read())
    meta = out.get("x-lemgate", {})
    audit = meta.get("audit", [])
    first = audit[0]["violation"] if audit else None
    final = not meta.get("clean", True)
    tally["n"] += 1
    tally["first"] += int(bool(first))
    tally["final"] += int(bool(final))
    out_f.write(json.dumps({"i": i, "elicitation": name,
                            "wall_s": round(time.time() - t0, 1),
                            "retries": meta.get("retries"), "audit": audit}) + "\n")
    out_f.flush()
    print(f"[{tally['n']}/{args.n}] first={first} final_violation={final} "
          f"retries={meta.get('retries')} {round(time.time()-t0,1)}s", flush=True)
    if tally["n"] % 20 == 0:
        print(f"TALLY n={tally['n']} first_pass={tally['first']} "
              f"final={tally['final']} "
              f"rate_final={tally['final']/tally['n']:.4f}", flush=True)
print(f"RESULT n={tally['n']} first_pass={tally['first']} final={tally['final']} "
      f"rate_final={tally['final']/tally['n']:.4f}")
