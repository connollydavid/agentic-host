# plan/0077 reference resolver: a register number resolves, and a bare issue number stops being dead text

Closes [host-lifecycle#17](https://github.com/connollydavid/host-lifecycle/issues/17) and the parked full-URL row in [PLAN.md](../../PLAN.md) (operator, plan/0042 review; sharpened by plan/0049: the reference must sit in a markdown link to the full URL, so it renders in the site). Queue position four of the 2026-07-22 closure ruling, cut 2026-07-23 after plan/0074 shipped.

## Why

The methodology makes a number an identity: a bare number at the plan root names a milestone, a numbered file under `call/` names a decision. Every room, every commit message and every doc then refers to those numbers, and nothing resolves them. In this repository alone, 122 distinct `plan/NNNN` and `call/NNNN` references appear across the authored docs; all 122 resolve by hand and none of them resolve by tool, so in the published site they are text that looks like a link and is not one.

The same gap has a second face. A bare `#N` issue reference is not a safe full URL: it renders as nothing in the site, and read outside GitHub it does not even say which repository it belongs to. This tree carries 374 of them outside code fences, 187 in the append-only `MEMORY.md` and 35 in a dated review artifact, which is the shape of the answer as much as the size of the problem: the record layer is excluded, never rewritten.

The two halves are one capability. Resolving `plan/0074` to a path, a markdown link or a GitHub URL is the same act as turning `#17` into `https://github.com/connollydavid/host-lifecycle/issues/17` inside a link; a checker that reports dead references needs the resolver that would have made them live.

## Scope

1. **The resolver.** A host-lifecycle subcommand that takes a reference and emits the local path, a markdown link, or a GitHub URL derived from the repository's origin remote, with a `#anchor` preserved so a task node resolves to its heading.
2. **The dead-reference check.** A mode that reports references the site cannot render: a bare `#N` outside a link, and a `plan/`, `call/` reference that resolves to nothing. Record-layer paths are excluded by the same discipline the prose gate uses, because an append-only log is never rewritten to satisfy a checker.
3. **The cross-host case.** A `plan/` or `call/` reference in a software repository belongs to its governing host, not to the software repository, and it carries no repository name. An unresolvable reference is reported as unresolved-here rather than resolved wrongly or passed silently.

Out of scope, recorded so it is not assumed: linkifying commit messages in the generated site (the issue names it as a use case; it needs the resolver first and is its own milestone), and rewriting the references this check reports.

## Open questions the gather-data node settles

- The verb: `resolve`, `link`, or `ref`, and whether the emission is flag-selected or positional. Settled by a rotation-proof weak-agent probe, as the `bootstrap` and `--verify-setup` names were.
- The check's home: its own mode, a fold into `validate`, or a fold into the prose sweep that already walks authored markdown.
- Whether the check gates (non-zero) or advises on day one, given a wall of 374 bare references of which perhaps 150 sit in live documents.
- How the record layer is excluded: reuse `.host-lintignore`, or an explicit list.
- Whether a software repository names its owning host, so a cross-repo reference resolves at all.

## Build sequence

### The settled conditionals {#gather-data}
- verify: every open question above has a row in gather-data.md, the naming probe transcript is recorded, and the wall is measured per file
- depends: none

### The reference surface {#write-spec}
- verify: the Allium spec models the reference kinds, the resolution outcomes (resolved, unresolved-here, unresolved-anywhere), the emission forms, and the check verdict; `allium check` and `analyse` exit 0 with zero findings
- depends: #gather-data

### The obligations {#write-obligations}
- verify: every `allium plan` obligation carries a disposition, and each names a test that exercises the rule rather than a helper beside it
- depends: #write-spec

### The resolver {#implement-resolve}
- verify: `cargo test` green; a reference resolves to its path, its markdown link and its GitHub URL, with the anchor preserved and the origin remote read for the URL
- depends: #write-obligations

### The dead-reference check {#implement-check}
- verify: `cargo test` green; a bare issue number outside a link is reported, a resolving register reference is not, an unresolvable one is reported as unresolved, and every record-layer path is excluded
- depends: #implement-resolve

### The test matrix {#write-tests}
- verify: the suite covers each reference kind, each emission form, each resolution outcome, the exclusions and the exit split; mutating the rule under each behavioural obligation fails its named test
- depends: #implement-check

### Cast consultation {#cast-consult}
- verify: each persona's concern is addressed or recorded, in design-review.md
- depends: #write-tests

### Adversarial review {#adversarial-review}
- verify: an independent multi-lens read of the built diff records every blocking finding fixed or carried, with a dedicated lens for the record-layer exclusion (a checker that pressures an append-only log is the failure that matters here)
- depends: #cast-consult

### The weak-agent acceptance {#fen-acceptance}
- verify: the real qwen3.5-4b reads the check's output and names the state-correct next action, and reads a resolved reference as a link rather than as text; rotation-stable, transcript recorded
- depends: #write-tests

### The spine doctrine {#write-spine-doctrine}
- verify: the template manual states the reference discipline (a number resolves, a bare issue number is not a reference) and the ledger entry names the day-one wall and the record-layer exclusion
- depends: #adversarial-review

### Release and re-pin {#release-and-re-pin}
- verify: the release cascades clean, `software --check .` is clean at the new pin, and host-lifecycle#17 closes with its outcome
- depends: #write-spine-doctrine, #fen-acceptance

### This tree's own references {#remediate-this-tree}
- verify: the live documents this check reports are remediated or their exclusion is recorded; `MEMORY.md` is untouched, and PLAN.md's parked row records the outcome
- depends: #release-and-re-pin
