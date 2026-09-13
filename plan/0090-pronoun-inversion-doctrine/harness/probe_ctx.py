"""Probe the edge for the served maximum context of qwen3.5-4b.

Sends padding of increasing size and reads the server's verdict: a success
reports usage.prompt_tokens (checked against the request, so silent
left-truncation cannot pass unnoticed); a context-length error names the
ceiling. Reads EDGE_BASE and EDGE_TOKEN from .env beside this file.
"""

import json
import pathlib
import sys
import urllib.request

HERE = pathlib.Path(__file__).parent
env = {}
for line in (HERE / ".env").read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()

BASE, TOKEN = env["EDGE_BASE"], env["EDGE_TOKEN"]
MODEL = "qwen3.5-4b"
PAD = ("order review gateway checkpoint digest ledger pipeline corpus "
       "snapshot manifest channel receipt buffer offset payload ").split()


def pad_text(words: int) -> str:
    return " ".join(PAD[i % len(PAD)] for i in range(words))


def probe(n_words: int) -> None:
    text = pad_text(n_words) + "\n\nReply with the single word ok."
    body = json.dumps({
        "model": MODEL, "max_tokens": 8,
        "messages": [{"role": "user", "content": text}],
    }).encode()
    req = urllib.request.Request(
        BASE + "/v1/chat/completions", data=body, method="POST",
        headers={"Authorization": "Bearer " + TOKEN,
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            out = json.loads(r.read())
        usage = out.get("usage", {})
        pt = usage.get("prompt_tokens")
        flag = "" if pt and abs(pt - (n_words + 9)) <= n_words // 20 else "  <-- PROMPT COUNT MISMATCH (truncation?)"
        print(f"words={n_words:>7}  OK   prompt_tokens={pt}{flag}")
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        print(f"words={n_words:>7}  HTTP {e.code}  {detail}")
        if e.code == 400:
            sys.exit(0)
    except Exception as e:
        print(f"words={n_words:>7}  ERROR {type(e).__name__}: {e}")


for n in [1000, 8000, 24000, 48000, 96000, 160000, 200000, 240000, 280000, 320000]:
    probe(n)
