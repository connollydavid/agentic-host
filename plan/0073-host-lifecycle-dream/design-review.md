# cast-consult for plan/0073 (2026-07-19)

Five-persona consultation on the dream feature: detector naming, the `--fix`
boundary, the MCP tool surface, and the report format. Each persona's concern
is stated, the finding recorded, and a disposition given (addressed now or
recorded as a follow-up).

## Mara (human operator)

**Concern:** does `dream` fit her workflow? When does she run it, and what
does she do with the findings?

**Finding M1 (cadence undocumented):** the `dream` cadence (when to run it)
isn't in the spine yet. Mara needs to know: run `dream` at the start of a
session that will rely on recalled memories, and at the end of a session
that superseded a decision. The #write-spine-doctrine task addresses this.

**Finding M2 (--fix is a no-op):** `dream --fix` currently acknowledges but
does nothing ("no structural-safe classes are auto-applied yet"). Mara
expects `--fix` to fix things. The message is honest but the empty `--fix`
surface is unsatisfying. The first structural-safe class (dangling-link
repair via remove from index) should land with the cast-review sign-off,
or `--fix` should be explicitly documented as "reserved for future safe
fixes" until then.

**Disposition:** M1 deferred to #write-spine-doctrine. M2 recorded; the
first `--fix` class lands at a follow-up or the `--fix` flag is marked
reserved in the spine.

## Wren (agentic LLM developer)

**Concern:** can Wren drive the memory tools? Are the schemas clear? Does
the dream report give Wren enough to act on?

**Finding W1 (no suggested fix text):** the dream report says WHAT is wrong
(kind + route + explanation) but not HOW to fix it. The issue text said
"suggested edits, printed verbatim." The current implementation omits the
verbatim fix. Wren must construct the fix from the explanation, which is
cognitively expensive and error-prone for a weak agent.

**Finding W2 (MCP schema is flat and clear):** the four memory tool schemas
are flat (slug, description, body, type, op). Wren can drive them. The
`memory_consolidate` output is a text block that Wren can read and route
to `memory_write` calls. Good.

**Disposition:** W1 recorded as a named follow-up: add a `suggestion` field
to Finding with the verbatim edit/append text. W2 addressed (the schema
is agent-legible).

## Bly (adopter agent, writes now reads cold later)

**Concern:** the per-user store at `~/.host-memory/` is local to this
machine and keyed by the encoded CWD. If Bly writes memories here and the
project moves, or Bly returns on a different machine, the store is
invisible.

**Finding B1 (path-sensitivity):** the encoded CWD means a moved project
loses its per-user store. `dream` on the new path reads a different (empty)
store silently — no warning. The envhash (plan/0074) would catch the move;
without it, `dream` is silently partial.

**Finding B2 (no cross-machine portability):** the per-user store is
intentionally local (never checked in). Bly on a different machine has no
per-user store; `dream` reports only the repo `MEMORY.md` findings. This
is by design (the per-user tier is machine-specific), but Bly needs to
know that the per-user tier is NOT portable across machines or contributors.

**Disposition:** B1 recorded; the envhash (plan/0074) catches the move
signal. B2 deferred to #write-spine-doctrine (document that the per-user
tier is local-only; team-shared memory is a future plan if a team-memory
tier is added, mirroring Qwen Code's `.qwen/team-memory/` pattern without
adopting their format).

## Orin (methodology maintainer)

**Concern:** what must every adopter's `dream` implementation do? What's
the contract? Are the heuristic detectors ship-grade?

**Finding O1 (heuristic detectors are MVP-grade):** three of seven detectors
(stale-state-over-lore, workaround-vs-plan, append-only-violation) use
simple heuristics with documented limitations. Orin would push for either
(a) documenting these as MVP-grade with named follow-ups, or (b) pulling
them into a later revision. The honest answer: they're MVP-grade; the
spine doctrine names them as the current bar with the understanding that
the cast review rules on whether they're ship-grade or need refinement
before the release.

**Finding O2 (dream/upgrade boundary not in spine):** the non-overlap is
confirmed (gather-data probe + spec disjointness check) but not yet in the
spine. The spine must name the boundary explicitly: `dream`'s surface is
memory-only; `upgrade`'s surface is template revisions + applied set;
they never cross.

**Finding O3 (the spec stays dream-only):** the weed+tend decision trimmed
the spec to dream-only (MemoryWrite/Suggestion/LinkRef entities removed).
Orin should rule at the adversarial review: does the spec need to grow to
model the MCP surface, or is the dream-only scope correct for this
milestone? My recommendation: keep the spec dream-only for plan/0073; the
MCP surface gets its own spec (or spec section) at a follow-up milestone
if the adversarial review confirms the need.

**Disposition:** O1 deferred to #write-spine-doctrine (name as MVP-grade).
O2 deferred to #write-spine-doctrine (name the boundary). O3 deferred to
#adversarial-review.

## Fen (weak agent, qwen3.5-4b Q8_0)

