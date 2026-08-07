# Briefing: the commit-message fault detectors (host-lint#28, plus host-lint#24's remainder)

## The issue (operator-filed 2026-08-06, condensed, faithful)

`host-lint --prose` catches trope shapes. Four faults recur in commit messages and PR
bodies and pass it:

1. **The message restates what the file already says.** One message repeated the header
   comment of the file it added, diagram included; deleting the duplication cost 116
   words and no facts. Mechanically checkable: compare the comment lines a commit adds
   against the message body, flag sentences appearing in both. Needs the diff and the
   message, no model.
2. **The message answers a point nobody made** (rebuts an alternative no reviewer proposed).
3. **Precedent stands in as defence** ("N other packages already do this"). Surface forms
   worth trying: `N <plural> already`, `others do`, `is what ... do`.
4. **Paragraphs argue for a change instead of describing it.**

Operator's suggested scope: fault 1 as a warning on the commit-msg path; fault 3 as an
advisory; faults 2 and 4 as written guidance ("a more honest outcome than a check that
mostly misses").

## Calibration (2026-08-06, 922 accepted commits across all seven repos)

Sentence-level, comment runs joined and markers stripped, normalized substring against
the message body with the subject line excluded:

| repo | commits | dup W>=5 | W>=8 | W>=12 | subject-matches |
|---|---|---|---|---|---|
| agentic-host | 300 | 0 | 0 | 0 | 5 |
| host-lifecycle | 209 | 12 | 10 | 2 | 1 |
| host-lint | 146 | 9 | 8 | 4 | 0 |
| host-grammar | 20 | 1 | 1 | 1 | 0 |
| host-prove | 21 | 0 | 0 | 0 | 0 |
| host-template | 203 | 0 | 0 | 0 | 6 |
| host | 23 | 0 | 0 | 0 | 0 |
| **total** | **922** | **22** | **19** | **7** | **12** |

Readings:
- The fault is real and current: one hit is a commit made TODAY during this session
  ("An upstream already set, by hand or by an earlier run, is kept as found" — in both
  the doc comment and the body). The corpus is the offender corpus, so hits are mostly
  true instances, with a minority of judgment-call quotes (a message quoting a factual
  claim like "--dry-run is not a flag of receipt --record").
- The subject line MUST be excluded: 12 hits are the house convention that a record
  commit's subject IS the added record's title (call/0053 etc.).
- Threshold: W>=8 keeps 19 of 22 while dropping short generic sentences; W>=12 loses
  most true instances.
- **Fault 3 scored ZERO in 922 commits**, even with widened patterns (spelled numbers,
  "already do this", "others do", "is what X do", "standard practice"). An advisory
  would cost nothing and, on this corpus, catch nothing.

## Standing constraints and precedent

- **Tiers**: flag=1 blocks, warn=3 advisory at the commit hook. Commit-msg warns are
  hook-only (the release gate's prose regression reads docs, not messages), so a new
  commit-msg warn cannot re-open the verify receipt.
- **VOCABULARY.md is host-lint's rule source.** An entry there that no code enforces
  breaks the property that VOCABULARY states what the tool enforces (the shape
  call/0046 retired `hermetic-exempt` for). Written-guidance-only content belongs in
  skill text, explicitly labeled unenforced — or nowhere.
- **The --stdin path already runs body prose advisory** through the shared host-grammar
  engine, so a new host-grammar trope reaches commit bodies with no new plumbing —
  but a grammar change costs the full grammar -> host-lint -> host-lifecycle vendored
  cascade. A host-lint-side rule costs one release.
- **Fault 1 needs the staged diff**, which host-lint's --stdin path does not receive
  today. The pure predicate (added-comment sentences x body sentences) is trivially
  unit-testable either way; the question is who observes the diff.
- **plan/0072's lesson**: calibration against accepted history rewrote four designed
  decisions two reviews had passed. **plan/0070's lesson**: precision at the warn tier
  is what keeps the advisory tier trusted.
- **host-lint#24 remainder**: the generic `<noun> <cardinal>` heading rule shipped
  (94cfb35); still open is the LEXICON carve-out for genuine heading designators
  ("Windows 11") paired with a recall-biased warn tier. Same detector-precision
  territory, same release vehicle candidate.
- **Push hold**: all work lands as local held commits; a milestone cut or call/ record
  waits for the lift. Design now, land the record then.

## The questions

**Q1 — who observes the diff for fault 1?**
- (a) host-lint runs `git diff --cached` itself when linting a commit message in a repo.
- (b) the commit-msg hook pipes the staged diff to host-lint alongside the message
  (explicit input, no git inside host-lint's stdin path).
- (c) a dedicated `host-lint commit` verb taking message file + diff, called by the hook.

**Q2 — fault 1 tier and threshold?**
- (a) warn (exit 3) at sentence threshold W>=8, subject excluded, commit-msg path only.
- (b) warn at W>=5 (higher recall, admits short generic sentences).
- (c) warn at W>=8 but also surfaced in --prose/PR-body contexts, not only commit-msg.

**Q3 — fault 3 (precedent), given zero corpus hits?**
- (a) do not build it; record the shape in guidance only; revisit if it ever appears.
- (b) build as a host-lint-side advisory on the commit-msg path (one release, no cascade).
- (c) build as a host-grammar trope (reaches all prose surfaces; full cascade).

**Q4 — faults 2 and 4 guidance placement?**
- (a) the commit-message section of the relevant skill text, explicitly labeled as
  not mechanized.
- (b) VOCABULARY.md alongside the enforced rules, labeled advisory-prose.
- (c) nowhere: unenforceable guidance is noise (honest silence).

**Q5 — packaging?**
- (a) one host-lint milestone bundling fault 1 + the #24 LEXICON-carve-out remainder,
  one release when the hold lifts.
- (b) fault 1 as an issue-scoped fix now (held commit), #24 remainder separate later.
- (c) wait: no detector work until the hold lifts and the milestone can be cut properly.

## What each persona returns

For each question: your position (2-4 sentences, grounded in your lens), then the
strongest objection to your own position, then a final ranked ordering of the options.
End with the single most important overall note. Under 500 words total.
