# plan/0077 adversarial-review: four lenses read the built diff

Date: 2026-07-26. Subject: `4f27c7a..7700cf4` in host-lifecycle — the resolver, the sweep, the waiver rename and `migrate-recipe`.

The cast round read `4f27c7a..06fa455` and recorded its blocking set in [design-review.md](design-review.md). Three commits landed after it: the refusal that names a real reference, the rename of the reproducibility waiver, and the tool-carried recipe migration. The last two had no independent read at all before this round.

## Who read it, and how

Four lenses, each independent, each required to reproduce every claim against the built binary before recording it:

- **the record layer**, the lens this milestone's plan names as the one that matters, because a checker that presses an append-only log into being rewritten has broken the thing it audits;
- **coverage honesty**, whether any verdict claims more than the tool read, the class already found and fixed twice here;
- **resolver correctness**, whether an emitted path, link or URL is right or merely plausible;
- **the rename and its migration**, the three unreviewed commits, read against the decisions that authorise them.

Fixtures were built outside both repositories, and no lens held write access to either. Findings the design review already records as fixed were re-attacked rather than re-reported; where a fix holds, that is recorded below under what could not be broken.

## The blocking set

### The verdict claims coverage the run does not have

This is the third instance of the class. The first printed a clean line after reading zero documents; the second claimed coverage of references it had skipped by design. Both are fixed. The shape survived in the walk itself.

**A document the tool cannot read is counted as swept, and a dead pointer inside it ships as exit 0.** `authored_docs` takes `git ls-files` output verbatim, and git quotes any path holding a non-ASCII byte under its default `core.quotepath`, so the quoted name is counted and the read fails. The failure is swallowed by `let Ok(text) = … else { continue }`. Reproduced:

```host-lint:ignore
$ git ls-files '*.md'
README.md
"na\303\257ve.md"                       <- holds a dead plan/0099
plan/0074-x/README.md
$ host-lifecycle refs --check .
-- 3 doc(s) swept; every reference in them resolves and renders
exit=0                                   <- expected exit 1, one dead pointer
```

An unreadable document and one holding invalid UTF-8 take the identical path. Two lenses found this independently. Defect: `src/main.rs:1920`, `src/refs.rs:456` and `:579`.

**The exclusion is never disclosed.** On this host the sweep excludes 19 documents holding 319 bare references, and reports 293. The excluded population is larger than the reported one, and no verdict line mentions that a document was withheld. The clean branch is the sharp case: with a list that excludes everything, a README carrying two dead pointers yields `1 doc(s) swept; every reference in them resolves and renders` at exit 0. Defect: `src/refs.rs:481-513`.

**The unchecked-register disclosure prints on the clean branch alone.** The design review's own fix sits after both early returns, so the advisory and dead verdicts drop it. A software repository, the case the disclosure exists for, almost always carries a bare `#N` and therefore never sees it. The dead verdict drops the swept count as well. Three lenses recorded this. Defect: `src/refs.rs:504-513`.

**A project whose rooms are renamed or nested gets an unqualified clean line.** `ROOMS` is a literal `["plan","call"]`, so a tree using `milestones/` and `decisions/` has its references pass through the grammar unseen: the hedge that would have said the room was not held cannot fire, because nothing was counted to hedge about. Defect: `src/refs.rs:25`, `:172-174`.

### The checker presses the record layer

**Three of five natural `.host-lintignore` spellings are silent no-ops, and the declared record then gates.** A leading `/`, a bare directory name and a leading `./` all fail to match, so an operator who has declared their append-only log excluded is told to rewrite it, at exit 1. An unreadable list degrades to no exclusions at all. A negation is ignored, so `*.md` with `!README.md` withdraws a live authored document from coverage instead. The list is never reported as having matched nothing. Defect: `src/main.rs:1900-1910`.

**Running the sweep on a subdirectory discards the exclusion list.** The list is read from the root passed on the command line while the paths are relative to it, so any invocation below the repository root loses every exclusion. Reproduced against this tree:

```host-lint:ignore
$ host-lifecycle refs --check plan/0072-ffmpeg-commit-rule-pack
bare     signals-digest.md: 37 issue number(s) written outside a link
bare     handover.md: 3 issue number(s) written outside a link
   Advisory: nothing is blocked. No flag fixes this; each reference is an edit.
```

Both files are named in this repository's own `.host-lintignore` under the comment that calls them the immutable record. Defect: `src/refs.rs:623` with `src/main.rs:1917`.

### The remedy sends the reader to the wrong tracker

**Both remedy strings hardcode `connollydavid/host-lifecycle`.** Every adopter is handed a command whose effect is to rewrite their own issue reference into a link to this project's tracker. The weak-agent acceptance is the evidence that the printed command gets run verbatim: both repeats of the refusal probe executed it exactly. This is the cast round's blocking finding, the bare `#N` resolved against whatever remote happened to be local, relocated from the resolver into the remedy line. Defect: `src/refs.rs:498` and `:613`.

