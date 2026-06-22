# plan/0032 delta design-review (the bundle, offline build, host-lifecycle feature, spine MUST)

> **Verdict: proceed only with major revisions.** A second, focused review of the surface the first
> review did not cover (the dependency bundle, the offline build, the host-lifecycle `deps-bundle`
> feature, and the spine MUST). The hermeticity property is sound and worth pursuing, but the re-cut
> is not yet implementable: it under-specifies cargo's offline contract, omits the load-bearing
> host-lifecycle staging logic, mis-frames the bundle's reuse and ownership, and raises a
> mechanism to a spine MUST that is neither generically enforceable nor escapable as drafted.

This is a frozen record (2026-06-22). The plan is re-cut a third time in response.

## A correction to one lens

Lens C concluded "the pgs precedent does not exist (pgs rebuilds deps every run, never publishes a
bundle)." That reading came from the **stale local clone** at `/home/david/development/pgs-release`
(its `ffmpeg-release.yml` does rebuild from source, and it has no `build-deps.yml`). The
**canonical** `connollydavid/pgs-release` is newer and does implement the pattern: `build-deps.yml`
publishes the static sysroot as the `sysroot-v2` release (and raw dep tarballs under `deps-v1`), and
`ffmpeg-release.yml` has a "Download pre-built sysroot" step (`curl .../releases/download/sysroot-v2/...
| tar xz`) before building. The precedent stands; the plan's analogy is correct. Lens C's other
findings do not depend on this and remain valid.

## Blocking design gaps (to resolve in the re-cut)

**G1. host-prove has zero dependencies, so the "one reusable bundle for all three" is false.**
host-prove's lockfile is a single package (itself); host-lifecycle has 11; host-lint has 77 (the
superset, and lifecycle's third-party set is a subset of it). The bundle is effectively host-lint's
vendor set; host-lifecycle reuses it incidentally; host-prove vendors nothing and builds offline
trivially against an empty source set. Reframe: name host-lint the bundle owner, drop the
three-way-overlap claim, and state host-prove is in scope only for the static-musl plus `--network
none` mechanism, not the bundle.

**G2. host-lifecycle pins a stale host-lint git rev, so distribute-equals-certify is already broken
inside it.** host-lifecycle's `Cargo.toml` depends on `host-lint` at git rev `93a43fa` (the
pre-version-bump commit), while the certified `.host-software` host-lint pin is now `1386e9a`
(v0.8.1). host-lifecycle's binary therefore embeds an older host-lint than the one certified, and a
combined bundle would carry two host-lint revisions. Reconcile host-lifecycle's `host-lint` git rev
to the certified pin **before** any bundle is cut; this is a Readiness prerequisite, and it is a
latent inconsistency carried over from the plan/0028 cutover.

**G3. The host-lifecycle staging logic, the load-bearing part, is unspecified and not expressible
today.** `software_verify_build` checks out a throwaway `.host-verify` worktree at the pin and calls
`run_build_in_container`, which mounts only `src:/src`. There is no step to extract the vendor
tarball into the worktree and write the source-replacement config, so an in-container `cargo build
--offline` resolves nothing. And `run_build_in_container` takes `(runtime, image, build, src)` with
no component context and chooses the network only from the global `HOST_LIFECYCLE_DOCKER_NETWORK`
env, so it cannot pass `--network none` per-component. The re-cut must specify: a host-side
fetch-and-sha-verify, extraction into the build tree, a merge of the vendored-sources stanzas into
the existing `.cargo/config.toml`, and a network-mode parameter threaded into
`run_build_in_container` (bundle present implies `--network none`; absent keeps the env behaviour, so
the change is additive for not-yet-converted components).

**G4. The source-replacement config collides with the tracked `.cargo/config.toml`.** All three
tools already track a `.cargo/config.toml` carrying the reproducibility `--build-id=none` rustflag.
The `cargo vendor` `[source.*]` stanzas must be **merged into** that file, not overwrite it, or the
build-id flag is lost and the hash moves for the wrong reason. This also interacts with Readiness's
existing note that the musl image may shadow the flag via a `CARGO_TARGET_*_RUSTFLAGS` env; the
re-cut must reconcile all three edits to that one file and prove the double-build hash is unchanged.

## Bundle specifics (to tighten in the re-cut)

- **Two git sources, not one.** `cargo vendor` must replace both `host-grammar` and (for
  host-lifecycle) the `host-lint` git source; the exact `[source."git+...?rev=..."]` keys must match
  the lockfile byte-for-byte. Capture `cargo vendor`'s full stdout and commit it; the plan names only
  host-grammar.
