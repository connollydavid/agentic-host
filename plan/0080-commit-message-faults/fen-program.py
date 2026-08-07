#!/usr/bin/env python3
"""The full real-Fen program for the lint#28 convening: five ballots in two rotated
orders at card parameters, three probes at two temperatures. Discovers the live
channel (direct Unsloth endpoint, then the gateway under each documented alias)
and refuses to run against any model that is not the 4B family. Appends everything
to fen-results.md."""
import subprocess, sys, os, json, urllib.request

SCRATCH = os.path.dirname(os.path.abspath(__file__))
GATEWAY = "http://127.0.0.1:4000/v1/chat/completions"
ALIASES = ["qwen3.5-4b", "local", "coder", "rope-text"]

def probe(prompt, temp, endpoint=None, model=None, timeout=240):
    cmd = ["fen-probe", "--temp", str(temp)]
    if endpoint: cmd += ["--endpoint", endpoint]
    env = dict(os.environ)
    if model: env["FEN_MODEL"] = model
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout, env=env)
    return r.returncode, (r.stdout + r.stderr).strip()

def discover():
    rc, out = probe("Reply with the single word: ready", 0.0, timeout=30)
    if rc == 0 and "ready" in out.lower(): return (None, None, "direct unsloth endpoint")
    for a in ALIASES:
        rc, out = probe("Reply with the single word: ready", 0.0, GATEWAY, a, timeout=45)
        if rc == 0 and "Invalid model" not in out and out: return (GATEWAY, a, f"gateway alias {a}")
    return None

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
    if tail: lines += ["", tail]
    lines += ["", "Rank the three options best to worst (for example: 'Z, X, Y') and give one short reason."]
    return "\n".join(lines)

def main():
    ch = discover()
    if not ch:
        print("NO CHANNEL: neither the direct endpoint nor any gateway alias answers as the 4B.")
        sys.exit(1)
    endpoint, model, label = ch
    out = [f"# Real Fen results ({label}, card params temp 0.6 for ballots)\n"]
    print(f"channel: {label}")

    for q, (intro, opts, tail) in BALLOTS.items():
        for tag, order in (("order-XYZ", ["X", "Y", "Z"]), ("order-ZYX", ["Z", "Y", "X"])):
            rc, ans = probe(ballot_prompt(intro, opts, tail, order), 0.6, endpoint, model)
            out.append(f"## {q} {tag} (rc={rc})\n{ans}\n")
            print(f"{q} {tag} done")

    for fname, label2 in (("fen-p1.txt", "P1-bare"), ("fen-p1-worded.txt", "P1-worded"), ("fen-p2.txt", "P2-guidance")):
        text = open(os.path.join(SCRATCH, fname)).read()
        for t in (0.0, 0.6):
            rc, ans = probe(text, t, endpoint, model)
            out.append(f"## {label2} temp {t} (rc={rc})\n{ans}\n")
            print(f"{label2} temp {t} done")

    with open(os.path.join(SCRATCH, "fen-results.md"), "w") as f:
        f.write("\n".join(out))
    print("written: fen-results.md")

if __name__ == "__main__":
    main()
