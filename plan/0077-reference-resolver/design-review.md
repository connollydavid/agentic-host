# plan/0077 design-review: the cast reads the built diff

Date: 2026-07-23. Subject: the reference resolver and sweep, `4f27c7a..06fa455` in host-lifecycle.

This document was written after its receipt, which is itself a finding: the `#cast-consult` receipt named this path in its verify line while the file did not exist, and two chairs found that independently in the next consultation. The record is repaired here rather than quietly; see the closing note.

## Who read it

Mara, Bly, Orin and Wren each read the plan, the built diff and the sources their lens calls for, and each ran the built binary against this host (two rooms), the component worktree (no rooms), and fixtures of their own. Fen's contribution is the weak-agent acceptance in [fen-acceptance.md](fen-acceptance.md), which failed the advisory state across three output revisions.

## The blocking set, and where it came from

**A bare `#N` was resolved against whatever remote happened to be local.** Mara reproduced it: `resolve '#8' --markdown .` in this host emits a link to *agentic-host* issue 8, while the reference it came from (`plan/0024-sound-discharge/README.md`) means host-lifecycle issue 8. Every one of the 182 bare references the sweep counted would have been rewritten to the wrong tracker by the remedy the tool printed. An issue reference now names its repository, `component#N` takes the origin's owner, and a bare number is refused with the form to write instead.

**The clean line was printed after reading zero documents.** Bly ran it against a nonexistent directory and against a directory that is not a git repository: both printed "every reference in the authored docs resolves and renders", exit 0. The verdict now names how many documents were swept and fails closed when the walk finds none.

**The clean line also claimed coverage of references it had skipped.** In a software repository every register reference is skipped by design (the numbers belong to the governing host), and the verdict said nothing about them. It now counts them and says they were not checked.

**A freshly scaffolded project has no exclusion list**, so its append-only log was swept and told to rewrite itself on day one. Mara traced it precisely: `scaffold` writes no `.host-lintignore`, so the record-layer exclusion was conditional on the operator having already authored one. The record layer is now excluded by construction.

**Untracked markdown was invisible.** Wren's finding: an agent that authors a document, runs the sweep, sees clean and commits has verified nothing. The walk now includes untracked-but-not-ignored files.

**The forge-URL constructions were untested, and Bly proved it by mutation** — replacing both with a wrong host left 278 unit and 11 integration tests green. They now have a test that gives its fixture a real remote and asserts the URLs byte for byte.

**The register `--url` emission was untested by the same method**, and `blob/main` was hardcoded, handing a 404 to any repository on another default branch. Both fixed.

**A CSS colour was counted as an issue number**, as was a reference-style link. Fixed for the colour; the reference-style link is carried.

## Carried, not fixed

- **Room names are hardcoded and must sit at the repository root** (Orin). A project that renamed its rooms, or nests them under `docs/`, gets a clean verdict from a tool that read nothing. The fix is either to read the names from `.host` or to say plainly that no room was found; it is carried to the adversarial node, because it is the same class as the sweep's other coverage claims.
- **Non-GitHub forges and GitHub Enterprise** are not recognised: `origin_slug` matches the literal `github.com`, so a self-hosted forge gets an advisory whose remedy cannot run.
- **A fork silently retargets every URL**, because the tool has no notion of an upstream.
- **A milestone directory with no README** is reported as "names no entry in that room", which is false: the directory is the record.
- **Nothing runs the sweep.** No CI lane, no verify recheck, no skill step. The capability ships and nothing surfaces it, which is the finding that most resembles the gap plan/0074 was filed to close.
- **The `unresolved here` message asserts the governing-host explanation even in a repository that owns the room**, so a wrong working directory is diagnosed as a wrong repository.

## The closing note, which is itself a finding

The `#cast-consult` receipt was recorded before this document existed, with a verify line naming it. The receipt's evidence string was accurate about the findings and false about the artifact, and the task gate accepted it because it checks neither. Two chairs found it in the very next consultation, one of them citing it as the same hollow-discharge shape the previous milestone had just learned to name.

The mechanical remedy is small and is recorded as owed: `tasks --record` should refuse a receipt whose verify line names a path that does not exist on disk.
