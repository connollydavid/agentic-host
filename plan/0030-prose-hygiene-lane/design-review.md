# plan/0030 — adversarial design review

Five independent lenses reviewed the original three-strand sketch (a `--prose --all` walk; a hash-pinned
`.host-lint-receipts` ack with "edit lapses the ack → clean to zero"; a five-file receipts-family
re-homing that moved the applied-set out of `.host` and split `.host-receipts`). Each lens was grounded
in the actual repo. The findings converged, and on a single root: the sketch claimed a tool-owner
partition rule but enforced a concern-based one, and bolted a self-asserted exclusion onto a project
whose receipts are re-derived. Verdict: **re-scope** — ship the walk + a sound exclusion; defer the
re-homing. Two operator decisions followed (see end).

## Lens 1 — ontology & boundary stability

- **The "tool-executed" rule does not produce the proposed split.** `lifecycle.manifest` declares every
  one of the 8 phases as a `host-lifecycle` command, so by the tool-owner rule all receipts are
  host-lifecycle's; the methodology-version-vs-operational line is a *second*, disagreeing axis.
  Severity: high. *Resolution:* the split is real but is concern-keyed, not owner-keyed — stated as such
  in the deferred-milestone ontology; the prose work does not depend on it.
- **`remap`/`publish`/`classify`/`verify` are unassigned** by the two enumerated buckets, yet live in
  the current `.host-receipts`. *Resolution:* enumerate all 8 phases in the re-homing milestone.
- **A spine-bumping release writes two files with no transaction.** *Resolution:* deferred-milestone
  concern; out of scope here.
- **Collapse option:** an owner-keyed 3-file family (`.host` + `.host-lifecycle-receipts` +
  per-other-tool) keeps "one fact, one file, one owner" without a tool-less exception. Carried into the
  re-homing milestone as the alternative to weigh.

## Lens 2 — migration safety (the decisive lens for deferral)

All grounded in the shipped binary at the pinned rev CI cold-installs:

- **BLOCKER — moving the applied-set out of `.host` silently un-applies every recorded upgrade.**
  `software --check` reads the applied-set only from `.host` (`applied_ids` / `upgrade_claim_problems`);
  relocating it returns the empty set → all four applied entries become `pending`, and a later
  `upgrade --record` re-runs and re-appends them.
- **BLOCKER — splitting `.host-receipts` HAZARDs the `embed` and `release` gate.** `receipt_gate_problems`
  reads a single `.host-receipts`; any manifest phase with no stanza there → "no receipt" → HAZARD.
- **BLOCKER — `--record` writers still target the old files;** the new files would never be written.
- **BLOCKER — version skew.** Hooks and both CI workflows install `host-lifecycle` at a pinned rev that
  parses the old format; the triggered data move would meet an old-format binary in CI and every
  contributor's pre-commit.
- **Required ordering:** a dual-format binary (reads both layouts) → bump CI `--rev` pins + reinstall
  hooks → move data → UPGRADING entry with a `verify =` → re-record. The format change and the reader
  must ship in one version; the data move trails the binary, never leads it.

*Resolution:* this is a self-contained migration → **deferred to its own milestone.**

## Lens 3 — freeze/hash mechanism (the decisive lens for the mechanism choice)

- **BLOCKER — the freeze re-derives the wrong proposition.** `.host-receipts`' founding rule
  (`call/0017`) is "evidence re-derived, never self-asserted": every receipt carries a `recheck =` the
  gate runs. A `(path, hash, reason)` ack re-derives only "bytes unchanged"; the load-bearing claim
  (the GATE/FREEZE classification + reason) is human-asserted and unchecked. A weak agent greens the
  gate by freezing a trope-laden doc with a plausible reason.
- **BLOCKER — "edit lapses → clean to zero" weaponizes the tool against the records it protects.** The
  spine sanctions edits to immutable records (a MADR link fix, a `Status: accepted → superseded` flip,
  the §6 archive-first MEMORY rename, MEMORY corrections). Each lapses the ack → re-gates → *demands
  prose-rewriting the immutable record* — destroying the epistemic trail, against `CLAUDE.md` §6.
- **MAJOR — non-determinism.** Hashing working-tree bytes on this Windows/WSL/Linux-CI repo (no
  `.gitattributes`) flips on CRLF/trailing-newline → green local, red CI.
- **MAJOR — reintroduces the `call/0009` error `call/0019` superseded.** A whole-file hash exclusion is
  the blanket-exclude pattern dressed up; it mutes *future* real tropes until the hash lapses. The
  shipped, line-precise answer already exists: the `host-lint:ignore` fence (which the prose scanner
  already skips) boxes the quoted span; the rest of the file stays linted.

*Resolution:* **drop the hash ack.** Classify by a re-derivable predicate; exclude via the existing
fence + `.host-lintignore`.

## Lens 4 — weak-agent executability

- **BLOCKER — `--prose` flags a line, not a span or a fix;** one em-dash emits ten byte-identical
  records (no column) → a weak agent cannot count, locate, or know when it is done.
- **BLOCKER — some tropes have no fixable span** ("21/23 bullets open with bold lead-ins" is a
  whole-doc diagnosis). A zero bar over them is an unterminating loop.
- **MAJOR — GATE-vs-record needs PLAN.md status prose** for the 21 of 29 milestones with no inline
  `STATUS:`; a 4B parsing "spine shipped; dogfood deferred" is unreliable.
- **MAJOR — cleaning governance docs risks introducing naming tells (exit 1) or substance changes;**
  no STOP rule. **MAJOR — volume:** 1,652 trope-lines; no per-doc verify cadence → drift.
- **MAJOR — receipt generation must be tool-computed,** not hand-hashed.

*Resolution:* D2 (spans + fix hints + advisory-scoping of structural tropes), D3 (machine-readable
`STATUS:`/`Status:`), and D5's per-doc verifiable-goal cadence + STOP rule.

## Lens 5 — simplicity / scope / overfit

- **Split the milestone:** STRAND 1 is a ~15-line change, STRAND 3 a re-architecture of shipped files.
- **STRAND 2 does not need the re-homing;** a prose exclusion can exist with zero edits to the receipts
  family. **`.host-lint-receipts` is over-built** — the shipped `.host-lintignore` (whole-file) + the
  `host-lint:ignore` fence (line-precise, prose already skips fences) cover the real need.
- **CUT `.host-prove-receipts`** — a file for an absent consumer is YAGNI, and the per-host-tool file
  names bake this repo's tools into the generic spine (the `plan/0029` guardrail).

*Resolution:* adopted wholesale — ship D1 + a fence-based exclusion; cut the ack file and
`.host-prove-receipts`; defer the re-homing.

## Operator decisions

1. **Ack mechanism:** re-derivable classification (path + `STATUS:`/MADR `Status:`) + the existing
   `host-lint:ignore` fence and `.host-lintignore`. No hash ack file.
2. **Receipts re-homing:** deferred to its own dual-format `host-lifecycle` migration milestone. The
   settled ontology is recorded in the plan README's *Deferred* section; `.host-prove-receipts` cut
   until host-prove emits receipts.
