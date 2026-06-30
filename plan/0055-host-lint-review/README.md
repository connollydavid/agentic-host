# plan/0055 host-lint review: findings, the blocking-tier precision recut, and the no-hollow-green dogfood

This milestone records a maximum-effort review of `host-lint`, the prose-and-naming detector that
gates this repository and every adopter project, and the remediation decided for it. It is the last
review in the campaign, after `host-grammar` (plan/0053) and `host-prove` (plan/0054). It is treated
as doctrine-grade (operator ruling) on two counts: the review changes the blocking detection
contract, and it closes a no-hollow-green gap in the very tool whose grammar consumer enforces that
doctrine for the suite.

## What was reviewed

- Component: `host-lint` at its pinned release (`cefc9376`, v0.11.0): the detector core `src/lib.rs`
  (1077 lines), the CLI `src/main.rs` (554 lines), the `host-lint.allium` spec with its
  `host-lint.obligations` manifest and `.obligations.digests` ledger, `VOCABULARY.md` (the rule
  source), the `pre-commit`/`commit-msg` hook script, `test-integration.sh`, `lint-skill.sh`, the
  skill guides, `Cargo.toml`, and the CI workflow. The detector consumes `host-grammar` at `9470b81`
  (v0.4.0) for the prose lane.
- Method: six independent reviewers, one per surface (naming-tell detection; the LEXICON allowlist
  and masking; the prose lane and the ignore-fence engine; the CLI, git-root resolution, and
  exit-code dispatch; the allium spec and obligation discharge under the no-hollow-green lens; and
  VOCABULARY, the hooks, CI, and the integration suite). Each probed its claims empirically against
  the built binary; the load-bearing findings were reproduced independently before write-up.
- Result: 40 raw findings, deduped to 33 distinct, every one confirmed against the built v0.11.0
  binary. Two critical, eleven high, fourteen medium, six low. The audited source matches the pin
  digest (`cc31f540`), so the findings hold against the released artifact.

## The contract the findings test against

- **Precision at the blocking tier.** host-lint has three tiers: a blocking Flag (exit 1) for a
  confirmed tell, an advisory Warn (exit 3, recall-biased) for an ambiguous one, and a Note (exit 0).
  The recall bias is sanctioned only at Warn. A Flag blocks a commit, so the blocking tier must fire
  only on a confirmed tell; a false Flag there trains users to bypass the hook, which destroys the
  gate. The review measured the blocking tier against ordinary English and source.
- **No fail-open.** The detector must never silently pass a real tell. A masking allowlist, a
  git-root miss, an unclosed ignore fence, or a hook that reads the wrong bytes must fail closed or
  fail loud, never settle to a clean exit over content it did not scan.
- **No hollow green (plan/0052).** A lane that cannot perform its check must not report clean, and an
  obligation must be discharged by a test that exercises the rule. host-lint must hold itself to the
  doctrine its grammar lane enforces for the suite.
- **Reproducible build.** The release artifact must re-derive byte-identically from the recorded
  toolchain, and CI must prove it against the `.host-software` hash.

## Findings

The concrete trigger strings are boxed below so the doc gate does not read them as authored tells.

```host-lint:ignore
A. blocking-tier false-flags (the gate over-blocks legitimate text):
   "in this pass I fixed the parser bug"      blocked  (the pronoun "I" parses as Roman 1)
   "port the lexer pass to C"                 blocked  (the language letter "C" parses as Roman 100)
   "pass 2 arguments to the helper"           blocked
   "round 2 decimal places before display"    blocked
   "step into 3 dimensions of design"         blocked
   "## 2024" / "## 404"   (markdown heading)  blocked
   "release wave 2024-01 shipped"             blocked  (a date read as a numeric range)
   "// 200: OK response handler"  (comment)   blocked  (a status code read as a label prefix)

B. fail-open holes (the gate silently passes real tells):
   a bare LEXICON entry of a flag-noun masks the noun out of every real flag-noun-plus-numeral line
   an unclosed host-lint:ignore fence swallows the rest of the file
   a relative GIT_DIR collapses the repo root, dropping the LEXICON and downgrading strict to advisory
```

