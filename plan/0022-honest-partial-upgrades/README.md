# Honest partial upgrades: an applied-set stamp the tool carries

> **v2** — pivoted after an adversarial design review (see `design-review.md`).
> The original design keyed "applied" off **git ancestry** of ledger SHAs; the
> review proved that foundation wrong (below), so v2 keys off **ledger order**
> and an **explicit applied set**. The clusters after the pivot fold in the
> review's confirmed blockers/majors.

## Why

The `.host` stamp records a **single** `revision`; `host-lifecycle upgrade` lists
ledger entries newer than it as pending. That assumes entries are applied in
order, contiguously. A real adopter behind HEAD may need a *late, independent*
entry (a worktree bugfix) without an *earlier, large, unrelated* one (a spec
migration). The single revision can't express "applied the late one, skipped the
early ones", and the field workaround — jump the watermark, note the debt in
prose — **fails unsafe** (`upgrade` then reports "up to date" while work is owed).

Worked from four added personas (`cast/`: Orin, Bly, Fen — Sable folded into Bly),
the first design chose **watermark + applied set**, with "applied iff
ancestor-or-equal(revision) OR id ∈ applied". An adversarial design review then
proved that foundation is wrong, verified against real history:

- **Git ancestry of ledger SHAs is not the dependency order.** `7de7cb1` (the
  "independent" worktree fix) is a **descendant** of `b6232a5` (the spec
  migration), so a git-ancestry watermark reaching the fix would mark the whole
  migration applied. The linear chain is a commit artifact, not a dependency DAG.
- **Ancestry isn't even reliable.** The three earliest ledger keys (`8c28e33`,
  `325f2cf`, `71d12a8`) are **not ancestors of template HEAD** (rebased history),
  so any `merge-base --is-ancestor` against them fails — the computation is
  undefined for real entries.
- The watermark `revision` is virtually never itself a ledger-keyed commit, so
  "advance revision to `<rev>`" has no natural target.

## The pivot: ledger order, explicit applied set — no git ancestry

The ledger (`UPGRADING.md`) is the source of truth and defines a **total order by
stanza position** (file order), with each entry identified by its `[upgrade
"<id>"]` **key string**. The tool never resolves those ids as git commits.

`.host` gains two optional fields:

```
template = "…/host-template"
baseline = "<id>"            # every ledger entry AT-OR-BEFORE this stanza position is applied
applied  = "<id> <id> …"     # individual entries AFTER the baseline, applied out of order
revision = "<sha>"           # retained: the template commit the docs were last reconciled to
adopted  = "YYYY-MM-DD"
name     = "…"
```

An entry is **applied** ⇔ its ledger position ≤ `baseline`'s position **or** its id
∈ `applied`. Pure string/position math — no `merge-base`, so orphaned/rebased SHAs
and the descendant≠depends trap both dissolve. **Fail-safe:** an id not recorded is
pending and re-lists; the unsafe "advance past unapplied work" move is structurally
removed (the baseline only advances across a fully-applied contiguous run).

Initial adoption sets `baseline` to the latest entry (compact — no list). A
cherry-applied late entry goes into `applied` (baseline stays put; the skipped
earlier entries remain pending). When a contiguous run is finally complete, advance
`baseline` across it and prune those ids from `applied`.

## Hardening clusters (from the review)

### 1. `--record` is a *verified* claim, not a bare assertion (blocker)

`upgrade --record <id|ordinal>`:
- **Validates** the id is a real ledger entry (reject unknown / typo / wrong-repo
  SHA / ambiguous). Accepts a **ledger ordinal** or unambiguous form so Fen never
  retypes a hex SHA; the tool canonicalizes to the id.
- Where the entry declares a machine-checkable post-condition `verify = <check>`
  (a `host-lifecycle`/shell check; e.g. the worktree-escape check for `7de7cb1`),
  `--record` **runs it and refuses** to record on failure. Where no post-condition
  exists, recording **requires** an explicit `--unverified call/NNNN` citation
  (resolved like `repro-exempt`), so an un-attestable claim leaves a `call/` trail.
- **Atomic** write (temp+rename); **provenance** line `applied = <id>
  recorded=<date> via=<verify|call/NNNN>` (append-only); refuses if the entry's
  `depends` are unapplied.

### 2. `software --check` re-checks every claim (blocker)

