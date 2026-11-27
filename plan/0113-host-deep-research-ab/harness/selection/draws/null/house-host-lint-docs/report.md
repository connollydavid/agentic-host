# host-lint `--docs`: which release introduced the repo-wide prose lane, and what rules it consults

## Answer

- **Version:** host-lint **0.8.0** (tag `v0.8.0`, published 2026-06-21). It is the first release
  carrying the `--docs` repo-wide prose lane.
- **Rule source:** **`VOCABULARY.md`** — specifically its **§6, "Prose agentic tells (advisory): a
  token-free trope adaptation"** (the token-free adaptation of the tropes.fyi trope catalog, kept in
  `host-grammar`'s `tells` module, which host-lint calls).

## Evidence

### 1. The plan that specifies `--docs` names the shipping release

The milestone that defines the lane labels its first deliverable as shipped in v0.8.0: "### D1:
`--docs`, a repo-wide prose mode over authored docs *(host-lint, shipped v0.8.0)*"
(<https://raw.githubusercontent.com/connollydavid/agentic-host/main/plan/0030-prose-hygiene-lane/README.md>).
The same section explains the lane's scope: "Add a single, logically-named mode, **`host-lint --docs`**,
for the repo-wide prose audit, rather than overloading `--prose --all`"
(<https://raw.githubusercontent.com/connollydavid/agentic-host/main/plan/0030-prose-hygiene-lane/README.md>).
It also records why the lane was needed: the existing "`--prose` branch (`main.rs:453`) short-circuits
before `--all` and never loads `.host-lintignore`, so there is no repo-wide prose audit today"
(<https://raw.githubusercontent.com/connollydavid/agentic-host/main/plan/0030-prose-hygiene-lane/README.md>).

### 2. The 0.8.0 release commit introduces the mode and bumps the version in the same change

The commit subject is "host-lint 0.8.0: --docs repo-wide prose lane, plus located, fix-hinted, tiered
output"
(<https://api.github.com/repos/connollydavid/host-lint/commits/e652ffc3fb517ad1bf185e73a6d4a050d8365c7f>),
and its body states the scope: "D1 (plan/0030): a single --docs mode walks authored markdown only (git
ls-files, honors .host-lintignore, skips code/symlinks), the counterpart to the naming --all."
(<https://api.github.com/repos/connollydavid/host-lint/commits/e652ffc3fb517ad1bf185e73a6d4a050d8365c7f>).
That same commit carries the package version bump (its `Cargo.toml` diff shows `-version = "0.7.0"` /
`+version = "0.8.0"`) and the new lane, whose defining comment reads "// `--docs` is the repo-wide prose
lane — the counterpart to the naming `--all`."
(<https://api.github.com/repos/connollydavid/host-lint/commits/e652ffc3fb517ad1bf185e73a6d4a050d8365c7f>).
The release object for that tag confirms the version and its date: `"tag_name":"v0.8.0","target_commitish":"main","name":"v0.8.0"`
with `"published_at":"2026-06-21T23:45:23Z"`
(<https://api.github.com/repos/connollydavid/host-lint/releases/tags/v0.8.0>).

### 3. What the lane consults: the prose rule set in `VOCABULARY.md` §6

The shipped `--docs` walk restricts to markdown and hands each document to the prose scanner, per the
in-tree comment block above `fn run_docs` in `src/main.rs` at tag `v0.8.0`: "// `--docs` is the
repo-wide prose lane — the counterpart to the naming `--all`. // Scope determines type: naming tells
hide in any file, but prose tropes are a // property of authored narrative, so `--docs` walks `.md` only
and never runs the // prose engine over `.rs`/`.toml`/`.sh`"
(<https://raw.githubusercontent.com/connollydavid/host-lint/v0.8.0/src/main.rs>).

The prose engine's rule set is documented in the repository's own spec: the README's prose paragraph
covers both document modes and points at the section, "The engine lives in `host-grammar` and runs on
titles and drafts (`--stdin`) and on documents (`--prose`, `--docs`) ... See
[VOCABULARY.md](VOCABULARY.md) §6."
(<https://raw.githubusercontent.com/connollydavid/host-lint/main/README.md>), and the README states
up front that the tool "Implements the detection rules from [VOCABULARY.md](VOCABULARY.md)."
(<https://raw.githubusercontent.com/connollydavid/host-lint/main/README.md>).

`VOCABULARY.md` at tag `v0.8.0` is where those prose rules live, under the heading "## 6. Prose agentic
tells (advisory): a token-free trope adaptation"
(<https://raw.githubusercontent.com/connollydavid/host-lint/v0.8.0/VOCABULARY.md>). Its opening
paragraph names the upstream catalog and the module that carries it: "This is a token-free English
adaptation of the trope catalog at tropes.fyi (Ossama) ... It lives in `host-grammar`'s `tells` module and
host-lint calls it."
(<https://raw.githubusercontent.com/connollydavid/host-lint/v0.8.0/VOCABULARY.md>). Section 6 is the
whole rule book for the lane — the lexical phrase table (`ai-diction`, `magic-adverb`, `decoration`,
each cited as "tropes.fyi: ..."), the structural equations (`negative-parallelism`, `tricolon`,
`anaphora`), and the "Composite density" threshold rule
(<https://raw.githubusercontent.com/connollydavid/host-lint/v0.8.0/VOCABULARY.md>).

### 4. Summary of the chain

| Question | Finding | Source |
|---|---|---|
| Which release introduced `--docs`? | host-lint **0.8.0** (tag `v0.8.0`, 2026-06-21) | [plan/0030 D1](https://raw.githubusercontent.com/connollydavid/agentic-host/main/plan/0030-prose-hygiene-lane/README.md), [commit e652ffc](https://api.github.com/repos/connollydavid/host-lint/commits/e652ffc3fb517ad1bf185e73a6d4a050d8365c7f), [release v0.8.0](https://api.github.com/repos/connollydavid/host-lint/releases/tags/v0.8.0) |
| Which rule source does the lane consult? | **`VOCABULARY.md` §6** — "Prose agentic tells (advisory)", the tropes.fyi adaptation served by `host-grammar`'s `tells` module | [VOCABULARY.md @ v0.8.0](https://raw.githubusercontent.com/connollydavid/host-lint/v0.8.0/VOCABULARY.md), [README](https://raw.githubusercontent.com/connollydavid/host-lint/main/README.md), [`src/main.rs` @ v0.8.0](https://raw.githubusercontent.com/connollydavid/host-lint/v0.8.0/src/main.rs) |

## Caveats and precision

- The lane's *documentation* lagged its code: at tag `v0.8.0`, §6 still describes only the surfaces that
  existed then — "The engine runs on titles and drafts (`--stdin`, i.e. commit subjects and gh issue/PR
  titles before filing) and on documents on demand (`--prose`)"
  (<https://raw.githubusercontent.com/connollydavid/host-lint/v0.8.0/VOCABULARY.md>). The `--docs` flag
  is listed alongside `--prose` in the current README
  (<https://raw.githubusercontent.com/connollydavid/host-lint/main/README.md>). The rule source is the
  same section either way.
- Prose findings are advisory, not blocking: "Prose tells are advisory (warn, exit 3), as elsewhere"
  (<https://raw.githubusercontent.com/connollydavid/host-lint/v0.8.0/src/main.rs>), and §6 makes the same
  point — "**Every prose tell is warn-tier (exit 3) — advisory, never blocking**"
  (<https://raw.githubusercontent.com/connollydavid/host-lint/v0.8.0/VOCABULARY.md>).
- A separate mechanism, the repo-root `LEXICON`, masks sanctioned phrases in the prose lanes —
  "the prose lanes (`--prose`, `--docs`), where the phrase is masked before the host-grammar density
  engine as well" (<https://raw.githubusercontent.com/connollydavid/host-lint/main/README.md>) — but it
  is an allowlist, not the rule source the lane consults.

## Method notes (local verification, not citations)

- Cloning `connollydavid/host-lint` and grepping the release trees shows `--docs` in `src/main.rs` at
  `v0.8.0` and not at `v0.7.0`, and `git tag --contains e652ffc` resolves to `v0.8.0` as the earliest
  tag; this corroborates that 0.8.0 is the *first* release with the lane.
- Every quote in this report was checked character-for-character against the fetched page (raw files,
  the commit JSON, and the release JSON) before being copied into `sources.json`.
