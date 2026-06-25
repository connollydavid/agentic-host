# plan/0040: front-door from spine

Generate the front-door `host` repo from the spine, so its restated facts cannot
drift. Named as a follow-on in plan/0039 (the front-door principle: one spine,
everything else a copy-at-version of it or a pointer, never a restatement), now
picked up.

## Problem

The front-door repo (`github.com/connollydavid/host`) is a single `README.md`,
"the process": the adopt, migrate, and upgrade procedure an agent or a patient
human follows to bring a repo under the methodology. About sixty percent of it is
the unique procedure (the case a/b/c and mode preview/shallow/staged/deep
matrices, the step-by-step, the selection rules). The rest **restates the spine**:
the five-rooms table, the `.host` stamp format, the "Wire the tools" ladder and
its pins, the lifecycle-phase list, and the lanes-are-mandatory rule.

Those restatements are hand-authored and gated by nothing against `host-template`,
so every spine move (the nested layout in plan/0029, host-prove in plan/0023,
concept-as-URI in plan/0039) stales them silently. This is the self-blindness the
reconcile arm closes inside a host (plan/0036, plan/0039), but the `host` repo is
its own repo and sits outside any host's verify gate, so reconcile never sees it.

## Decision (operator, this session)

Realize copy-at-version by **generating** the front-door README from the spine:
the spine-derived sections are regenerated from a pinned template revision so they
cannot drift, rather than re-authored as independent prose. Two alternatives were
weighed and declined:

- **Gate only**: keep the README hand-authored and add a drift check. It catches
  drift but leaves the restatements in place, against the stated principle (never
  a restatement).
- **Point by link**: replace each restatement with a link to the spine's
  canonical definition (the concept-as-URI move of plan/0039). It breaks the front
  door's self-containedness, the "point an agent at one file, no checkout"
  requirement that is the whole reason the front door is a single file.

## The design (proposed, for adversarial review)

The adversarial review superseded the fragment mechanism below; see
`design-review.md` and the "Settled" section. This records what was proposed.

The README is assembled from two kinds of section:

- **Spine-derived** sections (the rooms, the stamp format, the ladder and pins,
  the phase list, the lanes rule), whose canonical source is the template at a
  pinned revision.
- **Procedure** sections (the case and mode matrices, the step-by-step, the
  selection rules), the front door's own content.

A host-lifecycle generator named `front-door` (a sibling of `book`) stitches the
pinned spine-derived sections and the procedure sections into the committed
`README.md`. A `front-door --check` regenerates and fails on any drift, the
`book --check` and reproducible-build re-derivation pattern (regenerate from the
pin, diff the committed output). The front-door repo records the seed revision in
a `.host`-style stamp, so the copy-at-version anchor is explicit and a later spine
move regenerates against the new revision.

The spine-derived sections are **audience-adapted** for the adopter-doing-migration
reader, not byte-identical to `CLAUDE.md`. So the template carries a
front-door-audience canonical fragment for each shared section, which the generator
reads at the pinned revision. The coverage discipline from reconcile carries over:
the components and verifiers come from `.host-software`, so a dropped or added tool
flows through without a hand edit.

## Open decisions (settle by review before building)

- **Procedure home.** The procedure sections live canonically in the `host` repo
  today, with the template pointing at them (`MIGRATION.md`). Generation can keep
  that split (template owns the spine-derived fragments, the host repo owns the
  procedure fragments, the generator stitches), or move the whole README source
  into the template. Recommendation: keep the procedure canonical in the host
  repo; the template owns only the spine-derived fragments. This preserves the
  `MIGRATION.md` direction and keeps the procedure with its audience.
- **Section granularity.** Which blocks are spine-derived (regenerated) versus
  procedure (authored). A first cut: regenerate the rooms table, the `.host` stamp
  block, the Wire-the-tools ladder and pins, the lifecycle-phase list, and the
  lanes-mandatory paragraph; author the rest.
- **Check strictness.** Byte-exact regeneration (the README is fully generated and
  the check fails on any change, like `book --check`) versus block-bounded (only
  the spine-derived blocks are checked for drift, so the procedure prose can be
  hand-edited between regenerations).
- **Scope.** Keep this agentic-host-local maintenance of the one published `host`
  repo, with no adopter obligation and no `UPGRADING` ledger entry, since most
  adopters have no front door (the plan/0038 precedent for meta-repo work). The
  host-lifecycle `front-door` capability is generic tooling, exercised only by
  agentic-host for the published front door.

## Settled (design review)

The two-lens adversarial review (`design-review.md`) found the fragment mechanism
flawed: a hand-authored template fragment is a second source of truth, so
`front-door --check` would prove the README matches the fragment and never that the
fragment matches `CLAUDE.md`. It relocates drift rather than removing it. The four
decisions are settled as:

