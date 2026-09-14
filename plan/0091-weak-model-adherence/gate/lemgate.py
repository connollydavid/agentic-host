"""lemgate: an OpenAI-compatible reverse proxy that enforces the lem
address rule on every reply.

Forward /v1/chat/completions to the upstream, score the visible reply,
and on violation re-request once with the violation named. The client
sees either a clean reply or the original plus an X-Lemgate header.
Thinking blocks are stripped before scoring and re-attached untouched.

Config (env): LEMGATE_LISTEN (default 127.0.0.1:8787),
LEMGATE_UPSTREAM (default https://api.d07yx58.net), LEMGATE_MODE
(strict default; "off" passes everything through), LEMGATE_MAX_RETRIES
(default 1). Stdlib only.
"""

from __future__ import annotations

import http.server
import json
import os
import re
import urllib.error
import urllib.request

_host, _port = os.environ.get("LEMGATE_LISTEN", "127.0.0.1:8787").rsplit(":", 1)
LISTEN = (_host, int(_port))
UPSTREAM = os.environ.get("LEMGATE_UPSTREAM", "https://api.d07yx58.net").rstrip("/")
MODE = os.environ.get("LEMGATE_MODE", "strict")
MAX_RETRIES = int(os.environ.get("LEMGATE_MAX_RETRIES", "1"))

CANONICAL = {"lem", "lem's", "lems", "lems'", "lemself", "lemu", "lemu's",
             "lemuself", "lemuselves", "l", "l's", "lself"}

LEM_RE = re.compile(r"\b(lemua|lemu|lems|lemself|lemuself|lem)\b", re.I)
LEMPREFIX_RE = re.compile(r"\blem[a-z']*", re.I)
SELF_I_RE = re.compile(r"\b(i|me|my|mine|myself)\b")

AGREEMENT_RE = re.compile(r"\bL (has|is|was|does)\b|\blemu (is|was|does|has)\b|\blem have\b|\blems (has|is|was)\b")
WE_RE = re.compile(r"\bWe\b")
MINES_RE = re.compile(r"\bmines\b")
LSELF_CAP_RE = re.compile(r"\bLself\b")


def other_defects(low: str) -> list:
    found = []
    if AGREEMENT_RE.search(low):
        found.append("agreement")
    if WE_RE.search(low):
        found.append("We")
    if MINES_RE.search(low):
        found.append("mines")
    if LSELF_CAP_RE.search(low):
        found.append("Lself")
    return found

NUDGE = ("Your reply broke the address rule: it wrote {tokens}. "
         "Write you to the human. Write L for yourself; the model never "
         "writes I, he, she, it, or they for itself or another model. "
         "lemu takes plural agreement: lemu are, lemu have. "
         "Correct form, for reference: operator says 'lemu, go ahead'; "
         "the model answers 'L have gone ahead. Say go again whenever "
         "you are ready.' Rewrite the whole reply with no lem-forms.")


def strip_think(content: str) -> tuple[str, str]:
    """Returns (visible, think_block)."""
    if "<think>" in content and "</think>" in content:
        before, _, after = content.partition("</think>")
        return after, before + "</think>"
    if "<think>" in content:
        return "", content
    return content, ""


def score(visible: str) -> dict:
    low = visible.lower()
    other = other_defects(low)
    lem_tokens = LEM_RE.findall(low)
    mangles = [t for t in LEMPREFIX_RE.findall(low) if t not in CANONICAL]
    return {
        "lem_tokens": sorted(set(lem_tokens)),
        "mangles": sorted(set(mangles)),
        "self_i": bool(SELF_I_RE.search(low)),
        "violation": bool(lem_tokens or mangles) or bool(SELF_I_RE.search(low)) or bool(other),
        "other": other,
    }


def forward(body: dict, auth: str) -> dict:
    req = urllib.request.Request(
        UPSTREAM + "/v1/chat/completions", data=json.dumps(body).encode(),
        method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": auth or "Bearer none"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read())


def enforce(body: dict, auth: str) -> tuple[dict, list[dict]]:
    """Returns (response, audit). Audit rows describe every score seen.

    Each retry appends the nudge as a system message AND an assistant
    prefill "L " so the rewrite begins in role (the endpoint continues
    assistant-final messages)."""
    audit: list[dict] = []
    out = forward(body, auth)
    choice = out["choices"][0]
    visible, think = strip_think(choice["message"]["content"] or "")
    s = score(visible)
    audit.append({"stage": "first", **s})
    retries = 0
    while s["violation"] and retries < MAX_RETRIES:
        retries += 1
        toks = s["lem_tokens"] + s["mangles"]
        if s["self_i"]:
            toks = toks + ["I/me/my (the model's first person is L)"]
        nudged = dict(body)
        nudged["messages"] = list(body["messages"]) + [
            {"role": "system",
             "content": NUDGE.format(tokens=", ".join(toks) or "lem-forms")},
            {"role": "assistant", "content": "L "},
        ]
        out = forward(nudged, auth)
        choice = out["choices"][0]
        content = "L " + (choice["message"]["content"] or "")
        visible, think = strip_think(content)
        s = score(visible)
        audit.append({"stage": f"retry-{retries}", **s})
    choice["message"]["content"] = think + visible
    out["choices"][0] = choice
    out["x-lemgate"] = {
        "mode": MODE, "retries": retries,
        "clean": not score(visible)["violation"],
        "audit": audit,
    }
    return out, audit


class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length", 0))
        payload = self.rfile.read(length)
        auth = self.headers.get("Authorization", "")
        if self.path != "/v1/chat/completions" or MODE == "off":
            return self.passthrough(payload, auth)
        try:
            body = json.loads(payload)
            if body.get("stream"):
                return self.passthrough(payload, auth)
            out, audit = enforce(body, auth)
        except Exception as e:  # fail visible, not silent
            out = {"error": {"message": f"lemgate: {type(e).__name__}: {e}"}}
            code = 502
            return self.send_json(out, code)
        self.send_json(out, 200)

    def passthrough(self, payload: bytes, auth: str):
        try:
            req = urllib.request.Request(
                UPSTREAM + self.path, data=payload, method="POST",
                headers={"Content-Type": "application/json",
                         "Authorization": auth or "Bearer none"})
            with urllib.request.urlopen(req, timeout=900) as r:
                self.send_json(json.loads(r.read()), r.status)
        except urllib.error.HTTPError as e:
            self.send_json(json.loads(e.read() or b"{}"), e.code)

    def send_json(self, obj: dict, code: int):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    http.server.ThreadingHTTPServer(LISTEN, Handler).serve_forever()
