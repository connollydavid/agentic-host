# plan/0046: the generated book moves to mdBook/, freeing docs/

`host-lifecycle book` generates a browsable mdBook site from a project's rooms. It writes
the generated mdBook source into a top-level `docs/` folder and clears that folder on every
run. connollydavid/host-lifecycle#3 reported this as a destructive `book` bug. The real
defect is narrower and deeper: `docs/` is a generic name, and a project brought under the
methodology that already keeps hand-written documentation in `docs/` loses it on the first
`book` run. This milestone moves the generated source and built HTML under a tool-named
`mdBook/` folder, which frees `docs/` for authored content and removes the collision at its
root.

## Problem

The generator reserves `docs/` as its output and wipes it each run (`fs::remove_dir_all`).
For a greenfield project adopted from the template that is safe, because `docs/` is gitignored
generated output from the start. For a migration it is a footgun: `classify` and `adopt` never
inspect a pre-existing `docs/`, so a project that keeps a tracked research record or
hand-written guides in `docs/` has them deleted the first time the doc site is generated. The
reporter's suggested fixes (stop defaulting to `docs/`, make the source dir configurable) point
at the generator, but the underlying choice is a location decision: where should generated
output live so it never collides with the one folder name projects most commonly use for
authored docs.

## Decision, settled with data and the cast

The generated mdBook source and built HTML move under one gitignored top-level folder named
`mdBook/`: `mdBook/src/` for the generated source and `mdBook/out/` for the built HTML. The
config `book.toml` stays at the repository root, so mdBook is still invoked exactly as before
(`mdbook build` from the root, no arguments). `docs/` is freed for authored content.

```toml
# book.toml (repo root, gitignored)
[book]
src = "mdBook/src"
[build]
build-dir = "mdBook/out"
```

This holds to mdBook's own conventions. `src` and `build-dir` are first-class config keys that
accept any relative path, and the generator already set a non-default `src = "docs"`, so
re-pointing them is ordinary use of the tool rather than a fight with it. The folder name
`mdBook/` makes it self-evident that the tree is the tool's generated workspace, so a migrating
project never mistakes it for authored content.

### The data (Fen, the real qwen3.5-4b)

The decision was settled against the project's weak-agent persona, driven directly through the
rope API with a true system prompt. A first probe fed the model mdBook's own idiom and it
preferred the standard source-folder name 4 of 5 times. A fair head-to-head that also stated the
ensemble's conventions favoured consolidating everything under one folder. The deciding fact is
that mdBook's `src` is configurable, so the consolidated layout keeps the root-level invocation
while tucking the generated trees under `mdBook/`. The locked layout then passed an acceptance
test: handed the same scenario of a project with hand-written `docs/`, the real model judged
`docs/` safe under the new layout 5 of 5 times, and judged the old `docs/`-as-output layout
dangerous 3 of 3 times. The weak agent perceives the footgun, and perceives it gone.

### The cast

Consulting the five personas confirmed the layout and added four requirements for shipping it.
Mara and Wren are served by a loud generated-versus-authored boundary that even a small model
reads correctly. Fen requires the migration to stay a single tool-driven command rather than a
hand-edit. Bly, the adopter several revisions behind, requires the change to apply as an
independent ledger entry and the cleanup of the old generated trees to fail safe, so a skipped
step re-lists rather than hides. Orin, the maintainer, requires the ledger entry to be
version-gated on the new host-lifecycle and safe when followed literally on old infrastructure.

## The design

### The generator

`write_book` writes the SUMMARY and room pages into `mdBook/src/` instead of `docs/`. `book_toml`
sets `src = "mdBook/src"` and adds `build-dir = "mdBook/out"`. The user-facing strings and the
tests follow the rename. The build still runs from the root.

### The spine and the gitignore