**Concern:** can a 4B read the new detectors and route correctly?

**Finding F1 (routing intuition differs from spec):** the Fen probe on the
three new detectors showed the model routes by FINDING CLASS (some findings
are "edit", some "append", some "report") rather than by STORE (per-user →
edit, repo → append). The spec encodes routing by store; the model's
intuition is class-based. The mismatch is not a design flaw — the store
-based routing is the correct methodology rule (the asymmetry is
load-bearing) — but the report format should make the route explicit so
the model doesn't need to infer it.

**Finding F2 (three new detectors readable):** the model correctly
identified the three new detector classes when given a constructed fixture
(the probe above). The naming (stale-state-over-lore, workaround-vs-plan,
append-only-violation) reads clearly to a 4B when presented in context.

**Disposition:** F1 addressed: the dream report already prints `route=edit`
or `route=append` explicitly in the text output, so the model doesn't infer.
F2 addressed: the detectors read at the 4B bar.

## Summary of dispositions

| Finding | Disposition |
|---|---|
| M1 (cadence) | deferred to #write-spine-doctrine |
| M2 (--fix no-op) | recorded; first class at follow-up or flag marked reserved |
| W1 (no suggested fix text) | named follow-up: add suggestion field to Finding |
| W2 (MCP schema clear) | addressed |
| B1 (path-sensitivity) | recorded; envhash (plan/0074) catches the move |
| B2 (no cross-machine) | deferred to #write-spine-doctrine |
| O1 (heuristic MVP-grade) | deferred to #write-spine-doctrine |
| O2 (boundary in spine) | deferred to #write-spine-doctrine |
| O3 (spec scope) | deferred to #adversarial-review |
| F1 (routing by class vs store) | addressed (route printed in report) |
| F2 (new detectors readable) | addressed |

Five findings deferred to #write-spine-doctrine, one to #adversarial-review,
one named follow-up (suggestion text), and three addressed. No blocking
findings for the current implementation.

## Adversarial review (2026-07-19)

Three named lenses plus a cast-completeness audit. Each lens examines a
load-bearing design decision the cast consultation surfaced or skirted.
Findings classified: **blocking** (must fix before release), **major**
(should fix or explicitly defer), **minor** (note and move on).

### Lens 1: Duplication risk vs. plan/0074's envhash

**Focus:** do dream's per-user store audit and plan/0074's envhash overlap
on the move-detection signal? Bly's finding B1 raised the path-sensitivity
concern.

**Analysis:** envhash fingerprints the local environment (repo abspath,
worktree paths, hook binary hash, image digest, submodule init state). Its
job is coherence: "is my tree still what I hashed?" dream audits memory
content for staleness: "is my recall stale?" The overlap point is the CWD:
if the project moves, dream's per-user store path changes and dream
silently reads an empty store (B1).

**Finding L1-1 (minor): dream must NOT try to detect moves.** Move detection
is envhash's job (plan/0074). dream should run over whatever store is
present and report what it finds. If the store is empty because the project
moved, that's envhash's signal to surface, not dream's. The two tools are
complementary, not duplicative: envhash says "your environment moved";
dream says "your memory is stale." Confirming the non-overlap.

**Finding L1-2 (minor, deferred): the per-user store encoding uses CWD.** A
project-name key (from `.host` stamp) would survive a move. This is a deeper
change; for MVP, the CWD encoding is the bar. Named follow-up for a future
revision.

### Lens 2: The spec scope question (auto-detect reversal + O3)

**Focus:** the weed+tend decision trimmed the spec to dream-only, removing
MemoryWrite/Suggestion/LinkRef entities. Orin's finding O3 deferred the
ruling to this review. Is the trim correct?