### A. Blocking-tier false-flags (precision)

| # | Sev | Finding |
|---|-----|---------|
| N1 | **critical** | `is_numeral` accepts canonical Roman numerals, so the pronoun "I" and the single letters C/D/V/X after any flag-noun settle to a blocking Flag. Ordinary commit-body prose blocks. |
| N2 / V1 | high | The verb and measurement nouns (`pass`, `round`, `step`, `level`, `part`) flag within a 2-word window, so ordinary English blocks. The `i+2` lookahead widens the collision. VOCABULARY.md documents immediate adjacency in comments, headers, and subjects; the code matches any line at a 2-word gap, so the rule source misdescribes the contract. |
| N3 | medium | `check_bare_numeral_header` flags any all-digit markdown heading, including a changelog year and a status-code reference, with no year guard. `gather_candidates` already skips a 4-digit year; this lane does not. |
| N4 | medium | `is_num_range` accepts a `YYYY-MM` date and a year range, so a date-stamped label flags. |
| N5 | medium | `check_label_prefix` flags a numeric-key comment such as an HTTP status line. |

The structural root: the blocking lane lacks the year and length guards `gather_candidates` already
has, accepts Roman numerals in a lane where single letters collide with English, and reaches a
numeral two words away rather than adjacent.

### B. Fail-open holes (recall, more dangerous for a gate)

| # | Sev | Finding |
|---|-----|---------|
| L1 | **critical** | LEXICON laundering: a bare flag-noun entry, or a multiword entry whose tokens stop short of a numeral, passes the G2 no-laundering guard, then masks the flag-noun out of a real line. The whole flag class then goes unscanned repo-wide, and strict mode no longer escalates it. G2 checks only the phrase's own class. It never checks whether masking the phrase would clear a flag elsewhere. |
| C1 | high | A relative `GIT_DIR` (which `git --git-dir=.git commit` exports) makes `repo_root()` return empty, so the LEXICON is dropped and a blocking strict Flag downgrades to an advisory Warn. |
| C2 | high | With an empty root, `--all` and `--docs` exit clean having scanned nothing, so a repository audit passes vacuously. |
| V4 | high | The pre-commit hook lints the working-tree file, not the staged blob, so a tell staged then edited out of the working tree commits unseen. |
| P2 | high | An unclosed `host-lint:ignore` fence leaves the ignore state set to end of file, so every later line is skipped and tells after a forgotten close are never seen. |
| V5 | medium | The hook acts only on exit 1 and exit 3, so an exit 2 (a usage error or a git failure) lets the commit through. On an error the gate becomes a no-op for that file, and the commit proceeds. |
| P4 | medium | A bare fence inside an ignore block closes it early, with no nesting awareness, so a quarantined citation leaks back to the linter. |
| L2 | medium | A phantom tracker reference cited to any unrelated URL masks a real review-code flag offline; the URL is never parsed or correlated, and the liveness lane is a separate non-default subcommand. |
| C4 | medium | `--prose` with no file arguments exits clean silently, so a script that trusts the exit code reads a vacuous pass. |

### C. Hollow green in host-lint's own ladder (the plan/0052 doctrine, dogfooded)

| # | Sev | Finding |
|---|-----|---------|
| S1 | high | The `RomanNumeralLength` invariant (cap 4) contradicts the pinned host-grammar, which has no length cap, and a `structural` disposition cannot test the invariant at all. A decorative green, on the same Roman acceptance that drives N1. |
| S2 | high | The verdict-lifecycle obligation block is discharged by single-line classifier tests, not by the matches-to-exit-code aggregation in `main.rs`. The negative `rule-failure.RecordFlag.1` maps to an always-positive test, so it is non-falsifiable. |
| V6 | high | The release CI job omits `allium` and `kani` from its `needs`, so a tag can ship with a red spec or a red proof. A hollow-green release path. |
| S3 | medium | The `exercises=` strengthening from plan/0052 is un-adopted: no `exercises=` links, no `--strict-discharge`. The gate confirms a test name resolves, never that the test exercises the rule, though host-lint's property tests are fully white-box and ready for the link. |
| S4 | medium | An unmodeled flag-tier rule (a review-noun plus a code), and a kani proof dispositioned to a rule whose code path it cannot reach. |
| S5 | medium | The spec under-models its own engine: the Note severity, the prose occurrence-mapping, the LEXICON guards, masking, gather, and the ignore-fence quarantine are tested but neither modeled nor obligated. |
| S6 | low | The entity-creation obligations assert only that a detector returned a match, never the modeled `Match` fields, and the spec rule names do not map to the code function names. |

