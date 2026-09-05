# gather-data: the census, the surface list, the declaration, the pointer (2026-09-05)

This records the #gather-data node. Everything measured against the tree at `0c9a7472` (host) and host-template `8214ee3`.

## The warn and non-ASCII census

Swept with the pinned prose engine, per candidate always-loaded file:

| file | warns | non-ASCII lines | populations |
|---|---|---|---|
| CLAUDE.md (host) | 0 | 4 | IPA in the pronunciation lines; the ł of Stanisław |
| STRUCTURE.md (host) | 0 | 0 | none |
| host-template/CLAUDE.md | 0 | 4 | the same two populations |
| host-template/STRUCTURE.md | 0 | 0 | none |

The zh partials were removed the same day the plan was cut (operator-directed, after the incident recorded in MEMORY.md), so the census's expected populations are exactly the two exempt ones. The strict tier's day-one job is therefore purely to hold zero.

**The skills are not in this host's corpus.** `.claude/skills/*` are generated, untracked symlinks into materialized components and tool submodules (link-skills.sh; the tracked-symlink lesson is call/0005), so their content is payload swept at its source: host-lint's and host-lifecycle's own repositories gate their SKILL.md files. The declared corpus here is the tracked manuals plus the territory and memory surfaces when plan/0083 builds them.

## The surface list naming CLAUDE.md

Complete as of this sweep, each with its migration shape:

| surface | shape |
|---|---|
| `host-lifecycle` src/main.rs:986, `classify_case` reads `CLAUDE.md` presence to classify an adoption | functional: accept either name, AGENTS.md first, during the migration window |
| src/main.rs:8326, `PLACED_ROOT_MD`, the known root documents of the book walk | functional: add `AGENTS.md` beside `CLAUDE.md` |
| src/main.rs:8601 to 8605, the How room places the manual (`dest: "CLAUDE.md"`, label `CLAUDE`) | functional: place AGENTS.md as the manual; the pointer file renders as the small page it is |
| src/main.rs tests 13827, 14053, 14070-14072 | functional: follow the placement changes |
| src/memory.rs:5, src/dream.rs (2 sites), src/main.rs doc comments 972, 1299, 1657, 6071, 6323, 13412 | text: update the comments to the new name where they describe live behavior; the two that cite `CLAUDE.md` section 6 as record history stay accurate either way because they describe where a rule is written, which is the pointer's target |
| `host/main/README.md`: the entrance's document | text: name AGENTS.md |
| STRUCTURE.md (host and template): the How room row | text: name AGENTS.md |
| host-template/lifecycle.manifest header comment | text: names the three prose copies; update with the rename |
| call/0053 and the plan/0079 handoff | record: call/0053 defines the spine as the byte content of the template's CLAUDE.md plus STRUCTURE.md. The renamed set is AGENTS.md plus STRUCTURE.md **plus the CLAUDE.md pointer**, because the pointer's exact text is doctrine an adopter must carry byte-for-byte. This is a note for plan/0079's render, not a rewrite of the record |

## The declaration's home and grammar

**Decision: a `[corpus "active"]` stanza in `lifecycle.manifest`, `file = <path>` entries, explicit paths only.** The reasoning:

- The manifest is already the single tool-readable journal the prose copies point at, and host-lifecycle reads it live: the same property `GATE-refs-in-verify` relies on. The plan/0074 lesson (derive the population from the recipe, never from directory listings) and the plan/0072 lesson (a discovery heuristic narrower than its subject reports completeness over whatever it saw) both point at an explicit declaration read from the recipe.
- `.host` was rejected: it is the template stamp (template, revision, name, baseline) read by the stamp reader; project-authored policy does not belong in a file whose shape the tool owns.
- Globs were rejected for the first cut: a glob is a discovery heuristic, and the declared corpus is four files today. An explicit list that names a missing file yields a missing-file verdict: exactly the failure the declaration exists to make loud. Globs can be added when a corpus actually needs them.

## The pointer text

Draft carried by this node, for the probe:

> The operating manual is AGENTS.md. This file is a pointer, kept so tools that look for CLAUDE.md find the manual's name.

Probe question (Fen, on the corrected protocol): handed a repository whose CLAUDE.md contains only that line, does the model open and follow AGENTS.md as the manual? Two draws. The channel state is the one recorded in plan/0084's fen-acceptance: the gateway answers 401 to a session with no channel credentials, so the probe is **owed**, labeled, with nothing simulated; the kit gains this cell when the channel exists.

## What lands where

The strict tier and the census are policy in host-lifecycle (the prose verb reads the declaration, escalates warns to flags for declared files, and discloses the census), with detection untouched in host-lint. This is the same split that keeps the engine shared and the verdicts local. The pre-commit hook keeps today's behavior: it gates flags, advises warns, and does not read the declaration; the declared corpus's teeth are in the prose verb and the verify recheck that runs it.
