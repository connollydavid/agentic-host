# Host methodology + tooling: gaps surfaced by a large case-b adoption (yarn-agentic)

We adopted the `host` methodology into `yarn-agentic`, a mature inference-engine project (131 milestones, 9 decisions, 4 personas, 18 spec-bearing milestones, two embedded forks), as five reviewed PRs merged to `main`. Verification is green: `host-lifecycle validate plan/call` = ok, `software --check` = both forks at pin with no HAZARD, the spec-TLA gate is green, and the book is published to GitHub Pages. A full candid case study (including our own missteps) accompanies this report.

This report files only defects/gaps we attribute to the **host methodology or its tools** — not to our environment or to external tools (allium/specula). The five headline findings (S1–S5) are doc-site/publishing gaps in room and spec rendering: S1 = no canonical publisher (the umbrella), S2 = the Where room absent, S3 = specs unrendered, S4 = non-lifecycle section order, S5 = no stub-coverage guarantee. `host-template` at the `.host` revision we adopted (`1fa9895`) ships no publishing tooling (verified via the GitHub tree API: `CLAUDE.md STRUCTURE.md MIGRATION.md UPGRADING.md README.md LICENSE call/ cast/ plan/ tools/ link-skills.sh` — no `book.toml`, no `SUMMARY.md`, no `scripts/`, no generator), so each adopter hand-rolls a publisher; our `scripts/gen-book.py` is one such instance and exhibits all five directly. **S1, S2, S4, and S5 also reproduce on the maintainer's own published site** (`connollydavid.github.io/agentic-host`), verified live: its nav lists Cast as the 10th of 11 top-level sections (second-to-last) and Calls last, with no Software/Where section. These are shared methodology gaps, not just our generator's. S3 (specs unrendered) is mechanism-specific to our generator — `agentic-host`'s only spec dir holds a `.gitkeep`, so it cannot exhibit it.

Suggested labels: `bug` for the render/publishing defects, `enhancement` for the reference-generator and tooling proposals, `documentation` where a doc fix suffices.

---

## S1. Methodology defines five rooms + spec formats but ships no canonical way to PUBLISH them

- **Severity:** major
- **Component:** methodology / doc-site-generator (host-template)

**Expected.** A methodology that mandates five rooms and two spec formats should ship or specify a reference publishing path that covers ALL rooms in lifecycle order, with at-least-a-stub coverage per room and a defined way to render specs — handling the `call/0005` constraint (mdBook `src` cannot escape `src=`; `src="."` walks the un-materialized worktrees) once, centrally, correctly.

**Actual.** There is no canonical publisher. `host-template` at the revision we adopted (`1fa9895`) ships no `book.toml`, no `SUMMARY.md`, no generator, and its `CLAUDE.md` never mentions mdBook or publishing (verified via the GitHub tree API at `1fa9895`). `host-lifecycle` and `host-lint` carry no publishing code. So every adopter hand-writes a mirror generator. Ours (`scripts/gen-book.py`, 108 lines) demonstrates the predictable failure modes: it omits Where (S2), renders specs as filename bullets with no body or copied source (S3), and orders sections non-lifecycle (S4). S2–S5 are all downstream of this one missing piece.

**Evidence / repro.**
```
ls tools/host-lifecycle/src        # main.rs only
grep -rniE 'book|publish|render|mdbook|gh-pages|SUMMARY' tools/host-lifecycle/src tools/host-lint/src
# -> no hits (no publisher in host code)
# host-lifecycle subcommands: adopt/validate/next/remap/software/upgrade — no book/publish/render
```
On `host-template` at `1fa9895` (verified via the GitHub tree API): `CLAUDE.md STRUCTURE.md MIGRATION.md UPGRADING.md README.md LICENSE call/ cast/ plan/ tools/ link-skills.sh .gitignore .gitmodules` — no `book.toml`, no `SUMMARY.md`, no `scripts/`, no generator. `call/0005` establishes the hard `src` constraint but offers no publishing remedy.

