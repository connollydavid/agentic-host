"""Run one variant of the lem section through the echo-amplification probe.

Usage: python run_variant.py --doctrine doctrine_current.md --name baseline
                            [--draws 8] [--elicitations go,window]

Per draw: one chat completion over the fixed prefix plus one elicitation.
The scorer strips the think block and counts, in the visible reply:
  - inversion  : any lem-family token at all (in a reply to the operator,
                 no lem-form should ever appear)
  - mangle     : a lem-prefixed token outside the canonical paradigm
  - self_i     : a first-person token (the model's first person is L)
Writes one JSON transcript per draw under samples/<name>/ and a summary.json.
Prints: RESULT name=<name> inversions=<k> mangles=<m> self_i=<s> valid=<v> draws=<n> rate=<k/v>
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import time
import urllib.request

from session import ELICITATIONS, prefix_messages, request_body

HERE = pathlib.Path(__file__).parent

env = {}
for line in (HERE / ".env").read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
BASE, TOKEN = env["EDGE_BASE"].strip(), env["EDGE_TOKEN"].strip()

CANONICAL = {"lem", "lem's", "lems", "lems'", "lemself", "lemu", "lemu's",
             "lemuself", "lemuselves", "l", "l's", "lself"}

INVERSION_RE = re.compile(r"\b(lemua|lemu|lems|lemself|lemuself|lem)\b", re.I)
MANGLE_RE = re.compile(r"\blem[a-z']*", re.I)
SELF_I_RE = re.compile(r"\b(i|me|my|mine|myself)\b")


def score(reply: str) -> dict:
    low = reply.lower()
    tokens = MANGLE_RE.findall(low)
    mangles = [t for t in tokens if t not in CANONICAL]
    return {
        "inversion": bool(INVERSION_RE.search(low)),
        "inversion_tokens": sorted(set(INVERSION_RE.findall(low))),
        "mangle": bool(mangles),
        "mangle_tokens": sorted(set(mangles)),
        "self_i": bool(SELF_I_RE.search(low)),
    }


def strip_think(content: str) -> tuple[str, bool]:
    """The visible reply: text after a closed think block. Returns
    (text, think_closed). An unclosed block means the budget ran out
    mid-think and the draw has no visible reply."""
    if "<think>" not in content:
        return content, True
    if "</think>" not in content:
        return "", False
    return content.split("</think>", 1)[1], True


def post(body: dict, timeout: int = 900) -> dict:
    req = urllib.request.Request(
        BASE + "/v1/chat/completions", data=json.dumps(body).encode(),
        method="POST",
        headers={"Authorization": "Bearer " + TOKEN,
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--doctrine", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--draws", type=int, default=8)
    ap.add_argument("--elicitations", default="go,window")
    ap.add_argument("--target-tokens", type=int, default=126000)
    ap.add_argument("--max-tokens", type=int, default=1024)
    ap.add_argument("--temperature", type=float, default=0.8)
    ap.add_argument("--framing", choices=["named", "neutral"], default="named")
    ap.add_argument("--thinking", action="store_true")
    ap.add_argument("--tail-line", default=None)
    ap.add_argument("--fewshot", action="store_true")
    ap.add_argument("--prefill", default=None)
    args = ap.parse_args()

    doctrine = pathlib.Path(args.doctrine).read_text(encoding="utf-8")
    prefix = prefix_messages(doctrine, args.target_tokens, framing=args.framing,
                             tail_line=args.tail_line, fewshot=args.fewshot)
    names = [e.strip() for e in args.elicitations.split(",") if e.strip()]
    for n in names:
        if n not in ELICITATIONS:
            sys.exit(f"unknown elicitation {n!r}; known: {', '.join(ELICITATIONS)}")

    out_dir = HERE / "samples" / args.name
    out_dir.mkdir(parents=True, exist_ok=True)

    results, prompt_tokens_seen = [], []
    for name in names:
        for draw in range(args.draws):
            body = request_body(prefix, ELICITATIONS[name],
                                temperature=args.temperature,
                                max_tokens=args.max_tokens,
                                thinking=args.thinking, prefill=args.prefill)
            t0 = time.time()
            out = post(body)
            choice = out["choices"][0]
            content = choice["message"]["content"] or ""
            reply, closed = strip_think(content)
            if not closed or not reply.strip():
                body["max_tokens"] = args.max_tokens * 2
                out = post(body)
                choice = out["choices"][0]
                content = choice["message"]["content"] or ""
                reply, closed = strip_think(content)
            usage = out.get("usage", {})
            prompt_tokens_seen.append(usage.get("prompt_tokens"))
            rec = {
                "name": args.name, "elicitation": name, "draw": draw,
                "finish_reason": choice.get("finish_reason"),
                "think_closed": closed,
                "valid": bool(closed and reply.strip()),
                "prompt_tokens": usage.get("prompt_tokens"),
                "wall_s": round(time.time() - t0, 1),
                "reply": reply.strip(),
                "raw": content,
                "score": score(reply),
            }
            results.append(rec)
            (out_dir / f"{name}-{draw:02d}.json").write_text(
                json.dumps(rec, indent=1), encoding="utf-8")
            s = rec["score"]
            print(f"[{args.name}] {name}#{draw:02d} "
                  f"valid={int(rec['valid'])} inv={int(s['inversion'])} "
                  f"mangle={int(s['mangle'])} self_i={int(s['self_i'])} "
                  f"ptok={rec['prompt_tokens']} {rec['wall_s']}s", flush=True)

    valid = [r for r in results if r["think_closed"] and r["reply"].strip()]
    inversions = sum(1 for r in valid if r["score"]["inversion"])
    mangles = sum(1 for r in valid if r["score"]["mangle"])
    self_i = sum(1 for r in valid if r["score"]["self_i"])
    rate = inversions / len(valid) if valid else 0.0
    summary = {
        "name": args.name, "draws": len(results), "valid": len(valid),
        "inversions": inversions, "mangles": mangles, "self_i": self_i,
        "rate": round(rate, 4),
        "prompt_tokens_seen": sorted(set(filter(None, prompt_tokens_seen))),
        "temperature": args.temperature, "max_tokens": args.max_tokens,
        "framing": args.framing, "thinking": args.thinking,
        "tail_line": args.tail_line, "fewshot": args.fewshot,
        "prefill": args.prefill,
        "target_tokens": args.target_tokens,
        "doctrine_file": args.doctrine,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1),
                                          encoding="utf-8")
    print(f"RESULT name={args.name} inversions={inversions} mangles={mangles} "
          f"self_i={self_i} valid={len(valid)} draws={len(results)} "
          f"rate={rate:.4f}")


if __name__ == "__main__":
    main()
