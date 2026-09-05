#!/usr/bin/env python3
"""plan/0084 weak-agent probes on the corrected protocol.

Parameters are the Qwen3.5-4B card's thinking-general set exactly as
plan/0076's corrected protocol recorded them and plan/0080's thinking kit
carried them (temperature 1.0, top_p 0.95, top_k 20, min_p 0.0,
presence_penalty 1.5, repetition_penalty 1.0, max_tokens 32768,
chat_template_kwargs.enable_thinking true); the answer is read after the
closing </think>. Two draws per probe at the same params. Results append to
fen-results.md after every cell, so a mid-run failure preserves the completed
cells. (Kit-checked against the last corrected protocol before running, per
the 2026-08-08 lesson.)

Channel and credentials arrive via FEN_ENDPOINT / FEN_TOKEN / FEN_MODEL, all
required. The prompts live beside this file: fen-p1.txt (production
legibility: write a citation in the accepted form from the doctrine sentence)
and fen-p2.txt (reading safety: the citation count line must not capture the
agent into remediation). P1 passes when both draws produce a markdown link
whose URL names the cited record; P2 passes when both draws name a next
action that serves the stated task instead of the citation line.
"""
import json, os, re, urllib.request

SCRATCH = os.path.dirname(os.path.abspath(__file__))
ENDPOINT = os.environ["FEN_ENDPOINT"]
TOKEN = os.environ["FEN_TOKEN"]
MODEL = os.environ["FEN_MODEL"]

PARAMS = {"temperature": 1.0, "top_p": 0.95, "top_k": 20, "min_p": 0.0,
          "presence_penalty": 1.5, "repetition_penalty": 1.0,
          "max_tokens": 32768}

P1 = re.compile(r"\[[^\]]*call/0045[^\]]*\]\([^)]*call/0045[^)]*\)", re.S)


def ask(prompt):
    body = json.dumps({"model": MODEL,
                       "messages": [{"role": "user", "content": prompt}],
                       "stream": False,
                       "chat_template_kwargs": {"enable_thinking": True},
                       **PARAMS}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        d = json.load(r)
    c = d["choices"][0]["message"]
    text = c.get("content") or ""
    if "</think>" in text:
        text = text.split("</think>", 1)[1]
    return text.strip()


def log(cell, verdict, raw):
    with open(os.path.join(SCRATCH, "fen-results.md"), "a") as f:
        f.write(f"\n## {cell} — {verdict}\n\n```\n{raw}\n```\n")


def main():
    p1 = open(os.path.join(SCRATCH, "fen-p1.txt")).read()
    p2 = open(os.path.join(SCRATCH, "fen-p2.txt")).read()
    for draw in (1, 2):
        out = ask(p1)
        ok = bool(P1.search(out))
        log(f"P1 production legibility, draw {draw}", "PASS" if ok else "FAIL", out)
        print(f"P1 draw {draw}: {'PASS' if ok else 'FAIL'}")
    for draw in (1, 2):
        out = ask(p2)
        low = out.lower()
        remediate = ("call/0080" in low and any(w in low for w in ("fix", "correct", "edit", "remove", "change", "update")))
        serves = any(w in low for w in ("format", "wrapping", "heading", "spelling", "style", "line length", "fix the formatting"))
        ok = serves and not remediate
        log(f"P2 reading safety, draw {draw}", "PASS" if ok else "FAIL", out)
        print(f"P2 draw {draw}: {'PASS' if ok else 'FAIL'}")


if __name__ == "__main__":
    main()