**A qualified reference on a non-GitHub forge builds a github.com URL.** The register form correctly refuses when the origin names another forge; `owner/repo#N` builds the link anyway, so a GitLab-hosted project's reference to its own issue points at an unrelated repository that may well exist. Defect: `src/refs.rs:246`.

**`component#N` guesses the owner from origin and ignores the owner the tree records.** This repository holds two components at foreign owners in `.gitmodules` and eight recipes carrying an explicit URL in `.host-software`, and the resolver consults neither: `allium#12` resolves to `connollydavid/allium` where the recorded owner is `juxt`. In a fork every `--url` retargets to the contributor's namespace, where the tracker is disabled by default. Defect: `src/refs.rs:235-243`.

**`--url` emits an anchor GitHub does not have.** The site renders `{#write-spec}` as literal heading text and slugifies the whole line, so the emitted fragment matches no element and the reader lands at the top of a long document. The markdown form is correct, because mdBook honours the explicit id; the URL form is wrong across 151 headings in this tree. The settled conditional says the anchor is preserved through all three forms so a task node resolves to its heading, and for one of the three it does not. Defect: `src/refs.rs:271`.

### A false resolution verdict

**Two entries sharing a number resolve to the alphabetically first, in silence.** A milestone directory beside an abandoned draft of the same number yields a confident path to the draft, at exit 0, and nothing else in the binary gates the collision. Defect: `src/refs.rs:138-139`.

**First match wins plus a README existence gate turns a present milestone into a gating dead pointer.** A stub directory that sorts first, and a milestone whose record is the directory rather than a README, both produce `names no entry in that room` at exit 1 about a room that demonstrably holds the entry. The design review carried this as wording; it gates. Defect: `src/refs.rs:139-142`.

**`resolve` reports a verdict for a root it never read.** The root is positional and unchecked, and an unrecognised flag falls through to become the root, so a mistyped `--md` produces the governing-host explanation at exit 1 inside the repository that owns the room. This is the sibling of the empty-corpus finding the cast round fixed for the sweep and never applied to the resolver. Defect: `src/refs.rs:544-560`.

### The block grammar admits prose and rejects code

**A fenced block inside a blockquote is read as prose**, producing a false dead pointer at exit 1. An indented code block and an HTML comment do the same. Defect: `src/refs.rs:405`.

**An unbalanced backtick hides every reference after it on the line.** A code span wrapped across a line break is legal and present here, so four live references in this tree are invisible to the sweep today, one of them a register reference in `plan/0053`. Odd fence-line parity swallows the whole tail of a document. This is the fail-unsafe direction: the gate loses a dead pointer rather than raising a false one. Defect: `src/refs.rs:377-379`, `:404-411`.

### The wall is not the size it reports

**"They name no repository" is false for the references it counted.** Every issue reference outside a link is classified as unrendered without consulting the repository it names, so `connollydavid/host-lifecycle#1` is counted and described as naming no repository. Distinct repositories on one line collapse into one finding, two occurrences of one number collapse, and a URL fragment, an HTML comment and an indented code block each count. In `PLAN.md` alone, most `#N` occurrences are already qualified. Three lenses recorded it. The reported wall of 293 conflates two populations, and the remediation node inherits the error. Defect: `src/refs.rs:425`, `:428-431`, `:491`.

### The migration, read for the first time

**The ledger's verify condition greps the token; the tool renames the key.** `migrate_recipe_text` rewrites a line matching the key form and preserves comments, values and longer keys by design and by test. The ledger asserts the token appears nowhere in the file. An adopter whose recipe carries one annotation comment naming the old key runs the migration, is told it succeeded, and can then never record the upgrade: `upgrade --record` refuses at exit 1 and `software --check` raises a permanent hazard with no tool remedy. A recipe migrated correctly and then annotated goes red the same way. Defect: `host-template/UPGRADING.md:315` and `:322` against `src/main.rs:8644`.

**`migrate-recipe --dry-run` writes, and `migrate-recipe --help` migrates the working directory.** Every argument beginning with a dash is discarded and the first remaining one becomes the target, defaulting to `.`. Three sibling verbs in this same CLI accept `--dry-run`, which makes it the natural probe on the one verb that rewrites the reproducibility anchor. Defect: `src/main.rs:8690`.

**A symlinked recipe is replaced by a regular file.** The atomic write renames over the link, so the real recipe stays unmigrated, the tree gains a second divergent recipe, and the tool reports success. Defect: `src/main.rs:6930`.

**A recipe with Windows line endings is silently converted.** The migration reads by lines and rejoins with a bare newline, so a working recipe becomes a whole-file diff reported as one change. The ledger's own text promises every other line is untouched. Defect: `src/main.rs:8647`, `:8678`.

**call/0047's consequence that every line an operator reads names the surviving key is false.** The release path prints the retired spelling on both of its messages, including the refusal that tells an operator their component is not exempt. The spine still documents the retired key in the multi-platform builds section, in the tool's own recipe reference, and in the reference CI comment; the retirement entry's title says the case is recorded with the old name while its action says the new one, and the title is what an operator is shown on record. Defect: `src/main.rs:9221` and `:9497`; `host-template/CLAUDE.md:854`; `host-template/tools/host-lifecycle/README.md:151`; `host-template/UPGRADING.md:311`; `host-template/.github/workflows/reproducible-build.yml:3`.

