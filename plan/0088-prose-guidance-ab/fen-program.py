#!/usr/bin/env python3
"""The weak-model rerun of the prose-guidance A/B (plan/0088).

Protocol: the plan/0076 corrected protocol (thinking on through the chat
template, the model card's thinking-general parameters), identical to the
kits in plan/0080 and plan/0086's lineage. For each condition (A bare, B
prohibition list, C positive exemplars) and each task (T1, T2), the model
writes `draws` samples; every output is saved unedited to
fen-samples/<condition>-<task>-<draw>.md and then swept with the pinned
`host-lint --prose` to count warning lines. The table at the end is the
result: mean warns per condition, which is the A/B answer for the
population the doctrine gates.

Channel and credentials arrive via FEN_ENDPOINT / FEN_TOKEN / FEN_MODEL,
all required. Draws default to 3 per cell. The prompts are the ones in
prompts.md, unchanged; edit nothing here between runs.
"""
import json, os, pathlib, subprocess, urllib.request

SCRATCH = pathlib.Path(__file__).parent
ENDPOINT = os.environ["FEN_ENDPOINT"]
TOKEN = os.environ["FEN_TOKEN"]
MODEL = os.environ["FEN_MODEL"]
DRAWS = int(os.environ.get("FEN_DRAWS", "3"))
HOST_LINT = os.environ.get("FEN_HOST_LINT", "host-lint")

PARAMS = {"temperature": 1.0, "top_p": 0.95, "top_k": 20, "min_p": 0.0,
          "presence_penalty": 1.5, "repetition_penalty": 1.0,
          "max_tokens": 32768}

TASKS = {
    "T1": "Write a short passage (80-120 words) for a README describing a new capability of a command-line tool: the tool reconciles a project's manifest files against a template that has moved, proposing merges instead of overwriting. Do not invent features beyond this.",
    "T2": "Write a short summary paragraph (80-120 words) for a project record, summarizing a milestone that migrated a repository from numbered folder names to names derived from each folder's contents, and gated the rename with a dictionary-driven checker.",
}
GUIDANCE = {
    "A": "",
    "B": "\n\nAvoid these words and constructions: delve, tapestry, synergy, landscape, intricate, nuanced, multifaceted, realm, showcase, leverage (as a verb), harness (as a verb), framework (in the grandiose sense), deeply, fundamentally, remarkably, profoundly, crucially, \"serves as\", \"stands as\"; avoid em-dashes, arrows, and three-part parallel sentences.",
    "C": "\n\nWrite in the manner of these examples: \"The checker reads every manifest, compares each against the template's current revision, and proposes a merge per drifted file. Nothing is overwritten without an explicit confirmation, and every proposal names the files it touched.\"",
}


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
    text = d["choices"][0]["message"].get("content") or ""
    if "</think>" in text:
        text = text.split("</think>", 1)[1]
    return text.strip()


def warns(path):
    out = subprocess.run([HOST_LINT, "--prose", str(path)],
                         capture_output=True, text=True)
    return sum(1 for line in (out.stdout + out.stderr).splitlines()
               if "warning:" in line)


def main():
    outdir = SCRATCH / "fen-samples"
    outdir.mkdir(exist_ok=True)
    tallies = {c: [] for c in GUIDANCE}
    for cond, guidance in GUIDANCE.items():
        for task, task_text in TASKS.items():
            for draw in range(1, DRAWS + 1):
                name = f"fen-{cond.lower()}-{task.lower()}-{draw}"
                path = outdir / f"{name}.md"
                if path.exists():
                    body = path.read_text().split("\n\n", 1)[1]
                else:
                    body = ask(task_text + guidance)
                    path.write_text(f"# Sample {name}\n\n{body}\n")
                n = warns(path)
                tallies[cond].append(n)
                print(f"{name}: warns={n}")
                with open(SCRATCH / "fen-results.md", "a") as f:
                    f.write(f"\n## {name}\n\nwarns={n}\n\n```\n{body}\n```\n")
    print("\n=== result: mean warns per condition ===")
    for cond in GUIDANCE:
        xs = tallies[cond]
        mean = sum(xs) / len(xs) if xs else 0
        print(f"{cond}: mean={mean:.2f} over {len(xs)} sample(s)")


if __name__ == "__main__":
    main()
