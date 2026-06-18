# Parallelizing the prose scan escalates run-accumulation to the timing lane

- Status: accepted
- Date: 2026-06-18
- Scope: host-grammar
- Relates: `call/0002` (verification lanes by property type — invokes its
  escalation bridge); `plan/0007` (the prose-tell engine being parallelized);
  `plan/0008` (the milestone that implements this).

## Context and Problem Statement

`plan/0007` shipped the prose-tell engine (`host-grammar::scan_prose`) as a
single sequential pass. For large documents we want to parallelize it. The
lexical and per-sentence tells are embarrassingly parallel, but three equations
accumulate state **across** sentences — anaphora, countdown, listicle — so a run
can straddle a chunk boundary. A chunked-parallel scan must therefore reconcile
boundary runs and assemble output in document order while K workers complete in
**arbitrary order**.

`call/0002` reserves the TLA+/Specula lane strictly for timing and concurrency
("for all interleavings") and routes functional invariants to allium. The
question: does the parallel scan stay in allium's lane, or does it cross the
escalation bridge into Specula's?

## Decision

**The parallel scan splits across both lanes; the worker-completion ordering
crosses the bridge into the Specula/TLA+ lane.**

- **allium lane (functional).** The merge of per-chunk run summaries is an
  associative monoid; `parallel(split) == sequential` for all sentence sequences
  and all split points. This is a "for all inputs" property — property-based
  testing in host-grammar.

- **Specula lane (temporal/interleaving).** K workers complete in any order and
  their partial results are assembled into one ordered output. The invariant —
  *for every completion interleaving, the assembled output is identical and in
  document order* — plus liveness (every worker joins; no chunk is dropped) is a
  "for all interleavings" property that property-based testing cannot
  exhaustively explore. This is exactly the bridge condition in `call/0002`, so
  it escalates. A TLA+ spec model-checks it with TLC.

This is a software decision about `host-grammar`, not a methodology change
(anti-ouroboros): it applies `call/0002`'s existing rule, it does not amend it.

## Consequences

- Good: the bridge is exercised for the first time with a concrete, honest
  trigger; TLA+ is used on its home ground, not as a general requirements tool.
- Good: the two lanes stay complementary — PBT proves the merge math, TLC proves
  the interleaving safety/liveness; neither subsumes the other.
- Cost: a TLA+ spec and a TLC run join the milestone's obligations, and (per the
  milestone decision) TLC is wired into CI, adding a Java/tla2tools dependency to
  the pipeline.
- Constraint: the implementation must keep workers free of shared mutable state
  (each returns an owned summary; the merge is sequential), so the model the spec
  checks matches the code.