**Proposed fix.** Ship a reference book generator in `host-template` (e.g. a `host-lifecycle book` subcommand or a documented reference `gen-book`) that: (1) emits sections in lifecycle order Who→What/When→Where→Why→How; (2) renders specs (fenced code or copied+linked raw files); (3) emits a Where stub from `.host-software` (component, url, pin, materialize command) and a How stub from `CLAUDE.md`; (4) asserts at-least-a-stub per room and fails the build otherwise; (5) encapsulates the `call/0005` `src`-scoping rule so adopters do not re-derive it (and re-derive it wrong). This converts S2–S5 from per-adopter footguns into one maintained, tested artifact.

---

## S2. The Software / Where room is entirely absent from the published book — no section, no stub

- **Severity:** major
- **Component:** doc-site-generator / methodology

**Expected.** Every room should have at least a stub page. The Where room — the hosted forks, the action the whole project exists to produce — should have a navigable presence: a stub describing the room, the recorded pins from `.host-software`, and the materialize command. `call/0005` explains *why* the worktrees themselves cannot be walked by mdBook, which argues for a stub, not for omission. A stub reads only committed files, so it is safe in an un-materialized CI checkout (`call/0005`-compliant).

**Actual.** No Software/Where section and no stub exists in our published book. This reproduces on `agentic-host`'s own site (verified live): its sidebar has no Software/Where section, even though `call/0010`/`call/0011` describe the bare-store model — a shared methodology gap, not just our generator. In our repo the only Where-adjacent presence is `call/0004` (the *decision* describing the model) and a non-linked prose mention on `home.md`.

**Evidence / repro.**
```
grep -niE 'software|where|host-software|materializ|worktree' scripts/gen-book.py
# -> only docstring/comment lines (7,8,14); no executable Where handling
grep -nE '^# ' docs/SUMMARY.md
# -> # Summary / # Plan / # Call — decisions / # Cast — personas / # Reference / # Memory  (NO Software/Where)
find docs -iname '*software*' -o -iname '*where*'
# -> only docs/call/0004-...md (the WHY decision, not a Where room)
cat .host-software   # carries the stub data: ik_llama.cpp @ b217881, llama.cpp @ d238d79, urls, materialize recipe
```

**Proposed fix.** The reference generator should emit a Where stub parsed from `.host-software`: per-component name, url, pin, worktree set, the `host-lifecycle software --materialize .` command, and a pointer to `call/0004`/`call/0005`. It reads only the committed recipe file, so the `call/0005` walk-the-worktrees hazard does not apply.

---

## S3. The What detail (specs) renders as filename bullets only — the contract content is never published

- **Severity:** major
- **Component:** doc-site-generator / methodology

**Expected.** The What room (behaviour `.allium` + timing `.tla`/`.cfg` contracts) should be visible in the published record — at minimum each spec linked to a raw copy, ideally embedded as a fenced code block (mdBook renders `.allium`/`.tla` fine as preformatted text even though it cannot syntax-render them natively).

**Actual.** The milestone DOES link to a per-spec index page: `mirror_plan` appends `  - [specs](plan/<slug>/spec-index.md)` to `SUMMARY.md` (live at `docs/SUMMARY.md:78` for milestone 0066), so a "specs" entry is navigable from the milestone. What is genuinely absent is the spec **body/content**: that `spec-index.md` page lists each spec as a bare backtick-quoted **filename bullet** — no markdown link, no embedded body — and the spec source is never copied under `docs/`, so even a raw-link target does not exist. The What contract content is invisible on the published site. (This is mechanism-specific to a generator that discovers specs but renders only their names; `agentic-host` cannot exhibit it because its only spec dir holds just a `.gitkeep`.)

