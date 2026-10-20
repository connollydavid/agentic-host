"""Word-effectiveness sweep (plan/0101): which words in the teaching lines
earn their place on the weakest model. Real qwen3.5-4b, deployment sampling,
strict ACTION-line scoring, no LLM judge. Variants vary ONE dimension each."""
import json, urllib.request, pathlib, sys, time
TOKEN = pathlib.Path.home().joinpath(".edge-token").read_text().strip()
URL = "https://api.d07yx58.net/v1/chat/completions"
T = pathlib.Path("/tmp/opencode")
PROBES = {t: (T / f"{t.lower()}.txt").read_text() for t in ("P1", "P2", "P3", "P4")}

VARIANTS = {
 "V0-current": """You are the agent working inside a software project governed by the host loop. Tool output arrives in the user message. The tool output's NEXT line names your single next move. If NEXT is a command, run it exactly as printed. If NEXT says work <key>, begin that task. If the tool refused to emit, run the command on its last line. Reply with exactly one line starting with ACTION: naming that move. Nothing else.""",
 "V1-terse": """You work inside a software project governed by host loop. The tool output's NEXT line names your single next move. A command runs as printed. work <key> begins that task. A refusal's last line runs. Reply with one line: ACTION: the move.""",
 "V2-do-verb": """You are the agent working inside a software project governed by the host loop. Tool output arrives in the user message. The tool output's NEXT line names your single next move. If NEXT is a command, run it exactly as printed. If NEXT says do <key>, do that task now. If the tool refused to emit, run the command on its last line. Reply with exactly one line starting with ACTION: naming that move. Nothing else.""",
 "V3-format-first": """Reply with exactly one line starting with ACTION: naming your single next move. Nothing else. You are the agent working inside a software project governed by the host loop. The tool output's NEXT line names that move. If NEXT is a command, run it exactly as printed. If NEXT says work <key>, begin that task. If the tool refused to emit, run the command on its last line.""",
 "V4-no-frame": """The tool output's NEXT line names your single next move. If NEXT is a command, run it exactly as printed. If NEXT says work <key>, begin that task. If the tool refused to emit, run the command on its last line. Reply with exactly one line starting with ACTION: naming that move. Nothing else.""",
 "V5-ste-strict": """You run the host loop. The NEXT line of the tool output names your next move. Run a command as printed. If it says work <key>, start that task. If the tool stops, run the last line. Answer with one line: ACTION: <the move>.""",
}

def ask(sysmsg, prompt):
    body = json.dumps({"model": "qwen3.5-4b", "temperature": 0.6, "max_tokens": 1024,
                       "messages": [{"role": "system", "content": sysmsg},
                                    {"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(URL, data=body,
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=240) as r:
        return json.load(r)["choices"][0]["message"]["content"].strip()

def action_line(text):
    if "</think>" in text:
        text = text.split("</think>")[-1]
    for ln in text.splitlines():
        if ln.strip().lower().startswith("action:"):
            return ln.strip()
    return ""

def score(tag, a):
    low = a.lower()
    inv = "--force" in low or "--fix " in low
    if tag == "P1":
        ok = "plan/0101#run-loop" in low and any(w in low for w in ("work", "begin", "start", "do"))
    elif tag == "P2":
        ok = any(s in low for s in ("tasks --record", "ci --record", "goal repair", "re-derive"))
    elif tag == "P3":
        ok = "goal unpark" in low
    else:
        ok = "goal repair" in low
    return ok and not inv

results = {}
for name, sysmsg in VARIANTS.items():
    per = {"pass": 0, "total": 0, "invented": 0, "empty": 0, "rows": []}
    t0 = time.time()
    for tag in ("P1", "P2", "P3", "P4"):
        for rep in range(1, 5):
            try:
                a = action_line(ask(sysmsg, PROBES[tag]))
            except Exception as e:
                per["rows"].append(f"{tag} r{rep} ERROR {str(e)[:40]}"); continue
            if not a:
                per["empty"] += 1; per["rows"].append(f"{tag} r{rep} EMPTY"); continue
            inv = "--force" in a.lower() or "--fix " in a.lower()
            ok = score(tag, a) and not inv
            per["total"] += 1; per["pass"] += ok; per["invented"] += inv
            per["rows"].append(f"{tag} r{rep} {'PASS' if ok else 'FAIL'}: {a[:90]}")
    per["secs"] = round(time.time() - t0)
    results[name] = per
    print(f"== {name}: {per['pass']}/16 empty={per['empty']} invented={per['invented']} ({per['secs']}s)", flush=True)

pathlib.Path("/tmp/opencode/word-sweep/results.json").write_text(json.dumps(results, indent=1))
print("SWEEP-DONE")
