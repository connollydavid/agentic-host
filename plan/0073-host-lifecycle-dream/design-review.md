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