**Evidence / repro.**
```
python3 scripts/gen-book.py
grep -n '0066' docs/SUMMARY.md
#  77:- [0066 tree mtp foundation](plan/0066-tree-mtp-foundation/README.md)
#  78:  - [specs](plan/0066-tree-mtp-foundation/spec-index.md)   <- the index page IS linked
cat docs/plan/0066-tree-mtp-foundation/spec-index.md
# ->  - `per_step_ssm_ancestor.allium`
#     - `tree_mtp_decode.allium`      (bare backtick bullets — no link, no body)
grep -c '](' docs/plan/0066-tree-mtp-foundation/spec-index.md     # -> 0  (no links INSIDE the index page)
find docs -name '*.allium' -o -name '*.tla' -o -name '*.cfg'      # -> EMPTY  (no spec body copied under docs/)
find plan -path '*/spec/*.allium' | wc -l   # 46   (.tla 55, .cfg 52) — all bodies unrendered across 18 milestones
```
Source: `scripts/gen-book.py:64-72` discovers specs by suffix, emits the index page at line 70 with `f"- \`{s.relative_to(...).as_posix()}\`"` (a backtick code-span, not a markdown link or fence), and links *that index page* into SUMMARY at line 72. So the room has a reachable index page, but the index renders names only.

**Proposed fix.** The reference generator should, for each spec, copy it under `docs/` and either (a) wrap its contents in a fenced code block on a per-spec page and link that page from the index, or (b) emit a real markdown link from the index to the raw copy. At minimum, link — do not bullet a bare filename. The methodology should specify how the What room body gets published, since mdBook cannot render `.allium`/`.tla` natively.

---

## S4. Published sidebar order is arbitrary (Plan→Call→Cast→Reference→Memory), not the five-rooms lifecycle order

- **Severity:** minor
- **Component:** doc-site-generator / methodology

*(Tiered below S2/S3 deliberately: a mis-ordered but visible room is less severe than a room with no rendered body or page.)*

**Expected.** Section order should follow the lifecycle the methodology is keyed to (Who→What→When→Where→Why→How): **Cast (Who, the start)** first, then Plan + specs (What/When), then a Software/Where section, then Call (Why), then Reference/CLAUDE (How), then Memory.

**Actual.** Cast (Who) is buried THIRD, after Call (Why). The order is the source-code call order, not the lifecycle. `agentic-host`'s own site shows the same non-lifecycle order (verified live): Plan, then the loose root chapters, then Cast as the 10th of 11 top-level sections (second-to-last), then Calls last — a shared methodology gap reproduced independently of our generator.

**Evidence / repro.**
```
grep -n '^# ' docs/SUMMARY.md
# -> 5:# Plan / 158:# Call — decisions / 170:# Cast — personas / 177:# Reference / 192:# Memory
```
Source: `scripts/gen-book.py` `main()` (lines 98–102) hardcodes `mirror_plan` → `mirror_flat("call")` → `mirror_flat("cast")` → `reference_block` → Memory — the call mirror before the cast mirror, nothing derived from the lifecycle. Lifecycle baseline: `STRUCTURE.md:9-14` / `CLAUDE.md:30-35` (Who=cast first). No host/template doc specifies a canonical section order (`grep -ri 'section order|sidebar|nav order' CLAUDE.md call/` → none), so each adopter re-derives it and gets it wrong.

**Proposed fix.** Order sections by lifecycle in the reference generator: cast (Who) → plan+specs (What/When) → software/where stub (Where) → call (Why) → reference/CLAUDE (How) → memory. If publishing stays adopter-authored, document the canonical room order in the methodology so each hand-written generator agrees.

---

## S5. No stub-coverage guarantee — a reader of the public record cannot see two of the five rooms

- **Severity:** major
- **Component:** methodology

**Expected.** Maintainer principle: every room/aspect should have AT LEAST a stub page in the published book, with a check (or generator contract) that fails when a room has no rendered page (or only a content-free index).

**Actual.** Nothing enforces room coverage. What-detail (specs) renders only filenames with no body or link (S3); Where (software) has no page at all (S2). Two of five rooms are effectively absent from the public record, yet the build is green — demonstrating no coverage gate exists anywhere in the methodology. Because each adopter hand-writes their own generator, there is no shared guarantee to inherit.

