# plan/0085 active-default surfaces: the always-loaded content is warn-free and named AGENTS.md

Operator-directed (2026-09-05), three asks over one partition, with the definition settled by iteration in the cutting session. The partition is the one the calx-knap doctrine already names: the **always-loaded surfaces** (CLAUDE.md's calx-knap adoption note): the manual, STRUCTURE.md, the linked skills, and the territory and memory surfaces as they come to exist. Three changes:

1. **Zero host-lint warnings, held strict:** within the declared corpus a warning counts as a flag; outside it, today's tiers stand unchanged. This is the whole of the ASCII-only ask as the operator defined it in iteration: em-dashes, arrows, and the decoration family are warning-tier tropes today, so the strict reading flags them where it matters and no separate byte rule is built.
2. **A counted non-ASCII census, disclosed not gated:** the declared corpus's non-ASCII bytes are counted beside the verdict, so the exempt populations (Chinese script, which waits for the deferred full zh translation; the IPA of the pronunciation lines) stay measured and a new category is visible on arrival. Nothing gates on non-ASCII as a category; exempt means the census carries it, not that a rule spares it.
3. **The manual is `AGENTS.md`;** `CLAUDE.md` becomes a one-line text pointer to it, never a symlink (this working tree sits on a filesystem where the link bits do not survive, and a text pointer renders on the forge, survives Windows checkouts, and diffs honestly).

## Why

The warn half is about holding ground, not retaking it: the manuals sit at zero prose warnings today (the trope pass of 2026-09-05), and zero is only as durable as the tier that guards it. The advisory tier exists for records and drafts; the always-loaded surfaces are the text every session reads and executes, and a warn there is advice to the instruction itself. The verify recheck's prose clause already blocks, but only at release time and over the whole tracked corpus; the strict reading makes the state visible and gateable where the content lives.

The census half exists because the operator exempted two populations by name (zh script, IPA) while wanting "ASCII-only" for the decoration typography. A census keeps that shape honest: the exempt populations are counted and disclosed on every verdict, so "exempt" never silently becomes "anything goes", and a new non-ASCII category announces itself instead of arriving unmeasured.

The rename half adopts the vendor-neutral convention [DESIGN-LEM-MEMORY.md](../../DESIGN-LEM-MEMORY.md) recorded as the open direction (the feedback register's "AGENTS.md is the emerging vendor-neutral convention", ruled by the operator now). It is a spine change: template-first, ledger-carried, with this host migrating in full. Tool surfaces naming the old name are enumerated, not guessed: 20 references in host-lifecycle's source (the generator and spine paths), plus memory.rs, dream.rs, and the entrance's README. Sequenced before [plan/0079](../0079-spine-is-a-rendered-artifact/README.md) starts its build, because call/0053 defines the spine as the byte content of the template's manual plus STRUCTURE.md, and the rendered artifact must be defined over the renamed file set, not renamed mid-render.

## The lem correction

The manual carries **partial zh translations** of the pronoun system: Chinese columns in the paradigm tables, zh and Cantonese example sentences, and a zh pronunciation line. Those are **removed** from the always-loaded copies (template and host) as a content edit; the system is taught in English with the IPA pronunciations intact. The **full zh translation is deferred** by operator ruling and recorded in PLAN.md's follow-up table, so the deferred work is on the record rather than implicit; when it lands, the census already measures it.

**Landed early (2026-09-05, operator-directed).** The zh removal is no longer waiting for this plan's build: the partial zh content was observed switching an agent into Chinese mid-session, so both manuals were edited the same day — the quick-reference Chinese column, the Chinese paradigm, the zh pronunciation and example lines, the zh-specific rules, and the decoration characters beside them (the section sign and three arrow glyphs) are gone from the always-loaded copies. What remains here is the census, the strict tier, the declaration, and the rename.

## Decision

- **The corpus is declared, never discovered.** The always-loaded file set is declared in the recipe (the exact home is a gather-data question: a manifest stanza versus a `.host` key), and the gate derives its population from the declaration. The plan/0074 lesson governs: deriving requirements from directory listings made emptying a directory delete the question.
- **Strict inside the declaration.** The gate reads the declared set and applies one rule no other corpus carries: a warning is a flag. Outside the declaration, today's tiers stand unchanged. One declaration serves every checker that needs it; the `.host-lintignore` lesson (one list silently serving two checkers) is the failure shape this avoids.
- **The census discloses and never gates.** Non-ASCII bytes in the declared corpus are counted on every verdict. The two known populations (zh script, IPA) are what the count is expected to hold; the point of the count is that a third population is news.
- **The pointer is text.** After the rename, `CLAUDE.md` holds a line naming `AGENTS.md` and nothing else. Tools that look for the old name find a pointer that says where the manual is; the pointer file is itself in the declared corpus and passes its own gate. The exact pointer text is a Fen question: does the weak model, handed the pointer, open the manual?

## Scope

1. **The declaration and the gate**: host-lifecycle reads the declaration and applies the strict tier to the declared files in the prose walk and the verify recheck; the census rides the same verdict.
2. **The rename**: template-first (`git mv` keeps the manual's history), the pointer file, the host-lifecycle surface changes, the entrance, this host's migration.
3. **The lem content edit**: the zh partials leave the always-loaded copies; the deferred full translation is recorded in the follow-up table.

Out of scope, recorded so it is not assumed: the full zh translation (deferred by operator ruling, its own future work); gating on non-ASCII as a category (declined by definition this session); rewriting records (plan/, call/, MEMORY.md keep their own bytes); the `.host-lintignore` two-list separation (still owed, its own milestone, and the new declaration must not become a second ignore list); the strict tier over any corpus beyond the declaration; plan/0079's render (this plan only fixes the file set it will render); symlink support (declined above, recorded why).

## Open questions the gather-data node settles

- The declaration's home: a `lifecycle.manifest` stanza or a `.host` key, and the exact grammar (globs? explicit lists?).
- The skills' census: which linked skills carry warns or non-ASCII bytes today, and whether skill frontmatter counts as always-loaded.
- The complete surface list naming `CLAUDE.md` (source, docs, workflows, the entrance), each with its migration shape.
- Which lem lines are zh partials (removed) and which are doctrine that stays; the census's expected populations stated per file.
- The pointer file's exact text, settled by a Fen probe: does the weak model, handed the pointer, open the manual?

## Build sequence

### The settled conditionals {#gather-data}
- verify: the warn and non-ASCII census recorded per declared file, with the exempt populations stated; the surface list naming CLAUDE.md complete with migration shapes; the declaration home settled with the grammar written; the zh partials enumerated line by line against the doctrine that stays; the pointer text Fen-probed on the corrected protocol, transcripts recorded
- depends: none

### The declaration and the strict tier {#write-spec}
- verify: the Allium spec models the declared corpus, the strict tier (a warning is a flag inside the declaration), and the census disclosure; `allium check` and `analyse` exit clean
- depends: #gather-data

### The obligations {#write-obligations}
- verify: every new obligation carries a disposition naming a test that exercises the rule, and the day-one state is expressed as tests (the declaration reddens on any warn inside it, and the census discloses zh and IPA without flagging them)
- depends: #write-spec

### The gate {#implement-gate}
- verify: `cargo test` green; a declared file's warning flags and an undeclared one advises; the census counts non-ASCII without flagging it; the population comes from the declaration, so deleting a declared file is a missing-file verdict, never a smaller corpus
- depends: #write-obligations

### The rename {#implement-rename}
- verify: template carries AGENTS.md with the pointer file; host-lifecycle accepts both names during the migration window and generates AGENTS.md at the new revision; the entrance and every enumerated surface migrated; `git mv` history intact
- depends: #implement-gate

### This host migrates {#migrate-this-host}
- verify: this repo's manual is AGENTS.md with the pointer file; STRUCTURE.md and the forward documents cite the new name; the declared corpus passes its own strict gate on the real tree
- depends: #implement-rename

### Cast consultation {#cast-consult}
- verify: each persona's concern addressed or recorded in design-review.md, with Mara pricing the gate's keeping-green cost and Bly reading the adopter migration path cold
- depends: #migrate-this-host

### Adversarial review {#adversarial-review}
- verify: an independent multi-lens read of the built diffs records every blocking finding fixed or carried, with a dedicated lens for the declaration becoming a second ignore list, one for the census growing into a gate by drift, and one for the doctrine fragmenting between the manual and the future zh translation
- depends: #cast-consult

### The weak-agent acceptance {#fen-acceptance}
- verify: the real qwen3.5-4b, on the corrected protocol, follows the pointer file to AGENTS.md, applies the pronoun system from the manual without the zh partials, and reads the strict verdict without remediating records; rotation-stable, transcripts recorded; an unreachable channel is labeled and the probes owed, never simulated silently
- depends: #write-obligations

### The spine doctrine {#write-spine-doctrine}
- verify: the ledger entries land (the rename with adopter migration steps; the declared-corpus invariants and census superseding the lem entry's sync instruction); the template manual states the strict tier where it states the reference discipline
- depends: #adversarial-review

### Release and re-pin {#release-and-re-pin}
- verify: the component releases cascade clean, `software --check .` is green at the new pins for everything this milestone owns, and the grammar-cascade hazards plan/0084 carried are named beside whatever remains; PLAN.md and MEMORY.md record the outcome in their own commits
- depends: #write-spine-doctrine, #fen-acceptance
