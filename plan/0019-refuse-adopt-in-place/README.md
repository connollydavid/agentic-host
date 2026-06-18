# Refuse to adopt a software repository in place

## Why

A host is a *separate* meta-repo: it holds the thought (rooms, plans, decisions)
and embeds the software it governs as the *Where* room — a bare store with
worktrees recorded in `.host-software`. Running adoption *inside* a software
codebase conflates the two: the code repo becomes the host, and the separation
the methodology rests on is gone. Nothing in `classify`/`adopt` stopped this, so
an agent pointed at a software repo on first adoption would happily scaffold rooms
on top of it.

## What ships (host-lifecycle v0.12.0)

`host-lifecycle classify <dir>` gains a first-adoption guard. When the target
carries a root-level build manifest (`Cargo.toml`, `package.json`, `go.mod`,
`pyproject.toml`, `pom.xml`, …) and has **no** `.host` stamp and **no**
`.host-software` recipe — i.e. it is software, not an empty folder and not an
existing host — `classify` **refuses**: it prints why and the exact steps to embed
the software into a separate host, and exits non-zero instead of a case letter.

- `software_manifest()` — the first root manifest present.
- `adopt_in_place_refusal()` — `None` unless software is present without a stamp or
  `.host-software` recipe.
- `refuse_adopt_in_place()` — the refusal text with the embed-into-a-host steps.

## Spine

Refusing is now a **MUST** (host-template `CLAUDE.md` "Never adopt a software
repository in place"; UPGRADING `ae1e688`). The refusal is not the end of the
task — embed the software the right way instead.

## Verification

- Unit test `refuse_adopting_software_in_place`: empty dir → proceed; `Cargo.toml`
  → refuse (names the manifest); `.host` stamp or `.host-software` → proceed.
- CLI smoke: empty → `a`; software dir → refusal + exit 3; host root → `c`.
- `host-lifecycle classify .` on this host prints `c` (no false refusal); 38 tests
  + clippy green; `software --check .` clean.