## The structural finding

The specification cannot catch any of the coverage class. `host-lifecycle-refs.allium` has no document entity and no walk: its universe begins where a reference already exists, so `CleanVerdictSawNothing` proves that a clean verdict reported nothing and never that everything was read. `ExcludedIsNeverReported` quantifies over a per-reference field while the implementation decides exclusion per document, in a function the specification does not model. Every finding in the first two sections above sits outside what the obligations can bite on, which is why they survived a discharge-clean manifest. Defect: `host-lifecycle-refs.allium:118-133`, `:214-227`, `:281`.

## Carried, with the reason

- **Nothing runs the sweep.** No lane, no verify step, no skill. The diff adds specification lanes for a capability nothing invokes. Carried from the design review, unchanged, and it bounds the blast radius of every gating finding above to human and agent invocation.
- **A mistyped register number is invisible.** The grammar matches four digits exactly, so `plan/074` and `call/45` never enter the corpus, and `plan/0074x` resolves as a different reference.
- **No percent-encoding in any emission form.** Bounded by the slug convention, which nothing enforces.
- **The default branch falls back to a literal `main`** on a detached head, which is what a lane checkout gives.
- **Shorthand hex colours of three and four digits** are still counted as issue numbers; the six and eight digit forms were fixed.
- **The anchor is never validated**, though `validate` rejects the identical token as a task reference.
- **The dead summary still prints a placeholder** of the form the weak-agent acceptance records the model pasting verbatim, and which was removed from the advisory and refusal lines for that reason.
- **The migration widens file permissions**, overrides a read-only recipe, and destroys a sibling file named for its temporary, all inherited from the shared atomic write.
- **A recipe carrying both spellings** lets the retired line win by order and migrates into a silent duplicate key.

## Disposition

The operator ruled one pass over the whole set, specification included, on the
reasoning that fixing instances of a class that has recurred three times leaves
the fourth to be found by somebody else.

**Every blocking finding above is fixed**, in `58dd019` and `1b166fa` (host-lifecycle)
and `e830c70` (host-template). The structural finding is fixed first, because it is
the reason the rest survived a discharge-clean manifest: the specification now
carries a document, a readability fact and an exclusion fact, and three invariants
that bite on the corpus rather than on the reference. Each new disposition names a
test that drives the built binary over a corpus with a known hole in it, and each
was proven by mutation — reverting the unread gate, the disclosure, or the remedy
slug fails its named test, and the restored tree is green.

Two of the fixes were narrowed on the evidence rather than applied as reported:

- **Shorthand hex colours of three and four digits stay in the corpus.** Excluding
  them would drop `#123` written as issue 123, which this tree is far likelier to
  contain than a bare colour outside code, and the block grammar now removes the
  places a colour actually appears. The six-digit rule stands.
- **The earlier ledger entries keep the retired spelling.** They are history, they
  run before the rename entry in ledger order, and the migration cleans up what
  they wrote. Rewriting them would make the ledger disagree with what an adopter
  applying it in order actually does.

The carried list stands as carried, with one promotion: **nothing runs the sweep**
is now the largest remaining gap, because the capability is correct and still
surfaces nowhere. It is the `#remediate-this-tree` node's dependency and is
recorded there rather than here.

One measured consequence worth stating: the corrected grammar and classification
move this tree's own wall from a reported 293 to 297 issue references, of which 183
name no repository. The earlier number was both too small (four live references sat
behind an unmatched backtick) and wrong in kind (qualified references were counted
as naming none). `#remediate-this-tree` inherits the corrected figure.

## What the review attacked and could not break

The acceptance rests on this as much as on the findings.

`refs --fix` never writes: eight argument combinations all refuse, and the tree hashes identically before and after. `MEMORY.md` is genuinely excluded by construction, at any depth, in a fresh scaffold with no list authored, and in the component worktree. A freshly scaffolded project's append-only log is never pressed. The empty-corpus fail-closed holds for a nonexistent directory, a directory that is not a repository, a file passed as a directory, and an empty repository. Untracked authored markdown is swept. Every one of the 127 distinct register references in this tree was resolved and the emitted path stated: 125 exist, none is a phantom, and the two unresolved are illustrative references inside ignore fences. Sweeping the entire tree with every exclusion removed finds no dead register pointer hiding in the record layer, so the exclusion currently hides legibility debt alone. Nested repositories are not descended into. The migration's wrong-line resistance is clean against a token in a URL, in a value, in a comment, as a longer key and in another component's section, and byte-identity on an unchanged file is proven with `cmp`. Idempotence holds. The dual parse is equivalent on stdout, with the deprecation on stderr alone. Both ledger verify conditions can fail, so neither joins the vacuous class this project has found 25 members of.