- **Exact commands.** Multi-manifest vendoring needs `cargo vendor --locked --sync <manifest> ...`,
  not a bare `cargo vendor`; and `cargo vendor` must run `--locked` or it can silently update the
  lock and vendor a drifted set. The build flag is `--locked --offline` (or `--frozen`).
- **Bundle determinism is its own gate.** The tarball sha must be reproducible (normalized tar:
  `--sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner`, gzip `-n`), proven by a double-produce
  on two machines, or the published sha is a trusted blob, not a verifiable input. Add this to
  Readiness.
- **Bundle home: host-lint, not agentic-host.** Hosting the bundle on an agentic-host release would
  invert the dependency direction (the software's producer CI would build-depend on the host). Host
  it on host-lint's releases (it is the dep superset); host-lifecycle consumes host-lint's bundle (it
  already depends on host-lint); host-prove consumes nothing. Record this in Decisions, not as an
  execution detail.
- **One source of truth for the pin.** The `deps-bundle` pin lives in `.host-software` (agentic-host),
  but each producer CI (in its own repo) also needs the URL and sha to converge. Avoid two
  hand-edited copies: either commit a `deps-bundle.lock` in the producer repo that `software --check`
  asserts equals `.host-software`, or generate the producer CI from `.host-software`.
- **Scope the bundle to `--release`.** `cargo vendor` vendors the whole lockfile, including
  host-lint's `proptest` dev-dependency tree (60-plus crates, with proc-macros). Harmless for
  `cargo build --release`, but it bloats the bundle and, if offline `cargo test` is ever run, raises a
  host-target proc-macro question. State `--release`-only scope.
- **Release-build worktree hygiene.** `release` builds in the live canonical worktree, not a
  throwaway, so a staged `vendor/` and a config edit land in the tree the operator commits. Revert the
  edit and gitignore `vendor/` after the build so the worktree is not left dirty against the pin.
- **Bound the hermeticity claim.** The producer `cargo vendor` job and the gate-driver `cargo install
  --rev` seed are network-allowed by design; the MUST scopes only to the per-component container
  build. `install_hooks` only copies the artifact, so it stays bundle-unaware.

## The spine MUST: the decision the review forces

The fourth lens argues the MUST, as drafted (mandate the bundle mechanism, verified by `--network
none`), has four problems: (1) `--network none` proves no egress, not that the build consumed the
pinned bundle, so the real proof is bundle-sha verification plus a clean `CARGO_HOME`; (2) it is too
strong for a general adopter and has no escape, where the reproducible-build anchor it builds on
ships a `repro-exempt = call/NNNN` escape; (3) it is enforceable only for a component that opts in by
recording `deps-bundle`, so a static-shipping component that omits it is invisible to the gate, which
makes the universal wording unverifiable; (4) authoring a spine MUST inside an agentic-host project
plan and a project `call/` risks forking the spine, which the anti-ouroboros rule forbids.

The review's recommended shape, which preserves the MUST strength where it belongs:

- The spine requirement is the **property**: a component distributing release binaries MUST be able
  to reproduce them offline from pinned inputs. The bundle is the **recommended mechanism**,
  documented in build guidance, not itself the MUST.
- Ship a `hermetic-exempt = call/NNNN` escape, mirroring `repro-exempt`, so a non-pure-Rust adopter
  is not trapped.
- The **enforceable gate invariant** is honest and specific: a component that records a `deps-bundle`
  MUST build offline under `--network none` and its staged bundle sha MUST match the recorded hash.
- **Author in `host-template` first**, migrate onto agentic-host via the `UPGRADING.md` ledger and a
  `.host` baseline advance; the agentic-host `call/` records only the software decision (the
  `deps-bundle` production-anchor change, instance-scoped), never the methodology MUST.

This keeps a MUST (on the property), makes it general and escapable, makes the gate's claim match what
it checks, and respects copy-at-version. The operator chose a MUST; this refines where the MUST
attaches rather than reversing it.

## Per-lens verdicts

- cargo vendor and offline correctness: proceed-with-revisions (sound in principle; the offline
  contract, the two git sources, and the `--sync`/`--locked` commands must be specified and the
  config merge proven).
- host-lifecycle feature and bootstrap: blocking-incomplete (the staging logic and the `--network
  none` path do not exist yet and are the load-bearing work).
- bundle hosting, versioning, reuse: re-scope (host-prove has no deps, host-lifecycle pins a stale
  host-lint rev, the bundle home is a real dependency-inversion decision, and the pin has two sources
  of truth).
- spine MUST soundness and adopter impact: re-scope (attach the MUST to the property with an
  exemption and an honest gate invariant, author it in the template first).
