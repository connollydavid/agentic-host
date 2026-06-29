# plan/0051 host-lifecycle review: findings and component remediation

This milestone records a maximum-effort review of `host-lifecycle`, the lifecycle gate,
generator, and migrator, and remediates its component-local findings. It is the first review
in the campaign reserved for software other than `host-reference` (whose review is plan/0050).

The review was driven inside our own tooling rather than by the external lane that produced
plan/0050: a multi-agent pass of nine reviewers across the functional surfaces, then adversarial
verification of every raised finding, then synthesis. That was a deliberate test of whether an
in-house review is as effective as the external pass. It found a genuine headline defect and the
adversarial layer culled a large fraction of the raised findings, so the answer for our own
components is yes.

## The cross-cutting result is split out

The review found that a verification lane can report clean without performing its check. The
obligation-discharge check confirms only that a test name resolves, never that the named test
exercises the rule; and `software --verify-build` attests "every non-exempt build reproduces its
recorded artifact" even when no build was rebuilt (no container runtime present). The same
discharge gap appeared independently in the host-reference review (plan/0050), which makes it
methodology-level, not a host-lifecycle bug.

That cross-cutting doctrine, "a verification lane that cannot perform its check must not report
clean", is remediated in **plan/0052 (no-hollow-green)** under its own cast-reviewed design. The
findings that belong to it (findings 1, 3, 4, 5, 10, and 17 below) are recorded here for the audit
trail and dispositioned *remediated in plan/0052*. Everything else is component-local and fixed in
this milestone.

## What was reviewed

- Component: `host-lifecycle` at its pinned release (`cbe72e6`, v0.31.2): the single `src/main.rs`
  (about 9,557 lines, 356 functions, 115 inline tests), its `host-lifecycle.allium` spec, and its
  `host-lifecycle.obligations` manifest.
- Method: nine reviewers, one per functional surface (subprocess handling, path safety,
  reproducibility, receipts, manifest parsing, doc gates, fail-safe discipline, reuse, test
  adequacy), each reading the real code. Every raised finding was handed to an adversarial verifier
  instructed to refute it against the source, defaulting to refuted where it could not be
  substantiated. A synthesis pass deduped and ranked the survivors.
- Result: 44 findings raised, 17 refuted by verification, 27 surviving, deduped to 24 ranked. Zero
  critical, zero high, 6 medium, 18 low. The verification pass corrected several severities and
  rejected several reviewer exploits as self-defeating or factually wrong.

## The contract the findings test against

- **Fail-safe gates.** Every gate subcommand (`software --check`, the `release` verify gate,
  `prose`, `reconcile`, `entrance --check`, `obligations`) must fail closed: HAZARD or non-zero on
  doubt, no silent skip, no partial mutation. A gate that passes when it should HAZARD, or that
  attests a guarantee it did not establish, is the most severe class.
- **Determinism (call/0018, call/0030).** Discharge is byte-identical re-derivation in a pinned
  toolchain. The artifact-hash comparison, the deps-bundle drift check, and toolchain-pin
  enforcement must be sound.
- **Receipts (call/0042).** The task graph is gated by receipts, latest-receipt-wins, staleness
  detected when an input changes, and a milestone is not complete before its task receipts land.
- **Host-root escape (DetectOffPin).** No worktree or path may escape the host root, and a tracked
  symlink into an un-materialized worktree is rejected.
- **Subprocess hygiene.** It spawns git, curl, tar, sh, a container runtime, sha256sum, host-prove,
  and allium. Unchecked exit status, missing-tool fail-open, argument injection, and
  download-without-integrity are in scope.

## Findings remediated in plan/0052

These six are the no-hollow-green cluster. They are listed here for completeness, with the same line
references the review cited; their remediation, doctrine, and the cast review live in plan/0052.

1. **`software --verify-build` attests "every build reproduces" with no container runtime.**
   `src/main.rs:3450` skips each build when `container_runtime()` returns `None` without
   incrementing the failure count, then `:3510` prints the clean guarantee and exits 0 having
   rebuilt and compared nothing. The sibling `release` path at `:7290` blocks on the identical
   condition, so the correct fail-closed behaviour already exists one lane over. (confirmed)
