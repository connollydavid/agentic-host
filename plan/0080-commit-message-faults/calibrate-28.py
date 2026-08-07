#!/usr/bin/env python3
"""Sentence-level calibration for host-lint#28 over accepted history.

Fault 1 (duplication): a sentence from ADDED comment lines (comment runs joined,
markers stripped, sentence-split) appearing normalized inside the commit BODY
(subject excluded). Word-count thresholds swept at 5 / 8 / 12.
Fault 3 (precedent-as-defence): widened surface patterns over the body,
spelled numbers included.

Subject-in-added-lines is counted separately: the record-title convention
(subject == the added file's heading) is house style, and the count is the
evidence for excluding the subject from the comparison.
"""
import subprocess, re, collections

S1, S2, S3 = '\x01', '\x02', '\x03'
ROOT = '/mnt/c/Users/dconnolly/Development/agentic-host'
repos = {
    'agentic-host': ROOT,
    'host-lifecycle': f'{ROOT}/software/host-lifecycle/main',
    'host-lint': f'{ROOT}/software/host-lint/main',
    'host-grammar': f'{ROOT}/software/host-grammar/main',
    'host-prove': f'{ROOT}/software/host-prove/main',
    'host-template': f'{ROOT}/host-template',
    'host': f'{ROOT}/software/host/main',
}
COMMENT = re.compile(r'^\s*(#|//|/\*|\*\s|--\s|<!--|///|//!)')
LEADER = re.compile(r'^\s*(#+|/{2,3}!?|/\*+|\*+|-{2,}|<!--)\s?')
NUM = r'(?:\d+|two|three|four|five|six|seven|eight|nine|ten|a dozen|several|many|most)'
PRECEDENT = [
    ('N-other-plural', re.compile(rf'\b{NUM}\s+other\s+\w+s\b', re.I)),
    ('N-plural-already', re.compile(rf'\b{NUM}\s+\w+s\s+already\b', re.I)),
    ('already-do-this', re.compile(r'\balready\s+do(?:es)?\s+(?:this|the same)\b', re.I)),
    ('others-do', re.compile(r'\bothers\s+do\b', re.I)),
    ('is-what-X-do', re.compile(r'\bis\s+what\s+\w+\s+do(?:es)?\b', re.I)),
    ('standard-practice', re.compile(r'\bstandard\s+practice\b', re.I)),
]

def norm(s):
    s = re.sub(r'[`*_\'"“”‘’().,;:!?\[\]{}<>#=|-]', ' ', s.lower())
    return re.sub(r'\s+', ' ', s).strip()

def sentences(text):
    return [p.strip() for p in re.split(r'[.!?]+(?:\s+|$)', text) if p.strip()]

grand = collections.Counter()
for name, path in repos.items():
    out = subprocess.run(
        ['git', '-C', path, 'log', '--no-merges', '-n', '300',
         f'--format={S1}%H{S2}%B{S3}', '-p', '--unified=0'],
        capture_output=True, text=True, errors='replace').stdout
    total = 0
    hits = {5: 0, 8: 0, 12: 0}
    subj_hits = 0
    examples, prec_hits = [], []
    for e in out.split(S1)[1:]:
        try:
            sha, rest = e.split(S2, 1)
            msg, diff = rest.split(S3, 1)
        except ValueError:
            continue
        total += 1
        lines = msg.splitlines()
        subject = norm(lines[0]) if lines else ''
        body = '\n'.join(lines[1:])
        nbody = norm(body)

        # comment runs from added lines
        runs, cur = [], []
        for line in diff.splitlines():
            if line.startswith('+') and not line.startswith('+++') and COMMENT.match(line[1:]):
                cur.append(LEADER.sub('', line[1:]).strip())
            else:
                if cur:
                    runs.append(' '.join(cur))
                    cur = []
        if cur:
            runs.append(' '.join(cur))

        matched_w = set()
        subj_seen = False
        for run in runs:
            for sent in sentences(run):
                n = norm(sent)
                w = len(n.split())
                if w >= 5 and subject and n in subject and not subj_seen:
                    subj_hits += 1
                    subj_seen = True
                if not nbody:
                    continue
                for W in (5, 8, 12):
                    if w >= W and n in nbody and W not in matched_w:
                        hits[W] += 1
                        matched_w.add(W)
                        if W == 8 and len(examples) < 8:
                            examples.append((sha[:8], sent[:110]))
        pr_seen = set()
        for label, rx in PRECEDENT:
            m = rx.search(body)
            if m and label not in pr_seen:
                prec_hits.append((label, sha[:8], m.group(0)))
                pr_seen.add(label)

    print(f'== {name}: {total} commits')
    print(f'   duplication (body, subject excluded): W>=5: {hits[5]}  W>=8: {hits[8]}  W>=12: {hits[12]}')
    print(f'   subject matched an added comment sentence: {subj_hits}')
    for sha, s in examples:
        print(f'     dup@8 {sha}  {s}')
    for label, sha, t in prec_hits[:6]:
        print(f'     prec  {sha}  [{label}]  {t[:80]}')
    grand['total'] += total
    for W in (5, 8, 12):
        grand[f'w{W}'] += hits[W]
    grand['subj'] += subj_hits
    grand['prec'] += len(prec_hits)

print(f"\n== TOTAL: {grand['total']} commits | dup W>=5: {grand['w5']}  W>=8: {grand['w8']}  "
      f"W>=12: {grand['w12']} | subject-title hits: {grand['subj']} | precedent hits: {grand['prec']}")