`software --check` (and `verify`) gain stamp+ledger plumbing: they re-run each
applied entry's `verify` post-condition and emit a loud `DRIFT` on any
claimed-but-unsatisfied entry — symmetric with the existing repro-exempt/artifact
attestation. This is the teeth against a recorded lie (the unsafe direction the
membership set alone can't catch).

### 3. Robust stamp I/O (blocker)

- Every `.host` writer (`adopt`/`stamp_body`, `--record`, baseline advance)
  **preserves all fields** — `name`, `applied`, `baseline`, unknown lines — instead
  of rewriting from a fixed list (today it silently drops `name`).
- The stamp parser tolerates an inline `# comment` after a quoted value and defined
  whitespace; the `applied` serialization has a defined separator + dedup + stable
  order so repeated `--record` is byte-idempotent.

### 4. The tool carries the process for Fen (blocker)

- `host-lifecycle upgrade --next` prints (and, with `--record`, the agent runs) the
  **single next action** — no multi-line listing to parse, no column to read.
- Accept **ordinals**, not SHAs; print a **positive confirmation** after a record
  ("recorded <id> (<title>); N still pending"). The tool parses the ledger; the
  model never emits structured/grammar-constrained output (the wedge lesson).

### 5. Dependency hints, reconciled (major)

- `depends = <id> …` (logical entry prerequisite) is distinct from the existing
  `requires = host-lifecycle vX.Y.Z` (tool-version); the plan names and checks both.
- Define: transitive deps, a `depends` into baseline range = satisfied, and reject
  cycles / self-deps / both-`independent`-and-`depends` / unknown dep ids. `--record`
  refuses an entry whose `depends` aren't applied (fail-safe).
- Back-fill by **logical** dependency (not git ancestry): the spec-lane chain
  `c771d60→b6232a5`, `b8c54fc→c771d60`, `821a216→b6232a5,c771d60`; `7de7cb1` and
  `ae1e688` are `independent`.

### 6. Migration, version, docs, tests (completeness)

- **Migrate existing `.host`**: a documented (and tool-assisted) conversion of the
  legacy single-`revision` watermark to `baseline` (+ empty `applied`), so current
  adopters are not silently mis-read.
- `host-lifecycle version` prints `baseline` + `applied` + pending count (today it
  prints only `revision` and would mislead once an applied set exists).
- Spine `CLAUDE.md` + README *Upgrading* + the UPGRADING entry describe the **new
  two-field model**, not the old one.
- Bundle the two pending `host=` corrections (the `host=windows`→omit example and
  the `host=` vs `attest-host` materialize-OS-vs-build-OS wording) + the issue #2
  comment fix; specify before/after text.

## Build (software-first; each step with its check)

1. **Stamp model** — parse `baseline`/`applied`; `is_applied(entry)` by ledger
   position OR membership (no git). Robust parse (comments/whitespace) + all-field
   preserving writer + defined `applied` serialization. *verify:* unit tests incl.
   orphaned-SHA keys, comment-after-value, field preservation, byte-idempotent write.
2. **Ledger parse** — stanza order; `independent`/`depends`/`verify`; reject
   cycles/self-dep/both. *verify:* parse tests + a malformed-ledger test.
3. **`upgrade` rewrite** — list pending by ledger order ∖ applied; `--next`;
   machine-readable; dependency advice; loud consistency error. *verify:* fixture
   ledger+stamp → expected pending/next; inconsistent dep → non-zero.
4. **`--record`** — validate id, ordinal input, `verify` post-condition or
   `--unverified call/NNNN`, atomic, provenance, deps-gate, idempotent. *verify:*
   record/validate/idempotent/reject-unknown/reject-unverified tests.
5. **baseline advance** — only across a fully-applied contiguous run; prune absorbed
   ids. *verify:* advance blocked on a gap; allowed + prunes when contiguous.
6. **`software --check` plumbing** — re-check applied post-conditions, surface
   partial state, loud DRIFT on a stale claim. *verify:* check flags a lie.
7. **Back-fill ledger** `independent`/`depends`/`verify` (logical). *verify:*
   `upgrade` advice matches the real dependency structure.
8. **version output + migration** of legacy `.host`. *verify:* version shows
   baseline/applied/pending; a legacy stamp converts.
9. **Spine + README + UPGRADING** (new model) + the two `host=` corrections +
   issue #2 comment. *verify:* docs describe the two-field model; `validate` clean.
10. **Apply here** — version bump + tag, re-pin, migrate agentic-host's own `.host`
    to `baseline`, bump CI rev; MEMORY. *verify:* `upgrade .` up to date;
    `software --check .` clean; tests + clippy green.

## Persona acceptance

- **Orin:** the stamp is the contract, read by ledger position not fragile git
  ancestry; sparse annotations; orphaned SHAs don't break it.
- **Bly:** cherry-applies the late independent entry now; the deferred rest stays
  pending; a later cold read cannot be deceived (re-check + fail-safe).
- **Fen (real `qwen3.5-4b`):** `--next` + ordinal `--record` + confirmation mean the
  tool carries every state change; the model never reasons about ancestry, hand-edits
  `.host`, or emits constrained output. **Baseline observed:** handed today's flow,
  the real 4B *wedges* on the reasoning+edit task (it doesn't answer wrong, it hangs)
  — the bar the tool surface must clear.

## Verification (milestone done)

`cargo test` + clippy green; every build-step check passes. **Fail-safe invariant
test:** no sequence of (record, advance, hand-edit, run) makes `upgrade` report clean
while a ledger entry is unapplied — including a recorded-but-unverified claim, which
`software --check` must flag. **Round-trip:** parse→write→parse is byte-stable.
**Orphaned-SHA test:** a rebased ledger key is handled by position, never by
`merge-base`. **Fen acceptance gate (real model, A/B + adversarial leg):** the 4B
completes a cherry-apply via `--next`/`--record` without hand-editing `.host`
(after the timeout/server are healthy); and when induced to `--record` an entry it
did **not** perform, the tool refuses (no `verify`/citation) or `software --check`
later flags it. Pin/fallback the external model so the gate is reproducible.
Applied here with `upgrade .` up to date and `software --check .` clean; tagged.