3. **Seven hazarded-verdict and DetectOffPin obligations are dispositioned to a pure-function
   test.** `host-lifecycle.obligations:22,24,40,41,42,45,51` all point at
   `host_root_escape_is_detected` (`src/main.rs:8416`), which asserts only the helper
   `escapes_root` and never calls `software_check`, produces a Finding, settles a verdict, or
   observes an exit. (confirmed)
4. **DetectUnreproducedArtifact is dispositioned to a test that proves the rule does not bite.**
   `host-lifecycle.obligations:28` names `provenance_attestation_and_exemption`, which exercises the
   benign-note path and sets `build: None` so the rule's precondition is never satisfied. (confirmed)
5. **Receipt re-derivation obligations are mapped to tests that do not exercise re-derivation.**
   `host-lifecycle.obligations:32,50` name a book-layout test and a parse test (a name collision on
   the word "record"); the genuine staleness enforcement is tested elsewhere but not by the named
   obligations. (confirmed)
10. **`software --check` under-enforces DetectArtifactNotReproducible.** `provenance_problems`
    (`src/main.rs:4439`) fires on artifact plus no-toolchain, but never on the rule's second
    disjunct (artifact plus no build recipe), which is caught only in the heavy `--verify-build`
    lane. (confirmed, latent)
17. **The plan/0048 re-deriver-runnability gate has no automated test for its HAZARD branch.**
    `tier_rederiver_problems` (`src/main.rs:4607`) HAZARDs when a declared deep rung cannot run, but
    the only test asserts the green path; the HAZARD branch, added because a missing host-prove
    install hid for two weeks, has no coverage. (confirmed, low)

## Component findings, remediated in this milestone

The eighteen component-local findings, in the review's rank order.

2. **`software --materialize` does not enforce the host-root-escape guard that `--check`
   enforces.** `escapes_root` runs only in `software_check`; the mutating `software_materialize`
   (`src/main.rs:3831`) never calls it, so a `.host-software` name or branch containing `..` could
   place a bare store or worktree above the host root, and the fresh-clone flow runs `--materialize`
   before `--check`. The realistic blast radius is litter in the wrong location, because the
   manifest is trusted operator config and git refuses a non-empty target, but the defensive
   asymmetry is real. Fix: call `escapes_root` on the name, branch, and worktree entries at the top
   of `software_materialize` (and reject in the parser), reusing the exact checks `software_check`
   runs so the two paths cannot diverge. (confirmed)
6. **The deps-bundle provenance cross-check silently no-ops when the lock is absent.**
   `provenance_problems` (`src/main.rs:4464`) prints a note and does not fault when it cannot read
   `deps-bundle.lock`. The reviewer's framing (absence equals corruption, HAZARD always) is wrong:
   the live recipe has legitimately-onboarding components that declare a bundle and have no lock
   yet, and that fix would turn `--check` red for them. The real, narrow gap is that deleting a
   tracked lock in a materialized worktree leaves the cross-check bypassed while the pin reads
   clean. **Engineered, not applied verbatim:** gate the lenient note on an explicit
   not-yet-locked condition and HAZARD a missing lock only for a materialized component that
   declares a bundle. (uncertain)
7. **The task skip gate accepts an arbitrary free-text reason, weaker than the recorder.**
   `task_verdict` (`src/main.rs:2474`) validates the reason only when it begins with `call/`; a
   non-citation reason such as `wip` falls through to a pass, where the recorder `tasks_record`
   requires a valid citation and exits non-zero. The gate is the fail-safe authority over hand-edited
   receipt files, so the asymmetry lets work through with an unaccountable justification. Fix:
   require a valid cited decision in the skip arm and HAZARD otherwise. (confirmed)
