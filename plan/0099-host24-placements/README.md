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

**The stop-gate round-trip (2026-09-28, later):** the landings above were
exercised end to end the same night, and two defects surfaced by running the
gates rather than by reading them. The cold-clone lane's skill-link assertion
hardcoded a count (eleven) that the ci skill's landing had already made
twelve, reddening the host's reproducible-build lane from outside any record;
the gate now recounts the linker's shapes and names any missed link (the fixed
run concludes green, and its receipt discharges at the fix). The ci record
verb resolved the default revision from the first path segment, so a
component's pin never resolved unless `--revision` was passed (host-lifecycle
v0.60.4, c140ea2; the label is everything before the lane). Separately, the
lint kani lane was discovered to have NEVER concluded in CI: six consecutive
runs cancelled at exactly GitHub's 6-hour ceiling, `cargo kani` proving all
six harnesses in one job; the lane now shards one harness per job (lint
fc580ad) with the obligations re-derivation in its own job, which had sat
after the proof step and so had never once run in CI (it now passes there).
Four of six harnesses conclude green within minutes; the remaining three were
still proving at this record's writing. The v0.22.4 kani receipt records the
honest failure at the pin (the blocker record); the shard on lint main is the
fix, and the next lint release carries it.

**The cascade settles (2026-09-28, latest):** the fix shipped as lint v0.22.5
(d4cd801, artifact 641ef6a23d4d1a44cabb8ef920a6d524358353cb8aa295a0d68506429777f5e3),
the embed-equality chain followed it (call/0052): lifecycle's embedded engine
moved to v0.22.5, the deps bundle graduated by hand to vendor-v14 (the
onboarding `--lock` verb neither builds nor uploads a bundle), and lifecycle
v0.60.5 (4ad90ae) landed carrying both. The sharded kani lane's first CI
verdict on the released rev: four harnesses and the obligations re-derivation
conclude green; the three remaining harnesses were still proving, and their
receipt records the in-progress state at the pin until the run concludes.
Every worktree sits at its pin, the hooks are reinstalled against the new
canonical hash, and the three gates read green with the one disclosed note.

**The sharded lane's verdict (2026-09-28, final):** the run concluded with the
three harnesses each cancelled at the 6-hour ceiling standalone
(scan_line_never_panics, hits_are_word_bounded,
form_and_mangle_hits_are_classified_by_the_table), so the sharding's finding is
precise: these three proofs have never concluded anywhere in CI, and the four
others (plus the obligations re-derivation) pass in minutes. The receipt
records the failure at the pin d4cd801 and the gate passes with the disclosed
note. The owed work is proof engineering per harness, filed as host-lint#32:
bound the input spaces, split a harness that carries several obligations, or
carry an explicit bounded mode, then re-measure to a conclusion inside the
ceiling.

**The v0.22.6 verdict (2026-09-28, final):** the same three harnesses hit the
ceiling on the released tag run (36424678016), the four fast ones and the
obligations re-derivation pass, and the failure receipt stands recorded at the
pin f0fcd22 with the gate green on the disclosed note. The proof-engineering
work owes nothing further to the lane layer: the finding is stable across two
runs, sharded, on two revisions (host-lint#32).
