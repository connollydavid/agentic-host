# plan/0022 design review — confirmed findings

Adversarial design review (workflow `wf_43f48892`, 58 agents, 7 dimensions × find→verify). 51 candidates, 50 confirmed, 1 dropped. 98% confirm rate means the verifier ran lenient; the load-bearing ancestry claims were re-verified by hand against host-template history (orphaned SHAs and descendant≠depends both confirmed). Findings drive the v2 design in README.md.


## Blocker (15)

### [ancestry-and-guard] Earliest ledger entries are orphaned from template HEAD, so the watermark-advance guard can NEVER be satisfied at HEAD — every adopter is permanently blocked or permanently over-reported
*verdict: partial*

**Scenario.** Run against the real template. `git merge-base --is-ancestor 8c28e33 HEAD` is NO, likewise 325f2cf and 71d12a8 (the early 'bare store', 'worktree-absence', 'tool-submodule coherence' entries) — they were rebased/rewritten off the mainline when PRs #1/#2 etc. were merged (common ancestor is bf5837f). Consequence A (guard): the guard refuses advancing `revision` to <rev> if ANY entry ancestor-or-equal <rev> is unapplied. But these 3 entries are NOT ancestor-or-equal to HEAD, so they are invisible to the guard's `ancestor-or-equal(<rev>)` enumeration — meaning a brand-new adopter who applies them and stamps HEAD is fine, BUT an adopter who has them in their `revision` lineage (stamped at an old commit on the rewritten branch) can never advance because their old `revision` is also not an ancestor of HEAD, so `merge-base --is-ancestor have HEAD` fails and `upgrade_applies`/the guard treat the relationship as undefined. Consequence B (upgrade listing): `upgrade_applies(have=431f781, landed=8c28e33)` returns false (HEAD is not an ancestor of 8c28e33), so these three real, structurally-important entries are silently never listed as pending by anyone whose watermark is on the current mainline — the very migrations the ledger exists to carry are unreachable by ancestry.

**Fix.** Fold an "orphaned-ledger-key" classification and a loud-on-unresolvable rule into plan/0022's listing/guard model. The defect is real (the three earliest keys 8c28e33/325f2cf/71d12a8 are not ancestors of template HEAD 431f781; merge-base bf5837f), but it lives in the ancestry-listing assumption, not the guard, and it is a silent UNDER-report (fail-unsafe drop) — not the "permanent block at HEAD" the reviewer claims. Corrections:

1. Replace the pure pairwise `merge-base --is-ancestor have landed` test in `upgrade_applies` with classification relative to BOTH the adopter's `revision` and the template tip being upgraded toward (default HEAD). For each ledger id resolve it, then bucket:
   - in-range / applied: reachable-from `revision` OR id ∈ `applied` → APPLIED.
   - owed: reachable-from-tip AND not-reachable-from `revision` AND not in `applied` → PENDING.
   - ORPHANED: resolves but is reachable from neither tip nor `revision` (e.g. 8c28e33) → emit a distinct `ORPHANED — off the upgrade lineage; cannot order by ancestry, status by \`applied\` membership only` line. It is owed unless its id is in `applied`; never silently dropped.
   - UNRESOLVABLE: id does not resolve in the local template → hard-error (the ledger references a SHA the fetched template lacks), since `git_ok` currently masks this as the same `false` as a non-ancestor. Add a `git_out rev-parse --verify` probe so unresolvable is distinguished from non-ancestor and surfaced loud, not buried.

2. The watermark-advance guard must enumerate "ledger ids reachable from <rev>" and additionally treat any ORPHANED-or-UNRESOLVABLE id encountered while computing the set as a hard error (not a silent pass), so a rewritten-history ledger fails loud rather than letting an early migration fall outside the `ancestor-or-equal(<rev>)` window. Do NOT adopt the reviewer's claim that the guard blocks at HEAD — at HEAD the orphans are outside the enumerated set today; the fix is to make them visible-and-classified, not to relax the guard.

3. Cheaper structural alternative to fold in alongside: re-key the three orphan entries to their landed mainline equivalents (8c28e33→96244fc, 325f2cf→291113c, 71d12a8→d2e8105) so the ledger keys lie on the live lineage; this restores ancestry-listability for all adopters and is a one-line-per-entry ledger edit. The classification logic in (1)/(2) is still required to make future rebases fail loud, but re-keying removes the present silent drop immediately.

### [ancestry-and-guard] Sibling/non-linear ledger entries make 'ancestor-or-equal(revision)' ill-defined: a watermark on one branch marks a sibling entry neither applied nor advanceable-past
*verdict: partial*

**Scenario.** `71d12a8` and `bbbfdc3` are siblings — `git merge-base --is-ancestor` returns false in BOTH directions (common ancestor bf5837f). The design's core predicate 'applied iff ancestor-or-equal(revision) OR id in applied' assumes a total order. With siblings: if an adopter's `revision` is bbbfdc3, then 71d12a8 is NOT ancestor-or-equal(bbbfdc3), so it lists as PENDING forever even though bbbfdc3 is 'later' in the ledger file order and the work may be moot. Worse for the guard: advancing `revision` to a commit C that is a descendant of bbbfdc3 but where 71d12a8 is reachable-from-neither means the guard's enumeration of 'entries ancestor-or-equal C' may or may not include 71d12a8 depending on whether the rewritten 71d12a8 is on C's lineage — the answer is genuinely undefined for sibling history. The tool will either block an upgrade that should proceed or wave through one that skips a real entry, non-deterministically across adopters with different `revision` branches.

**Fix.** Fold a ledger-soundness model into plan/0022 that survives the repo's own history rewrites rather than forbidding them.