8. **`tasks --rederive` reports success when the verify passes but the receipt cannot be written.**
   `tasks_rederive` (`src/main.rs:2846`) prints a cannot-write note and increments neither the
   failure nor the refreshed count, so a run where every verify passed but every write failed exits
   0 having persisted nothing. The manual-record path treats the same error as fatal. Fix: treat the
   write error as a failure so the exit code reflects the unpersisted state. (confirmed)
9. **`migrate-receipts` writes three files individually-atomic but not atomic as a set.**
   `migrate_receipts` (`src/main.rs:6789`) writes the stamp (which strips the applied lines) before
   the receipts file (which should receive them), so an I/O fault between the two leaves the applied
   set deleted from one and never written to the other, recoverable only through git. Fix: write the
   data-receiving file before the data-shedding file, or stage all three and rename in dependency
   order. (confirmed, low)
11. **`milestone_complete` reads raw markdown while `parse_tasks` masks fenced code.** Within the
    task gate the two plan-README sub-parsers disagree on fences (`src/main.rs:2497` versus `:2141`),
    so a fenced `## Status` example flips the receipt-gating completeness verdict. This weakens the
    gate whose purpose is to refuse a complete milestone whose receipts have not landed. Fix: run
    `milestone_complete` over the fence-masked view, or factor one fence-aware document scan shared
    by every plan-doc check. (confirmed, latent)
12. **The reconcile concept and link-integrity gate has no fence masking.** `scan_concept_anchors`
    and `concept_links_on` (`src/main.rs:1583`) scan raw lines with only a per-line backtick guard,
    so a heading or link inside a fenced example is treated as a live concept home or link, yielding
    a false duplicate-home HAZARD or a dead-anchor link that passes. The sibling task gate already
    tracks fence state, so the two markdown gates disagree on identical input. Fix: thread the
    fence-masked view through the concept and reconcile scans. (confirmed, latent)
13. **Two divergent readers decide whether a deep rung is declared.** The tier gate uses a raw
    substring `contains("kani:")` over concatenated obligation bodies (`src/main.rs:4532`) while the
    obligations engine parses dispositions and requires `parse_rung` to see the prefix as a real
    token (`:4857`), so a comment line or a non-rung disposition makes the gate demand a CI lane and
    a re-deriver for a tier the engine does not treat as a rung. Fix: have the lane gate parse
    manifests with the same parser the engine uses. (confirmed)
14. **`[verification]` is not a singleton and `drivers` is last-wins.** `parse_project_facts` guards
    `[entrance]` against duplicates and emptiness but not `[verification]` (`src/main.rs:1398`), so a
    second stanza, a repeated key, or an empty `drivers` silently disarms the reconcile
    verifier-coverage check. Fix: mirror the `[entrance]` handling (count stanzas, flag a repeated
    key, treat an empty `drivers` as a problem). (confirmed)
15. **The software-root and spec-home concepts have only link-integrity, no content bite.**
    `concept_checks` (`src/main.rs:1702`) runs the content check only for components and verifiers;
    the single-value homes get anchor and link checks but no content verification, and the old
    predicate that checked their content runs only over the deprecated inline annotations agentic-host
    has deleted. **Engineered, not applied verbatim:** the reviewer's lift-the-old-predicate fix is
    unsound (the real spec-home text "never under plan/" would false-positive); add a content
    assertion correct against the canonical wording instead. (confirmed)
16. **A duplicate `[software "<name>"]` stanza is silently accepted.** `parse_software`
    (`src/main.rs:3537`) pushes a fresh entry per header with no duplicate-name detection;
    materialize and release act on the first, so the second's url is ignored. The project-facts
    parser already flags duplicates, so this is an inconsistency. Fix: reject duplicate component
    names with a precise error. (confirmed, low)
18. **`milestone_complete` reads a narrow completion lexicon only from the milestone README.**
    Completion is recognised only when the first line under `## Status` begins with
    complete, done, or landed (`src/main.rs:2497`); a synonym, a markdown bullet, or completion
    marked only in PLAN.md reads as open. Every live plan uses the recognised words today, so this is
    a missed nudge, not a false complete. Fix: broaden the lexicon and strip list markers. (uncertain)
