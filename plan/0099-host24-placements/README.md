# plan/0099 host24-placements: the five placements, built and enforced

Operator-directed (the goal: drive the /host#24 placements to done, efficiently).
The five placements from the bench worker's report, recut against what already
landed: the verify-setup commit-gate requirement **shipped in v0.59.0**
(f0f7703, the CommitGateDeclared requirement; a recipe declaring components and
no gate provider is itself the gap). The remaining four build here, batched so
one lifecycle release carries every code placement.

## The placements

1. **The cfg-declaration rule** (code): `software --check` walks each
   materialized component's Rust sources; `#[cfg(kani)]` code with no `kani:`
   disposition in the component's obligations manifest is a HAZARD; the
   two-way remedy (declare the rung, or remove the code with a recorded
   reason). The invisible-twice-over state (no lane compiles it, no obligation
   declares it) becomes a named finding.
2. **`software --artifact-delta <component> <refA> <refB>`** (code): rebuild
   both refs in the recorded toolchain and report identical-or-not; the
   mechanical answer to the comment-only-diff placement (a comments-only pass
   that moves `file:line:column` bytes is not byte-neutral, and the delta
   proves which passes moved nothing).
3. **The derived inventory** (code): every source file of a materialized
   component appears in some task's `inputs`, or in an explicit exclusion
   carrying a reason; the reconcile-coverage model applied to the task graph;
   a dropped file fails by absence.
4. **The naming sweep joins CI** (template/docs): the workflow example carries
   the sweep as a standard lane, the manual names the placement.
5. **The shared-index manual clause** (template/docs): fan-out workers stage
   explicit paths; `git add -A` under a live bench is the finding.

## Results

**The shared-index clause (2026-09-27):** the template manual carries
the fan-out staging rule (bb0e0e1); while a bench works in one tree, workers
stage explicit paths and never `-A`; a commit whose message names fewer paths
than it touches is a finding to read. The forge adopted the pointer in the same
hour.

**The sweep lane landed (2026-09-28, template 1202877, ledger 13b14e6):** the
reference `.github/workflows/check.yml` runs `host-lifecycle software --check .`
on every push, so the naming sweep's recheck, the cfg scan, and the derived
inventory block at the push boundary. The lane no-ops on a tree with no
`.host-software` and builds the tool from the `tools/host-lifecycle` submodule
the template ships, so no separate host-lint pin decision exists to make: the
check needs only the lifecycle the template already carries, and the UPGRADING
entry (requires v0.60.3) moves existing adopters. The host itself already ran
the sweep at a CI boundary (the verify-build lane's `software --check` step),
so the gap the brief measured was the adopter's, and the reference lane closes
it. The landing also paid the lanes' duty the placement preaches: the
template's Prose lane had gone red on two em-dash decorations the previous
landing carried into STRUCTURE.md; reworded, and Prose, Site, and the new Check
lane all conclude green on the ledger commit.

**The derived inventory landed in v0.60.3** (component abc415e, pin 90d435e,
artifact 157477c9ca53b5781b35c46ac17b0f0b38330bd4fd1fef04c27cb3e7325e8fef):
`software --check` derives the module inventory instead of reading a typed one.
Every Rust source under a materialized component's `src/` must appear in some
task's `- inputs:` line (the plan room's task graphs; a directory input covers
everything under it) or carry a reasoned exclusion in the tracked
`.host-inventory`; a file in neither fails by absence, and an exclusion without
a reason is its own HAZARD rather than a cover. The first sweep flagged
thirteen files across six components, the typed-inventory harm of the placement
alive in the forge's own house; the stock is recorded with per-file reasons and
new work cites its inputs. Regression tests cover coverage by task input,
coverage by directory input, the reasoned exclusion, and the reasonless one.

**The cfg-declaration rule landed in v0.60.2** (3071ed29, artifact
61ead199b5b52d06464247303c591f149925cc71f7645c50b87d96075c6014d6): the check
sweep walks each materialized component's Rust sources; `#[cfg(kani)]` code with
no `kani:` disposition in the component's obligations manifests is a HAZARD
naming the two-way remedy. Regression test covers both directions. The rule's
first sweep flagged the forge's own house; the lifecycle's and lint's kani
harnesses were invisible to every gate exactly as the placement described; the
rungs are now declared in the manifests. The record pair (pin e09c6b2d's tree,
artifact af1c5858) is container-proven; the template's tools submodule settles
at v0.60.2. The artifact-delta verb shipped in the same landing.