**Analysis:** the MCP surface IS tested (4 integration tests over stdio
JSON-RPC). The MemoryWrite safety property ("memory_write never writes to
the repo store") is enforced by code (no code path exists) and tested
(memory_write doesn't accept a store parameter). But it's not asserted in
the spec.

**Finding L2-1 (major, ruled): accept the code-level enforcement for plan/0073
MVP.** The spec stays dream-only. Rationale: the dream feature's load-bearing
semantics (detector set, routing, verdict lifecycle, invariants) are fully
modeled. The MCP surface is a transport layer over the dream engine; it's
tested behaviourally. A formal spec for the MCP surface would add modelling
weight without changing runtime behaviour. If the methodology later needs the
formal contract (e.g. a second consumer of memory_write, or a Kani proof of
the repo-refusal invariant), a follow-up milestone restores the entity.

**Finding L2-2 (major): the Finding entity lacks a suggestion field.** Wren's
finding W1 noted the dream report says WHAT is wrong but not HOW to fix it.
The code's Finding has `explanation` (prose) but no `suggestion` (verbatim
fix text). For MVP this is acceptable (the operator reads the explanation and
constructs the fix), but it limits the `--fix` surface's future. The
adversarial review rules: **defer to a named follow-up plan** (not
plan/0073). The suggestion text is a UX refinement, not a correctness gap.

### Lens 3: MCP surface shape

**Focus:** are the four memory tools the right shape? Does memory_write's
safety property hold? Are there gaps?

**Finding L3-1 (minor): the `op` schema conflates create and update.** The
MCP schema exposes `op: write | delete`; the original spec had
`MemoryWriteOp = create | update | delete`. The code's `write` is an
idempotent create-or-update (MemoryStore::write checks if the slug exists and
preserves `created` on update). This is simpler and matches the operator's
mental model. Acceptable for MVP; the three-value form is a follow-up if
the distinction becomes load-bearing (e.g. refusing to update a Fact entry
without confirmation).

**Finding L3-2 (minor): no scoping on memory_consolidate.** The tool audits
both stores unconditionally. For MVP this is correct (dream's job is to catch
staleness everywhere). A `--scope per-user|repo|both` flag is a future
refinement if the operator needs to isolate.

**Finding L3-3 (addressed): memory_write preserves `created` on updates,
sets `last_edited` to today.** Correct behaviour; verified by the integration
test `memory_write_then_list_then_read_round_trips`.

### Lens 4: Cast consultation completeness audit

**Focus:** ensure every cast finding has a clear owner, timeline, and
disposition. No finding left vague or dangling.

| Cast finding | Owner | Status |
|---|---|---|
| M1 (cadence) | #write-spine-doctrine | clear |
| M2 (--fix no-op) | follow-up or spine | **ruled here**: document as reserved in spine; first safe class at follow-up |
| W1 (no suggestion text) | named follow-up plan | **ruled here**: deferred to a follow-up plan, not plan/0073 |
| W2 (MCP schema clear) | addressed | closed |
| B1 (path-sensitivity) | envhash (plan/0074) | clear complement |
| B2 (no cross-machine) | #write-spine-doctrine | clear |
| O1 (MVP-grade detectors) | #write-spine-doctrine | clear |
| O2 (boundary in spine) | #write-spine-doctrine | clear |
| O3 (spec scope) | **ruled here** (L2-1) | closed: spec stays dream-only |
| F1 (routing by class) | addressed | closed |
| F2 (detectors readable) | addressed | closed |

**Finding C1: O3 resolved.** The spec stays dream-only for plan/0073; the MCP
surface is code-tested, not spec-modelled. A follow-up milestone restores the
spec entity if the methodology needs the formal contract.

**Finding C2: W1 deferred to a follow-up plan.** The suggestion text is a UX
refinement, not a correctness gap for MVP.

**Finding C3: M2 ruled.** `--fix` is documented as "reserved" in the spine;
the first safe class (dangling-link repair) lands at a follow-up with
cast-review sign-off.

### Verdict

No blocking findings. Two major findings ruled:
- L2-1: spec stays dream-only (MVP; MCP surface is code-tested)
- L2-2: suggestion text deferred to a follow-up plan

Three minor findings noted and deferred:
- L1-2: per-user store encoding by project-name (follow-up)
- L3-1: three-value MemoryWriteOp (follow-up)
- L3-2: memory_consolidate scoping (follow-up)

The plan/0073 implementation proceeds to #write-spine-doctrine with the
ruled dispositions folded into the spine text.

## Post-acceptance correction (2026-07-20): two hollow dispositions

The #fen-acceptance run against the real qwen3.5-4b falsified two of the
dispositions above. This section records the correction so the epistemic
trail stays honest.

**W1 and L2-2 were not a UX refinement.** The review deferred the suggestion
text as "a UX refinement, not a correctness gap for MVP" (C2, L2-2). The
acceptance probe showed the opposite: without the verbatim imperative, the 4B
routes the per-user edit class wrong at both temperatures, so the acceptance
criterion "Fen routes each finding class correctly" was not met. The
suggestion text is load-bearing at the weak-agent bar, not cosmetic.

**F1 was recorded "addressed" when it was not.** F1's disposition read
"addressed: the dream report already prints route=edit or route=append
explicitly, so the model does not infer." The probe transcripts show the model
does not read the `route=` token at all; it follows the explanation prose. For
the per-user store the prose and the printed route diverge, and the model
follows the prose. Printing the route was necessary but not sufficient.

**Resolution (host-lifecycle v0.41.1).** Both are the same root cause and both
are fixed by promoting the W1 suggestion text into the report surface: each
finding gains a route-carrying imperative in the natural language the model
reads. The routing re-probe then passed four of four at both temperatures
(recorded in fen-acceptance.md).

**Re-audit.** Because F1 was hollow, every disposition in this document was
re-verified against the code, spec, spine, and tests. W1, F1, and L2-2 (one
root cause) were the only hollow ones. Every other disposition verified
authentic: implemented, honestly documented as a no-op or MVP-grade, or a
follow-up the acceptance does not contradict. The re-audit table is in
fen-acceptance.md.