1. State the invariant the predicate actually needs, and a fail-loud lint: every `[upgrade "<id>"]` id MUST be resolvable AND reachable from the template tip (`git merge-base --is-ancestor <id> <tip>`). Add `host-lifecycle upgrade --lint-ledger` (and fold into `software --check`) that errors loud listing any id that is unresolvable, orphaned-from-tip, or a sibling of another id. Run it on the REAL ledger first: it will immediately flag 8c28e33, 325f2cf, 71d12a8 as orphaned (they live only on archive/pre-host-rename; 71d12a8's content moved to d2e8105). This converts today's silent unsoundness into a visible, must-fix error.

2. Because those orphaned SHAs are the permanent residue of a sanctioned past history rewrite and MADR/append-only forbids rewriting historical entries, do NOT require a relinearized chain. Instead give the ledger entry an optional rebase/identity bridge: a `superseded-by = <live-sha>` (or `moved-to`) key on an orphaned `[upgrade]` stanza pointing at the content-equivalent commit now on the tip's lineage (71d12a8 -> d2e8105). `upgrade_applies`/the applied-predicate then evaluate ancestry against `superseded-by` when present, so an adopter at bbbfdc3 correctly sees 71d12a8 as APPLIED (d2e8105 is its ancestor) instead of PENDING-forever, and the guard's enumeration includes it. `--lint-ledger` accepts an orphaned id ONLY if it carries a resolvable, tip-reachable `superseded-by`; otherwise it errors.

3. Make the guard's enumeration sound against orphaning: 'entries that must be applied before advancing revision to C' = every ledger entry whose effective id (the `superseded-by` if present, else the id) is ancestor-or-equal C. Document explicitly that a bare scalar watermark summarizes only a contiguous PREFIX of the *tip-reachable* effective chain; the `applied` set carries everything above it, and an orphaned-without-bridge id is a hard ledger error, never silently skipped.

4. Add the concrete regression fixture from the live repo to the build-step checks: ledger with orphaned 71d12a8 + bridge to d2e8105, adopter stamped bbbfdc3 -> 71d12a8 reports APPLIED; same ledger with the bridge removed -> `--lint-ledger` exits non-zero naming 71d12a8 as orphaned. Also add a note that the design's stated fail-safe property only holds for tip-reachable ids — orphaned ids without a bridge are the one way the SHA-keyed predicate can mislead, which is exactly why the lint must gate.

### [ancestry-and-guard] When the template repo is absent/unfetched, every ancestry call fails and the guard/consistency-check silently degrade — fail-safe for listing, but fail-OPEN for the guard
*verdict: real*

**Scenario.** `upgrade_applies` already returns true (lists as pending) when `landed` can't be resolved — fail-safe for listing. But the new watermark-advance guard depends on enumerating 'entries ancestor-or-equal <rev>' via `merge-base --is-ancestor`, which returns false (via `git_ok` → `unwrap_or(false)`) when git fails, the template isn't fetched, or <rev>/the entry id is unresolvable. A guard that enumerates by 'is-ancestor returns true' will see ZERO qualifying entries when the template is absent, conclude there is no unapplied work below <rev>, and ALLOW the advance — burying every owed migration. The CLAUDE.md flow even tells adopters to 'fetch the template to the target revision first', i.e. a shallow/partial fetch is normal, so the orphaned early entries and any not-yet-fetched entries are routinely unresolvable. The consistency check (applied entry whose `depends` is unapplied) similarly can't evaluate `depends` reachability without the template and would pass vacuously.

**Fix.** Make the watermark-advance guard and the dependency consistency check fail-CLOSED on any unresolved ancestry, and add an explicit precheck — do NOT reuse the listing path's fail-safe-as-true logic, whose polarity is inverted for a guard.

1. Three-state ancestry primitive. Add a helper distinguishing the three git outcomes instead of collapsing two into false, e.g. enum Ancestry { Ancestor, NotAncestor, Unknown } from the exit code of `git merge-base --is-ancestor a b`: status 0 -> Ancestor, status 1 -> NotAncestor, anything else (incl. spawn failure) -> Unknown. git_ok's unwrap_or(false) must NOT back guard/consistency decisions. The listing path (upgrade_applies) may keep its fail-safe-true behaviour — that path is correct as-is.

2. Guard precheck (fail-closed). Before evaluating the guard, resolve <rev> AND every ledger entry id AND every depends id with `git rev-parse --verify <id>^{commit}` in the template. If <rev> is unresolvable, or any ledger id the guard needs is Unknown/unresolvable, refuse the advance non-zero: "cannot verify the ledger against the template at <rev>: <id> is unresolvable — fetch the full template (git -C <template> fetch --unshallow / fetch origin) and retry. Refusing to advance the watermark." Never advance on Unknown.

3. Guard rule, safe polarity. Refuse if there EXISTS a ledger entry E with Ancestry(E.id, <rev>) in {Ancestor, Unknown} that is neither ancestor-or-equal the post-advance revision nor in applied. Treating Unknown as potentially-blocking is the fail-closed default; the precheck (step 2) converts Unknown into a hard refusal with a fetch hint rather than a silent skip.

4. Consistency check, fail-closed. A depends id counts as applied ONLY if it is in applied (pure string-set membership, no git) OR provably Ancestor-or-equal the watermark revision. If a depends id is Unknown/unresolvable AND not in applied, ERROR (do not pass): "applied entry <e> declares depends <id> which cannot be verified against the template — fetch it and re-check." Never let an unverifiable dependency pass silently.

5. Tests for the degraded states. Add tests pointing the guard at (a) git unavailable / not a repo, (b) a clone missing older ledger objects (shallow), (c) an unresolvable <rev> — each MUST refuse the advance non-zero, not allow it. Mirror the existing applies_by_strict_ancestry test (main.rs:3410) so a future refactor that reuses git_ok for the guard is caught.

### [back-compat] Re-stamp writers (adopt's stamp_body, and the new --record/guard writers) rewrite .host from a fixed field list and silently drop unknown lines — erasing `applied` (and `name`)
*verdict: partial*

**Scenario.** stamp_body() at src/main.rs:291 builds .host from exactly template+revision+adopted. The live /mnt/c/Users/david/dev/agentic-no-phase-skill/.host already carries a `name = "agentic-host"` line that stamp_body does NOT emit, so running `adopt` over an existing host today already drops `name`. The plan adds `applied` as a fourth, OPTIONAL line and says `--record` and the watermark-advance guard write `.host` themselves. If those writers reuse the stamp_body whole-file-rewrite pattern (the only stamp writer that exists), then: (1) `upgrade --record 7de7cb1` writes a .host that has `applied = 7de7cb1` but no `name`; the next `book` call loses the project title. (2) Worse for the stated fail-safe goal: any writer that rewrites the file from known fields and is run by a tool build that does not yet include `applied` in its field list will DELETE a previously-recorded `applied` set — turning cherry-applied entries back into PENDING with no record they were done, or (if the deletion is of the watermark-guard's understanding) burying debt. The README's central promise ('a forgotten record re-lists, never hides owed work') holds only if every stamp writer is round-trip-preserving of unknown/optional lines, which the current single writer is not.

**Fix.** Make all .host writers read-modify-write, never regenerate-from-field-list. Add a stamp model that (a) parses every line of the existing .host into an ordered list of (key, raw-line) pairs, preserving unknown keys, comments, blank lines, and exact spacing/quoting byte-for-byte; (b) mutates ONLY the targeted field (revision for the guard/adopt, applied for --record), inserting a new line in a defined position if the field is absent; (c) re-serializes every line it read. Route adopt, upgrade --record, and the watermark-advance guard through this single serializer. Fix the pre-existing name-drop in the same change: today `adopt` over an existing host erases `name = "agentic-host"`, which silently changes the mdBook title (stamp_title falls back to the checkout dir name) — read-modify-write fixes this for free, but add it as an explicit acceptance.

Add round-trip tests (currently none exist): load a .host containing template+revision+adopted+name, run `upgrade --record <id>`, assert template/revision/adopted/name survive unchanged and `applied` gained exactly that one id; re-record the same id and assert the file is byte-identical (idempotent); record a second id and assert it appends without disturbing the first or any other line; run the watermark-advance guard's writer and assert `name` and `applied` both survive.

Scope-correct the reviewer's framing in the design rationale: dropping a recorded `applied` set is the FAIL-SAFE direction (those entries re-list as PENDING via is_applied = in-range OR in-applied) — it cannot bury debt; that is the design's intended property. The data-loss risk that actually warrants the blocker is the silent erasure of `name` (and any future unknown key), not debt-burying. State this so the round-trip requirement is justified by the correct hazard.

### [completeness] `software --check` cannot surface partial-upgrade state — the function has no stamp or ledger plumbing at all
*verdict: real*

**Scenario.** The plan (design bullet 4 and build step 3) says the consistency check fires in 'software --check where cheap'. But `software_check()` (main.rs:1469) only iterates `.host-software` recipe stanzas and checks worktree pins; it never reads `.host`, never calls `find_template_dir`, never parses `UPGRADING.md`. A cold-start auditor (Sable) or a CI gate runs `software --check .`, gets a clean 'ok' on every worktree, and concludes the repo is healthy — while an applied entry with an unapplied `depends` sits in the stamp undetected, because the only place that check lives is `upgrade`, which CI does not run as a gate. The plan's fail-SAFE claim ('a CI gate cannot be deceived into up-to-date while work is owed') is unbacked: no CI workflow runs `upgrade` as a gate, and `--check` (which CI does run) is blind to the stamp.

**Fix.** Pick one gate location and name it in the build steps; the plan currently ships neither. Recommended: add a dedicated `upgrade --check <dir>` mode plus a CI job, and stop relying on `software --check` "where cheap".

Concretely fold in:

1. New build step (between current 3 and 4): "`upgrade --check <dir>` — re-run the applied-set computation and the dependency consistency check, exit non-zero on ANY inconsistency (an `applied` id whose declared `depends` is unapplied) OR an unresolvable/unknown id in `applied`. Pending-but-consistent is exit 0 (pending is informational, per the fail-safe model). verify: fixture with an inconsistent stamp -> non-zero; clean-but-pending -> zero." This reuses `find_template_dir` + `parse_upgrading` + `is_applied`, which `upgrade` already needs, so it is cheap to add there and avoids retrofitting stamp/template plumbing into `software_check` (which today has none).

2. Guard `--record` at write time (amend build step 4): "`--record <id>` refuses (exit non-zero) if `<id>`'s declared `depends` are not already applied, so the sanctioned path cannot create an inconsistent stamp in the first place. verify: record of a depends-on-unapplied entry is rejected." This closes the only reachable route to an inconsistent stamp and makes `upgrade --check` a defense-in-depth backstop rather than the sole guard.

3. New build step (CI wiring): "Add an `upgrade --check .` step to the CI workflow (`reproducible-build.yml`, alongside `software --check`) so the cold-read CI gate the design promises (lines 106–108; cast/bly.md) actually runs against the stamp. verify: a deliberately-inconsistent `.host` on a branch fails CI."

4. Edit design bullet 4 to drop "(and `software --check` where cheap)" — replace with "exposed as `upgrade --check`, run as a CI gate." Edit the Bly acceptance bullet / verification section so "a CI gate cannot be deceived" cites `upgrade --check`, not `software --check`. The plan's existing `software --check .` step (build step 9) stays for pins/lanes but is no longer claimed to surface stamp inconsistency.

If instead you prefer option (a) — wiring into `software_check` — the plan must explicitly scope passing the stamp+template into `software_check` (it currently takes only `&[Software]`), reading `.host` via `parse_revision`/the new `applied` parser, calling `find_template_dir` + `parse_upgrading`, and emitting a HAZARD line on inconsistency so it joins the `bad` count. That is more new surface than option (b)+CI for the same guarantee, so prefer the `upgrade --check` route.

### [completeness] No migration story for existing adopters' `.host` files (the legacy hand-jumped watermark)
*verdict: real*

**Scenario.** The Why section says the only workaround today is 'jump the watermark and note the debt in prose MEMORY'. That means a real stuck adopter already has a `.host` whose `revision` was advanced past unapplied work — exactly the debt-burying state the new guard forbids. After they bump host-lifecycle, the new model treats every entry ancestor-or-equal to that jumped `revision` as APPLIED (the contiguous-baseline rule), so the buried debt is now silently blessed as done — the migration LAUNDERS the very unsafe state the plan exists to fix. The plan adds back-compat for a stamp with no `applied` line but says nothing about a stamp whose `revision` was dishonestly advanced.

**Fix.** Add a one-time legacy-stamp migration, carried as both an UPGRADING.md entry and a step in the upgrade skill, addressed to any adopter whose `revision` was hand-advanced past unapplied work (the documented "jump the watermark + prose MEMORY" workaround). The tool cannot auto-detect this — the only record of what was truly applied was prose — so the migration is procedural and must run before the new applied-set semantics are trusted:

1. Roll `revision` back to the true contiguous baseline: the newest entry such that EVERY ledger entry ancestor-or-equal to it was genuinely applied, in order, with no gap. (When in doubt, roll further back — over-listing is the fail-safe direction.)
2. For each entry the adopter genuinely applied out of order above that baseline, run `host-lifecycle upgrade --record <id>` so it lands in the `applied` set through the tool, never by hand-editing the stamp.
3. Run `host-lifecycle upgrade` and confirm every entry that is actually still owed now shows PENDING. The buried debt re-lists; nothing is silently blessed.

Make this the upgrade skill's mandatory first check for any pre-0022 stamp: before reporting status against a legacy stamp (no `applied` line), the skill must prompt the operator to confirm the `revision` is the honest contiguous baseline, and walk the rollback-then-record procedure if it was ever hand-jumped. Tie the rationale to the existing guard: the guard only stops FUTURE debt-burying advances; this migration is what converts an ALREADY-buried advance into the same fail-safe channel, so the plan's "never hides owed work" property holds for the field victims it was written for, not only for future upgrades. Cover it with a fixture test: a legacy stamp whose `revision` was jumped over an unapplied entry, after the documented rollback+record, must re-list the skipped entry as PENDING (proving the laundering is undone), and the consistency check must remain silent on the corrected stamp.

### [dependency-hints] The proposed back-fill is factually wrong: the two 'independent' entries (7de7cb1, ae1e688) are DESCENDANTS of the entire spec-lane chain, so they can never be cherry-applied 'without' it under the watermark+applied model the design defines
*verdict: partial*

**Scenario.** git in host-template/ confirms: `merge-base --is-ancestor 821a216 7de7cb1` = YES, and 7de7cb1 contains b6232a5/c771d60/b8c54fc/821a216/ae1e688 (all are ancestors of 7de7cb1). The README's motivating story is 'an adopter several revisions behind needs the late independent 7de7cb1 WITHOUT the earlier specs-to-software migration b6232a5..821a216', recorded via `applied = 7de7cb1`. But an entry is applied iff ancestor-or-equal(revision) OR id in applied. Marking 7de7cb1 applied does NOT mark its ancestors applied, so `upgrade` correctly still lists b6232a5..821a216 as PENDING — good. The hole is the *annotation*: the design says 7de7cb1 is `independent`. It is not independent of the spec migration in any operational sense — applying the worktrees-under-root rule (7de7cb1) to a repo that never relocated its specs (b6232a5) is fine in isolation, but the back-fill labels it `independent` as a blanket claim. Worse, the symmetric claim that ae1e688 (adopt-in-place) is independent while ae1e688 is itself an ancestor of 7de7cb1 means the two 'independent' entries are themselves in an ancestor relationship, so 'cherry-apply 7de7cb1 alone' implicitly drags ae1e688 into watermark range the moment revision advances. The empirical premise of plan/0022 (a real stuck adopter cherry-applying 7de7cb1) does not match the actual commit graph.

**Fix.** Fold three changes into plan/0022, scoped to the "Dependency hints" section and the back-fill/verification steps — the stamp model, guard, and fail-safe property are unchanged.

1. DEFINE `independent` precisely as an ACTION-semantics claim, explicitly decoupled from git ancestry. Add to the design: "`independent = true` asserts only that this entry's action has no precondition on any earlier ledger entry's effect (its preconditions are satisfiable on a repo that never applied the earlier actions). It says NOTHING about git ancestry: an `independent` entry is still, in a linear history, a descendant of earlier ones, and its earlier entries remain owed and PENDING until separately applied or recorded. `independent` never authorizes advancing `revision` (the watermark) or skipping ancestors — only an `applied = <id>` cherry-record applies a single entry out of order." This kills the unsafe reading and resolves the ae1e688-vs-7de7cb1 incoherence (both can be action-independent of the spec relocation while one is an ancestor of the other).

2. RE-DERIVE the back-fill from entry CONTENTS, audited against the real graph (per the deep-audit-each-target rule), and state the audit explicitly: the spec-relocation chain acts on `.allium`/`.tla` specs and the spec-lane CI; 7de7cb1 acts on `.host-software` worktree paths; ae1e688 acts on `classify` refusing software repos. These three act on disjoint surfaces, so 7de7cb1 and ae1e688 are action-independent of the spec relocation — which is the design's intended point. Keep the spec-lane internal `depends` chain (c771d60 depends b6232a5, etc.) as a genuine action-precondition chain, not a restatement of ancestry. Correct the README's motivating sentence so it does not imply ancestry-skipping: e.g. "apply the worktrees-under-root action (7de7cb1) now via `applied = 7de7cb1`, leaving the specs-to-software migration (b6232a5..821a216) PENDING and owed."

3. ADD a test fixture built from the ACTUAL host-template ledger SHAs (b6232a5, c771d60, b8c54fc, 821a216, ae1e688, 7de7cb1 against a 699db99 baseline), replacing/supplementing the synthetic r1/r2 fixture, so the back-fill's claims are checked against ground truth: assert that with `applied = 7de7cb1` and `revision = 699db99` the spec chain still reports PENDING (fail-safe), that the `depends` consistency check fires when an applied entry's declared dep is unapplied, and that the watermark-advance guard refuses advancing `revision` to 7de7cb1 while any ancestor entry is neither in range nor in `applied`.

### [dependency-hints] is_applied / is_ancestor is built on git ancestry, but three ledger SHAs (8c28e33, 325f2cf, 71d12a8) are NOT ancestors of template HEAD — they are on an orphaned/rebased branch
*verdict: partial*

**Scenario.** `merge-base --is-ancestor 8c28e33 HEAD` = NO for all three; merge-base(8c28e33,HEAD) is an unrelated commit bf5837f. The current `upgrade_applies` already silently mis-handles this: for any adopter whose `have` is on the current line, `merge-base --is-ancestor have 8c28e33` is false, so the bare-store-with-worktrees migration (8c28e33) is reported NOT pending even for a brand-new adopter who never did it. The new design inherits this primitive for both `is_applied` and the consistency check. A `depends = 8c28e33` (or any depends naming a SHA that got rebased out) will then be evaluated by ancestry against a dead commit and the result is undefined/false-negative, defeating the 'fail loud' guarantee.

**Fix.** Fold a resolvability+reachability gate into the design's shared ancestry helper, and stop relying on ancestry to mean "applied/owed" for ids not on the adopter's line. Concretely:

(1) Resolve-or-error, in the helper that backs is_applied, the consistency check, AND the watermark guard: for every ledger `[upgrade "<rev>"]` id and every `depends`/`applied` id, first `git rev-parse --verify <id>^{commit}` in the local template. If it does not resolve, `upgrade` must EXIT NON-ZERO with a loud "unresolvable ledger id <id> — fetch the template (incl. archive tags) to the target revision" — never silently treat it as applied/owed/safe. (Note: today's upgrade_applies returns true=PENDING on unresolvable `landed`, which is fail-safe for *listing* but the wrong default for the new guard/consistency predicates, which need an explicit error.)

(2) For a resolvable id that is NOT ancestor-or-equal of EITHER the adopter's revision OR template HEAD (an off-mainline / rebased-out id like 8c28e33, whose merge-base with HEAD is an earlier commit), do not let any predicate fall through to a bare is-ancestor=false. Detect it (`! merge-base --is-ancestor <id> HEAD` while `<id>` resolves) and surface it as a distinct status, e.g. `ARCHIVED <id> <title> — superseded line; applied iff your stamp predates the fork (bf5837f) or it is in `applied``. This makes the orphan entries' status explicit instead of silently not-owed, and keeps the fail-safe: a pre-fork adopter still sees them PENDING.

(3) Do NOT adopt "freeze against tags" as written — the template has no vX.Y.Z release tags (those are host-lifecycle's, a different repo). If a stable id is wanted, add an explicit ordinal/seq key per `[upgrade]` stanza and order by ledger position, using git ancestry only as a secondary applied-test against ids that resolve and are on-line; this removes the dependence on rewritable/orphaned template SHAs without inventing tags that don't exist.

(4) Add a regression fixture mirroring this repo's real topology (a fork commit, an archived orphan line carrying entries, a rebased live line carrying the equivalent work): assert (a) a pre-fork stamp lists the orphan entries PENDING, (b) a live-line stamp lists them ARCHIVED (not silently absent), (c) an unresolvable id errors loud in all three predicates, (d) the guard refuses to advance past a genuinely-unapplied on-line entry.

### [fail-safe] `--record <id>` (and a hand-added `applied` id) asserts application without verifying it — recording an unperformed INDEPENDENT entry hides owed work permanently
*verdict: real*

**Scenario.** Adopter is behind HEAD. `upgrade` lists `7de7cb1` (worktrees, annotated `independent`) as PENDING. Fen (the 4B) is told to apply-then-record; it runs `host-lifecycle upgrade --record 7de7cb1` but never actually performed the worktree-relocation action (it fumbled, or skipped the manual step, or recorded the wrong-but-valid id). `--record` writes `applied = 7de7cb1` into `.host` unconditionally — step 4's only validation is that the id is a well-formed/known ledger id, not that the action ran. Now `is_applied(7de7cb1) = (7de7cb1 in applied) = true`. `upgrade` drops it from the PENDING list and, if it was the only newer entry, prints "up to date". The consistency check cannot fire because `7de7cb1` is `independent` (no `depends` to be unapplied). Owed work is silently hidden and never re-lists. This is the design's exact inverse failure mode: it proves "a forgotten record re-lists" (the safe direction) but the membership set is monotonic-trusting in the unsafe direction — a *premature/erroneous* record buries. The whole point was to serve a low-reliability agent whose tool calls cannot be trusted, yet `--record` trusts the very tool call most likely to be issued without the work behind it.

**Fix.** Make `applied` a *claim register*, not a *trusted set*, and make `--record` more than a bare assertion. Concretely fold these into plan/0022:

1. Post-condition gate where the ledger declares one. Add an optional `verify = <shell-or-host-lifecycle-check>` field to UPGRADING `[upgrade]` entries (a machine-checkable post-condition; e.g. for `7de7cb1` worktrees, the no-worktree-escapes-root check that `software --check` already runs). `upgrade --record <id>` runs that `verify` and refuses to write `applied = <id>` if it fails. An entry whose action has no machine-checkable post-condition carries no `verify`; recording it then REQUIRES an explicit `--unverified call/NNNN` decision citation (resolved exactly like `repro-exempt`'s `cited_decision_exists`), so an un-attestable out-of-order claim is never silent — it leaves a `call/` paper trail a cold auditor can find.

2. Cross-check every recorded claim at gate time. `software --check` (and `verify`) iterate the `applied` set and re-run each entry's `verify` post-condition, erroring loud ("DRIFT: applied 7de7cb1 but its post-condition no longer holds") on any claimed-but-unsatisfied entry — symmetric with the existing repro-exempt/artifact attestation pattern. This converts the monotonic-trusting membership into a continuously re-checked claim. (The existing `depends` consistency check stays; this adds the missing independent-entry coverage.)

3. Provenance, append-only. `--record` writes not a bare id but a dated line — `applied = <id>  recorded=<YYYY-MM-DD>  via=<verify|call/NNNN>` (today() already exists) — into `.host` so Sable sees WHEN and UNDER WHAT each out-of-order claim was made. Never rewrite a prior record line.

4. Tighten the Fen acceptance gate to the adversarial path: add an A/B leg where the 4B is induced to `--record` WITHOUT performing the action; the gate passes only if the tool refuses the record (no `verify`/decision) or a later `software --check` flags the unsatisfied claim. This proves the unsafe direction is closed, not just the happy path.

Reject a plain "second confirming token / --applied-action-ran flag" as the sole defense: against a low-reliability agent that will issue `--record` without the work, it will also pass the confirming flag — that only relocates the bare assertion. The verifiable post-condition (or an explicit decision citation when none exists) is the durable teeth.

### [fail-safe] Watermark-advance guard reads the ledger at the LOCAL template pin, so entries newer than the un-fetched pin are invisible and the guard waves the advance through
*verdict: real*

**Scenario.** The guard's promise: refuse advancing `revision` to `<rev>` if any ledger entry ancestor-or-equal `<rev>` is neither in range nor in `applied`. But `upgrade`/the guard read `UPGRADING.md` from the template submodule *at whatever commit it is currently checked out to* (`find_template_dir` → `template.join("UPGRADING.md")`), and resolve revisions against that local clone. The methodology's own upgrade instruction is 'Fetch the template to the target revision first.' An adopter (or Fen) advances `revision` to a SHA that is newer than the locally-checked-out template pin without fetching. The ledger text the guard sees does not yet contain the entries between the old pin and the target SHA (they were authored upstream after the local pin), so the guard enumerates zero offending entries and permits the advance. The watermark now sits past entries that exist upstream and were never applied; on the next `upgrade` after a fetch they should re-list — except `is_applied` now reports them ancestor-or-equal `revision` = APPLIED. Owed work is buried by stamping ahead of an un-fetched ledger.

**Fix.** Make the watermark-advance guard fail-CLOSED on an under-fetched target, the opposite default from `upgrade_applies`'s fail-open. Two preconditions, both checked before the guard enumerates any offending entry, against the template submodule's CHECKED-OUT commit `C = git -C <template> rev-parse HEAD` (the on-disk UPGRADING.md the tool reads is exactly the content at `C`):

1. The target must resolve locally: `git -C <template> rev-parse --verify <rev>^{commit}` must succeed. Otherwise refuse.

2. The checked-out template must already contain `<rev>` in its history — i.e. `<rev>` is ancestor-or-equal of `C`: `git -C <template> merge-base --is-ancestor <rev> C` must succeed (and `<rev> == C` is allowed). This guarantees every ledger entry that became required at or before `<rev>` is present in the on-disk UPGRADING.md, so the offending-entry enumeration is complete. If `C` is an ancestor of `<rev>` (or they are unrelated), the local ledger is missing entries between `C` and `<rev>`; refuse.

On either failure, emit and exit non-zero:
  `refuse: fetch the template to <rev> and check it out before advancing the watermark; the ledger past the locally checked-out commit (<short C>) is not visible to the guard, so unapplied entries between them would be silently buried.`

This converts the prose "Fetch the template to the target revision first" step into a tool-enforced precondition — the only fix that protects Fen, who skips prose steps by construction. Hardening note (optional, not required once precondition 2 holds): the guard may read the ledger via `git -C <template> show <rev>:UPGRADING.md` rather than the on-disk file, making the source explicitly tied to the resolved target; with precondition 2 in place the on-disk content already equals the checked-out commit's, so this is belt-and-suspenders. Add a guard test for: advance to a `<rev>` newer than the checked-out template (and to an entirely unfetched SHA) is refused; advance to an ancestor-or-equal of the checked-out commit with no gap is allowed. Reflect the precondition in plan/0022 Build step 5 and in the Verification section.

### [fail-safe] The contiguous-watermark advance sweeps EARLIER unapplied entries into APPLIED because the ledger is a linear chain — the guard can be satisfied by recording only the newest of a contiguous run
*verdict: real*

**Scenario.** Confirmed empirically: every ledger key is an ancestor of the next on `main` (8c28e33 < … < b6232a5 < c771d60 < … < 821a216 < ae1e688 < 7de7cb1). The guard refuses advancing `revision` past an entry that is 'neither in range nor in applied'. Adopter at `revision=b6232a5` (so b6232a5 in range; c771d60, b8c54fc, 821a216 PENDING — the big spec-lane migration). They genuinely apply ONLY the newest of that run, `821a216`, and `--record 821a216`. Now they try to advance `revision` to `821a216` to tidy up. The guard enumerates entries ancestor-or-equal `821a216` not in range and not in `applied`: that is `c771d60` and `b8c54fc` — both have `depends` chains (c771d60 depends b6232a5 [in range]; b8c54fc depends c771d60). The guard SHOULD refuse. But if the implementer writes the guard as 'every such entry is in applied OR in range' and the adopter, prompted by the consistency check that 821a216 depends on c771d60+b6232a5, then *also* records c771d60 and b8c54fc to clear the dependency error WITHOUT applying them — the guard is now satisfied (all are in `applied`), the watermark advances to 821a216, sweeping c771d60/b8c54fc into the contiguous baseline. The consistency check that was supposed to be the teeth instead *trains the agent to record the unapplied dependencies* to silence it, because recording is the only lever the agent has and the tool never distinguishes 'recorded because applied' from 'recorded to satisfy a depends'.

**Fix.** Make `applied` an evidence-bearing record, not a bare id set, and gate every state-change on evidence — so recording can never be the lever that silences the consistency check.

1. Stamp model. Replace the flat `applied = <id> ...` set with provenance-tagged entries. Each recorded id carries WHY it counts as applied, exactly one of:
   - `verified` — a tool post-condition proved it (e.g. `software --check` clean for the lane the entry mandates; the entry names its check), OR
   - `cited <call/NNNN>` — an explicit, recorded decision authorizing a skip/waiver for THIS adopter.
   A bare "I did it" claim is not an accepted provenance. `upgrade` output prints the provenance so a cold read sees how each applied id earned its status.

2. `--record <id>` is NOT an unconditional write. It must (a) refuse unless every id in `id`'s declared `depends` is already applied (topological gate), AND (b) require evidence for `id` itself: either run/confirm the entry's named post-condition check and write `verified`, or be given `--cite call/NNNN` (a resolvable decision) and write `cited`. `--record` with neither evidence nor a citation is refused. This is the teeth the consistency check lacked: there is no unconditional path to put an id in `applied`.

3. Consistency check resolution is one-way. An "applied entry has an unapplied depends" error is resolvable ONLY by genuinely applying (and evidence-recording, per 2) the dependency — never by recording the dependency to quiet the error, because (2) forbids a bare record. Document loudly: `applied` is for genuinely-applied entries; the consistency check is a tripwire to GO DO the owed work, not a checklist to silence.

4. Watermark-advance guard refuses whenever any swept entry (ancestor-or-equal the target revision, not previously in range) rests on a non-`verified` provenance, unless that entry carries a `cited` provenance whose decision the guard re-resolves at advance time. I.e. advancing the contiguous baseline requires that everything it absorbs was genuinely verified or explicitly, decision-cited as skipped — never a bare claim. (Plain dependency-gating alone is insufficient: it only reorders unconditional writes — c771d60's sole dep b6232a5 is in range, so a dep-gate still lets the agent record c771d60 without applying it. The evidence requirement in 2/4 is what actually closes the loop.)

5. Fen-acceptance addendum. The A/B gate must now also drive the real 4B at the trap: present the consistency error for an applied late entry with an unapplied dep, and confirm the tool refuses a bare `--record <dep>` (directing the agent to apply-or-cite) rather than letting the record silence the error. The design passes only if the weak agent cannot bury debt by recording-to-silence.

### [fen-ergonomics] No single 'what do I do next' command — Fen must read a multi-entry listing, select the right line, and synthesize the command itself
*verdict: real*

**Scenario.** Adopter is several revisions behind. Fen runs `host-lifecycle upgrade .` and gets ~17 lines (the current ledger in host-template/UPGRADING.md has 17 `[upgrade]` entries from 8c28e33 through 7de7cb1), most PENDING. To cherry-apply the late independent fix 7de7cb1, Fen must (a) scan the whole listing, (b) find the line that is both `independent` AND `PENDING`, (c) extract its id, (d) build `upgrade --record 7de7cb1`. Steps (a)-(c) are exactly the parse-select-reproduce task fen.md says the 4B fumbles, and the long listing hits the 'wedges on long generation/long context' failure mode. The design (README step 3 and the Fen-acceptance gate) hands Fen the raw multi-line `upgrade` output and expects it to drive the loop; the persona's own requirement ('have the tool ... name the single next action') is unmet. parse-free for a *downstream tool* is not parse-free for Fen, who is the consumer here.

**Fix.** Add a single-next-action command as Fen's entry point, and make the Fen acceptance gate drive it (not the raw listing).

1. New subcommand `host-lifecycle upgrade --next <dir>`: compute the same applied-set/pending set as `upgrade`, then select and print exactly ONE recommendation and ONE runnable command. Selection rule, deterministic and fail-safe:
   - Among PENDING entries, prefer the entry that is (a) `independent` AND (b) has the fewest unmet `depends` (i.e. 0). Tie-break by ancestry order (oldest applicable first) so the choice is stable and reproducible.
   - Output is two lines, no prose to parse: `next: <id> <title> (independent|deps-met)` then `run: <apply hint>; host-lifecycle upgrade --record <id>`. The literal record command is emitted by the tool so Fen copies, never reconstructs, the id.
   - If the only PENDING entries all have unmet `depends`, print the earliest entry whose deps are satisfiable and name the blocking dep explicitly (`next: apply <dep> first`), so Fen is never pointed at an entry that would trip the consistency check.
   - If nothing is pending: `up to date`. Exit 0 when a next action exists or up-to-date; the command is idempotent and re-running after a `--record` advances to the next one.

2. Keep the multi-line `upgrade` listing unchanged as Orin/Sable's audit view.

3. Amend the Fen acceptance gate (README lines 122-129) to drive `--next` as Fen's loop: hand the 4B only the two-line `--next` output and the emitted `--record` command, confirm it completes the cherry-apply by reading one line and running one command — no selection among many, no id reconstruction. This directly satisfies fen.md's "name the single next action" requirement and removes the parse-select-reproduce step the gate currently depends on.

Note for the doc pass: the README's "one line per entry" listing should stay (it serves the audit seat), but `--next` becomes the documented Fen entry point in both README step 3 and the Fen persona-acceptance bullet. Also reconcile the cast/ set — README cites Sable but cast/sable.md is missing.

### [fen-ergonomics] `--record <id>` still forces Fen to reproduce an exact hex SHA — the hand-edit failure relocated to argv, not eliminated
*verdict: real*

**Scenario.** fen.md's core constraint is 'Never be required to hand-edit a stamp file correctly' and the 4B 'hand-edits a config file and gets a field subtly wrong'. Typing/copying a 7-or-40-char hex SHA into `--record 7de7cb1` is the same lossy exact-token operation: the model transposes a digit (7de7cb1 -> 7dec7b1) or truncates. The design removed hand-editing `.host` but kept an exact-id argument as the one thing Fen must emit precisely. README step 4 verify says only 'bad id rejected' — rejection makes Fen retry and re-fumble; it is correct-but-not-ergonomic, the very gap this dimension targets.

**Fix.** Eliminate the exact-hex-token argument for the common path; keep `--record <id>` only as a fallback.

1) Stable short index (primary): the machine-readable `upgrade` listing already prints one line per entry in ancestry order — prefix each PENDING line with a 1-based index, e.g. `1  7de7cb1  worktrees  [independent]  PENDING`. Add `upgrade --record <n>` that resolves index n against the *same* freshly-recomputed pending listing and writes the resolved full SHA into `.host` `applied`. The agent emits a single digit, not a hex token. Print the resolved SHA in the success line so the record is auditable: `recorded 7de7cb1 (worktrees) — applied`.

2) `--record --next` (zero-token path for the recommended move): add `upgrade --next` that prints the single next safe-to-apply entry (lowest-ancestry PENDING entry that is `independent` or whose `depends` are all applied), and let `upgrade --record --next` record THAT entry with no id/index argument at all. This is the literal "tool names the single next action" pattern fen.md asks for.

3) Prefix + near-miss recovery (fallback for `--record <id>`): accept any unambiguous prefix of a pending id; on a non-matching near-miss, do NOT just reject — print the recovery as a copy-able tool-emitted command: `no entry 7dec7b1; did you mean 7de7cb1 (worktrees)? run: host-lifecycle upgrade --record 1` (prefer the index form in the suggestion so recovery costs one digit, not a re-typed SHA).

Keep all forms idempotent and fail-safe: an unresolvable index/prefix is rejected with no write, and the entry re-lists. Update README build-step 4 verify from "bad id rejected" to: "index/`--next` records the resolved entry without an exact-SHA argument; an ambiguous prefix or out-of-range index is rejected and re-lists; a near-miss prints a copy-able `--record <n>` recovery command." Add to the Fen acceptance gate: the 4B must complete the cherry-apply using the index or `--next` form, emitting no hex SHA.

### [record-cmd] Rewriting .host via stamp_body() silently drops the `name` field (and any other non-template key) — the live agentic-host stamp would lose its name on the first --record
*verdict: real*

**Scenario.** The actual /mnt/c/Users/david/dev/agentic-no-phase-skill/.host has four lines: template, revision, adopted, AND `name = "agentic-host"`. But `stamp_body(revision, date)` (src/main.rs:291) only ever emits template+revision+adopted — it has no knowledge of `name`. If `--record` is implemented the obvious way (parse revision, append id, re-serialize through stamp_body), the rewrite produces a 3-line stamp and the `name` line vanishes. `name` is load-bearing: it titles the published book (project_name reads stamp `name`, src/main.rs:2545; test at 3480 asserts it pins the title). So a single `upgrade --record <id>` would silently corrupt the book title and erase an adopter-set field. Any future field added to .host has the same fate. This is the exact 'corrupt the stamp' failure the dimension warns about, and it bites agentic-host itself.

**Fix.** Mandate a field-preserving in-place stamp edit for every write of an existing `.host`; forbid `stamp_body()` (a from-scratch regenerator) as the writer for `--record` and for the watermark-advance/re-stamp paths.

Concretely:
- `upgrade --record <id>` MUST read the current `.host` verbatim and edit only the `applied` line: if an `applied = ...` line exists, rewrite that line in place (add the id to its space-separated set, idempotent — a no-op if already present); otherwise insert a new `applied = <id>` line immediately after the `revision` line. Every other line — `template`, `adopted`, `name`, any unknown/future key, blank lines, comments — stays byte-for-byte unchanged. Same rule for the step-9 re-stamp and the step-5 watermark advance: they edit the `revision` line in place and touch nothing else.
- Rationale to record in the design: `stamp_body(revision, date)` (src/main.rs:291) is a 3-field generator that not only omits `name` but also resets `adopted` to `today()` and forces `template` to the hardcoded `TEMPLATE_URL`. Reusing it for any edit of an existing stamp silently destroys adopter-set state (`name`, the real adoption date, a non-canonical template URL). `name` is load-bearing (`stamp_title`, src/main.rs:2547 → `book_toml`, 2535; book title), so the immediate symptom is a corrupted/empty book title, but the underlying defect is "regenerate instead of edit."
- Add a regression test: write a 4-line stamp carrying `name = "agentic-host"` (and a non-today `adopted`), run `--record <id>`, then assert the output (a) contains the unchanged `name` line byte-for-byte, (b) preserves the original `adopted` value, (c) preserves the original `template` line, and (d) now contains `applied` with the recorded id. A second `--record` of the same id must leave the file byte-identical (true idempotence).
- Document in the design's build steps that no `.host` mutation may go through `stamp_body`; the only sanctioned mutators are the in-place line editors above. (`stamp_body` remains correct for the initial `adopt` write only, where there is no prior stamp to preserve.)

### [record-cmd] stamp_field cannot parse the design's own example stamp: an inline `# comment` after a quoted value corrupts the parsed id
*verdict: real*

**Scenario.** The README's example stamp writes `revision = "699db99"            # contiguous baseline` and `applied  = "7de7cb1 ae1e688"   # cherry-applied above it`. stamp_field (src/main.rs:302-311) computes the value as `rest.trim_start().strip_prefix('=')?.trim().trim_matches('"')`. For the revision line that yields `699db99"  # contiguous baseline` (leading quote stripped, trailing char is a letter so no trailing strip) — a corrupted revision. The same parser will be reused to read back `applied`, so an `applied` line with a trailing comment yields a token list polluted with `"` and `#`. Then --record (idempotency check), the applied-membership test, and the watermark guard all operate on garbage, and a re-record will duplicate the id because the membership test never matches the corrupted stored value. The design literally documents a stamp format the tool mis-parses.

**Fix.** Fix stamp_field (tools/host-lifecycle/src/main.rs:302-311) so it ignores anything after the quoted value, then add parse tests AND make the README example self-consistent.

1. Rewrite the value extraction to take the substring between the first quote pair (discarding any trailing ` # comment`), with a loose fallback for the legacy unquoted form:

```rust
fn stamp_field(text: &str, key: &str) -> Option<String> {
    for line in text.lines() {
        if let Some(rest) = line.trim_start().strip_prefix(key) {
            let after_eq = rest.trim_start().strip_prefix('=')?.trim_start();
            // Quoted scalar: value is between the first and second double-quote;
            // anything after the closing quote (e.g. ` # comment`) is ignored.
            let v = if let Some(inner) = after_eq.strip_prefix('"') {
                inner.split('"').next().unwrap_or("")
            } else {
                // Loose unquoted form (e.g. `revision=v0.1.0`): cut an inline
                // comment, then trim.
                after_eq.split('#').next().unwrap_or("").trim()
            };
            if !v.is_empty() {
                return Some(v.to_string());
            }
        }
    }
    None
}
```

This was compiled and verified against: the README's commented `revision`/`applied` lines (now parse to "699db99" and "7de7cb1 ae1e688"), the legacy comment-free quoted form, the existing loose `revision=v0.1.0` test case (main.rs:2811), and the empty-as-absent case (main.rs:3519) — all correct.

2. Add parse tests covering the design's own format:
   - `stamp_field("revision = \"v\"  # comment\n", "revision") == Some("v")`
   - `stamp_field("applied  = \"a b\"  # note\n", "applied")` then split_whitespace == ["a", "b"]
   These tests must exist BEFORE the applied-set feature lands, since no current test exercises a commented line.

3. Fold a one-line note into plan/0022 build step 1: the stamp grammar is "key = \"value\" with an optional trailing `# comment`", and stamp_field is the single reader for revision AND applied (so the applied-membership test, --record idempotency check, and watermark-advance guard all consume the comment-stripped value). This makes the design state the property the parser must hold, so the docs and parser cannot drift again.