### D. Reproducible build and CI integrity

| # | Sev | Finding |
|---|-----|---------|
| V7 | high | CI builds on the stock runner with apt musl-tools, without `--locked` or `--offline` and ignoring the deps-bundle, and never verifies the artifact against the `.host-software` hash. The Cargo.toml comment claiming CI proves the byte-identical artifact is false; no such step exists. |

### E. Test and coverage gaps

V2 (medium): the VOCABULARY core regex omits nine enforced terms, and the documented header
restriction for the machine-learning term is unimplemented. V3 (medium): nothing keeps VOCABULARY.md
in sync with the code constants, and thirteen of twenty-five flag terms have no test. V8 (medium):
the ignore-fence exemption has no integration test, and the hook script itself is exercised nowhere.
V9 (medium): the should-flag integration cases assert a nonzero exit, conflating Flag and Warn, so a
Flag-to-Warn regression stays green.

### F. Robustness and lower severity

L3 and P1 are the same bug (high): `escalate_subject_decoration` over-escalates a body decoration to
a Flag whenever the subject contains the same character, because it tests substring containment of
the match text rather than the match line. P3 (high): a second, markdown-normalised occurrence of a
repeated prose tell is silently dropped, under-reporting. P5 (medium): the occurrence mapping lacks a
word boundary, so a short tell mislocates onto a longer word. C3 (medium): `escape_json` emits raw
control bytes, producing invalid JSON. C5 (low): the per-file path follows symlinks while `--all`
skips them. P6 and L4 (low, speculative): a char-boundary panic on a masked multibyte phrase, and a
non-ASCII mask boundary. N6 (low): a typographic dash range is missed. N7 (low): `milestone` and
`tier` are absent from the terms, and a review-noun plus a bare numeral does not flag (a vocabulary
judgment). N8 (low): the co-author exemption is position-agnostic. N9 (low): a strict decimal Warn
cannot be escaped through the LEXICON.

### Checked and cleared

The reviewers confirmed several load-bearing negatives. The G1 master-key guard holds (a lettered
phrase never masks a bare numeral). The masking offset arithmetic is byte-safe for the ASCII case.
The ignore fence is honored only in markdown, so a code file or a commit message cannot open one, and
an ordinary code fence stays linted so a tell cannot be laundered by inline quoting. The kani tier is
re-run for real through host-prove with a fresh digest ledger, and the detection rules whose tests
genuinely exercise the mapped function are honestly discharged. No naming-lane panics were found.

## Operator decisions

1. **The blocking tier holds only the high-centrality work-unit words; the disposition is grounded in
   corpus data, not assertion.** The operator's first ruling demoted the verb and measurement terms
   (`pass`, `round`, `step`, `level`, `part`). The operator then asked to ground the rest in data
   rather than assert a noun is collision-prone. Measuring the `<noun> <numeral>` shape across roughly
   35,500 real `.rs` files (a proxy for adopter code) showed six more nouns I had kept blocking are
   overwhelmingly domain usage with zero in-project tells: `section` (the single largest source),
   `chapter`, `epoch`, `batch`, `era`, `period`. The operator ruled to demote all six. The blocking
   tier now holds the work-unit words (`phase`, `stage`, `sprint`, `iteration`, `cycle`, `increment`,
   `wave`) plus the near-zero-exposure synonyms and the host#16 checklist terms (`steps` stays blocking
   by operator decision). The clear-bug part of class A (the Roman acceptance, the two-word window, the
   year and status guards) is fixed regardless of tier. The contract change is recorded in `call/0037`
   and reflected in VOCABULARY.md, the rule source.