19. **The reconcile coverage check uses substring rather than token matching.** `cover`
    (`src/main.rs:1697`) tests membership with `str::contains`, and `host-reference` is a substring
    of the longer helper names. The reviewer's cited exploit is self-defeating (the example still
    contains the token as a delimited word), and STRUCTURE.md names all members today, so it is a
    precision gap in a recall-biased heuristic, not currently triggered. Fix: match on token
    boundaries. (uncertain)
20. **The entrance tools coverage is an un-anchored substring search over the whole document.**
    `entrance_problems` (`src/main.rs:1860`) checks each wired tool with a whole-document substring,
    so a tool named only inside a URL or a fence satisfies the restatement. The doc-comment marks
    this as an intentional lenient-presence choice and a test asserts it, so it is a genuine
    bug-versus-intent ambiguity. Fix, if treated as a defect: require the token at a word boundary in
    masked prose; otherwise record the intent. (uncertain)
21. **Recorded artifact, hooks, and deps paths bypass the escapes_root guard.** These paths feed
    `Path::join` without the lexical guard applied to name and branch (`src/main.rs:3652`), and an
    absolute artifact path replaces the base so `--verify-build` would hash a file outside the
    throwaway worktree. The manifest is trusted operator config and the footgun is largely
    self-detecting, so this is defence-in-depth. Fix: reject an absolute or escaping artifact, hooks,
    or deps path in the parser. (uncertain)
22. **`release` stages the deps-bundle into the live canonical worktree.** An abnormal termination
    between staging and restore (`src/main.rs:7352`) leaves vendored deps and an edited
    `.cargo/config.toml` behind, with no Drop guard. The vendored files are gitignored and the tool
    never commits, so the operator sees the modified tracked file in git status before any commit.
    Fix: stage in a throwaway detached worktree as `--verify-build` does, or register the restore on
    a Drop guard, or refuse to proceed when a prior staged snippet is detected. (uncertain)
23. **There is no single shared markdown document view.** The heading and anchor primitives are
    already shared functions, so the headline is overstated; the genuine kernel is that the inline
    backtick guard is hand-copied at several sites and two block-fence loops exist. No correctness
    defect follows directly; the fence divergences in findings 11 and 12 are the concrete cost. Fix:
    consolidate the duplicated inline-backtick guard and unify the two block-fence loops. (uncertain)
24. **`collect_files` follows symlinks.** It classifies entries with `is_dir`/`is_file` (which
    follow symlinks) with no guard, unlike the sibling `tracked_markdown` which skips symlinks
    (`src/main.rs:864`). `remap` is an operator-run self-targeting migration that refuses on a dirty
    tree and acts only on the operator's own dictionary, so there is no untrusted-input vector; this
    is the lowest-ranked finding (verdict uncertain, reachable false). Fix: take the type from the
    DirEntry without following, and skip symlinks, mirroring `tracked_markdown`. (uncertain)

## What was checked and cleared

The negatives bound the work. The review confirmed the verification ladder's deep rungs already
discharge correctly (the `--rederive` path runs the verifier through host-prove and requires a PASS,
and a missing re-deriver returns UNPROVEN and exits non-zero), so the no-hollow-green work in
plan/0052 finishes an uneven application of a pattern the codebase already trusts, rather than
inventing one. Determinism in the gate output, the receipt parse and latest-wins logic, and the
manifest validation for url and pin presence are sound. The path-safety and manifest findings are
bounded by `.host-software` being trusted, gitignored, operator-authored config.

## Disposition

The eighteen component findings are remediated in this milestone and released as a host-lifecycle
version, with findings 6 and 15 engineered rather than applied as the reviewers suggested. The
six no-hollow-green findings (1, 3, 4, 5, 10, 17) are remediated in plan/0052 under its cast-reviewed
doctrine. The review campaign stays open: the reviews of host-lint, host-prove, and host-grammar are
still pending, each to be cut under its own milestone.
