# plan/0099 host24-placements: the five placements, built and enforced

Operator-directed (the goal: drive the /host#24 placements to done, efficiently).
The five placements from the bench worker's report, recut against what already
landed: the verify-setup commit-gate requirement **shipped in v0.59.0**
(f0f7703, the CommitGateDeclared requirement — a recipe declaring components and
no gate provider is itself the gap). The remaining four build here, batched so
one lifecycle release carries every code placement.

## The placements

1. **The cfg-declaration rule** (code): `software --check` walks each
   materialized component's Rust sources; `#[cfg(kani)]` code with no `kani:`
   disposition in the component's obligations manifest is a HAZARD — the
   two-way remedy (declare the rung, or remove the code with a recorded
   reason). The invisible-twice-over state (no lane compiles it, no obligation
   declares it) becomes a named finding.
2. **`software --artifact-delta <component> <refA> <refB>`** (code): rebuild
   both refs in the recorded toolchain and report identical-or-not — the
   mechanical answer to the comment-only-diff placement (a comments-only pass
   that moves `file:line:column` bytes is not byte-neutral, and the delta
   proves which passes moved nothing).
3. **The derived inventory** (code): every source file of a materialized
   component appears in some task's `inputs`, or in an explicit exclusion
   carrying a reason — the reconcile-coverage model applied to the task graph;
   a dropped file fails by absence.
4. **The naming sweep joins CI** (template/docs): the workflow example carries
   the sweep as a standard lane, the manual names the placement.
5. **The shared-index manual clause** (template/docs): fan-out workers stage
   explicit paths; `git add -A` under a live bench is the finding.

## Results

Recorded as the phases land.

## Results

**Phase A (the shared-index clause, 2026-09-27):** the template manual carries
the fan-out staging rule (bb0e0e1) — while a bench works in one tree, workers
stage explicit paths and never `-A`; a commit whose message names fewer paths
than it touches is a finding to read. The forge adopted the pointer in the same
hour.

**The cfg-declaration rule** (the code placement): the scan lives in the check
flow (`cfg_kani_problems`) — a component whose Rust sources carry
`#[cfg(kani)]` with no `kani:` disposition in its obligations manifests is a
HAZARD naming the two-way remedy. Regression test covers both directions
(gated code with no declared rung hazards; declaring the rung in the
obligations manifest clears it). Committed, release pending.

**Phase B (the sweep lane, pending the host-lint pin decision):** the
naming-sweep workflow example needs the template to record which host-lint rev
it pins — the same derived-pin pattern as prose.yml, which is Orin's seat.

**Pending:** `--artifact-delta` and the derived inventory (the two remaining
medium builds), recorded for the next cut.
