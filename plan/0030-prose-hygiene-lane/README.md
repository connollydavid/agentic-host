# plan/0030: The prose-hygiene lane: a walking docs audit (`--docs`), weak-agent-fixable output, and re-derivable record exclusion

> **Re-scoped after a five-lens adversarial review** (`design-review.md`) and a Qwen-3.5-4B
> classification probe. The original sketch bundled three strands: a repo-wide prose walk, a
> hash-pinned `.host-lint-receipts` ack file, and a receipts-family re-homing. The review came back
> convergent and grounded in the repo's own shipped code and prior decisions, and the operator took
> two decisions from it:
>
> 1. **Exclude immutable records by a re-derivable predicate + the existing fence, not a
>    self-asserted hash ack.** A `(path, hash, reason)` freeze would be the project's first
>    self-asserted receipt (inverting `call/0017`'s "evidence is re-derived, never self-asserted"),
>    and its "edit lapses the ack, then clean to zero" rule would *force rewriting the immutable records it
>    protects* (against `CLAUDE.md` §6). The need is already met: `.host-lintignore` whole-file-excludes
>    the append-only memory log, and the `host-lint:ignore` fence (`call/0019`, spine `da000aa`)
>    line-precisely boxes irreducible citations, and the prose scanner already skips fenced blocks.
> 2. **Defer the receipts-family re-homing to its own milestone.** Moving the applied-set out of
>    `.host` and splitting `.host-receipts` rewrites two shipped, gate-bearing files; the installed
>    binary breaks (the gate reads the applied-set only from `.host` and reads a single `.host-receipts`),
>    and CI cold-installs a pinned old-format binary. That is a dual-format `host-lifecycle` migration,
>    orthogonal to the prose need. The settled ontology stands; only its build is sequenced after. See
>    **Deferred** below.
>
> This milestone is what remains: make the prose audit a **real, walking, weak-agent-executable gate
> lane**, with immutable records excluded soundly by the *existing* mechanisms. Execution of the
> repo-wide clean still waits for the operator's literal front-door sentence (the triggered migration,
> D5); the design and the tooling land now.

## Context

`host-lint --prose` (the tropes.fyi LLM-slop detector, `plan/0007`/`0008`/`0010`) ships and works on a
file or stdin, but it is **unused by the lifecycle** and **does not walk**: the `--prose` branch
(`main.rs:453`) short-circuits before `--all` and never loads `.host-lintignore`, so there is no repo-wide prose
audit today. The spine already carries the standing rule:
**"Prose hygiene is the same lane, applied continuously"** (host-template `950fbd6`,
`CLAUDE.md:220-229`): the `verify` phase applies the prose audit and `software --check` re-verifies by
re-running the prose audit, `MEMORY.md` excepted via `.host-lintignore`. But that rule's enforcement
(a `recheck =` in `lifecycle.manifest`) is **inert until a repo-wide prose mode walks the tree** (D1
adds it as `host-lint --docs`) and `950fbd6` is **pending** in `.host` (recording it now would HAZARD on the ~1,652 existing
trope-lines). The front-door README (`software/host/main/README.md`) already encodes the prose clean as
a triggered migration step.

So the lane is authored but toothless. The deliverables below make it real and dogfoodable down to the
weak-agent (Fen / Qwen-3.5-4B) bar.

## Deliverables

### D1: `--docs`, a repo-wide prose mode over authored docs *(host-lint, shipped v0.8.0)*

Add a single, logically-named mode, **`host-lint --docs`**, for the repo-wide prose audit, rather than
overloading `--prose --all`. The principle is **scope determines type**: naming tells hide anywhere, so
`--all` scans every scannable file (code + docs); prose tropes live only in authored narrative, so
`--docs` walks **markdown only**. It reuses the `--all` directory walk (`git ls-files`, `path_ignored`,
the `book/` / embedded-worktree / `host-template/` exclusions, `.host-lintignore`) but **restricts to
`.md`** and **skips generated markdown** (`SUMMARY.md` from `host-lifecycle book`, a file the generator
overwrites cannot be hand-cleaned). Prose-scanning `.rs`/`.toml`/`.sh` would flag em-dashes and tricolons
in code comments and string literals (false positives, and a nonsensical clean-to-zero bar over source).
`--all` (naming, everywhere) and `--docs` (prose, docs) are the two single-flag repo modes; `--prose
[file]` stays for one doc or stdin. This is the capability `950fbd6`'s `recheck` already assumes.

### D2: weak-agent-fixable output, carved out to `plan/0031`