2. **One milestone.** plan/0055 carries both the component fixes and the no-hollow-green dogfood
   (class C), released together, rather than the plan/0051-plus-0052 split host-lifecycle used.
3. **Doctrine-grade.** The remediation is gated by a cast review and a real qwen3.5-4b probe before
   release, the same bar as plan/0052 and plan/0054, because it changes the contract and closes the
   dogfood gap.

## Remediation plan

Fix everything toward the contract above. The blocking tier is recut for precision (drop Roman in the
blocking lane, require immediate adjacency, add the year and status guards, demote the verb terms to
Warn). The fail-open holes are closed (the LEXICON guard tests the masking effect; the empty root
fails closed; the unclosed fence fails loud; the hook lints the staged blob and treats an unexpected
exit as a block). The no-hollow-green gap is closed (the false invariant corrected and re-dispositioned,
the verdict aggregation given white-box coverage, the `exercises=` links and `--strict-discharge`
adopted, the release job gated on allium and kani). The reproducible build is wired in CI against the
recorded hash. The coverage gaps are filled. Then host-lint is released, re-pinned, and propagated to
host-lifecycle (host-lint is a library dependency of the in-process prose lane, so a host-lint change
obliges a re-vendor and re-release of host-lifecycle, as in plan/0053). The whole suite must be green.

## Process note

One reviewer ran without worktree isolation and committed two probe fixtures into the shared host-lint
worktree, which then sat two unpushed commits ahead of the pin with stray tracked files. The audited
source was untouched (the digest matches the pin), so the findings stand. The worktree is reset to the
pin before remediation. The lesson: run probing reviewers under worktree isolation. This is recorded
in MEMORY.

## In-house remediation

The whole in-house layer is complete, tested, and committed in the host-lint worktree on top of the
v0.11.0 pin. Every finding above is fixed or dispositioned.

- Detector and lexicon: the blocking-tier recut (N1, N2, N3, N4, N5, N6), the lexicon anti-laundering
  guard (L1), the corpus-grounded demotion of the domain-heavy nouns, and the citation-gate number
  correlation (L2). The verb-and-domain-noun demotion contract is recorded in `call/0037`.
- Fail-opens and prose lane: the CLI fail-opens (C1, C2, C3, C4), the prose lane and ignore-fence
  engine (P1, P2, P3, P4, P5, P6), and the hook's staged-blob scan with fail-closed exit handling
  (V4, V5).
- Rule source and coverage: VOCABULARY.md rewritten to the two-tier contract with a doc-to-code sync
  test (V1, V2, V3); the integration suite asserts exact exit codes and covers the ignore fence and
  the hook end to end (V8, V9).
- No-hollow-green dogfood in host-lint's own ladder: the false `RomanNumeralLength` invariant removed
  (S1), the verdict aggregation given a `verdict_code` helper and a real test (S2), `exercises=` links
  on every test disposition with `--strict-discharge` in CI (S3), the review-code flag rule modelled
  and the Kani harnesses re-attributed (S4), an auditable scope note for the unmodelled engine (S5),
  an entity-creation test that asserts the Match shape (S6), and the release CI gated on allium and
  kani (V6). The reproducible-build CI builds the published linux asset by the pinned recipe and the
  false Cargo.toml claim is corrected (V7).
- Low-severity, recorded rather than changed: C5 (an explicit file argument is followed by design,
  unlike the `--all`/`--docs` tree walk; the hook no longer scans by path, so it is unaffected); N7
  (`tier` measured domain-heavy at 91 corpus hits, so it stays out of the blocking set; `milestone`
  has zero corpus hits and adding it is left to the operator, not widened here); N8 (the co-author
  exemption is intentionally lenient per its attribution rationale); N9 (the bare-decimal warn is
  recall-biased by design; a strict escalation of it is the intended cost of a declarable lexicon).
