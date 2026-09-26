# plan/0094 ci-lanes-red: every red lane in the family surveyed, triaged, closed

Operator-directed ("we have CI failures all over too"), continuing plan/0093's
sweep to the lanes. The survey (2026-09-26, `gh run list` across the nine repos)
found three red sources and cleared the rest:

| Repo | Runs | Cause | Class |
|---|---|---|---|
| host-lifecycle | v0.54.3, v0.54.4, main red (v0.54.2 green) | the Clippy lane (`-D warnings`) denies `manual_strip` on the plan/0093 anchor-strip code, which local `cargo test` cannot see | R2, fixed in v0.54.5 |
| host-lint | v0.20.0, v0.21.0, v0.22.0 red (red since 09-14) | the test job exits 127: `test-integration.sh` cd's into a temp dir and then invokes `$BINARY`, which CI passes relative (`./host-lint-linux-amd64`), so the not-found trips `set -e` before a verdict prints; locally green under an absolute path, which is why 219/219 passed at the landing | R2, fixed this plan |
| host-grammar | Allium lane red on v0.7.0 (09-14) | `cargo install allium-cli --version 3.4.2` without `--locked` re-resolves dependencies and broke when allium-parser v3.5.3 shipped a changed signature — the defect /host's bcbf449 fixed for its own installs | R2, one line |
| host-lint upstream-drift job | failure, tolerated | `continue-on-error: true` by design (host-lint#22): a network lane comparing FFmpeg ground truth against upstream HEAD must never redden the build; its drift is the pack's watch-item, not a gate | by design, stands |
| connollydavid/host, host-prove, host-grammar Test/Specula/host-prove lanes | green | one historical Install failure on /host, fixed at tip by the lockfile commit | nothing owed |

## Fixes

1. **host-lifecycle v0.54.5** (ef20eaea, artifact 14dd149bfaa2e3a79161bc6f6411c6777b782d64dff132a97173708fdc22d1c5):
   the anchor strip goes through `strip_prefix`; `cargo clippy --all-targets -- -D
   warnings` (CI's exact command) run locally before the push. The release itself
   was blocked once by a residue of the interrupted attempt (a staged `vendor/`
   remnant the kill-time guard never reached); the cleanup and re-run are recorded
   in the Results.
2. **host-lint v0.22.1**: two lines of `test-integration.sh`. The binary is
   absolutized once at the top, so every `( cd "$dir" && "$BINARY" ... )` section
   survives the cd; and the lem section-exclusion fixture declares its coverage the
   way the contract requires, a `LEXICON` carrying `# host-lint: lem`, not an
   in-file marker (the fixture's inline marker is a markdown heading the scanner
   rightly ignores). Measured 218/218 under the relative invocation, the shape CI
   runs.
3. **host-grammar v0.7.1**: `--locked` on both tool installs in the Allium lane,
   the /host bcbf449 pattern.

## The /host#21 evidence, live

v0.54.3 and v0.54.4 shipped with red CI: the release receipt is blind to lane
outcomes, which is the exact defect connollydavid/host#21 names. The receipt
records the verify gate, the obligations, and the reproduced artifact; the CI
matrix is a separate lane whose outcome enters nothing. Two more instances for
that design record: the release-verification lesson (run CI's own lint command
locally, not only tests), and the read-back discipline (verify the run concludes
green after the push, as the template push now reads `origin/main` back).

## Also this plan: the pronoun gate reaches the wire

The operator ruled the session model must dog-food the lem contract's MCP server.
Measured: `host-lint mcp` (v0.22.0) serves `check_reply`, `ask`, `table` over
newline-delimited JSON-RPC; a violating sample returns three pinpointed violations
with the rewrite rule, a doctrinal sample returns clean. Registered as a
workspace-scoped MCP server (`.zcode/config.json`), which is gitignored here, so
the registration is machine-local until bootstrap learns to write it (a small
host-lifecycle feature, noted upstream). The PATH `host-lint` had gone stale
below the mcp mode's introduction and was refreshed from the embed build per the
2026-09-05 lesson.

## Results

Recorded 2026-09-26, same session as the cut.

- **host-lifecycle v0.54.5** (ef20eaea, artifact
  14dd149bfaa2e3a79161bc6f6411c6777b782d64dff132a97173708fdc22d1c5): the anchor
  strip goes through `strip_prefix`; CI green on the tag and main. The first
  release attempt failed in the container on a residue of the interrupted
  predecessor: the kill stopped before the staging guard could restore, and the
  bind-mounted worktree carried the half-state into the build. The guard's
  backstop covers panics, not kills — a hardening note for the release path.
- **host-lint v0.22.1** (a0d22055, artifact
  d2c25034c12aed234dec7799de408d9a9c5c919fe54f862a5574e25aa59a56d2): the
  integration script absolutizes the binary once at the top, so every
  `( cd "$dir" && "$BINARY" ... )` section survives the cd, and the lem
  section-exclusion fixture declares coverage through the `LEXICON`, the
  contract's actual mechanism — the fixture's inline marker was a markdown
  heading the scanner rightly ignores. Measured 218/218 under the relative
  invocation, the shape CI runs. The section-exclusion test had been unreachable
  in CI since v0.20.0 because the 127 aborted the script before it, which is how
  a stale expectation survived three releases.
- **host-grammar v0.7.1** (6cd41c3): both Allium-lane installs carry `--locked`;
  the lane is green on main.
- **The recipe pins hold at the revs the embeds consume** (call/0052): grammar
  `b9cace10` (v0.7.0) and host-lint `0eeabc2` (v0.22.0) stay pinned, because the
  released binaries' vendored engines are those revs; adopting v0.7.1 and v0.22.1
  into the vendored bundles is the next embed-equality cascade (re-cut bundles,
  consumer revs, releases), the plan/0082 pattern. Neither new release carries a
  library change: lanes and fixtures only. `software --verify-build --item
  host-lint` re-proved the v0.22.0 record (386b254c reproduces in the recorded
  toolchain) after a local build had overwritten the canonical binary in the
  worktree — the recorded hash is the container's, and the gating artifact is
  built in its recorded toolchain, never ambiently.

**Dispositions.** upstream-drift stands as designed (`continue-on-error`, a
network lane whose drift is the pack's watch-item). The /host Install red and
host-prove's historical red are fixed at tip; nothing owed. The R4 set is
unchanged: /host#21 (receipt-CI coupling, now carrying three live instances from
this session), /host#24 (the five placements), host-lifecycle#23
(room-touching), /host#18 (plan/0075).