The clean (not the classify) is the hard part for a weak agent, and the current output defeats it: one
em-dash emits **ten byte-identical records** with no column, and some tropes report a whole-document
diagnosis with no location at all. Making the output one-record-per-occurrence + columned + fix-hinted +
advisory-tiered grew into a multi-repo engine question (the over-emission lives in `host_grammar`), so it
is now its own milestone, **`plan/0031` (fixable prose output)**. `plan/0030`'s D5 (the triggered clean)
**depends on `plan/0031`**: the clean is not weak-agent-executable until the output is locatable.

### D3: re-derivable immutable-record classification (no self-asserted acks) *(methodology + small tool support)*

What gets cleaned versus boxed must be decided by a **re-derivable predicate**, never a human "reason"
string. The disposition rule (extends `call/0019`'s reword / box / path-exclude, keyed on facts the
tool can re-check):

| Class | Re-derivable predicate | Disposition |
|---|---|---|
| **Live** | editable doc; milestone `STATUS:` ≠ done; live/proposed governance | reword to **zero** locatable tropes (GATE) |
| **Immutable record** | accepted/superseded MADR `Status:`; milestone `STATUS:` done; dated review artifact | **box** the irreducible/quoted tropes in a `host-lint:ignore` fence (`call/0019`); the rest of the file stays linted |
| **Append-only** | the agent's memory log (`MEMORY.md`) | whole-file `.host-lintignore` (already present) |

To make "Live vs Immutable record" re-derivable rather than inferred from prose, **add an inline
`STATUS:` line to every `plan/NNNN/README.md`** (only 4 of 31 carry one today) and read the MADR
`Status:` field. The convention is the existing form (a `> **STATUS: <STATE> (date).**` blockquote near
the top) and the predicate reads the `<STATE>` token: `COMPLETE` / `done` / `shipped` yields **Record**,
anything else (`planned`, `built`, in-progress) yields **Live**. The `.gitattributes` (`*.md text eol=lf`)
lands now for cross-platform determinism; the 27 `STATUS:` additions are applied with the triggered clean
(D5), where the classification is consumed. Classification becomes a field lookup a weak agent can do,
not an adjudication of
"deferred" vs "done" from a status paragraph. No new file format, no content hash, no edit-lapses-clean
trap; the exclusion is the existing, diff-visible, line-precise fence + ignore, and a future real trope
edited into a record is still caught (the fence boxes only the quoted span, the rest stays scanned).

### D4: wire the lane into the `verify` gate, re-derivably *(adopted spine copy + manifest)*

Apply the already-authored spine rule `950fbd6`: add `host-lint --docs` to the `verify` phase
`recheck =` in this project's `lifecycle.manifest`, so
`software --check` re-runs the prose audit and a regressed doc re-opens the **existing** `.host-receipts`
`verify` receipt as a HAZARD (re-derivation, per `call/0017`, *not* the deferred re-homing). Add a
`.gitattributes` (`*.md text eol=lf`) so the walk is identical across the Windows/WSL/Linux-CI split.
The `upgrade --record 950fbd6` happens as part of D5 (recording it before the docs are clean would
HAZARD). The `950fbd6` ledger text names `host-lint --prose`, written before this mode existed; the
recheck uses `host-lint --docs` (the repo-wide mode D1 adds); the spine wording can be refreshed in a
later prose-rule touch.

### D5: the triggered clean (waits for the operator's front-door sentence)

On the literal sentence *"Read and follow https://github.com/connollydavid/host to keep this repository
an agentic project."*, follow the front-door README to bring agentic-host to exemplar state: run
`host-lint --docs`; for each flagged doc apply the D3 disposition (clean Live to zero locatable
tropes; box record citations in fences; `MEMORY.md` already excluded); **one doc per commit** (audited
docs, each a verifiable goal, where `--prose <doc>` returns clean and `host-lint <doc>` stays naming-clean
before the next); then `host-lifecycle upgrade --record 950fbd6`; whole-suite green.
**STOP rule:** if removing a trope would change a normative claim or force a naming tell (exit 1), box
it or leave it and record; never mangle a doc to force the gate green. `plan/0031`'s fixable output
(spans + fixes + advisory tiers) and D3 (re-derivable classes) are what make this executable at the 4B
bar; until they ship, the clean is a manual cryptographic-and-judgement task and must not start.

## Deferred: the receipts-family re-homing (its own milestone)

The ontology settled with the operator stands and is recorded here for the follow-up milestone, built
as a **dual-format `host-lifecycle` migration**, not bundled with this prose work:

| File | Records | Written by |
|---|---|---|
| `.host` | the stamp: template, adopted revision, name, baseline | host-lifecycle |
| `.host-receipts` | **adoption + upgrade**, the methodology-version trail (the `.host` `applied` set **moves here**) | host-lifecycle |
| `.host-lifecycle-receipts` | host-lifecycle **operational executions**: embed, release, materialize, verify-build, install-hooks | host-lifecycle |
| `.host-lint-receipts` | host-lint executions (if ever needed beyond the re-derivable model) | host-lint |
| `.host-prove-receipts` | **cut until host-prove emits receipts** (no file for an absent consumer) | none |