(The README example comments can stay as-is once the parser strips them — no need to denude the docs, which is what makes option (a) the right choice over option (b).)


## Major (28)

### [ancestry-and-guard] The watermark `revision` is virtually never a ledger-keyed commit, so 'advance revision to <rev>' has no natural <rev> and the contiguity the guard assumes does not exist
*verdict: partial*

**Scenario.** This repo's own `.host` records `revision = 431f781` = template HEAD, which is NOT any `[upgrade "..."]` key (verified). Ledger keys are the commits where an action 'became required'; the watermark is whatever commit the adopter fetched/stamped. So 'every ledger entry ancestor-or-equal to revision is applied' is the claimed contiguous-baseline invariant, but nothing ever sets `revision` to a ledger key — it gets set to an arbitrary tip by `adopt`/re-stamp. The guard 'refuse advancing revision to <rev> if any entry ancestor-or-equal <rev> is unapplied' presumes the agent supplies a meaningful <rev>; but the normal advance is 'stamp the new template HEAD', and HEAD is ancestor-or-equal to itself and a descendant of every applied entry — so the guard reduces to 'all entries below HEAD must be applied', which is exactly the all-or-nothing contiguous upgrade the design set out to escape. The cherry-apply case (apply 7de7cb1, skip b6232a5) can record 7de7cb1 in `applied`, but the moment the adopter wants to advance the watermark at all (even to pick up a doc change), the guard blocks because b6232a5 is ancestor-or-equal to the new HEAD and unapplied.

