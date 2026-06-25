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

## Build sequence (after the review settles the design)

1. Settle the open decisions by adversarial review. Verify: a recorded
   design-review subdoc with a proceed verdict.
2. Add the `front-door` generator and `--check` to host-lifecycle, with the
   template carrying the front-door section fragments. Verify: unit tests, and a
   regenerate-then-diff that reproduces the committed README.
3. Section the front-door README, regenerate it from the pinned template, and
   write the seed stamp. Verify: `front-door --check` clean; the README reads
   unchanged in meaning; `host-lifecycle prose` clean.
4. Wire `front-door --check` into the `host` repo CI and into the agentic-host
   verify recheck, so a spine move that stales the front door is caught. Verify: a
   deliberately staled section fails the check; whole-suite CI green.
5. Release host-lifecycle, re-pin `.host-software`, record the receipt and a
   `call/` decision. Verify: the released binary gates green; `software --check`
   and `--verify-build` clean.

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

Open, design phase. Operator ruling recorded (generate from the spine). Awaiting
adversarial review of the open decisions before building. Independent of
plan/0041.
