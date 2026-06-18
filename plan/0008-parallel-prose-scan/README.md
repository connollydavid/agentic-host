# Parallel prose scan for large documents

Parallelize `host-grammar::scan_prose` so large documents scan across cores,
while preserving the exact sequential result. Driven through the full
methodology: a `call/` decision, both verification lanes, and a reproducible
re-pin.

See `call/0015` for why this splits across the allium and Specula lanes.

## Design

The work is the per-sentence equation evaluation and lexical matching; sentence
segmentation is a cheap single pass. So:

1. **Segment once** (sequential) into a sentence vector.
2. **Below a threshold** (small docs, titles) stay sequential — thread overhead
   is not worth it.
3. **Split** the sentence vector into K contiguous chunks (K = available
   parallelism), with `std::thread::scope` — no new dependency, so the
   digest-pinned reproducible-build anchor is untouched.
4. Each worker computes, for its chunk, an owned **partial result**:
   - lexical tells and per-sentence structural tells (negative parallelism,
     tricolon, participial tail, false range) — independent;
   - a **run summary** for each cross-sentence equation (anaphora, countdown,
     listicle): `(prefix_run, interior_run_scores, suffix_run)` plus the
     boundary state for countdown / self-answered adjacency.
5. **Merge** adjacent partials left-to-right (sequential, associative): a left
   suffix run and a right prefix run with the same opener join; interior runs
   finalize. Output is assembled in document order.

Workers hold no shared mutable state — each returns an owned partial; the merge
is sequential. This keeps the implementation equal to the model the TLA+ spec
checks (`call/0015`).

## Verification lanes

- **allium / PBT (functional).** New property: for all sentence sequences and
  all split points, `parallel_scan == scan_prose` (order, ids, weights). The
  merge-monoid associativity. Extends `host-grammar.allium` and
  `tests/prose_properties.rs`.
- **Specula / TLA+ (temporal).** `plan/0008/spec/ParallelScan.tla` models K
  workers completing in arbitrary order assembling one ordered output.
  Invariants: the assembled result equals the sequential decomposition **for
  every completion interleaving** (safety); every chunk is merged exactly once
  and the join terminates (liveness). Model-checked with **TLC, wired into CI**
  (a Specula lane job installs Java + tla2tools and runs the check on every
  push).

## Lifecycle / chain (software-first)

1. **host-grammar**: add `scan_prose_parallel` (or make `scan_prose` parallel
   above the threshold); keep the public API stable; PBT; commit/push.
2. **host-lint**: pick up the new host-grammar rev; `--prose` benefits
   transparently; tests; commit/push.
3. **agentic-host**: TLA+ spec under `plan/0008/spec/`; CI Specula job; re-pin
   host-lint in `.host-software`, rebuild in the pinned container, record the
   artifact, `software --verify-build`; PLAN.md + MEMORY entries.

## Verification

- host-grammar PBT green incl. the parallel==sequential refinement.
- TLC green on the bounded model (locally and in CI).
- Reproducible build re-pin verified in the pinned container.
- Self-dogfood: `host-lint --prose` over this repo's large docs still advisory.