**Fix.** Fold a clarifying note into plan/0022 (the Stamp-model section, near L29-44), do NOT change the guard mechanics:

"`revision` is a watermark, not a ledger key. It is whatever template tip the adopter fetched and stamped (`adopt`/re-stamp set it; HEAD is normally an UPGRADING-bookkeeping commit, a child of the last action commit, so it is virtually never itself an `[upgrade "..."]` key). The contiguous baseline is therefore computed by REACHABILITY: an entry is in-baseline iff its id is ancestor-or-equal `revision`. Applied-ness is `in-baseline OR id ∈ applied` (the `is_applied` helper, build step 1) — never 'revision equals a ledger key'.

The watermark is intentionally un-advanceable while any below-target entry is unapplied; that is the fail-safe, not a limitation. Cherry-apply is delivered by `applied`, not by advancing `revision`: record the late independent entry with `upgrade --record <id>` and leave `revision` where it is — `upgrade` then shows the late entry APPLIED and the skipped earlier ones PENDING, and a cold read can never be fooled into 'up to date'. Picking up doc-only / non-ledger template commits needs no watermark move at all: re-pin the template submodule pointer (independent of `.host`); `upgrade` lists only ledger actions, so non-ledger changes carry nothing to apply.

The advance guard's `applied` clause already credits a recorded out-of-order entry as applied for the advance check (L67-69). Optionally, when an advance succeeds, drop from `applied` any id that has fallen ancestor-or-equal the new `revision` (now contiguously covered) — pure housekeeping; it never fires while a gap remains below the target, so it cannot drop owed work."

### [ancestry-and-guard] Abbreviated ledger ids and full-SHA `--record` writes mean 'id ∈ applied' string membership can mismatch, and abbreviation collisions over years of history can silently mis-resolve
*verdict: real*