**Evidence / repro.**
```
python3 scripts/gen-book.py            # build green at merge c296d0d despite missing room content
grep -nE '^# ' docs/SUMMARY.md         # no Software/Where; specs are filename-only index pages
.github/workflows/pages.yml:25-31      # runs gen-book + mdbook build, no coverage assertion
```

**Proposed fix.** Define a stub-coverage contract: the published book MUST contain at least one rendered page *with content* per room (cast / plan+specs / software / call / reference+CLAUDE). Express it as a post-build check (a `host-lifecycle` subcommand or a CI assertion against `SUMMARY.md` and the rendered pages) so a generator that omits a room — or ships a content-free index — fails the build instead of shipping a half-room site.

---

## 6. `host-lifecycle`: `.host-software` captures one pin per component, so a parallel worktree (branch+pin) is not reproducible by `software --materialize`

- **Severity:** minor
- **Component:** host-lifecycle

**Expected.** `software --materialize` on a fresh clone should reproduce every worktree the project depends on, including a parallel dev/release line at its own branch and pin.

**Actual.** `.host-software` records exactly one `pin` per `[software "name"]` stanza and derives a parallel worktree's branch from its dir suffix. A fresh materialize would mis-create our `ik_llama.cpp.256k` on a new branch `256k` at the canonical pin `b217881`, not `perf/256k-single-context @ a0506f2` (the only commit carrying the 256k change) — a silent wrong tree. We therefore dropped the parallel line from the recipe and hand-manage it.

**Evidence / repro.** In `tools/host-lifecycle` at pin `8fb0183`: `struct Software` (src/main.rs:608-613) has a single `pin` and `worktrees: Vec<String>` of dir names only. `software_materialize` line 752 `let branch = wt.strip_prefix(&format!("{}.", s.name))` derives the branch from the dir suffix; line 757 `git worktree add -b {branch} {path} {s.pin}` creates it at the single component pin. Ground truth: `git -C ik_llama.cpp.256k rev-parse --abbrev-ref HEAD` = `perf/256k-single-context`, HEAD = `a0506f2`; canonical HEAD = `b217881`. The gap is documented verbatim in our `.host-software` NOTES block and self-flagged "a host-lifecycle feature to add upstream."

**Proposed fix.** Add optional per-worktree branch+pin fields to the `[software]` stanza (e.g. a repeatable `worktree = <dir> <branch> <pin>`) so `--materialize` can faithfully recreate parallel lines and `--check` audits each at its own pin.

---

## 7. `host-lifecycle remap` does not scan `.allium`/`.tla`/`.cfg`, so spec-internal cross-references survive a migration stale

- **Severity:** minor
- **Component:** host-lifecycle

**Expected.** A migration that renames/renumbers milestones (`remap --apply`) should rewrite cross-references wherever they occur, including inside the spec files a milestone owns — or at least report the spec files it could not rewrite.

**Actual.** `remap` gates each file on `host_lint::is_scannable(ext)`, and that allowlist does not include `allium`/`tla`/`cfg`, so spec files are skipped entirely in both `--apply` and `--check`, with no warning that they were skipped. Spec-internal references to the old layout dangle silently after a migration.

**Evidence / repro.**
```
grep -n is_scannable tools/host-lifecycle/src/main.rs   # line 485, inside is_target() (fn ~475); used by remap_check (501) + remap_apply (547)
sed -n '378,380p' tools/host-lint/src/lib.rs            # is_scannable allowlist: md|txt|rst|py|rs|... — no allium/tla/cfg
find plan -path '*/spec/*' \( -name '*.allium' -o -name '*.tla' -o -name '*.cfg' \) | wc -l   # 153 files remap skips
grep -rl 'PHASE_\|phase-[0-9]' plan --include='*.allium' --include='*.tla' --include='*.cfg' | wc -l   # 30 spec files with stale phase refs
# e.g. plan/0011-nstream-kv/spec/kv-cache/n_stream_layer.allium:17 cites the retired PHASE_NSTREAM_KV
```
Self-documented in `call/0007` Consequences ("Spec-internal references … are not host-lint-scannable and were likewise untouched").

