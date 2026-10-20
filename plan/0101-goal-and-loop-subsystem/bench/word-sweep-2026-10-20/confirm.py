"""The confirmation stage (protocol v2, pre-declared 2026-10-20).

Arms: A untaught (format only), B the original V0 teaching lines,
C the locked candidate (selected mechanically from sweep3 per the rule:
the best-scoring arm not below the in-round incumbent, fewest empties
tiebreak; fallback R4). Probes: the four selection states plus four
HELD-OUT states never used in any round. Fully interleaved draws.

PRE-DECLARED CONFIRMATION CRITERIA (the ship decision):
1. Hard gate: zero invented commands across every C draw.
2. C beats A by >= 8/32 pooled (outside drift, which measured 3).
3. C non-inferior to B pooled, and C held-out pooled >= B held-out pooled.
4. Per-state floor: no C probe below 2/4.
5. Failing any criterion: nothing ships; the record states which.
"""
import json, urllib.request, pathlib, random, time, importlib.util
TOKEN = pathlib.Path.home().joinpath(".edge-token").read_text().strip()
URL = "https://api.d07yx58.net/v1/chat/completions"
T = pathlib.Path("/tmp/opencode")

spec = importlib.util.spec_from_file_location("sweep3", T / "word-sweep/sweep3.py")
# sweep3 runs at import; instead parse its VARIANTS by exec of the literal block
src = (T / "word-sweep/sweep3.py").read_text()
r4 = src.split('R4 = """', 1)[1].split('"""', 1)[0]
ns = {"R4": r4}
block = src.split("VARIANTS = {", 1)[1].split("\n}", 1)[0]
exec("VARIANTS = {" + block + "\n}", ns)
S3 = ns["VARIANTS"]

r3 = json.loads((T / "word-sweep/results3.json").read_text())
in_round = r3["S0-r4-incumbent"]["pass"]
eligible = [(v["pass"], -v["empty"], k) for k, v in r3.items() if v["pass"] >= in_round]
cand_name = max(eligible)[2] if eligible else "S0-r4-incumbent"
print(f"candidate locked: {cand_name} (in-round incumbent {in_round}/16)", flush=True)

ARMS = {
 "A-untaught": "Reply with exactly one line starting with ACTION: followed by the single next move you make. Nothing else.",
 "B-v0": """You are the agent working inside a software project governed by the host loop. Tool output arrives in the user message. The tool output's NEXT line names your single next move. If NEXT is a command, run it exactly as printed. If NEXT says work <key>, begin that task. If the tool refused to emit, run the command on its last line. Reply with exactly one line starting with ACTION: naming that move. Nothing else.""",
 "C-candidate": S3[cand_name],
}
PROBES = {t: (T / f"{t.lower()}.txt").read_text() for t in ("p1","p2","p3","p4","h1","h2","h3","h4")}
HELD_OUT = ("h1","h2","h3","h4")

def ask(sysmsg, prompt):
    body = json.dumps({"model":"qwen3.5-4b","temperature":0.6,"max_tokens":1024,
        "messages":[{"role":"system","content":sysmsg},{"role":"user","content":prompt}]}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Authorization":"Bearer "+TOKEN,"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=240) as r:
        return json.load(r)["choices"][0]["message"]["content"].strip()

def action_line(text):
    if "</think>" in text: text = text.split("</think>")[-1]
    for ln in text.splitlines():
        if ln.strip().lower().startswith("action:"): return ln.strip()
    return ""

def score(probe, a):
    low = a.lower()
    inv = "--force" in low or "--fix " in low
    ok = {
      "p1": "plan/0101#run-loop" in low and any(w in low for w in ("work","begin","start","do")),
      "p2": any(s in low for s in ("tasks --record","ci --record","goal repair","re-derive")),
      "p3": "goal unpark" in low,
      "p4": "goal repair" in low,
      "h1": ("nnnn" not in low) and any(w in low for w in ("propose","cut","milestone","operator","ask")),
      "h2": "goal repair" in low,
      "h3": "goal unpark" in low,
      "h4": "tasks --record" in low and "plan/0100#second" in low,
    }[probe]
    return ok and not inv, inv

draws = [(arm, probe, rep) for arm in ARMS for probe in PROBES for rep in range(4)]
random.Random(20261020).shuffle(draws)
res = {a: {"pass":0,"empty":0,"invented":0,"per_probe":{}} for a in ARMS}
for arm, probe, rep in draws:
    try:
        a = action_line(ask(ARMS[arm], PROBES[probe]))
    except Exception as e:
        print(f"{arm}/{probe} r{rep} ERROR {str(e)[:50]}", flush=True); continue
    if not a:
        res[arm]["empty"] += 1; continue
    ok, inv = score(probe, a)
    res[arm]["pass"] += ok; res[arm]["invented"] += inv
    pp = res[arm]["per_probe"].setdefault(probe, [0,0]); pp[0] += ok; pp[1] += 4 and 1
    print(f"{arm} {probe} r{rep} {'PASS' if ok else 'FAIL'}{' INV' if inv else ''}: {a[:80]}", flush=True)

summary = {}
for arm, r in res.items():
    held = sum(r["per_probe"].get(p,[0,0])[0] for p in HELD_OUT)
    summary[arm] = {"pass": r["pass"], "of": 32, "empty": r["empty"], "invented": r["invented"],
                    "held_out": held, "per_probe": {k: f"{v[0]}/4" for k, v in r["per_probe"].items()}}
c, a, b = summary["C-candidate"], summary["A-untaught"], summary["B-v0"]
crit = {
 "1-zero-invented": c["invented"] == 0,
 "2-c-beats-a-by-8": c["pass"] - a["pass"] >= 8,
 "3-noninferior-to-b": c["pass"] >= b["pass"] and c["held_out"] >= b["held_out"],
 "4-state-floor": all(int(v.split("/")[0]) >= 2 for v in c["per_probe"].values()),
}
print("=== CONFIRMATION SUMMARY ===", flush=True)
print(json.dumps(summary, indent=1), flush=True)
print("CRITERIA:", json.dumps(crit), flush=True)
print("SHIP" if all(crit.values()) else "NO-SHIP", flush=True)
(T / "word-sweep/confirm-results.json").write_text(json.dumps({"candidate": cand_name, "summary": summary, "criteria": crit}, indent=1))
print("CONFIRM-DONE", flush=True)