**Scenario.** Ledger keys are 7-char abbreviations (`7de7cb1`). `upgrade --record <id>` writes `.host` itself; an agent (or Fen) may pass a full 40-char SHA, a different-length abbreviation, or a tag. The design defines applied as 'id ∈ applied' — if that is raw string equality, `applied = "7de7cb1d6734..."` will not match a ledger key `7de7cb1`, so the entry re-lists as PENDING (fail-safe direction, but the cherry-apply silently 'didn't take' and the agent loops). If instead membership resolves via `git rev-parse`, then (a) it needs the template fetched (see next hole) and (b) a 7-char abbreviation that is unique today can become ambiguous as the template's object count grows, making `rev-parse` fail or, worse, resolve to a different object — a recorded `applied` id silently pointing at the wrong commit. The existing `upgrade_applies` already normalizes via `rev-parse --verify ^{commit}`; the new membership test must do the same or the two halves disagree.

**Fix.** Canonicalize the applied-set on both write and read, against the template repo, exactly as the existing `upgrade_applies` already does for ancestry — so the two halves of `is_applied` cannot disagree.

WRITE (`upgrade --record <id>`): resolve `<id>` in the template via `git rev-parse --verify <id>^{commit}` and store the FULL 40-char SHA in `applied` (NOT the abbreviation the README example shows). If `<id>` does not resolve, reject with a loud error rather than recording an unverifiable token — this also makes "fetch the template first" a hard precondition of recording, not a silent assumption. Before storing, run `git rev-parse --disambiguate=<id>` (or equivalent) and fail loud if it yields more than one object.

READ / membership (`is_applied`): resolve each ledger key the SAME way — `git rev-parse --verify <ledger-key>^{commit}` in the template — and compare FULL SHAs to the (already-full) stored `applied` SHAs. Never raw substring/abbreviation equality. A ledger key that resolves ambiguously is a loud error (consistent with the write-side guard); a ledger key that does not resolve locally must NOT be silently treated as a member (do not borrow `upgrade_applies`'s "unresolvable landed => applies" rule on the membership side — that would over-claim APPLIED and could hide owed work, breaking the fail-safe invariant).

DOC: update the README example to full SHAs (`applied = "7de7cb1d6734…f924… …"`) so the spec does not re-introduce the abbreviation ambiguity it is removing, and state explicitly that resolution happens in the template repo at the target revision. Add a unit test mirroring the existing `upgrade_applies` test: record a full SHA, assert the matching ledger abbreviation reads back APPLIED (proving full-SHA-stored vs abbrev-key membership agree), and assert re-record is a no-op on the canonicalized value.

### [ancestry-and-guard] Auto-pruning redundant `applied` ids on watermark advance is unspecified, and getting it wrong either resurrects owed work or hides it
*verdict: partial*

**Scenario.** The dimension asks whether advancing the watermark should auto-prune now-redundant `applied` ids. The design (README) does not say. Two failure modes: (1) If pruning is naive 'drop any applied id that is ancestor-or-equal the new revision', and that test runs against an absent/partial template (is-ancestor → false), nothing is pruned and `applied` accretes stale ids forever — harmless until one of those ids later becomes ambiguous or the entry's `depends` no longer resolves, tripping the consistency check on phantom debt. (2) If pruning is too eager and an `applied` id is a SIBLING of the new revision (the 71d12a8/bbbfdc3 case), it is neither ancestor-or-equal nor safe to keep meaningfully — the tool must decide, and silence means the next agent re-records it or the guard re-lists it. Either way a cherry-applied entry's record can be lost across a single watermark advance, violating the stated fail-safe ('a forgotten record re-lists, never hides' — but re-listing an ALREADY-DONE entry is its own fumble that drives Fen into a redundant re-apply).

**Fix.** Add one sentence to the stamp-model section clarifying that the `applied` set is never pruned by default, and that pruning, if ever implemented, is purely cosmetic and fail-closed — NOT framed as a correctness hazard:

"`applied` is append-only in normal operation: `--record` adds an id; advancing `revision` rewrites only the watermark and leaves `applied` untouched. A stale id (one now ancestor-or-equal the new `revision`) is harmless — membership is an OR, so the entry reports APPLIED via the baseline clause whether or not it is also listed, and it can never falsely trip the consistency check (a baseline-covered entry's ancestor-dependencies are themselves baseline-covered). The tool MAY optionally drop, in the same atomic `.host` write as the advance, exactly those full-SHA `applied` ids reachable-from the resolved new tip; this is cosmetic only and MUST fail closed — if the tip cannot be resolved, the advance is already refused by the guard, so pruning never runs against partial/absent history, and any id that is a sibling of (not reachable from) the new tip is kept. A missed prune is harmless over-listing of a redundant id, never lost work or re-listing of a done entry."

Add the corresponding unit test from the reviewer (keep it, it is sound): advance past a previously-applied id leaves the entry reporting APPLIED (and may drop the now-redundant id); advance with a sibling or unresolved `applied` id keeps it and the entry does not re-list as PENDING. Do NOT adopt the reviewer's "resurrects owed work or hides it / major" framing — under the OR-semantics neither outcome is reachable from no-pruning, and the only real risk (an eager/buggy prune that DROPS a sibling) is excluded by the reachable-from-resolved-tip + fail-closed rule above.

### [back-compat] An older host-lifecycle binary reading a new .host ignores `applied` AND cannot honor the watermark-advance guard — its re-stamp path can erase the applied set
*verdict: partial*

**Scenario.** Forward-compat: adopter Bly cherry-applies 7de7cb1 with a new binary (writing `applied = 7de7cb1`), then later runs an OLDER host-lifecycle (a stale tools/host-lifecycle pin, or a globally installed older copy). (a) Old `upgrade` calls parse_revision (src/main.rs:296) which reads only `revision`; the `applied` line is invisible, so 7de7cb1 RE-LISTS as PENDING — that direction is fail-safe (over-reports), which is acceptable. (b) But the old binary has NO watermark-advance guard and NO `--record`; if the adopter, seeing 7de7cb1 re-listed, advances `revision` with the old tooling (or the old `adopt` re-stamp overwrites .host via stamp_body), the `applied` line is dropped and, if `revision` is moved past the skipped spec-lane chain, debt is now buried with no tool able to detect it. The guard is the 'structural teeth' but teeth only exist in the new binary; nothing forces the adopter onto a new-enough binary before the applied-set semantics matter.

**Fix.** Fold a defense-in-depth, NEW-binary-enforced floor into plan/0022 rather than relying on the advisory `requires`:

1. Add a `stamp-format` line to the stamp model. When ANY writer emits an `applied` line it also writes `stamp-format = 2` (absent = 1 = legacy). This is the durable forward-incompatible marker. Extend stamp_body() so the applied-set path always co-writes it (today stamp_body takes only revision+date and emits three fields — it must learn the applied set and the format key together, and `--record` must round-trip ALL stamp fields it does not understand, never re-derive a three-field body).

2. Make the NEW binary refuse to lossily re-stamp. Replace the blind stamp_body() overwrite on the upgrade/record/adopt-re-stamp paths with a read-modify-write that preserves every line it does not own (revision/applied/stamp-format). If the new binary reads a stamp it cannot round-trip (a format newer than it knows), it errors loud and refuses — this is the structural teeth that survive even when a still-newer field appears later. (This does not fix an OLD binary, but it stops the new binary from being the eraser and sets the precedent the reviewer's part (2) gestured at.)

3. Make `requires` actually gate. Add a tool self-version (the binary's own Cargo version, distinct from the template `version` subcommand) and have `upgrade` and a new `software --check` stamp consistency pass REFUSE (non-zero) when the stamp carries `stamp-format >= 2` (or any entry with `requires` above the running tool) — telling the operator their host-lifecycle is too old to safely operate the stamp. Put this consistency pass in `software --check` so CI (which the methodology already runs per spine) catches a stale local/pinned binary even when the dev box is behind. This is the only place that closes the old-binary direction: the gate runs in CI on a current binary and fails the stale-pin case, so a debt-burying re-stamp produced by an old local copy is caught at the gate.

4. Keep the reviewer's step-7 UPGRADING entry for the applied-set change, but its teeth are (1)-(3), not the `requires` string alone. Note in plan/0022 that agentic-host itself is contiguous at HEAD (gains no `applied` line), so add a fixture test in the cross-binary direction — an old-binary re-stamp dropping `applied` MUST be caught by the new `software --check` stamp pass — since the repo's own gate would otherwise never exercise it.

### [back-compat] `stamp_field` returns only the FIRST matching line and trims a single pair of quotes, so a multi-id `applied` value has no defined whitespace/quote contract and a duplicate/legacy line is silently shadowed
*verdict: real*

**Scenario.** stamp_field (src/main.rs:302) loops lines and returns the first `applied = ...` it finds, after `.trim().trim_matches('"')`. The README shows `applied  = "7de7cb1 ae1e688"` (quoted, space-separated). trim_matches('"') strips the surrounding quotes, leaving `7de7cb1 ae1e688`, which the caller must split on whitespace — fine. BUT: (a) if `--record` ever appends a SECOND `applied = ...` line instead of editing in place (a plausible naive append, the simplest write), stamp_field reads only the first and silently ignores the rest — ids in the second line vanish from the applied set, re-listing real work (noisy but safe) OR, if the guard reads the same first-only value, the guard sees fewer applied ids than truly recorded. (b) trim_matches strips ALL leading/trailing quotes, so a malformed value is silently accepted. (c) An unquoted `applied = 7de7cb1 ae1e688` also parses (trim leaves it), so there are two on-disk encodings; whichever the writer emits must match what the back-compat readers tolerate.

**Fix.** Fold an explicit stamp encoding + reader/writer contract into plan/0022, and gate it with tests. Specifically:

1. ONE canonical on-disk encoding for `applied`: a single line, double-quoted, space-separated lowercase short SHAs: `applied  = "<id> <id> …"`. Document this in the README stamp model block and make it the ONLY accepted form.

2. A dedicated reader `parse_applied(text) -> Result<Vec<String>, StampError>` distinct from the lax `stamp_field`. It MUST:
   - match the key EXACTLY (`applied`), not by prefix — guard against `applied_at`/`applied-on` collisions and the `?`-returns-None-for-whole-function trap (src/main.rs:305) that today silently empties the set;
   - require the single-quoted form and reject an unquoted value (so there is exactly one encoding, closing claim c);
   - strip exactly one leading and one trailing quote and ERROR on unbalanced/extra quotes (replace trim_matches('"'), which strips all — claim b);
   - ERROR LOUD if more than one `applied` line is present (a corrupted stamp hides owed work or silences the consistency check — fail closed, claim a + the prefix/no-eq edges d/e). Do not silently take the first.
   `upgrade`, the watermark-advance guard, and the consistency check MUST all route through this one reader so they can never disagree about the applied set.

3. `upgrade --record <id>` is an IN-PLACE edit of the single `applied` line (insert the line if absent, add the id to the existing line if present, no-op if already present), NEVER an append. It writes the canonical quoted form. Re-record is idempotent. A `<id>` not present in the ledger is rejected (exit non-zero).

4. Tests (add to the tests module): quoted multi-id round-trips through write→read; an unquoted value is REJECTED (records the decision, closes c); a duplicate `applied` line ERRORS, not silent-shadow (a); an unbalanced/extra-quote value ERRORS (b); a sibling key sharing the `applied` prefix (`applied_at`) does NOT shadow the real line, and the real set is read (d); `--record` twice is a no-op and produces exactly one `applied` line.

5. README note correcting the fail-safe wording: stamp_field-style first-match-wins can only UNDER-report the applied set, which is safe for listing and the guard; the one place a mis-read is dangerous is the consistency check (a silenced "applied dep unapplied" error), which is why the reader fails CLOSED on any malformed/duplicate `applied` rather than tolerating it.

### [completeness] No discovery path: the design never says HOW an adopter learns which PENDING entries are safe to cherry-apply alone
*verdict: real*

**Scenario.** Bly is 6 revisions behind. `upgrade` prints (per the plan) one line per entry: `<id> <title> [independent | depends: <id>…] PENDING|APPLIED`. The spec-lane chain entries (`c771d60 depends b6232a5`, etc.) print their `depends` ids, but the worktree fix `7de7cb1` and `ae1e688` print `independent`. Every OTHER existing ledger entry (8c28e33, 325f2cf, 71d12a8, bbbfdc3, 7ae93cd, 6db01f3, 07025a7, e3b174d, c137567, d3dc5ed) has NO annotation — the plan back-fills only the two independents and the four-entry spec chain. The README says 'absent annotation = independence undeclared (the tool says so; it does not assume safe)'. So Bly sees ~10 PENDING entries with neither `independent` nor `depends` and the tool gives no verdict on whether picking the late one is safe — it does not even tell her WHICH earlier unannotated entries the late one might transitively need. The whole motivating use case (take 7de7cb1 now, defer b6232a5) only works because those two specific ids happen to be annotated; for any other late entry the adopter is back to reading prose, which is the failure the plan set out to remove.

**Fix.** Add an explicit discovery affordance with two parts.

(a) Back-fill independent/depends on ALL 18 existing ledger entries, not just the two independents and the three-entry spec chain. This is a bounded, one-time annotation of a known set: the structural-migration entries (8c28e33, 325f2cf, 71d12a8, bbbfdc3 — submodule->bare-store, coherence, rename) and the build/publish entries (7ae93cd, 07025a7, e3b174d, c137567, d3dc5ed, f62d766, 0e83e3f) are each `independent` of one another at the action level (each is a self-contained recipe change); b6232a5 (specs-to-software) is the chain head and should be marked `independent` (nothing earlier is its prerequisite), with c771d60/b8c54fc/821a216 keeping their `depends` edges. After this back-fill, 'absent annotation = undeclared' becomes the genuine exception that applies only to FUTURE entries an author forgot to annotate — which reconciles with Orin's 'sparse annotations' read as 'sparse for new entries, complete for the shipped history', not 'most of the ledger is a verdict-free blank'.

(b) Have `upgrade` COMPUTE and print, per PENDING entry, a concrete 'safe alone: yes | no | unknown' verdict by resolving the transitive `depends` closure against the applied set, instead of echoing only the raw `depends` line: yes = every transitive dependency is already applied (or the entry is `independent`); no = some transitive dependency is PENDING; unknown = the closure transitively reaches an entry with NO annotation (independence undeclared) — preserving the fail-safe rule that the tool never assumes safe. Keep the existing post-hoc consistency error (an applied entry with an unapplied declared depends) as-is; it is orthogonal to this pre-apply verdict. This makes the Fen 4B read a one-token verdict rather than recomputing reachability over a `depends` graph it cannot reliably parse.

### [completeness] The Sable persona is cited as a design author but the cast/sable.md file does not exist
*verdict: partial*

**Scenario.** plan/0022 README ('Sable — cold-start auditor') and PLAN.md ('Worked from four added personas: Orin/Bly/Sable/Fen') both name Sable as one of the four stakeholder personas the design was driven from. cast/ contains orin.md, bly.md, fen.md — but NO sable.md. The design's central honesty property ('a later cold read of the stamp … cannot be deceived') is attributed to Sable's seat, yet the seat is undocumented. A reader auditing the design cannot check the cold-start-auditor requirements the plan claims drove it.

**Fix.** Disposition: complete the already-performed fold (commit 609c6e5 retired cast/sable.md into cast/bly.md but left two stale references). Do NOT add cast/sable.md — that seat was intentionally collapsed.

1. plan/0022 README "Why" paragraph (lines 19-23): stop naming four personas. Change "worked from four added stakeholder personas instead (`cast/`): Orin (maintainer), Bly (adopter behind), Sable (cold-start auditor), Fen (...)" to three: "worked from three added stakeholder personas (`cast/`): Orin (maintainer), Bly (adopter behind — who is also its own cold-start auditor, writing the stamp now and reading it back with no memory), Fen (low-reliability agent ...)". Drop "All four independently chose the same stamp model" -> "All three independently chose the same stamp model." This matches the README's own Persona-acceptance section, which the fold already corrected.

2. PLAN.md line 43: change "Worked from four added personas: Orin/Bly/Sable/Fen" to "Worked from three added personas: Orin/Bly/Fen (Bly carries the cold-read auditor seat)." Commit and push as an audited-plans edit (per the project's PLAN.md push discipline), separately from code.

3. Optional but closes the loop on the plan's own auditability theme: add a one-line note in the README (or a call/ MADR) recording that Sable was folded into Bly by the Cooper's-test collapse — same agent, write-now vs read-cold-later — so the seat count is traceable rather than living only in a commit message.

These are pure doc edits; no code, no change to the stamp/applied-set/guard design.

### [completeness] The new ledger entry for THIS change has no specified `requires` version, and the guard's interaction with re-stamping past it is unstated
*verdict: real*

**Scenario.** Build step 7 says 'UPGRADING entry for this change' and step 9 re-stamps agentic-host. Every existing ledger entry carries `requires = host-lifecycle vX.Y.Z`; the new applied-set/guard feature is itself gated on a tool version (you cannot honor `--record` or the guard with v0.13.0). The plan never states the new version (a 0.14.0 bump + tag per the tag-every-release rule) nor the `requires` line for its own entry. Worse: when agentic-host re-stamps `revision` to the new template HEAD, the watermark-advance guard (build step 5) will evaluate every entry ancestor-or-equal the new rev — including this new entry — and must find them all applied; the plan asserts 'agentic-host is contiguous at HEAD' but does not show the re-stamp passes its own new guard, which is a circular bootstrap (the guard is enforced by the very binary being released).

**Fix.** Two changes to plan/0022.

1) Pin the version and the new entry's `requires`. State the bump explicitly: host-lifecycle v0.14.0 (a new tag per the tag-every-release rule, entry 0e83e3f). Step 7's new UPGRADING entry MUST carry `requires = host-lifecycle v0.14.0`, matching every other entry — the applied-set/guard/`--record` feature cannot be honored by v0.13.0. (Note: `requires` is advisory-only in code today — it is printed, never gated — so this is a consistency/documentation fix, not a functional one; do not add version-gating to make it bite unless that is separately intended.)

2) Close the guard bootstrap, which is the real hole. The design forbids agents from hand-editing .host yet the re-stamp today IS a hand-edit (the only stamp writer is `adopt`); name the command that advances `revision` and make it the single guarded path — e.g. `host-lifecycle upgrade --advance <rev>` (or fold the advance into `--record`), which rewrites .host's `revision` and is the only thing the watermark-advance guard intercepts. Then state the guard semantics precisely: "in range" is evaluated against the CURRENT (pre-advance) revision, and a CONTIGUOUS advance is explicitly allowed — advancing `revision` from R to <rev> is permitted iff every ledger entry in the span (R, <rev>] is either being brought into range by this very advance with no gap (i.e. <rev> itself or its ancestors back to R, all consecutive) or already in `applied`; it is refused only when an entry ancestor-or-equal <rev> is left unapplied AND below the new watermark with a gap. Add a build-step check to step 9: after building the v0.14.0 binary, use IT to advance agentic-host 431f781 -> NEW and assert the guard PASSES (contiguous: the only span entry is the new entry keyed at NEW, brought into range by the advance), then assert `version .` == NEW and `upgrade .` reports up to date with no `applied` line — proving the self-release passes its own newly-shipped guard (the circular bootstrap is discharged, not assumed).

### [completeness] Build step 8 ('the two pending host= corrections') is unspecified — no file, no before/after text, no verification
*verdict: partial*

**Scenario.** Step 8 bundles 'the host=windows→omit example' and 'the host= vs attest-host materialize-OS-vs-build-OS wording' and 'correct the issue #2 comment'. There is no `host=windows` example anywhere in the repo (grep finds none in .host-software, CLAUDE.md, UPGRADING.md, STRUCTURE.md — only `attest-host` wording in template docs). The plan gives no path, no current text, and no corrected text for any of the three, and its 'verify' line in step 8 is absent entirely (steps 1-7 and 9 each have a *verify:*; step 8 does not). A reviewer cannot tell what is being changed or how to confirm it is right, and bundling two unrelated doc corrections into a stamp-model milestone violates the surgical-changes discipline.

**Fix.** Treat step 8 as a real but minor (not major) specification gap. Do not assert the example is missing — it exists. Fold this into plan/0022:

1. Split step 8 out of the stamp-model milestone into its own small, separately-pushed doc commit (per CLAUDE.md §3 surgical changes), OR fully specify it inline. Either way, add a verify line (currently absent).

2. Specify the three corrections concretely (all targets are known):
   a. host=windows→omit. Target: the closing comment on connollydavid/host#2. Current text ends: `worktree = ik_llama.cpp.windows windows/msvc-port <pin> store=/mnt/d/dev/ik_llama.cpp host=windows`. Defect: `/mnt/d/...` is the WSL/Linux-side view of the Windows Dev Drive, so std::env::consts::OS there is `linux`; `host=windows` gates the line off on the exact box the agent runs from (Bly's frustration, cast/bly.md:24). Corrected text: drop the `host=windows` token entirely (`... store=/mnt/d/dev/ik_llama.cpp`); the store path already pins the location and the OS gate is wrong/harmful here. The existing unit test (tools/host-lifecycle/src/main.rs:3237, `host=linux`) already models the correct pairing.
   verify: the issue #2 comment no longer contains `host=windows`; `echo "<new comment>" | host-lint --stdin` does not flag.

   b. host= vs attest-host wording (materialize-OS vs build-OS). Targets: host-template/CLAUDE.md:351, plan/0021-worktrees-under-host-tree/README.md:32, and the doc-comment at tools/host-lifecycle/src/main.rs:828 (and the matching MEMORY.md:370 entry, which is append-only — correct via a NEW MEMORY entry, do not rewrite). Defect: each says host= "mirrors attest-host", conflating the OS a worktree materializes on with the OS that reproduces/attests a build — distinct gates. Corrected wording: state that `host=<os>` gates which OS the worktree materializes on (it is skipped off-platform), analogous to but not identical to a build's `attest-host`, which gates which OS reproduces a build's artifact.
   verify: grep for "mirrors `attest-host`"/"mirroring a build" returns no live-doc hits (the MEMORY line stays, corrected by a new appended entry); `host-lifecycle validate` / `software --check .` clean.

   c. Correct the issue #2 comment = re-edit that GH comment to carry the (a) omit fix and the (b) clarified wording.
   verify: `gh issue view 2 --repo connollydavid/host --comments` shows the updated example and wording.

### [completeness] Spine doc + README + UPGRADING are listed as targets but the plan never states they describe the NEW two-field model (watermark + applied set), only the old one
*verdict: real*

**Scenario.** Build step 7 says 'host-template CLAUDE.md upgrade-model section + README Upgrading rewrite'. The current CLAUDE.md 'Upgrading' section and README 'Upgrade — version to version' describe a SINGLE `.host` revision and 'prints every entry newer than it' — there is no mention of an applied set, `--record`, the guard, `independent`/`depends`, or the consistency check. The plan asserts these docs will be rewritten but gives no acceptance text and no check that the rewrite actually teaches the fail-safe model (the watermark-vs-applied distinction, why a forgotten record re-lists, that an agent must never hand-edit the stamp). For a 4B-driven workflow the doc IS the interface; an under-specified rewrite risks teaching half the model.

**Fix.** Make step 7's target list and verify concrete and complete, and ADD the upgrade SKILL.md as a target.

(1) Target list for the doc rewrite (name the exact files — the plan's bare "README *Upgrading*" is ambiguous):
  - host-template/CLAUDE.md "## Upgrading" section.
  - tools/host-lifecycle/README.md "## Upgrade — version to version" section (this is where the "prints every entry strictly newer / git ancestry" prose actually lives; host-template/README.md has no upgrade section).
  - tools/host-lifecycle/skills/upgrade/SKILL.md (currently teaches the OLD model: line 14 "prints every entry newer than the stamp", line 17 "Apply each printed entry's action, in order", line 33 "Apply every entry newer than the stamp before re-stamping" — all three contradict cherry-applying out of order and MUST be rewritten).

(2) Required content (the rewrite of each of the three must teach, not just mention):
  (a) the watermark-vs-applied-set distinction and the iff rule: an entry is applied IFF ancestor-or-equal(revision) OR id in `applied`; `upgrade` reports the complement;
  (b) the fail-safe property in plain terms — a forgotten `--record` re-lists the entry (over-reports pending), it can never hide owed work;
  (c) that `host-lifecycle upgrade --record <id>` is the ONLY sanctioned way to mark an entry applied — an agent NEVER hand-edits `.host` (the SKILL.md especially must state this, mirroring the publish SKILL's "do not hand-edit" discipline);
  (d) the watermark-advance guard (advancing `revision` past an unapplied entry is refused) and the consistency error (an applied entry whose declared `depends` is unapplied -> loud error);
  (e) `independent` / `depends` annotations and that absent annotation means independence is undeclared (the tool says so; it does not assume safe);
  (f) the SKILL.md "## Do" step and "## MUST" must replace "apply in order / apply every entry newer than the stamp" with: read the machine-readable PENDING/APPLIED listing, apply a PENDING entry (preferring `independent` ones safe to take alone), `--record` it, and re-stamp/advance the watermark only when contiguous — explicitly permitting leaving earlier unrelated entries PENDING.

(3) Strengthen step 7's verify from "docs describe the model" to a checkable assertion: a grep/fixture check that each of the three files mentions the applied set, `--record`, the guard, AND the consistency check; plus a manual acceptance read that the upgrade SKILL.md no longer says "in order" and no longer says "apply every entry newer than the stamp." Fold the SKILL.md rewrite into the Fen acceptance gate: the 4B is driven from this SKILL.md + the machine output, so the gate already exercises whether the rewritten skill teaches the cherry-apply correctly.

### [completeness] Testing strategy omits the fail-safe invariants and the round-trip; only happy-path fixtures are named
*verdict: real*

**Scenario.** The build-step verifies cover in-range/in-applied/neither, parse, a fixture listing, record idempotency, and the guard. Missing: (1) the load-bearing fail-safe property — a stamp whose `applied` is MISSING an id that was actually applied must RE-LIST it as PENDING (over-report), proved by a test, since this is the entire safety argument; (2) stamp round-trip preservation — `--record` rewrites `.host` and must preserve `template`/`adopted`/`name` and any unknown lines byte-for-stable (the existing `stamp_body` hardcodes only three fields and would DROP `name` and `applied` on any naive rewrite — see main.rs:291 `stamp_body` which has no `name`/`applied` params); (3) a malformed/duplicate `applied` id; (4) the consistency check when `depends` cites an id NOT in the ledger at all (dangling dep).

**Fix.** Fold into plan/0022 a "stamp writer rework + test matrix" requirement. Concretely:

1. Rework the stamp writer (design note, blocking): the current `stamp_body` (main.rs:291) regenerates only template/revision/adopted and is structurally incapable of carrying `name` or the new `applied` line. `--record` (and the step-9 re-stamp) MUST be read-modify-write: parse the existing `.host`, mutate only `revision`/`applied`, and write back preserving `template`, `adopted`, `name`, and any unknown/extra lines. Note explicitly that today's 3-field formatter would DROP `name` (this repo's real .host:4 has `name = "agentic-host"`, read by stamp_title/main.rs:2547 for the book title) and — worse — would drop a previously-recorded `applied` on the second `--record`, silently hiding owed work and inverting the fail-safe guarantee.

2. Add these named tests to the Build section:
   - Stamp round-trip: write a stamp with template/revision/adopted/name (+ an unknown line), run `--record <id>`, assert ALL prior fields survive byte-stable and only `applied` changed; then `--record` a SECOND id and assert the first id is still present (the no-drop property the idempotency claim depends on).
   - Fail-safe re-list at the upgrade-output level (not just the is_applied unit): given a stamp whose `applied` is MISSING an id that was in fact applied, `upgrade` must RE-LIST that id as PENDING (over-report) — the load-bearing safety invariant.
   - Duplicate/malformed `applied` token: `--record` of an already-recorded id is a true no-op (no `applied = "x x"`); a malformed/empty token in `applied` is parsed deterministically (skipped or errored, pick one and test it).
   - Dangling `depends`: an applied entry whose `depends` cites an id that is NOT a ledger entry at all is handled deterministically by the consistency check (define and test: error as a loud inconsistency), distinct from the already-listed "depends an unapplied entry" case.
   - `--record` of an id not present in the ledger is rejected (the existing "bad id rejected" check — keep it, but state the contrast with the dangling-depends case so they are not conflated).

### [completeness] Milestone done-criteria are not all verifiable, and the Fen acceptance gate depends on an unpinned external model with no fallback
*verdict: real*

**Scenario.** The Verification section's main criteria are checkable (cargo test, clippy, fixture, guard, `upgrade .` up to date). But the Fen acceptance gate requires driving 'the actual qwen3.5-4b (Q8_0, via the pal MCP)' through an A/B and passing 'when the tool-carried flow succeeds where the prose flow fails'. This is non-deterministic (a 4B model's output varies run to run), has no defined pass threshold (1 of 1? best of N? what counts as the prose-flow 'fumble'?), and binds milestone completion to an external MCP/model being installed and reachable in this environment — `mcp__pal__listmodels` would have to confirm qwen3.5-4b is even present. If the model is unavailable the milestone cannot be marked done, yet the plan offers no fallback or deterministic substitute. 'Complete means whole-suite green' (your MEMORY) cannot be satisfied by a flaky LLM A/B with no threshold.

**Fix.** Make the deterministic mechanism the sole blocking gate, and demote the 4B A/B to bounded, recorded corroborating evidence with a hard fallback. Concretely, rewrite the Verification section so that "milestone done" is satisfied entirely by the deterministic checks already listed (cargo test + clippy green; the build-step unit/fixture checks for is_applied, ledger independent/depends parse, machine-readable upgrade listing, idempotent --record, the watermark-advance guard blocking a debt-burying re-stamp, the loud applied-with-unapplied-depends consistency error; `upgrade .` up to date; `software --check .` clean; version tagged). These do not depend on any external model.

For the Fen gate, replace the open-ended A/B with: (1) A mandatory scripted adversarial harness (a shell/integration test, in-repo, deterministic, run in CI) that drives the tool through the exact fumble modes the design must survive — wrong-id `--record`, double `--record` (idempotency), a hand-edit-the-stamp attempt that the guard must catch, and a forgotten record that must re-list as PENDING. This harness, not the LLM, is the blocking acceptance criterion, and its transcript is committed as the evidence artifact. (2) An OPTIONAL empirical 4B run, gated on a reachability precheck: first confirm qwen3.5-4b answers via pal (a bounded liveness probe); if it does not respond within a fixed timeout, skip the LLM run and record "Fen A/B SKIPPED — model unreachable" rather than blocking the milestone. (3) When the 4B is reachable, run it with an explicit bounded protocol: N≥5 trials, gate passes if the tool-carried flow is correct in ≥4/5 AND the prose/hand-edit baseline is incorrect in ≥3/5, with "correct" = (independent late entry recorded, earlier ones still PENDING, `.host` not hand-edited) and "fumble" = (stamp mis-edited OR debt buried OR wrong/owed entry left unrecorded). Commit the full trial transcript (prompts, tool calls, resulting `.host`) as the audit artifact so Sable can verify the gate post hoc rather than trusting an assertion. Note in the plan that the empirical run is corroboration of "serves Fen," never the thing that turns the milestone red — the scripted harness already proves fumble-survival deterministically.

### [dependency-hints] Transitive dependency satisfaction is unspecified: A depends B, B depends C, with A and C applied but B not
*verdict: partial*

**Scenario.** Real chain: 821a216 depends c771d60, c771d60 depends b6232a5 (per the design's back-fill). Suppose `applied = 821a216 b6232a5` but c771d60 is NOT applied. The loud check as written ('an applied entry whose declared depends is unapplied -> error') fires on 821a216 (its direct dep c771d60 is unapplied) — good. But consider `applied = 821a216` alone with c771d60 in watermark range and b6232a5 NOT in range and NOT in applied: the check on 821a216 sees c771d60 satisfied (in range) and passes, never transitively checking that c771d60's own dep b6232a5 is satisfied. The design only checks DIRECT depends of APPLIED entries; it never validates the deps of an entry that is satisfied-by-range. So a broken transitive chain through a watermark-satisfied middle entry is invisible.

**Fix.** Add to plan/0022 a stated INVARIANT rather than a transitive-closure check: "A ledger entry's `depends` MUST name an ancestor entry (a revision ancestor-or-equal to the depending entry in template history). The tool rejects a `depends` pointing to a non-ancestor as a malformed ledger." Justify it: with backward-only deps, the watermark range is downward-closed over `depends`, so any entry satisfied-by-range has all its transitive deps also satisfied-by-range, and the existing direct check ("an applied entry whose declared `depends` is unapplied -> error") is already equal to the transitive closure — no closure walk is needed. Implementation note for build-step 3: when validating an applied entry's `depends`, also reject any `depends` id that fails `merge-base --is-ancestor <dep> <entry>` (reuse the ancestry call already in upgrade_applies). Add a verification fixture for the broken case the direct check DOES need to catch — `applied = {A, C}`, B unapplied, A depends B (B unapplied -> non-zero) — and a fixture asserting a forward/non-ancestor `depends` is rejected as malformed. Drop the reviewer's specific 821a216/c771d60/b6232a5 "middle-entry satisfied by range" example from the design: it is impossible because b6232a5 is an ancestor of c771d60, so c771d60 in range forces b6232a5 in range.

### [dependency-hints] A depends pointing into watermark range is satisfied implicitly, but the design never says so — risk of a false-positive loud error or of hiding a debt
*verdict: partial*

**Scenario.** c771d60 depends b6232a5. If an adopter's `revision` is at/after 821a216, then b6232a5 is ancestor-or-equal(revision) and thus applied-in-range. If c771d60 is recorded in `applied` (cherry), the consistency check must treat its dep b6232a5 as satisfied via range, not demand it appear literally in the `applied` set. The README defines `is_applied` correctly (range OR membership) but the consistency-check bullet only says 'declared depends is unapplied', leaving open whether 'unapplied' is evaluated with the same range-OR-membership predicate. If an implementer naively checks `depends ⊆ applied-set` (membership only), every in-range dep produces a spurious loud error.

**Fix.** In the "Dependency hints" section and the "Consistency check" bullet, state explicitly that the check evaluates each `depends` id through the SAME `is_applied(id, revision, applied)` predicate (range OR membership), not membership in the `applied` set alone — reuse the guard bullet's existing phrasing: a dep counts as satisfied when it is "in range OR in `applied`". Concretely: "An entry recorded as applied is consistent iff every id in its `depends` is itself applied — `is_applied(dep, revision, applied)` — so a dep already covered by the watermark (ancestor-or-equal `revision`) needs no entry in `applied` and must NOT trigger the loud error; only a dep that is neither in range nor in `applied` is an inconsistent record."

Then add the discriminating fixture to Build step 3's *verify* line, alongside the existing TRUE-error case: revision = b6232a5 (the lane-chain base, in range), `applied = "c771d60"` with `c771d60 depends b6232a5` -> dep satisfied by range -> NO error / exit 0. Pair it with the negative twin already implied: revision below b6232a5, `applied = "c771d60"`, dep b6232a5 neither in range nor in `applied` -> loud error / non-zero. These two fixtures together pin the predicate and reject a membership-only implementation.

(Note for the design author, not part of the fix text: the reviewer's stated scenario "revision at/after 821a216" is incoherent — at that watermark c771d60 is already in range and would never be cherry-recorded; the coherent scenario sets the watermark at b6232a5, between the dep and the cherried entry.)

### [dependency-hints] Cycles, self-deps, an entry marked BOTH independent and depends, and a depends naming a non-existent/abbreviated id are all unhandled
*verdict: real*

**Scenario.** (a) A typo'd back-fill could write `c771d60 depends 821a216` while `821a216 depends c771d60` -> a cycle; the transitive-closure check could loop or, worse, mutually 'satisfy' if implemented as a fixpoint without a visited-set. (b) An entry annotated `independent = true` AND `depends = b6232a5` is contradictory; the design lists both as valid annotations but never forbids co-occurrence. (c) `depends = b623` (abbreviated) or `depends = deadbeef` (a SHA never in the ledger) — the design's fail-safe story rests on ids resolving; a non-existent id should be a load error, an abbreviated one needs canonicalization against the ledger, but neither is specified. Given the driver is a low-reliability 4B that cannot hand-edit, a maintainer fat-fingering the ledger back-fill is the realistic failure, and the tool currently has no validation pass over the ledger's own depends graph.

**Fix.** Add a ledger self-consistency validation pass that runs at the start of `upgrade` (and, where cheap, `validate`/`software --check`), executed before any applied-set / advice computation, so the depends graph is proven well-formed before it is trusted. It must, erroring loudly (non-zero) with the offending entry id on any violation:

1. Resolve-and-canonicalize: every `depends`/`applied`/`requires`-style id (and the back-fill `depends` examples like `b6232a5`) must match exactly one DECLARED `[upgrade "<rev>"]` header in the SAME ledger. Match by the ledger's own declared ids (string/abbrev-prefix against declared headers), NOT by `git rev-parse` against template history — a `depends` is a reference to another ledger row, not an arbitrary git object. Reject an id that resolves to zero declared entries (e.g. `deadbeef`) as a load error; reject an abbreviation that prefix-matches two-or-more declared entries as ambiguous. Canonicalize accepted abbreviations to the declared id internally so the consistency check compares like for like. This keeps the fail-safe honest: a `depends` cannot silently dangle.

2. Mutual-exclusion: reject any entry carrying BOTH `independent` (true) and `depends` — the two are contradictory and the design only ever uses one per entry.

3. Self-dep: reject an entry whose `depends` list contains its own (canonicalized) id.

4. Cycles: detect cycles in the depends graph with an explicit visited/on-stack set (DFS three-colour or equivalent) and error with the cycle path; never traverse as an unbounded fixpoint. This also makes the design's downstream "applied entry whose transitive `depends` is unapplied" check terminating and well-defined.

Document in plan/0022 that this hygiene pass is the maintainer's (Orin's) gate over the ledger, distinct from the adopter-stamp consistency check (the applied-entry-with-unapplied-dep error). Add the design note that `depends` references resolve against declared ledger ids — not template git history — and add unit tests for: unknown id (load error), ambiguous abbreviation (rejected), `independent`+`depends` together (rejected), self-dep (rejected), and a 2-cycle / 3-cycle (rejected, terminating).

### [dependency-hints] 'requires = host-lifecycle vX.Y.Z' (tool-version prerequisite, already in every entry) and the new 'depends = <id>' (entry prerequisite) are two prerequisite axes the design never reconciles
*verdict: real*

**Scenario.** The spec-lane chain entries all carry `requires = host-lifecycle v0.9.1 / v0.10.0 / v0.11.1`. The design adds `depends = <id>` as a parallel concept but says nothing about whether `requires` participates in the consistency check or the 'safe to apply alone' advice. b8c54fc's action ('--check enforces the spec lane, HAZARD') is genuinely unusable without host-lifecycle v0.10.0 (its `requires`), which is a harder real-world blocker than its `depends c771d60`. An adopter could satisfy all `depends` yet have an old host-lifecycle that cannot perform the action, and the tool would advise 'safe to apply alone'.

**Fix.** Add a short subsection to plan/0022 "Dependency hints on ledger entries" reconciling the two prerequisite axes explicitly. Scope the design to entry-deps and declare `requires` out of scope for the consistency check, but make the tool surface it so the advice can never silently mislead:

1. Scope statement: "There are two prerequisite axes. `depends = <id>` (entry-on-entry) participates fully in the applied-set computation, the consistency check, and the 'safe to apply alone' advice. `requires = host-lifecycle vX.Y.Z` (tool-version) is an independent, human-read gate and is NOT part of the consistency check — the tool does not know its own semver at runtime (no CARGO_PKG_VERSION wiring today; `host-lifecycle version` reads the .host stamp, not the binary), and adding a semver parser + free-text `requires` parser is out of scope here."

2. Advice safety (cheap, no version comparison): when the machine-readable `upgrade` line marks an entry PENDING and `independent`/all `depends` satisfied, do NOT print a bare "safe to apply alone". Instead always echo the entry's `requires` alongside the safe-to-apply hint, e.g. `<id> <title> independent PENDING (needs: host-lifecycle v0.10.0)`, so the agent/human confirms the local tool meets `requires` before acting. This reuses the already-parsed `requires` field (Upgrade.requires) — no new machinery — and keeps the fail-safe property: the tool never claims an entry is actionable on the local tool, it only states entry-dependency readiness and prints the tool-version gate for the operator to check.

3. (Optional, deferred) Note that a future revision MAY fold the tool-version gate into actionability by wiring CARGO_PKG_VERSION + a semver compare against a structured `requires`, but that is explicitly deferred and not required by 0022.

### [fail-safe] Re-stamp via `adopt`/`stamp_body` silently drops the `applied` set (and already drops `name`), and a re-stamp is the routine end-of-upgrade step
*verdict: partial*

**Scenario.** `stamp_body` (main.rs:291) emits only `template`, `revision`, `adopted` — it already omits the `name = "agentic-host"` line that the live `.host` carries, proving re-stamp is lossy today. The plan's step 9 re-stamps `.host` at the end of an upgrade. An adopter with `applied = 7de7cb1 ae1e688` (two cherry-applied independents) runs any flow that calls `adopt`/re-stamp to bump `revision` to the new contiguous baseline `699db99`. The rewritten stamp has no `applied` line. If `699db99` is NOT an ancestor of `7de7cb1`/`ae1e688` (they are LATER independents), they are no longer in range AND no longer in `applied`. Direction-wise this re-lists them as PENDING — fail-SAFE for those two. BUT the same lossy re-stamp is the mechanism by which a partial state is destroyed: the asymmetry means the tool's own re-stamp path and its `--record` path write the stamp through two different code paths with different field-sets, so any future field (a record-timestamp history, a `depends`-satisfied cache) added to one is silently dropped by the other. The integrity invariant 'the stamp is the complete contract' is violated by construction the moment two writers disagree on the field set.

**Fix.** Fold a single-writer, merge-not-replace stamp discipline into plan/0022 as a named build step, ahead of the `--record` step.

1. Add one read-modify-write stamp function in host-lifecycle that is the ONLY code path that writes `.host`. It parses ALL existing key/value lines (the existing `stamp_field` parser already generalizes over any key), updates only the targeted key(s), re-emits every other line verbatim (template, revision, adopted, name, applied, and any unknown future key), and writes the result. Field order/formatting of untouched lines is preserved.

2. Route BOTH writers through it:
   - `adopt` re-stamp / revision-bump: merge `revision` (and `adopted`) into the existing stamp instead of calling `stamp_body` to overwrite. For a true first adoption (no existing `.host`), `stamp_body` may seed the initial three fields, but if a `.host` already exists `adopt` MUST merge, never replace — and MUST refuse (exit non-zero) rather than silently drop a key it does not recognize. This also fixes the present-day `name`-loss bug (stamp_title regression) independent of plan/0022.
   - `upgrade --record <id>`: merge the id into the `applied` set via the same function (idempotent; re-record is a no-op).

3. Make the watermark-advance / re-stamp step itself non-lossy: when step 9 bumps `revision` to the new contiguous baseline, entries still listed in `applied` that are NOT ancestor-or-equal to the new revision MUST be retained in `applied` (they remain genuinely applied), not silently dropped. The guard already refuses burying unapplied work; this extends the same write path so a legitimate advance never discards a still-valid `applied` id.

4. Add a round-trip regression test that seeds a `.host` carrying `name` and `applied = 7de7cb1 ae1e688`, runs it through (a) an `adopt`/revision-bump and (b) `upgrade --record <new-id>`, and asserts that after each, `name` is intact, every prior `applied` id is still present, and no field was lost. Strengthen `stamp_round_trips` (currently revision-only) accordingly.

This keeps the design's fail-safe direction (forgotten/owed work still re-lists) and additionally makes partial-upgrade state durable across the routine end-of-upgrade re-stamp — which is the property plan/0022 actually promises. It also closes the existing `name`-drop bug as a free side effect.

### [fail-safe] `upgrade_applies` fails OPEN on an unresolvable revision, but the new APPLIED computation and consistency check inherit no symmetric fail-closed default — a rebased/garbage-collected ledger key flips owed work to hidden
*verdict: real*

**Scenario.** `upgrade_applies` (main.rs:2128) returns `true` (entry applies/pending) when either `have` or `landed` cannot be resolved — fail-safe for the pending list. The new design adds the inverse computation (membership in `applied` marks APPLIED) and a consistency check on `depends`. Consider an entry recorded in `applied` by short SHA, e.g. `applied = 7de7cb1`. Upstream later rebases or amends the template history (the ledger keys are commit SHAs on `main`; a force-push / history rewrite is possible), so `7de7cb1` no longer resolves in the freshly-fetched template. The id is still a literal string in `applied`, so `is_applied` via membership returns true by pure string match — it does not re-validate that `7de7cb1` is still a real ledger entry. Meanwhile the entry's *replacement* commit (new SHA, same action) appears as a fresh PENDING entry — fine — but a `depends = 7de7cb1` on some OTHER entry now points at a vanished id; the consistency check ("applied entry whose declared `depends` is unapplied → error") cannot evaluate `depends` against a key it can't resolve, and if it treats unresolvable-depends as 'satisfied' (the open default), it green-lights an inconsistent stamp. Symmetric danger: an entry genuinely *removed* from the upstream ledger (action retracted) simply stops appearing — acceptable — but an entry whose key is GC'd while still owed disappears from `upgrade` entirely.

**Fix.** Make every id-resolution in the new applied/depends machinery fail-CLOSED, and add a ledger cross-check so a vanished key is loud rather than silent. Fold these into plan/0022:

1. Single resolver, explicit polarity. Define one helper `is_applied(id, revision, applied, ledger) -> Resolved(bool) | Unresolvable`. APPLIED iff (a) `id ∈ applied` (raw-SHA membership), OR (b) `id` resolves in the template AND ancestor-or-equal(revision). Do NOT reuse `upgrade_applies` for this: its unresolvable arm returns true ("pending"), which has the wrong meaning for membership/consistency. For the applied/depends semantics, unresolvable ancestry is NOT proof of applied.

2. Cross-check every `applied` id against the parsed ledger on each `upgrade`/`verify`/`software --check`. An `applied` id that matches no current `[upgrade "<key>"]` key AND does not resolve as an ancestor-or-equal of `revision` is a loud ERROR: `stamp records applied=<id> but no UPGRADING.md entry has that key at this pin — the ledger was rebased/GC'd or the id is a typo; refetch the template or reconcile the stamp`. (Carve-out: an `applied` id that is ancestor-or-equal to `revision` is redundant-but-harmless — downgrade to a note, since it just duplicates the watermark.)

3. Cross-check every `depends` id the same way. Resolving `depends` is part of the consistency check: for each APPLIED entry E with `depends = D…`, each D must be APPLIED *and resolvable*. If a D matches no current ledger key and is not ancestor-or-equal(revision) and is not in `applied`, that is an ERROR, never a silent pass: `entry <E> declares depends=<D>, which is not present in the template at this pin and not recorded applied — cannot prove the dependency was satisfied; refetch or reconcile`. Treat "cannot evaluate" as failure, not as satisfied.

4. Symmetric vanished-entry guard. Because the listing universe is `parse_upgrading(current UPGRADING.md)`, an owed entry whose stanza was rewritten/GC'd silently disappears. Close this by reporting, on `upgrade`/`verify`, any id named in the stamp (`applied`) or in any surviving entry's `depends` that does not resolve to a current ledger key — as the loud errors above — so a vanished-but-owed key surfaces as a reconcile demand instead of vanishing. (A genuinely retracted action — stanza removed and nothing references its key — produces no error, which is correct.)

5. Keep `applied` as raw SHAs (no rewrite on the agent's behalf); the cross-check is read-only and 4B-driveable: the tool emits the exact reconcile error, the agent does not hand-edit. Add fixture tests: (a) `applied` id matching no ledger key -> error; (b) `depends` -> vanished id -> error; (c) `applied` id that is ancestor-or-equal(revision) -> note, not error; (d) rebased entry whose action re-lands under a new SHA -> the new SHA lists PENDING and the stale `applied` id raises the reconcile error.

### [fail-safe] Hand-editing `.host` to advance `revision` (or add `applied`) bypasses the guard entirely — the structural teeth only bite the tool path, while the prompt's threat model explicitly includes hand edits
*verdict: real*

**Scenario.** The guard, `--record`, and the consistency check are all in `host-lifecycle`. The design asserts 'an agent never hand-edits the stamp,' but that is a convention, not an enforcement: `.host` is a plain key/value text file (stamp_field at main.rs:302), and the prompt's adversary explicitly may 'edit .host by hand.' A capable-but-careless operator (or a different tool, or a merge resolution) sets `revision = 821a216` directly in `.host`, skipping the guard. The big migration was never applied. Next `upgrade` computes `is_applied` by ancestry against the hand-set `revision`: every entry ancestor-or-equal `821a216` reports APPLIED. `upgrade` prints fewer/zero PENDING. There is no checksum, signature, or cross-witness on `.host`, so neither `upgrade` nor `software --check` nor `verify` can tell a hand-advanced watermark from a tool-advanced one. The 'watermark-advance guard' provides zero protection against the very edit it names as dangerous, because nothing forces the advance to go through the tool.

**Fix.** Make the watermark an auditable invariant, not an honor-system tool gate, by adding an independent witness and recomputing reachability — but fail-SAFE on a missing witness, not hard-error.

1. Append-only attestation log (a sibling `.host-applied`, gitignore-free / tracked, append-only like MEMORY.md). On every tool-driven `revision` advance or `--record`, append one line: prior-revision, new-revision, date, and the entry ids swept into range / recorded. `adopt` writes the genesis line (the adoption baseline).

2. New check (run by `upgrade` and folded into `software --check`/the `verify` sweep): recompute that the current `.host` `revision` is reachable from the adoption baseline only through attested advances, and that every id in `applied` has a `--record` attestation. 

3. Fail-SAFE, not fail-loud-and-brick, on a gap:
   - A `revision` (or `applied` id) with NO covering attestation is treated as UNATTESTED: the affected entries are re-listed as PENDING (work re-surfaces, never hides) and a clear note prints: "watermark advanced outside the tool — re-run `upgrade --record`/reconcile to attest." This preserves the design's core invariant (a forgotten/forged record over-reports, never under-reports).
   - Back-compat: a `.host` with no `.host-applied` log at all (pre-attestation adopters, and agentic-host today) is permitted but its watermark is reported as "unattested baseline" with a one-time reconcile prompt, exactly paralleling the no-`applied`-line back-compat clause (README:46). It must not block a legitimate contiguous-at-HEAD repo.

4. This is the genuine analog of the worktree-escape HAZARD the design invokes: `escapes_root` is auditable regardless of provenance; the watermark must likewise be checkable by the cold-start auditor (Sable) regardless of who moved it. Update the design text accordingly: replace "the dangerous operation is removed entirely" and "Debt cannot be buried by stamping early" with the honest statement that the tool path enforces it AND the audit recomputes it fail-safe, so a hand-edit/merge that jumps `revision` re-surfaces the owed work rather than passing silently.

### [fen-ergonomics] Ambiguous id form — printed ids vs accepted ids are unspecified, so Fen's copy of the listed token may not match what --record accepts
*verdict: real*

**Scenario.** The ledger keys are 7-char ids (`8c28e33`); `short()` in main.rs truncates display to 12 chars; full SHAs are 40. The design's machine line prints `<id>` and `--record <id>` consumes `<id>`, but nowhere fixes which form. If `upgrade` prints the 7-char ledger key but `--record` does `git rev-parse --verify <id>^{commit}` (the existing `upgrade_applies` pattern), a 7-char prefix resolves only if unique in the template's object DB — and across the full template history a 7-char prefix can become ambiguous, making `git rev-parse` fail. Fen then copies the exact token it was shown and still gets a rejection it cannot diagnose. This is a silent mismatch between the two halves of the one loop Fen must drive.

**Fix.** Pin the id to the verbatim ledger-key string and make the round-trip the contract, not git resolution:

1. Canonical id = the exact string in the UPGRADING `[upgrade "<id>"]` header (the 7-char key). `upgrade` MUST print that string verbatim in the machine line; `applied = <id>` MUST store that same string; `--record <id>` MUST accept that same string.

2. `--record <id>` validates by STRING membership against the parsed ledger keys first — never via `git rev-parse`. Unknown id → reject with a message that lists the valid ledger ids (so a Fen fumble re-lists the legal tokens instead of dead-ending on a git error). Known id → write it verbatim into `applied`; re-record is a no-op (idempotent).

3. Membership "id ∈ applied" is STRING equality on the ledger-key form. Git ancestry (`merge-base --is-ancestor`, the upgrade_applies pattern) is used ONLY for the contiguous-watermark test (`ancestor-or-equal(revision)`), never for the applied-set test. This keeps --record and the consistency/guard checks immune to abbreviation ambiguity as the template history grows.

4. Add the explicit invariant + test: "the id printed by `upgrade` is byte-for-byte the id `--record` accepts and the id stored in `applied`." Test must cover: record a listed id; the upgrade listing then shows it APPLIED (proving the stored form matches the printed/compared form); a non-ledger token is rejected with the valid-id list. Document in the host-template upgrade-model section that ledger ids are opaque strings matched literally, not git revisions to be resolved.

### [fen-ergonomics] `--record` records intent without evidence — Fen can record an entry whose action it never performed (or performed wrong), and the stamp now lies fail-UNSAFE for that entry
*verdict: real*

**Scenario.** The whole fail-safe story rests on the watermark guard, but that guard only protects advancing `revision`. The cherry-apply path Fen actually drives is `--record <id>`, which has no check that the entry's action was done — it just writes the id into `applied`. A fumbling 4B, told to apply 7de7cb1, does the wrong edit (or none) and then dutifully runs `upgrade --record 7de7cb1` because that was the named next step. Now `upgrade` reports that entry APPLIED and stops listing it — owed work is buried for that specific entry. The design's 'a forgotten record re-lists, never hides owed work' covers the forgot-to-record direction but not the recorded-without-doing direction, which is the more likely 4B failure (it follows the record instruction more reliably than the apply instruction).

**Fix.** Add an evidence requirement to `--record`, declared per ledger entry, so a record can never silently outrun the action.

1. Ledger gains an optional `verify = <shell command>` key on a `[upgrade "<id>"]` entry (parse it alongside title/action/requires/independent/depends in parse_upgrading). The command is the entry's machine-checkable post-state assertion, run with cwd at the adopter root; exit 0 means the action's effect is observable. Back-fill it for the mechanical entries: `7de7cb1` (worktree-under-root) -> `verify = host-lifecycle software --check .` (must be clean — no escaping-path HAZARD); pin-bump entries -> a grep/rev-parse of the pinned revision; `book` entry -> `host-lifecycle book --check .`. Entries whose post-state is not machine-checkable (prose re-applies) carry no `verify`.

2. `upgrade --record <id>`: if the entry declares `verify`, run it BEFORE writing the id into `applied`. On non-zero exit, refuse to record (exit non-zero) with a message naming the failed check — "refuse: 7de7cb1's verify (`software --check .`) still HAZARDs; the action is not in effect, so I will not record it." This makes the mechanical cherry-apply path fail-SAFE in both directions: a wrong/absent edit blocks the record, so the entry keeps re-listing.

3. Where no `verify` exists, keep recording but make the entry's `action`/verify-hint re-surface in the machine-readable `upgrade` output as the immediate next line after the record (not a new `--next` verb — extend the existing listing): emit a "just recorded `<id>` — confirm: <action>" advisory on the next `upgrade` run for any id recorded in this session/most-recently, so a wrong un-checkable apply is caught on the very next loop iteration rather than buried. (A lightweight "last-recorded" marker in the tool's run, or simply always echoing the most-recently-added `applied` id's action once, suffices; do not over-build a session log.)

4. Keep `--record` idempotent: a re-record of an already-applied id is still a no-op, but re-running the `verify` on a no-op record is cheap insurance and should still gate (refuse to leave a stale record standing if its verify now fails — surfaces drift).

This ties recording to observable post-state exactly where it is cheap (the mechanical entries that dominate the worked example and the Fen gate), and degrades to a next-iteration re-surfacing where it is not — closing the recorded-without-doing direction without claiming to check the uncheckable. Fold the Fen acceptance gate accordingly: the A/B must include the wrong-apply case (Fen does the wrong/no edit then records) and confirm the tool refuses the record rather than burying the entry.

### [fen-ergonomics] Status column requires Fen to read PENDING vs APPLIED off the right line — a column-parse the 4B is poor at, with no positive confirmation after a record
*verdict: real*

**Scenario.** The machine line is `<id>  <title>  [independent | depends: <id>...]  PENDING|APPLIED`. After Fen runs `--record 7de7cb1`, the only feedback the design specifies is that re-running `upgrade` shows that line now ends APPLIED. Distinguishing PENDING from APPLIED on the correct row of a 17-row table — and trusting it changed — is precisely the long-table column-reading the persona says fails. There is no terse, single-line success confirmation from `--record` itself (the README calls it idempotent but does not specify it echoes 'recorded 7de7cb1; N entries still PENDING').

**Fix.** Specify that `host-lifecycle upgrade --record <id>` MUST emit a single, parse-free confirmation line to stdout naming (a) what was recorded, (b) the dependency class of the recorded entry, and (c) the remaining pending count — so Fen learns the state change landed and how much is left WITHOUT re-parsing the status column of the long ledger table. Idempotent re-record echoes the same line marked already-recorded. Format:

  recorded 7de7cb1 (independent); 14 entr(y/ies) still PENDING

A bad/unknown id still exits non-zero with a one-line error (per build step 4). To give Fen the "single next action" the persona requires without inventing an undefined subcommand, append a pointer to the EXISTING surface rather than a new `--next`: `run \`host-lifecycle upgrade .\` for the remaining entries`. (Optionally, if a `--next` convenience is later added to print just the lowest-ancestry PENDING independent entry, the line may point there instead — but that is not required by this fix and must not be silently assumed, to avoid scope creep.) Add a verification to build step 4: assert `--record` prints the confirmation line with the correct remaining count, and that re-record prints the already-recorded variant. Fold the confirmation requirement into the Fen acceptance gate (README lines 122-129) so the gate exercises it: the 4B must rely on the `--record` confirmation line, not a re-parse of the table, to proceed to the next action.

### [fen-ergonomics] An applied INDEPENDENT entry above the watermark permanently freezes the watermark, so Fen can never finish the contiguous upgrade through the tool
*verdict: real*

**Scenario.** Bly/Fen cherry-applies the late independent 7de7cb1 (added to `applied`) and leaves the earlier specs-migration chain PENDING. Later the adopter wants to catch up fully: apply the earlier entries and advance `revision` to HEAD. The watermark-advance guard refuses advancing `revision` past any unapplied entry — correct — but the design gives Fen no tool-driven way to *advance the watermark contiguously while preserving the already-applied id*. There is `--record` (adds to applied) and an implied watermark-advance (guarded), but no `upgrade --advance <rev>` command in the toolset; advancing `revision` is exactly the field-edit fen.md forbids Fen from doing by hand. So the only completion path routes back through the hand-edit the design set out to remove.

**Fix.** Add the guarded watermark-advance as an explicit, single tool command so the contiguous catch-up never requires a `.host` hand-edit:

`host-lifecycle upgrade --advance [--next | <rev>] .`
- `--next` (preferred, Fen-friendly): the tool computes the newest revision reachable from the template HEAD all of whose ancestor-or-equal ledger entries are applied (in-range OR in `applied`), and advances `revision` to it. Fen supplies no SHA — it runs one command and reads the result.
- `<rev>` form: advance to an explicit revision.
- Precondition = the existing watermark-advance guard: refuse (exit non-zero) if any entry ancestor-or-equal the target is neither in range nor in `applied`. This gives the guard a real caller (closing the dead "allowed when contiguous" branch).
- On success the tool writes `.host` itself and FOLDS any now-subsumed ids out of `applied` (an id ancestor-or-equal the new `revision` is dropped), restoring the design's invariant that `applied` is the sparse out-of-order set strictly above the watermark. End state for a full catch-up: advanced `revision`, empty `applied` — matching apply-here step 9 ("gains no `applied` line — contiguous at HEAD").
- Use the same command for the maintainer's own re-stamp (apply-here step 9), which today has the identical no-command gap (only `adopt` writes `.host`).

Also close the degenerate path the guard alone leaves open: `upgrade --record <id>` for an id that is already ancestor-or-equal the current `revision` (or would become contiguously coverable) should not bloat `applied` — record should advance the watermark (or refuse with advice to run `--advance --next`) so an adopter cannot accidentally freeze `revision` and accumulate the whole ledger in `applied`. Add a Fen-acceptance sub-case driving the real 4B through the full contiguous catch-up via `--advance --next` (not just the cherry-apply), asserting `.host` ends with the advanced revision and no `applied` line, with zero hand-edits.

### [record-cmd] --record performs no validation that <id> is a real ledger entry — Fen can record a lie (a typo, a hallucinated id, a wrong-repo SHA) and the stamp will swear work is done
*verdict: real*

**Scenario.** A 4B model running `upgrade --record 7de7cb1` mistypes it as `7dec7b1`, or records the id of a host-lint commit instead of a host-template one, or records an arbitrary 7-hex string it invented. If --record blindly appends the string to `applied`, the stamp now claims an entry is applied that does not exist in the ledger. is_applied(entry, revision, applied) will never match the real entry (different id), so the real entry correctly re-lists as PENDING (fail-safe holds for the real entry) — BUT the bogus id sits permanently in `applied`, and the consistency check ('applied entry whose declared depends is unapplied') can't fire because the bogus id matches no ledger entry to look up depends on. The stamp accretes lies that no check ever flags, and a cold-start auditor (Sable) reading `applied = "7dec7b1"` is told a falsehood. The dimension explicitly asks whether --record should validate against the fetched ledger: it must.

**Fix.** Fold two distinct guarantees into the design's --record and consistency-check sections, both reusing the path `upgrade` already uses (find_template_dir + parse_upgrading + `git rev-parse --verify <id>^{commit}` against the template, per upgrade_applies in main.rs:2128).

1. Record-time validation (make this the normative spec, not just a test criterion): `upgrade --record <id>` MUST fetch/parse the template's UPGRADING.md and confirm <id> resolves to an actual ledger entry's revision *in the template repo* (resolving against the template, so a wrong-repo SHA — e.g. a host-lint commit — is rejected even if 40-hex valid). If it resolves to no ledger entry, exit non-zero, write nothing, and print the list of valid pending ids. Before writing, canonicalize the recorded id to the ledger entry's own id form (resolve an abbreviation/near-miss to the exact ledger key) so `applied` always holds ids in the form is_applied compares against — see the abbreviation hole.

2. Standing junk-id check (the half the consistency check cannot do): whenever `upgrade` (and `software --check` where cheap) reads the stamp, after parsing `applied`, emit a loud WARN for any id in `applied` that resolves to no current ledger entry — separate from the depends-consistency error, because a bogus id matches no entry and the depends check provably never fires on it. This surfaces accreted falsehoods to a cold-start auditor (Sable) instead of letting them sit silently. A WARN (not a hard error) is correct: the ledger can legitimately shrink/rekey across template history, so this is "stamp claims an entry the ledger no longer knows — verify," not an outright failure.

Update README.md:61-63 so the normative --record description states the validation and canonicalization (today it implies a blind write), keep step 4's "bad id rejected" but tie it to mechanism 1, and add the standing junk-id WARN to the consistency-check bullet (README.md:71-73), explicitly noting it is the check the depends-consistency rule cannot cover. Record in the rationale that the fail-safe property for the real owed entry is unchanged — this fix protects stamp integrity / the cold auditor, not owed-work visibility.

### [record-cmd] Abbreviated vs full id: --record stores whatever string the agent typed, so the same entry can be recorded under two non-equal spellings, breaking idempotency and membership
*verdict: real*

**Scenario.** Ledger keys entries by short SHAs like `7de7cb1`. An agent records `--record 7de7cb1` once, then later (different session, no memory) records `--record 7de7cb1f3a9...` (full 40-char) or a 8-char abbrev `7de7cb1f`. The applied-membership test in is_applied is presumably a string-set check; `"7de7cb1" != "7de7cb1f3a9"`, so the second record appends a duplicate, `applied` grows two spellings of one entry, and idempotency (re-record is a no-op — README step 4) is violated. Worse, if the membership test is exact-string while `upgrade`'s PENDING/APPLIED computation resolves ids through git, the two halves of the tool disagree on whether the entry is applied.

**Fix.** Canonicalize recorded ids to a full commit SHA on write, and test applied-membership by resolved commit identity — never by raw string equality. Concretely, fold into plan/0022:

1. `--record <id>` resolves the supplied id against the TEMPLATE submodule (the repo carrying the ledger — the same `find_template_dir(&root)` that `upgrade` uses), via the existing idiom `git rev-parse --verify <id>^{{commit}}` (already used by `upgrade_applies`, src/main.rs:2129). Store the resulting full 40-char SHA in `applied`, regardless of the spelling typed. If the id does not resolve, reject loudly and write nothing (honours step 4's "bad id rejected" and means a fumbled id never lands as a junk membership string).

2. `is_applied(entry, revision, applied)` tests membership by resolved identity, not string equality: resolve the ledger entry's key and each `applied` element through `git rev-parse --verify …^{{commit}}` against the template and compare full SHAs (mirroring `upgrade_applies`'s `have_sha != landed_sha` comparison at 2135). This makes any spelling of the same commit count as applied, and keeps the two halves of the tool (`upgrade`'s ancestry computation and the `applied`-set test) resolving ids the same way, so they cannot disagree.

3. Dedup `applied` by resolved SHA on every write so re-record under any spelling is a true no-op (step 4) and the set never accumulates two spellings of one commit.

4. Apply the same git-resolution when evaluating the `depends`/`independent` consistency check, so a `depends`-id and a recorded id that name the same commit under different spellings compare equal.

Note for the design: this is a correctness/idempotency fix in the record-cmd dimension, not a safety fix — the un-canonicalized failure mode is fail-safe (a mismatched spelling re-lists the entry as PENDING, over-reporting, never hiding owed work, consistent with README line 42). But because the design promises idempotency (step 4) and must be drivable by a 4B model that will type ids inconsistently across sessions, canonicalize-on-write is the right invariant to state explicitly in the build plan (steps 1 and 4).

### [record-cmd] Non-atomic stamp write: a crash or full disk during --record can leave a truncated or empty .host, destroying the watermark and the applied set together
*verdict: real*

**Scenario.** --record reads .host, computes new content, and (per the existing pattern, fs::write at src/main.rs:202) writes in place. If the process is killed or the disk fills mid-write, .host is left partially written or zero-length. The next `upgrade` finds no parseable revision and exits 2 ('not an adopted repo'), or worse parses a truncated revision. For a low-reliability Fen looping the tool, an interrupted run is plausible, and losing the stamp loses both the baseline AND the record of every cherry-applied entry — the adopter's entire upgrade state. fs::write is not atomic.

**Fix.** Make every stamp write atomic, and route ALL stamp writes (adopt, upgrade --record, and any future re-stamp) through one helper so the truncation class is removed everywhere, not just in --record.

Add a helper, e.g.:

  fn write_stamp_atomic(stamp: &Path, body: &str) -> std::io::Result<()> {
      let dir = stamp.parent().unwrap_or_else(|| Path::new("."));
      let tmp = dir.join(".host.tmp");      // same directory => same filesystem
      let f = fs::File::create(&tmp)?;
      use std::io::Write;
      { let mut w = std::io::BufWriter::new(&f); w.write_all(body.as_bytes())?; w.flush()?; }
      f.sync_all()?;                          // fsync the temp before rename
      fs::rename(&tmp, stamp)?;               // atomic replace on POSIX and Windows (Rust std)
      Ok(())
  }

On any error, remove .host.tmp and return non-zero, leaving the original .host untouched (do `let _ = fs::remove_file(&tmp);` in the error path). fs::rename over an existing destination is atomic on both Linux and Windows in current Rust std, so this needs no cfg split; the only requirement is that the temp file sit in the SAME directory as .host (it does), so the rename stays within one filesystem.

Fold into plan/0022:
- Build step 4 (`upgrade --record`): specify the write goes through write_stamp_atomic, not bare fs::write. State the invariant: ".host is never left partially written; on any write error the prior .host is intact and the command exits non-zero (the adopter retries safely)."
- Also convert the existing `adopt` write at src/main.rs:202 to the same helper, so adopt is not a second truncation site.
- Idempotent no-op path: when --record finds the id already present, compute the new body, compare to the current file, and skip the write entirely if unchanged — so a re-record performs no rename at all (cheaper, and no window where .host is briefly replaced by an identical copy).
- Add a unit test that simulates the torn-write recovery contract: write a valid .host, then assert that a failed atomic write (e.g. a body-validation error before rename) leaves the original byte-for-byte intact and the .host.tmp removed.

Minor doc correction to the design rationale (not the fix): note that a truncated `revision` re-lists every entry (fail-safe over-report) rather than mis-applying; the harmful losses are (a) an empty/zero-length .host reading as "not an adopted repo" (upgrade exits 2), and (b) loss of the `applied` set causing already-applied, possibly non-idempotent ledger entries to re-list and be re-applied. The atomic write closes both.

### [record-cmd] Malformed or missing .host: --record has no defined behavior, and a 'helpful' create-from-scratch would fabricate a stamp / wrong template URL
*verdict: real*

**Scenario.** Fen runs `upgrade --record 7de7cb1` in a directory with no .host (wrong cwd, or pre-adoption), or with a .host that has a template line but a blank/garbage revision. If --record falls back to creating a stamp (like adopt's stamp_body), it would invent a revision-less or wrong stamp and write the wrong TEMPLATE_URL constant; if it appends to a revision-less stamp, the is_applied ancestry branch has no baseline and the guard has nothing to compare. Either way the tool manufactures state instead of refusing. version() (src/main.rs:230) already shows the precedent: no readable stamp → exit 1, not create.

**Fix.** Add to the design (Build step 4, `upgrade --record <id>`): `--record` MUST NOT create or repair a `.host` stamp. It is a second writer of `.host`, but unlike `adopt` it never calls `stamp_body`/the create-from-scratch path. Preconditions, checked before any write:

1. `.host` must exist and parse, with a non-empty `revision` (the same `parse_revision` that already collapses missing AND blank `revision = ""` to None). The `revision` is the baseline both `is_applied` (ancestor-or-equal(revision)) and the watermark-advance guard rest on; recording an `applied` id onto a revision-less stamp would record into a structure whose other half is broken, defeating the fail-safe claim.
2. If `.host` is absent: exit non-zero, message "no .host — not an adopted repo; run `host-lifecycle adopt <dir> <revision>` first." (Mirror `upgrade()`/`version()` refuse-on-missing; never fabricate the TEMPLATE_URL constant.)
3. If `.host` is present but `revision` is missing/blank/unparseable: exit non-zero, name the offending stamp and that `revision` is empty/unreadable, and refuse — do NOT suggest re-`adopt` here (the stamp is a broken adopted stamp, and re-adopt would clobber it via stamp_body). Tell the user to repair the `revision` line.
4. Only after both preconditions pass does `--record` write `.host` (idempotent append of the `applied` id; re-record is a no-op).

Update step 4's verify line to cover the new cases: "verify: record adds id; re-record no-ops; bad id rejected; **missing .host rejected (points at adopt); present-but-blank/unparseable `revision` rejected (refuses, does not re-adopt); never writes the TEMPLATE_URL constant from --record.**"

### [record-cmd] --record does not run (or gate on) the loud consistency check, so Fen can record an entry whose declared `depends` is unapplied and create an inconsistent stamp the tool only complains about later
*verdict: partial*

**Scenario.** The lane chain is annotated `821a216 depends b6232a5 c771d60`. An adopter at an old watermark runs `--record 821a216` without having applied b6232a5/c771d60 (neither in range nor in applied). The README puts the consistency error in `upgrade` and `software --check`, but if --record itself does not check, the write succeeds and produces a stamp that asserts a dependent migration is done while its prerequisites are not. The inconsistency surfaces only on the next `upgrade` run — by which point the agent has moved on believing the record succeeded. This is recording a (structurally) impossible claim.

**Fix.** Fold a consistency gate into `--record` (build step 4), so the teeth sit at the moment of the action, matching the Fen persona's "single command, tool-driven, fail-safe" requirement and the design's own consistency definition.

Define `--record <id>` as: (1) reject a bad id (id not in the ledger) — unchanged; (2) compute the would-be applied set = current applied set ∪ {id}; (3) evaluate the id's annotation:
  - `depends = <prereq>...`: if any prereq is unapplied under the would-be set (not ancestor-or-equal `revision` and not in `applied`), REFUSE — exit non-zero, write nothing, and name the missing prerequisites plus the `--record` commands that would satisfy them. (Refusal, not record-and-warn, for a `depends`-declared entry: an honest stamp should never momentarily assert a dependent migration done while its prereqs are not.)
  - `independent = true` or annotation absent (undeclared): record normally, exit 0.
Keep idempotency: re-recording an already-applied id is a no-op exit 0 even if a prereq is unapplied, so a forgotten record still re-lists rather than wedging (preserves the fail-safe over-report direction).
Update step 4's verification to add: "recording a `depends`-declared id whose prereqs are unapplied is refused non-zero and writes nothing; recording it after its prereqs are recorded succeeds." Keep the existing `upgrade`/`software --check` consistency error as the cold-read/CI backstop (defense in depth) while moving the primary teeth to the moment the inconsistent claim would be written.


## Minor (7)

### [back-compat] New `independent`/`depends` ledger keys are safe for an old binary (ignored) but absence-handling is asymmetric: a new binary over an OLD ledger must not treat unannotated entries as unsafe-by-default in a way that changes existing `upgrade` output
*verdict: partial*

### [completeness] Interaction with `host-lifecycle version` is unaddressed — `version` prints only `revision` and will mislead once an applied set exists
*verdict: partial*

### [dependency-hints] Whether `upgrade --record <id>` refuses to record an entry whose deps aren't applied is left as an open question in the prompt and unresolved in the design
*verdict: real*

### [dependency-hints] Watermark-advance guard and the applied-set interact unspecified-ly when an entry is BOTH in the advance range AND already in `applied`
*verdict: partial*

### [fail-safe] An `applied` id that is also an ancestor of the watermark masks the case where the watermark was advanced but the out-of-order entry was never actually applied — double-counting launders a gap
*verdict: partial*

### [record-cmd] Recording an id already ancestor-of-watermark is redundant and, if appended, pollutes `applied` with entries that should live only in the contiguous baseline
*verdict: real*

### [record-cmd] `applied` token-list serialization is undefined for dedup/order/whitespace, letting repeated --record calls produce divergent stamps and defeat idempotency byte-equality
*verdict: real*


*Full per-finding scenarios/fixes for minors omitted; see the workflow transcript `subagents/workflows/wf_43f48892-0e9` if needed.*
