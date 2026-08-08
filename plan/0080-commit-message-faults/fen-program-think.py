#!/usr/bin/env python3
"""Thinking-protocol rerun of the lint#28 convening ballots and probes.

Operator-directed 2026-08-08: thinking stays on for the 4B. Parameters are the
Qwen3.5-4B card's thinking-general set exactly as plan/0076's corrected
protocol recorded them (temperature 1.0, top_p 0.95, top_k 20, min_p 0.0,
presence_penalty 1.5, repetition_penalty 1.0, max_tokens 32768,
chat_template_kwargs.enable_thinking true); the answer is read after the
closing </think>. The no-think kit (fen-program.py) and its truncated run
(fen-results-spoiled-truncated.md) stay preserved beside this file.

Channel and credentials arrive via FEN_ENDPOINT / FEN_TOKEN / FEN_MODEL, all
required. Ballot cells run in two option orders as in the kit; each probe runs
two draws at the same params (the no-think kit's two-temperature axis has no
counterpart in this protocol). Results append to fen-results.md after every
cell, so a mid-run failure preserves the completed cells."""
import json, os, urllib.request

SCRATCH = os.path.dirname(os.path.abspath(__file__))
ENDPOINT = os.environ["FEN_ENDPOINT"]
TOKEN = os.environ["FEN_TOKEN"]
MODEL = os.environ["FEN_MODEL"]

PARAMS = {"temperature": 1.0, "top_p": 0.95, "top_k": 20, "min_p": 0.0,
          "presence_penalty": 1.5, "repetition_penalty": 1.0,
          "max_tokens": 32768}


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
    think = c.get("reasoning_content") or ""
    if think and "</think>" not in text:
        text = f"<think>{think}</think>\n{text}"
    return d.get("model", ""), text


def tail_of(text):
    if "</think>" in text:
        return text.split("</think>")[-1].strip() or "(empty answer after think)"
    return "(no think block: whole content is the answer)\n" + text.strip()


BALLOTS = {
 "Q1": ("A linter warns when a commit message repeats a sentence from a comment the commit adds. It needs the commit message and the staged diff.",
  {"X": "the linter runs git itself to read the staged diff when run inside a repository.",
   "Y": "the commit hook saves the diff to a file and passes it to the existing lint command as an extra flag.",
   "Z": "a new command `host-lint commit` takes two named files, the message and the diff."},
  "You are a small agent using this tool and re-running it after editing the message."),
 "Q2": ("The repeated-sentence warning fires when the sentence is long enough.",
  {"X": "fire on sentences of eight words or more, only at commit time.",
   "Y": "fire on five words or more, catching more but also short generic sentences.",
   "Z": "fire on eight words or more at commit time and also when checking documentation files, where no staged diff exists."},
  ""),
 "Q3": ("A second possible warning would flag justification-by-precedent phrases such as 'many other projects already do this'. It was tested against nine hundred and twenty-two accepted commit messages and matched none.",
  {"X": "do not build it; write the phrase shapes into guidance and build only if one ever appears.",
   "Y": "build it anyway as an advisory warning at commit time.",
   "Z": "build it into the shared grammar library used by every text check."},
  ""),
 "Q4": ("Some writing guidance cannot be machine-checked, for example 'describe the change, do not argue for it'. Where should it live?",
  {"X": "in the instructions an agent loads when writing commits, marked as guidance the tool does not check.",
   "Y": "in the rulebook file that otherwise lists only rules the tool enforces.",
   "Z": "nowhere; guidance the tool cannot check should not be written."},
  ""),
 "Q5": ("Two linter improvements will be ready around the same time: the repeated-sentence warning, and a separate allow-list for headings that look like version names.",
  {"X": "ship both in one release.",
   "Y": "ship the finished one first and the other in a later release.",
   "Z": "hold both until more design work is done."},
  ""),
}


def ballot_prompt(intro, opts, tail, order):
    lines = [intro, ""]
    for k in order:
        lines.append(f"{k}) {opts[k]}")
    if tail:
        lines += ["", tail]
    lines += ["", "Rank the three options best to worst (for example: 'Z, X, Y') and give one short reason."]
    return "\n".join(lines)


def main():
    served, text = ask("Reply with the single word: ready")
    if "ready" not in text.lower():
        print(f"NO CHANNEL: ready check did not answer ready (served model: {served})")
        raise SystemExit(1)
    print(f"channel ok, served model: {served}")

    cells = []
    for q, (intro, opts, tail) in BALLOTS.items():
        for tag, order in (("order-XYZ", ["X", "Y", "Z"]), ("order-ZYX", ["Z", "Y", "X"])):
            cells.append((f"{q} {tag}", ballot_prompt(intro, opts, tail, order)))
    for fname, label in (("fen-p1.txt", "P1-bare"), ("fen-p1-worded.txt", "P1-worded"),
                         ("fen-p2.txt", "P2-guidance")):
        text = open(os.path.join(SCRATCH, fname)).read()
        for draw in (1, 2):
            cells.append((f"{label} draw{draw}", text))

    results = os.path.join(SCRATCH, "fen-results.md")
    with open(results, "w") as f:
        f.write(f"# Real Fen results (thinking protocol, card params; served model: {served})\n\n"
                "Operator-directed 2026-08-08: thinking on for the 4B, plan/0076\n"
                "corrected-protocol sampling, answers read after </think>.\n")
    for label, prompt in cells:
        m, text = ask(prompt)
        with open(results, "a") as f:
            f.write(f"\n## {label}\n\n{text}\n\n### answer tail\n{tail_of(text)}\n")
        print(f"{label} done")
    print("written: fen-results.md")


if __name__ == "__main__":
    main()