- Self-consistency dogfood (operator-caught, beyond the review findings): host-lint's own internals
  named constructs by ordinal position, the exact tell it detects and the methodology forbids. The
  conformance gates, the lexicon guards, the warn-rule labels, and the severity tiers are renamed
  after their content; the bare review finding-code citations are dropped from the shipping artifact
  (the milestone is cited by its content-slugged name, the review record keeps its finding labels).
  Separately, the name-format conformance gate read the skill name from the directory holding
  SKILL.md, which is the worktree line `main` in the materialized layout, so it failed when run in the
  worktree; it now reads the parent directory's name, so the gate passes in the worktree as well as on
  an installed skill and a repo-named CI checkout.

## Doctrine gate

Gated like plan/0052 and plan/0054: a cast review across four lenses (Mara, Orin, Wren, Bly) and a
real qwen3.5-4b (Fen) probe. It earned its keep: it caught defects the in-house pass had missed,
one of which my own fix had introduced.

- **Fen probe (the real 4B): passed.** Three weak-agent-facing scenarios, routed correctly across three
  trials with sound reasoning and no miss: an advisory warn lets the commit proceed; a blocking flag is
  reworded, not bypassed; a refused lexicon entry is renamed, not hand-edited. The two-tier contract and
  the refusal UX hold at the 4B bar.
- **Cast review findings, all fixed (commit `5d6eb6a`):** a HIGH fail-open the V4 staged-blob fix had
  reopened (a non-ASCII filename is C-quoted, so `git show` failed and, without `pipefail`, fed empty
  input to the linter, committing a tell in `café.md` clean; fixed with NUL-delimited listing,
  `pipefail`, `.exe`, and a fail-closed read of an undecodable scannable blob); the Roman-acronym
  false-flag class (an uppercase abbreviation like `DC`, `XL`, or `MM` standing after a flag noun,
  fixed by bounding a blocking Roman to ordinal value `<= XXXIX`); a review-code laundering hole (a
  bare review code such as `F1` registered in the lexicon launders the review-code flag, fixed by
  refusing a standalone review code); a date/degenerate range (`12-07`, `1-1`, fixed by requiring an
  ascending range); and the `## 404` status-code header (fixed by skipping a 3+-digit bare integer).
- **Operator review during the gate** raised three sharp questions, each resolved with evidence.
  (1) Does the recut let Roman smuggle a phase tell? My first answer (drop Roman) did; reversed to
  the value bound, so an ordinal-roman phase up to `XXXIX` still blocks and cannot smuggle while the
  abbreviations do not false-flag. (2) Is the evidence enough? The `.rs` corpus grounds the demotions
  but is register-limited, so the gap was measured directly: `phase <UPPERCASE>` occurs zero times in
  35.5k `.rs` files, and `box`/`boxes`/`steps` + numeral occurs once in markdown, so the roman-acronym
  false-flag and the retained doc-register terms both carry low real exposure. (3) Does the LEXICON
  support a domain term like this? No, by design (`call/0006`, `call/0019`): the LEXICON registers
  genuine vocabulary and refuses a tell, an irreducible domain tell goes in a `host-lint:ignore` fence
  or is reworded; the no-laundering guard is what makes the LEXICON "not an escape".

## Status

In-house complete and the doctrine gate passed; releasing. The worktree carries the remediation on top
of the v0.11.0 pin (the recut and lexicon guard, the fail-opens and prose lane, the rule-source rewrite
and coverage, the no-hollow-green dogfood, the ordinal-naming self-consistency fix, and the cast-gate
fixes). Verification: 85 unit/property tests, clippy clean, 128 integration cases, the strict-discharge
gate clean across all 51 obligations with the kani rungs re-derived, `allium check` clean, and
`lint-skill.sh` passing in full (in the materialized worktree and on a repo-named checkout).

Remaining: the release and re-pin, and the host-lifecycle propagation (host-lint is a library
dependency of its in-process prose lane).
