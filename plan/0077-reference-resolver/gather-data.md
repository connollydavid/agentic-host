# gather-data: the naming probe and the settled conditionals (2026-07-23)

This records the #gather-data node. Two names were settled by the real weak agent, the rest by measurement of this tree and by the doctrine already in force.

## Channel

The gateway's OpenAI-compatible surface at the model card's thinking parameters, identical to the matrices recorded in [plan/0076](../0076-dream-store-model/gather-data.md) and [plan/0074](../0074-host-lifecycle-materialize-receipt-and-envhash/fen-acceptance.md). Each question ran twice with the option order rotated, so a first-position artefact is detectable. Probes and transcripts: `~/agentic-host-work/reference-resolver/` on the operator's machine.

## Decision 1: the verb that resolves one reference

Given the sibling subcommands and a description of a command that turns `plan/0074`, `call/0045` or `plan/0074#write-spec` into a path, a markdown link or a GitHub URL:

| Candidate | order 1 | order 2 |
|---|---|---|
| **resolve** | **A, chosen** | **D, chosen** |
| link | B | C |
| ref | C | B |
| locate | D | A |

Chosen in both rotations from opposite ends of the list. **Settled: `host-lifecycle resolve <ref>`.**

## Decision 2: how the sweep is invoked

Given the sibling checks and a description of a sweep that reports references the published site cannot render:

| Candidate | order 1 | order 2 |
|---|---|---|
| **`refs --check <dir>`** | **A, chosen** | **D, chosen** |
| `resolve --check <dir>` | B | C |
| `validate --refs <dir>` | C | B |
| `prose --refs <dir>` | D | A |

Rotation-proof again, and the pair reads coherently: `resolve` acts on one reference, `refs --check` sweeps a tree. **Settled: `host-lifecycle refs --check <dir>`.** The sweep is its own mode rather than a flag on `validate` or `prose`, which matches the ruling that made the completeness gate a separate verify mode: one command, one question.

## The measured wall

Counted over this repository's authored markdown, outside fenced code:

| Class | Count | Where |
|---|---|---|
| Bare `#N` issue references | 374 in 31 files | 187 in `MEMORY.md`, 35 in `plan/0072/signals-digest.md`, 18 in `PLAN.md`, the rest spread across milestone READMEs |
| Distinct `plan/NNNN` and `call/NNNN` references | 122 | every one resolves by hand; none resolves by tool |
| Unresolvable register references | 0 | this tree has no dead register pointer today |

Two facts follow. The register half has no wall here at all, so its check can gate from day one. The issue-number half has a wall of 374, of which 222 sit in files that are never rewritten.

## The settled conditionals

### The exit split

`0` clean, `3` advisory-only, `1` when any register reference resolves to nothing, `2` on a usage or IO error. This is the dream audit's split (call/0045) applied to a second surface, and the reasoning carries: a `plan/0099` that points at nothing is a dead pointer, mechanically evidenced and worth gating; a bare `#N` is legibility debt, real but not a defect in the record, and a wall of 374 that turns a tree red on the day it lands teaches an adopter to bypass the gate.

### The record-layer exclusion

`.host-lintignore`, the list the prose gate already honours, which in this repository already names `MEMORY.md` and the dated review artifacts. One exclusion list, not two: an operator who has decided that a file is a record should not have to say so once per checker. This is the concrete form of the append-only rule, which is why the adversarial node carries a lens for it: a checker that pressures an append-only log into being rewritten has broken the thing it was auditing.

### The emission forms

The path by default (`plan/0074-host-lifecycle-materialize-receipt-and-envhash/README.md`), `--markdown` for the link, `--url` for the full GitHub URL built from the origin remote. An `#anchor` is preserved through all three, so a task node resolves to its heading. A repository with no origin remote can still emit a path and a markdown link, and says plainly that it cannot build a URL.

### The cross-host case

A `plan/` or `call/` reference in a software repository belongs to its governing host and carries no repository name. The resolver reports `unresolved here` and names the room it searched, rather than guessing or passing silently. Teaching a software repository to name its owning host would make such a reference resolvable and is **out of scope**: it is a recipe change with its own spine doctrine, recorded here so it is not mistaken for an oversight.

### What the sweep reads

Authored markdown, by the same walk the prose gate uses, minus the exclusion list. Fenced code is skipped, because a fenced `#3` is an example rather than a reference — the same rule the tell gate applies to its own fixtures.
