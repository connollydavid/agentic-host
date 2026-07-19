# plan/0074 host-lifecycle materialize-receipt + envhash: provenance and coherence for the Where room

Closes [connollydavid/host-lifecycle#18](https://github.com/connollydavid/host-lifecycle/issues/18) and [connollydavid/host-lifecycle#19](https://github.com/connollydavid/host-lifecycle/issues/19). Paired by operator ruling (2026-07-19): they share every state-changing call site, so building them together with one explicit non-overlap discipline avoids the duplication a sequential pair of plans would risk.

## Why

Two gaps in the materialize/install-hooks lifecycle, with one root: `host-lifecycle software --materialize` re-realizes the worktrees (and the gating binary the commit hooks run) but leaves no auditable trace, and a subsequent move, image bump, partial submodule re-init, or ambient rebuild of the gating binary leaves the tree locally different from what the operator last touched, even though every checked-in record is unchanged.

- **#18 (provenance)**: after a clone + materialize, an operator cannot tell from the audit trail when, where, or by whom the worktrees were last realized, even though the gating binary they then trust was produced by that materialization.
- **#19 (coherence)**: after a repo move, a partial `submodule` re-init, an image bump, or an ambient rebuild of the gating binary, the local tree differs from what the operator last touched, with no signal that it moved.

They are complementary, not duplicative, **provided the call sites are wired with a strict event-vs-state discipline**. That discipline is the load-bearing part of this plan; without it the two features overlap and confuse.

## Scope

Two host-lifecycle features, one release:

1. **The materialize receipt (#18).** An operational receipt in `.host-lifecycle-receipts` written on `software --materialize` (and on a recorded `git submodule update` / checkout that touches the Where room), in the same append-only shape as the `embed` receipt.
2. **The environment hash (#19).** A gitignored `.host-envhash`, recomputed on demand, compared by a new `host-lifecycle env --check`. Local-only, never checked in, never fails the gate.

### Operator rulings (2026-07-19)

1. **Paired in one plan.** The shared call sites are wired once; the non-overlap discipline is enforced in one design, not reconciled across two.
2. **Two distinct files.** `.host-lifecycle-receipts` (checked-in provenance) and `.host-envhash` (gitignored coherence). Never the same file.
3. **Two distinct subcommands.** The receipt writes via the existing `software --materialize` (automatic); the envhash reads via the new `host-lifecycle env --check` (advisory, explicit). `env` writes happen automatically on the state-changing ops, never via a separate write subcommand.
4. **Full methodology.** Gather-data (only where there are conditionals), cast consultation (specifically on the non-overlap boundary), adversarial review (with the duplication risk as a named lens), then build.

## The non-overlap discipline (load-bearing)

The two features share every call site. What keeps them from duplicating is a single rule: **the receipt records the EVENT; the envhash records the STATE**. An event is "what happened, by what authority, when"; a state is "what is here now, hashed how". The non-overlap table:

| Fact | Receipt (#18, provenance) | Envhash (#19, coherence) |
|---|---|---|
| Materialization happened | yes (the event itself) | no (no event log) |
| Disposition (done/skip) | yes | **forbidden** (the issue is explicit) |
| Evidence (e.g. "git submodule update --init") | yes | **forbidden** |
| Timestamp | yes | **forbidden** (a digest has no time) |
| Component realized | yes (by name) | yes (by worktree presence) |
| Pin SHA | **reference only** ("at pin per `.host-software`") | **never** (pin adherence is `software --check`'s job) |
| Toolchain image reference | yes (e.g. `rust:1.95.0`) | no (the reference is in `.host-software`) |
| Toolchain image digest | **never** | yes (the digest of the currently pulled image) |
| Hook binary hash | **never** | yes (the hash of `.git/hooks/host-lint`) |
| Hook binary "installed" | yes (as part of the event) | no (the hash subsumes presence) |
| Repo abspath | **never** | yes |
| Submodule init state | **never** | yes (which tool submodules are initialized) |

The receipt and the envhash disagree about every row where they could overlap: one of them always defers. The disagreement is the design.

## The call-site wiring

Every state-changing op writes the receipt **and** the envhash, but records orthogonal facts:

- `software --materialize`: writes a materialize receipt (event, components realized, pin-by-reference, image reference, timestamp) and writes `.host-envhash` (worktree paths, hook binary hash, image digest, submodule init state, repo abspath).
- `software --install-hooks`: writes `.host-envhash` (new hook binary hash) and writes **no** receipt (it is not a materialization; a future `install-hooks` receipt is a named follow-up, out of scope here).
- `software --verify_build`: writes `.host-envhash` (image digest confirmed) and writes **no** receipt (it is a re-derivation, already receipted elsewhere).
- image pull: writes `.host-envhash` only (the receipt is unaffected; an image pull is not a host-lifecycle op).

`host-lifecycle env --check` recomputes the envhash from current state, diffs against the stored one, and prints only the delta. `software --check` reports the envhash state alongside the gate result, never as part of pass/fail.

## Open design questions

The gather-data and cast pass rule on these:

- **The receipt kind.** #18 names an open question: its own kind (a fourth, alongside methodology-version, operational, and task ledgers) vs re-opening the `embed` phase recheck. Our read is **its own kind**, so `embed`'s `test -f .host-software` recheck stays cheap and the materialization event is recorded where operators look for "what happened to this tree." Operator rules in gather-data.
- **The envhash format.** TOML or plain text. The issue says "the digest plus a per-input sub-hash line", which implies a flat key:value file. TOML is host-lifecycle's idiom.
- **The `env --check` exit code.** Advisory means exit 0 even on delta. The convention is `0` clean, `0` with delta printed (advisory), `2` cannot-proceed (no envhash ever written, no envhash on disk).
- **The image-digest probe.** Reading the locally pulled image digest requires shelling out to `docker` / `podman` inspect. If no runtime is present, the envhash records "no runtime" and the envhash is silent on the image dimension; `env --check` does not fail.
- **The spine change.** #18 is methodology-level (every materialization emits a receipt; a fourth receipt kind). The spine (host-template CLAUDE.md) names this. #19 is tooling-only and adds no spine doctrine.

## Verification

- **Unit tests** for the receipt writer (every field, the append-only discipline, the no-state-fields rule) and for the envhash writer (every input dimension, the per-input sub-hash, the no-event-fields rule).
- **Integration tests** for the non-overlap discipline: a single `software --materialize` run writes both files; the two files share NO data field by name. A test asserts the schema disjointness directly.
- **Integration tests** for `env --check`: a repo move, a hook binary rebuild, a submodule toggle, and a missing envhash each produce the expected advisory output and exit 0.
- **Allium spec** for the `MaterializeRun` and `EnvHash` entities, the no-overlap invariant (a `Reads` field on one is a `NeverReads` field on the other), and the append-only receipt rule. `allium check` + `analyse` + `plan` exit 0; obligations discharged by tests; Kani for the schema disjointness invariant.
- **Fen probe** (gather-data.md): the `env --check` delta format reads as a route (which dimension moved) to a 4B, and the receipt-vs-envhash distinction reads as two different concerns, not two names for the same thing.
- **Cast consultation** (cast/*.md): Bly (overstates-completeness; the envhash is NOT an audit), Orin (fails-unsafe; a missing envhash is a prompt, not a failure), Fen (weak-agent-trap; `env --check` must not read as a gate).
- **Adversarial design review** (design-review.md): five independent lenses, with the duplication risk as a named lens (a reviewer whose sole job is to find overlap between the two features).
- `host-lifecycle software --check .` clean at the new pin; the host-lifecycle release receipt recorded; #18 and #19 closed.

## Build sequence

The tasks are anchored receipted nodes (plan/0042), built as a forward graph:

### gather-data {#gather-data}
Grounds the few conditionals: the receipt-kind question (#18's open question), the envhash file format, the env-check exit code, and the image-digest probe (when no runtime is present). No UX probe needed; both issues are prescriptive.
- verify by: every conditional in this README traces to a gather-data.md row
- depends: none

### write-spec {#write-spec}
The `MaterializeRun` and `EnvHash` Allium surface, the no-overlap invariant, the append-only receipt rule, the envhash-is-not-a-receipt rule. Lives in the host-lifecycle repo.
- verify by: `allium check` + `allium analyse` exit 0, zero findings
- depends: #gather-data

### write-obligations {#write-obligations}
Every `allium plan` obligation dispositioned in a `<spec>.obligations` manifest, discharged by the unit and integration tests. The schema-disjointness obligation is a Kani harness.
- verify by: `host-lifecycle obligations <spec> --tests tests --strict-discharge` clean
- depends: #write-spec

### implement-receipt {#implement-receipt}
The materialize receipt writer: a new entry in `.host-lifecycle-receipts` on `software --materialize`, with the event-level fields only (components realized, pin by reference, image reference, timestamp, evidence line).
- verify by: `cargo test` green; a materialize run appends exactly one receipt with the schema fields and no state-level data
- depends: #write-obligations

### implement-envhash {#implement-envhash}
The envhash writer and the `env --check` reader: `.host-envhash` (gitignored), written by `--materialize` / `--install-hooks` / `--verify_build` / image pull, read by `env --check`. Per-input sub-hash for the five dimensions. Advisory exit codes.
- verify by: `cargo test` green; each state-changing op refreshes the envhash; `env --check` prints the delta and exits 0
- depends: #write-obligations

### wire-shared-call-sites {#wire-shared-call-sites}
Wire `software --materialize` to write both files in one call. Wire `--install-hooks`, `--verify_build`, and the image-pull path to write `.host-envhash` only. Assert the call-site-level non-overlap: one call site, two writers, no shared data field.
- verify by: a `software --materialize` run produces both artifacts; `--install-hooks` produces only the envhash; a test asserts the call-site wiring writes each file exactly when the design says to
- depends: #implement-receipt, #implement-envhash

### write-tests {#write-tests}
Integration tests covering every call site, every envhash dimension, every env-check delta path, and the schema-disjointness property (the two files share no data field by name).
- verify by: full test suite green; Kani proof of the schema disjointness
- depends: #wire-shared-call-sites

### cast-consult {#cast-consult}
Cast consultation across Mara, Wren, Bly, Orin, Fen on the non-overlap discipline and the envhash-is-not-a-receipt framing. Recorded in design-review.md.
- verify by: each cast persona's concern addressed or recorded as a follow-up
- depends: #write-tests

### adversarial-review {#adversarial-review}
A multi-lens adversarial review with one lens dedicated to finding overlap between the two features. Findings recorded in design-review.md; the re-cut staged there.
- verify by: every blocking finding fixed or recorded; the re-cut executed
- depends: #cast-consult

### write-spine-doctrine {#write-spine-doctrine}
The host-template CLAUDE.md gains the materialize-receipt doctrine: a materialization is an operational event that emits a receipt in `.host-lifecycle-receipts`. Names the fourth receipt kind. No spine doctrine for the envhash (it is tooling-only, local). An UPGRADING entry keys the new revision.
- verify by: `host-lifecycle upgrade` lists the entry on a pre-revision host; `upgrade --record` clears it
- depends: #adversarial-review

### release-and-re-pin {#release-and-re-pin}
`host-lifecycle release host-lifecycle --change-class adds-flag`, re-pin `.host-software`, record the release receipt, close #18 and #19.
- verify by: `host-lifecycle software --check .` clean at the new pin; #18 and #19 closed
- depends: #write-spine-doctrine

### fen-acceptance {#fen-acceptance}
The real `qwen3.5-4b` runs `env --check` on a moved repo and a rebuilt hook binary, and confirms the delta reads as a route (which dimension moved), not a gate verdict. Separately, the model distinguishes the receipt from the envhash given a one-line description of each, so the non-overlap reads at the weak-agent bar.
- verify by: Fen routes each delta correctly and distinguishes the two artifacts
- depends: #release-and-re-pin