Uniform rule: `.host-<tool>-receipts` = the items that tool executed; `.host-receipts` (tool-less) =
the project's methodology-version trail. Boundary: adopt/upgrade are methodology-version events
(`.host-receipts`); embed/release/etc. are operational (`.host-lifecycle-receipts`). **Why deferred:**
the shipped gate binary reads the applied-set only from `.host` (`applied_ids`) and the receipt gate
reads a single `.host-receipts`; moving/splitting them silently un-applies every recorded upgrade and
HAZARDs the embed/release gate, and CI cold-installs a pinned old-format binary, so it needs a binary
that reads both layouts, then CI repin, then data move, then UPGRADING entry, atomically. This milestone
deliberately reuses the **existing** `.host-receipts` `verify` receipt (D4), depending on none of it.

## Adversarial review + weak-agent data (inputs to the re-scope)

- **Five independent lenses, convergent.** Ontology (the "tool-executed" framing and the
  concern-based split disagree on 6 of 8 phases, so defer/clarify), migration (six blocking breaks in the
  shipped binary from re-homing), mechanism (the hash freeze re-derives the wrong proposition and
  weaponizes against `call/0017`/`call/0019`), weak-agent (line-not-span output, 1,652 trope-lines,
  unlocatable structural tropes), simplicity (STRAND 3 is a re-architecture smuggled beside a small
  feature; lean on the shipped fence + ignore). Recorded in `design-review.md`.
- **Qwen-3.5-4B:** 10/10 correct on clear-case GATE/FREEZE/APPEND classification, "no ambiguity",
  necessary but not sufficient: the *clean* is the hard part (now `plan/0031`), and classification at the margin
  needs the machine-readable `STATUS:`/`Status:` of D3, not status-paragraph inference.

## Verification

- **D1:** `host-lint --docs` from the repo root walks every tracked **`.md`** doc, excludes `book/` +
  the software worktrees + `host-template/` + generated `SUMMARY.md` + `.host-lintignore` entries, and
  skips non-markdown (no prose-scanning code); a unit/integration test asserts the walk + ignore honoring.
- **D2 in `plan/0031`:** the fixable-output golden tests (one record per occurrence + column, mechanical
  `fix:`, advisory tiers) are verified in that milestone; `plan/0030`'s D5 clean depends on them.
- **D3:** every `plan/NNNN/README.md` carries an inline `STATUS:`; the disposition table is documented;
  a classification helper (or the documented predicate) maps each doc to Live/Record/Append-only from
  path + `STATUS:`/`Status:` alone.
- **D4:** `lifecycle.manifest` `verify` `recheck` includes `host-lint --docs`; breaking a doc to
  slop re-opens the `verify` receipt as a HAZARD (non-vacuous); `.gitattributes` present; `software
  --check .` green.
- **D5 (on trigger):** `host-lint --docs` clean across Live docs (records boxed, `MEMORY.md`
  excepted); `.host` records `950fbd6`, 0 pending; whole-suite green (reproducible-build cold
  materialize + Site). Per-doc commits.
- New host-lint release re-pinned in `.host-software` with `software --verify-build` green.

## Push order (software-first)

1. **host-lint:** D1 (`--docs` markdown walk); new release; tests + CI green; (D2's output overhaul ships separately in `plan/0031`)
   re-pin in `.host-software`, `--verify-build`.
2. **agentic-host:** D3 (`STATUS:` lines + disposition table), D4 (`lifecycle.manifest` recheck +
   `.gitattributes`); `PLAN.md` row; `design-review.md`; `MEMORY.md` entry (separate commits, audited).
3. **D5** waits for the operator's literal front-door sentence; recorded then (`upgrade --record
   950fbd6`).

Spine note: no `host-template` change, since `950fbd6` (prose lane) and `da000aa` (box clause) are already
authored; 0030 delivers the tool capability they assume and applies them. If the re-derivable `STATUS:`
classification proves worth generalizing for every adopter, propose it as a follow-up spine clause.

## Risks / honesty

- The fixable-output work (spans / fixes / advisory tiers) is `plan/0031`; its engine-vs-host-lint fork
  and the span-less-trope handling are settled there. `plan/0030` ships the lane, classification, and gate.
- The triggered clean is a long mechanical campaign (~1,652 lines); the per-doc verifiable-goal cadence
  (D5) is what keeps a weak agent from drifting, not optional.
- Deferring the re-homing means the receipts family stays as plan/0025 shipped it (one `.host-receipts`,
  applied-set in `.host`) until the follow-up migration; that is intentional, not an oversight.
- All host-lint pushes and the GitHub-facing work are covered by the standing software-first
  authorization; any unpushable commit stops the line and is reported.
