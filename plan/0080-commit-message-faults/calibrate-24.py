#!/usr/bin/env python3
# Calibration sweep for host-lint#24's carve-out half: how often does the
# ordinal-scaffold heading rule fire across every tracked markdown heading in
# the materialized stores, and on what? Candidates are matched in python with
# the predicate mirrored from check_ordinal_scaffold_header, then every
# candidate is CONFIRMED against the real binary, so the binary stays the
# ground truth and the mirror only prunes.
import subprocess, sys, os

ROOT = "/mnt/c/Users/dconnolly/Development/agentic-host"
BIN = os.path.join(ROOT, "software/host-lint/main/target/release/host-lint")
FLAG_TERMS = {"phase","stage","iteration","sprint","cycle","increment","wave",
              "episode","instalment","leg","lap","box","boxes","step","steps"}

repos = {
    "agentic-host": ROOT,
    "host-template": os.path.join(ROOT, "host-template"),
    "host": os.path.join(ROOT, "software/host/main"),
    "host-lifecycle": os.path.join(ROOT, "software/host-lifecycle/main"),
    "host-lint": os.path.join(ROOT, "software/host-lint/main"),
    "host-grammar": os.path.join(ROOT, "software/host-grammar/main"),
    "host-prove": os.path.join(ROOT, "software/host-prove/main"),
    "host-reference": os.path.join(ROOT, "software/host-reference/main"),
    "host-reference-ocr": os.path.join(ROOT, "software/host-reference-ocr/main"),
    "host-reference-openscad": os.path.join(ROOT, "software/host-reference-openscad/main"),
}

def candidate(line):
    t = line.strip()
    hashes = 0
    for c in t:
        if c == "#": hashes += 1
        else: break
    if hashes == 0 or hashes > 6: return None
    rest = t[hashes:].strip().rstrip(":.—-").strip()
    words = rest.split()
    if len(words) != 2: return None
    noun, number = words
    if not (noun.isalpha() and len(noun) >= 2): return None
    if not (number.isdigit() and 1 <= len(number) <= 2): return None
    if noun.lower() in FLAG_TERMS: return None  # the lexical rule's business
    return rest

total_headings = 0
total_files = 0
fires = []
for name, path in repos.items():
    if not os.path.isdir(path):
        print(f"{name}: MISSING at {path}")
        continue
    files = subprocess.run(["git","-C",path,"ls-files","*.md","**/*.md"],
                           capture_output=True, text=True).stdout.split()
    seen = set()
    n_head = 0
    cands = []
    for f in sorted(set(files)):
        fp = os.path.join(path, f)
        if not os.path.isfile(fp): continue
        total_files += 1
        try:
            text = open(fp, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            ls = line.lstrip()
            if ls.startswith("#"):
                n_head += 1
                c = candidate(line)
                if c: cands.append((f, i, line.strip()))
    total_headings += n_head
    confirmed = []
    for f, i, line in cands:
        r = subprocess.run([BIN, "--stdin-as", "cal.md"], input=line+"\n",
                           capture_output=True, text=True)
        if r.returncode == 1:
            confirmed.append((f, i, line, r.stdout.strip().splitlines()[:1]))
    print(f"{name}: {n_head} headings, {len(cands)} shape candidates, {len(confirmed)} binary-confirmed fires")
    for f, i, line, out in confirmed:
        fires.append((name, f, i, line))
        print(f"    {f}:{i}: {line}")
print(f"\nTOTAL: {total_files} files, {total_headings} headings, {len(fires)} confirmed fires")