**Proposed fix.** Either extend `is_scannable` to cover spec extensions for the remap path (paths inside specs are plain strings), give remap a dedicated text-rewrite pass over spec files, or — at minimum — have `remap --check` warn that N spec files were skipped so adopters fix them by hand.

---

## 8. `host-lifecycle adopt` writes `.host` + scaffolds rooms but does not wire the tool submodules; no hint the step remains

- **Severity:** minor
- **Component:** host-lifecycle

**Expected.** After `adopt`, an adopter should either have the verification tools wired or be told the exact submodule-add + pin commands (and the hook-install step) so wiring is not undocumented manual work.

**Actual.** `adopt` only creates `cast/ plan/ call/` and writes `.host`. We wired all four `tools/` submodules (host-lint, host-lifecycle, allium, specula) and installed the host-lint hooks entirely by hand. An adopter who runs only `adopt` has no verification tools and no prompt that more is needed.

**Evidence / repro.**
```
host-lifecycle adopt $(mktemp -d) 1fa9895 --dry-run
# -> create cast/ (dry-run) / create plan/ (dry-run) / create call/ (dry-run) / write .host (dry-run)
#    no submodule/hook/checklist line
grep -n 'const ROOMS' tools/host-lifecycle/src/main.rs   # const ROOMS: [&str;3] = ["cast","plan","call"]
# adopt() at src/main.rs:109-155 touches only ROOMS + .host; README.md:20 scopes adopt to "scaffold cast/ plan/ call/ + write the stamp"
```

**Proposed fix.** `adopt` should print a copy-pasteable post-adopt checklist (the four `git submodule add <url>` + pin commands for the stamped revision, plus the hook-install command), or offer a `--wire-tools` flag.

---

## 9. `host-lifecycle`: released tag (`v0.5.0`) resolves to the annotated-tag object, not the commit — a pinning footgun

- **Severity:** nit
- **Component:** host-lifecycle / documentation

**Expected.** Documentation should tell adopters how to pin the host tools so they record the **commit** SHA, not the annotated-tag object SHA (which is invalid as a submodule gitlink).

**Actual.** `git ls-remote <repo> v0.5.0` returns the annotated-tag object (`d9d662c`), not the commit (`8fb0183`). Scripting that bare ls-remote SHA into a gitlink records the tag object, which is silently wrong; the correct dereference (`v0.5.0^{}`) is undocumented.

**Evidence / repro.** In `tools/host-lifecycle` (at v0.5.0):
```
git ls-remote . v0.5.0        # -> d9d662c... ; git cat-file -t v0.5.0 -> tag
git ls-remote . 'v0.5.0^{}'   # -> 8fb0183... (commit, == our recorded pin and HEAD)
```
The README and source document no dereference recipe.

**Proposed fix.** Document the pinning recipe (`git ls-remote <repo> 'v0.5.0^{}'` or `git rev-list -n1 v0.5.0`), or have `host-lifecycle` print the canonical commit SHA to pin for each released tool version.

---

*Reference-doc count note: the published book renders **12 reference pages** — 10 `.md` files in `docs/reference/` plus 2 in `docs/reference/handoffs/` (HANDOFF.md, TRANSFER.md), all 12 listed in `docs/SUMMARY.md:179-190`.*

*Not filed as host defects (recorded in the case study as adopter-friction context only): `host-lint` warn-tier numeral recall bias on version/decimal tokens (working-as-documented per `VOCABULARY.md:186`; advisory exit-3, suppressed via the documented `.host-lint-allow`/`.host-lintignore` mechanism), and our-environment items (Claude Code auto-mode tool-download gating, `allium-cli` rustc-1.96 build break, WSL2 loopback routing, CUDA toolchain churn).*