The generated trees are gitignored as one entry. `host-template/.gitignore` and agentic-host's
`.gitignore` carry `/book.toml` and `/mdBook/` in place of `/docs/` and `/book/`. The doctrine in
`host-template/STRUCTURE.md` states that generated output lives under `mdBook/` and that `docs/`
is available for authored content, which retires the earlier reserved-`docs/` reading. `call/0014`
is already superseded by the spine, so this is a spine change propagated through `UPGRADING`, not
a new project decision.

### The adopter ledger

`UPGRADING.md` gains one entry that is independent (it needs no earlier unrelated migration),
declares `requires` the new host-lifecycle version (an adopter on the old binary still writes
`docs/`), and carries a machine-checkable verify. The migration swaps the two gitignore lines and
removes the stale generated `docs/` and `book/` trees. An adopter records it with
`host-lifecycle upgrade --record`, so the step is tool-carried and the stamp is never hand-edited.

## Build sequence

### Decide the layout with data and the cast {#decide-layout}

Settle where generated output lives, against the real qwen3.5-4b (rope, true system prompt) and
the five personas. The acceptance test confirms the weak agent sees `docs/` safe under the new
layout and endangered under the old one.

- verify: attested operator

### Move the book generator to mdBook/ {#book-generator}

Re-point `write_book` and `book_toml` to `mdBook/src` and `mdBook/out`, and follow the rename
through the user-facing strings and the tests. The build runs from the root unchanged.

- depends: #decide-layout
- verify: cd software/host-lifecycle/main && cargo test

### Update the spine and the adopter ledger {#spine-and-ledger}

Update `host-template/STRUCTURE.md` doctrine and `.gitignore`, and add the independent,
version-gated, fail-safe `UPGRADING` entry with a machine-checkable verify.

- depends: #book-generator
- verify: attested operator

### Re-point agentic-host and clean the old trees {#repoint-agentic-host}

Swap agentic-host's `.gitignore` to `/book.toml` and `/mdBook/`, point `mdbook.yml` publishing at
`mdBook/out`, remove the stale generated `docs/` and `book/`, and regenerate the site locally to
confirm it builds.

- depends: #book-generator
- verify: attested operator

### Release, adopt, and verify the whole suite {#release-and-verify}

Release host-lifecycle, re-pin `.host-software`, record the release receipt, bump the CI install
pins, adopt the new spine revision on agentic-host through the ledger, and confirm the whole suite
is green and that the Site workflow serves `mdBook/out`.

- depends: #spine-and-ledger
- depends: #repoint-agentic-host
- verify: attested operator

## Risks

- An adopter that runs the new host-lifecycle without applying the gitignore swap would see the
  old generated `docs/` and `book/` linger as untracked clutter. The ledger entry handles the
  swap and the cleanup, and is version-gated so it pairs with the binary that changes the output.
- A migrating project that already tracks content in `docs/` is now safe by construction, since
  the generator no longer writes there. The classify-time guard discussed under #3 is no longer
  needed, because the reserved name is gone.

## Status

complete, released as host-lifecycle v0.30.2 (`f2b4607`, artifact `3a9e59ce`). `host-lifecycle
book` writes its generated source to `mdBook/src/` and the built HTML to `mdBook/out/`, with
`book.toml` kept at the repo root, so `mdbook build` runs from the root unchanged. `docs/` is freed
for authored content, which closes connollydavid/host-lifecycle#3 at its root: the generator no
longer reserves `docs/`, so the migration footgun cannot recur and the classify-time guard is
unnecessary. The spine carries the doctrine and the gitignore (host-template `e068828`) plus an
independent, version-gated, fail-safe `UPGRADING` entry (`e068828`, requires host-lifecycle
v0.30.2); agentic-host adopted it through the ledger (`upgrade --record e068828`). The decision was
settled against the real qwen3.5-4b, which read `docs/` as out of harm's way under the new layout in
every run and reproduced the footgun on the old layout in every run, and the five cast personas
confirmed it. A regression test pins the generator to `mdBook/src` and proves an authored `docs/`
is left intact. `software --check` is clean and the Site workflow serves `mdBook/out`. The whole
suite is green.
