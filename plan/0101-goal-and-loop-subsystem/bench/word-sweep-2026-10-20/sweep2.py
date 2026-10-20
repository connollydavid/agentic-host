"""Word-effectiveness sweep, round two (plan/0101): within-structure variants
against the V5 incumbent, informed by round one. Same instrument: real
qwen3.5-4b, deployment sampling, strict ACTION scoring, zero-invented."""
import json, urllib.request, pathlib, time
TOKEN = pathlib.Path.home().joinpath(".edge-token").read_text().strip()
URL = "https://api.d07yx58.net/v1/chat/completions"
T = pathlib.Path("/tmp/opencode")
PROBES = {t: (T / f"{t.lower()}.txt").read_text() for t in ("P1", "P2", "P3", "P4")}

V5 = """You run the host loop. The NEXT line of the tool output names your next move. Run a command as printed. If it says work <key>, start that task. If the tool stops, run the last line. Answer with one line: ACTION: <the move>."""

VARIANTS = {
 "R0-v5-incumbent": V5,
 "R1-v5-needs-you": V5.replace("Answer with one line", "If NEEDS YOU is not none, ask the operator first; nothing else runs. Answer with one line"),
 "R2-v5-numbered": """You run the host loop. The NEXT line of the tool output names your next move. Rules: 1. Run a command as printed. 2. If it says work <key>, start that task. 3. If the tool stops, run the last line. 4. Answer with one line: ACTION: <the move>.""",
 "R3-v5-exemplar": V5.replace("Answer with one line: ACTION: <the move>.", "Example: NEXT: host-lifecycle goal unpark . -> ACTION: host-lifecycle goal unpark . Answer with one line: ACTION: <the move>."),
 "R4-v5-never": V5.replace("Answer with one line", "Never invent a command or a flag. Answer with one line"),
 "R5-v5-no-frame": """The NEXT line of the tool output names your next move. Run a command as printed. If it says work <key>, start that task. If the tool stops, run the last line. Answer with one line: ACTION: <the move>.""",
 "R6-v5-ex-needs": V5.replace("If the tool stops, run the last line.", "If the tool stops, run the last line. If NEEDS YOU is not none, ask the operator first.").replace("Answer with one line: ACTION: <the move>.", "Example: NEXT: host-lifecycle goal unpark . -> ACTION: host-lifecycle goal unpark . Answer with one line: ACTION: <the move>."),
}

def ask(sysmsg, prompt):
    body = json.dumps({"model": "qwen3.5-4b", "temperature": 0.6, "max_tokens": 1024,
                       "messages": [{"role": "system", "content": sysmsg},
                                    {"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
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
    if tag == "P1":
        return "plan/0101#run-loop" in low and any(w in low for w in ("work", "begin", "start", "do"))
    if tag == "P2":
        return any(s in low for s in ("tasks --record", "ci --record", "goal repair", "re-derive"))
    if tag == "P3":
        return "goal unpark" in low
    return "goal repair" in low

results = {}
for name, sysmsg in VARIANTS.items():
    per = {"pass": 0, "empty": 0, "invented": 0, "per_probe": {}, "rows": []}
    t0 = time.time()
    for tag in ("P1", "P2", "P3", "P4"):
        pcount = 0
        for rep in range(1, 5):
            try:
                a = action_line(ask(sysmsg, PROBES[tag]))
            except Exception as e:
                per["rows"].append(f"{tag} r{rep} ERROR {str(e)[:40]}"); continue
            if not a:
                per["empty"] += 1; per["rows"].append(f"{tag} r{rep} EMPTY"); continue
            inv = "--force" in a.lower() or "--fix " in a.lower()
            ok = score(tag, a) and not inv
            per["pass"] += ok; per["invented"] += inv; pcount += ok
            per["rows"].append(f"{tag} r{rep} {'PASS' if ok else 'FAIL'}: {a[:90]}")
        per["per_probe"][tag] = f"{pcount}/4"
    per["secs"] = round(time.time() - t0)
    results[name] = per
    print(f"== {name}: {per['pass']}/16 empty={per['empty']} invented={per['invented']} probes={per['per_probe']} ({per['secs']}s)", flush=True)

pathlib.Path("/tmp/opencode/word-sweep/results2.json").write_text(json.dumps(results, indent=1))
print("SWEEP2-DONE")