- **Procedure home.** Keep the split; the host repo owns the procedure (the
  `MIGRATION.md` pointer is live and assigns the procedure there).
- **Section granularity.** Split by structured source, not by spine-derived.
  Coverage-check the phases against `lifecycle.manifest` and the wired tools against
  the `.host-software` `[verification]` drivers plus the lifecycle engine; generate
  the `.host` stamp block from the tool's format. The version pins, the
  lanes-mandatory rule, and the tool descriptions have no structured home and stay
  authored. A structured pin home is a named follow-up.
- **Check strictness.** Byte-exact on the generated stamp block, coverage on the
  structured fact-sets, run on every gate sweep. The procedure prose stays authored,
  so the front door's teaching quality is preserved.
- **Scope.** agentic-host-local, no `UPGRADING` entry. The binding check runs as a
  step in agentic-host's CI (the reproducible-build job), where the spine sources are
  materialized; it is a separate step, not the shared spine recheck, so no adopter
  without a front door runs it. The front-door repo keeps its plan/0038 prose gate and
  cannot run the coverage check itself.

## Build sequence

The build sequence as a task graph (plan/0042). Each entry is an anchored task, the
chain is linear, and each task carries a receipt in `.host-task-receipts`.

### Settle the open decisions by review {#settle-open-decisions}

Settle the open decisions by adversarial review, recorded in a design-review
subdoc with a proceed verdict.

- verify: attested operator

### Add the front-door generator {#add-front-door-generator}

Add the `front-door` and `front-door --check` subcommands to host-lifecycle: phase
coverage against `lifecycle.manifest`, tool coverage against the `.host-software`
`[verification]` drivers plus the lifecycle engine, and byte-exact generation of the
`.host` stamp block. No template fragments (the review rejected them as a second
source). The unit tests pass.

- depends: #settle-open-decisions
- verify: cd software/host-lifecycle/main && cargo test

### Bring the front door in line {#section-and-regenerate}

Add the omitted `release` phase, confirm every wired tool is named, regenerate the
`.host` stamp block, and write the seed stamp, so `front-door --check` is clean, the
README reads unchanged in meaning, and `host-lifecycle prose` is clean.

- depends: #add-front-door-generator
- verify: attested operator

### Wire the front-door check {#wire-the-check}

Wire `front-door --check` as a step in the agentic-host CI (the reproducible-build
job), where the spine sources are materialized, so a spine move that stales the front
door is caught (a deliberately staled section fails the check). It is a separate step,
not the shared spine recheck, so no adopter without a front door runs it. The
front-door repo keeps its plan/0038 prose gate; it cannot run the coverage check
itself, since it does not carry the sources. The whole-suite CI is green.

- depends: #section-and-regenerate
- verify: attested operator

### Release and re-pin {#release-and-re-pin}

Release host-lifecycle, re-pin `.host-software`, and record the receipt and a
`call/` decision. The released binary gates green, and `software --check` and
`--verify-build` are clean.

- depends: #wire-the-check
- verify: attested operator

## Risks

- The spine-derived sections are audience-adapted, so the template fragments must
  be written for the migration reader, not transcluded verbatim from `CLAUDE.md`.
  Getting the boundary wrong duplicates prose instead of removing it.
- Generation must preserve the README's teaching quality. It is a document a human
  or a weak agent follows literally, so a mechanically-stitched README that reads
  worse is a regression, not a fix.
- Bootstrap: the generator lives in host-lifecycle, which the methodology
  materializes, so regenerating the front door depends on a built host-lifecycle
  at the pinned revision.

## Status

complete, released as host-lifecycle v0.27.0 (2026-06-25; `302e87f8`, artifact
`0f63d960`). The `front-door` and `front-door --check` subcommands hold the
single-file front door (the `.host-software` member marked `front-door = true`) to
the spine's structured facts: coverage of the lifecycle phases (the manifest) and the
wired tools (the `.host-software` verifier drivers plus the lifecycle engine), and
byte-exact generation of the `.host` stamp block. A two-lens adversarial review
(design-review.md) rejected the original template-fragment mechanism as a second
source of truth, so the design was re-scoped to generate only from structured data;
the version pins, the lanes rule, and the tool prose have no structured home and stay
authored, with a structured pin home as a named follow-up. The check found and the
milestone fixed a live drift (the front door had dropped the `release` phase). The
binding check runs as a step in agentic-host's CI (the reproducible-build job); the
front-door repo keeps its plan/0038 prose gate and cannot run the coverage check
itself. `call/0026` records the decision; the build sequence is dogfooded as an
anchored receipted task graph (each of the five tasks carries a `.host-task-receipts`
receipt). Whole-suite CI green.
