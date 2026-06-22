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
2. **Below a threshold** (small docs, titles) stay sequential; thread overhead
   is not worth it.
3. **Split** the sentence vector into K contiguous chunks (K = available
   parallelism), with `std::thread::scope` (no new dependency), so the
   digest-pinned reproducible-build anchor is untouched.
4. Each worker computes, for its chunk, an owned **partial**: the per-sentence
   structural tells (negative parallelism, tricolon, participial tail, false
   range) plus the chunk's **run summary**: its ordered per-sentence metadata
   (opener, first word, is-question, word count).
5. **Merge** (sequential): concatenate the partials by chunk index. The run
   summary is a list, so the merge monoid is **concatenation**: a run that
   straddles a chunk boundary simply rejoins when the metadata lists are
   concatenated. The cross-sentence equations (anaphora, countdown,
   self-answered, listicle) then run once over the merged metadata. Lexical and
   paragraph-shape tells are computed once on the whole text. Output order is
   `lexical ++ per-sentence ++ run ++ shape`, the one order both paths produce.

Workers hold no shared mutable state; each returns an owned partial; the merge
is sequential and keyed on chunk index. This keeps the implementation equal to
the model the TLA+ spec checks (`call/0015`).

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

> **Relocated (plan/0012).** `ParallelScan.tla` + `.cfg` and the Specula lane now
> live in **host-grammar** (`spec/`, `.github/workflows/specula.yml`); the spec
> lives with the code it constrains (`scan_chunked`), not in this host. The paths
> below describe the original layout.

## Lifecycle / chain (software-first)

1. **host-grammar**: add `scan_prose_parallel` (or make `scan_prose` parallel
   above the threshold); keep the public API stable; PBT; commit/push.
2. **host-lint**: pick up the new host-grammar rev; `--prose` benefits
   transparently; tests; commit/push.
3. **agentic-host**: TLA+ spec under `plan/0008/spec/`; CI Specula job; re-pin
   host-lint in `.host-software`, rebuild in the pinned container, record the
   artifact, `software --verify-build`; PLAN.md + MEMORY entries.

## Verification

- host-grammar PBT green incl. `scan_chunked == scan_prose` for all k.
- TLC green on the bounded model (locally and in CI via the Specula workflow).
- Reproducible re-pin: host-grammar `d83b348` to host-lint `dff6895` to
  `.host-software` artifact `4655f966…`, double-build reproducible in the
  pinned `rust:1.95.0` container.

## Outcome

Done. `host-grammar::scan_prose_parallel` splits the per-sentence tokenization
across cores above a 64-sentence threshold; `scan_chunked(text, k)` forces `k`
for the property lane. host-lint `--prose` routes through it transparently
(advisory, warn-tier). Both lanes green: PBT proves the merge math, TLC proves
the interleaving safety/liveness.
