# plan/0032: Hermetic static builds, distribute equals certify, via a pinned dependency bundle

> **Goal (re-cut to hermetic-via-bundle, operator rulings 2026-06-22):** each host-* tool's
> distributed `x86_64-unknown-linux-musl` binary becomes a statically linked build that is also the
> `.host-software` canonical artifact `--verify-build` reproduces (distribute equals certify), and
> the build is genuinely hermetic: its dependencies come from a reusable, versioned, hash-pinned
> bundle published as a downloadable release and consumed offline, not fetched from upstreams at
> build time. The pattern (build the dependency layer once, publish it as a release, download and
> verify it, build with no network) is the `pgs-release` `sysroot-vN`/`deps-vN` pattern. This plan
> makes that pattern a **spine MUST** for any project shipping static release binaries, and applies
> it to the host-* family. Depends on `plan/0028` and the reproducible-build anchor (`plan/0005`,
> `plan/0006`).
>
> **Adversarially reviewed** (`design-review.md`, 5 lenses, re-scope) and re-cut twice: first to
> distribute-equals-certify, then to fold in the dependency-bundle hermeticity mechanism and the
> spine requirement. The bundle is the proper resolution of the review's M5 finding (the dropped
> hermeticity claim): with deps pinned in a downloaded bundle and the build run under `--network
> none`, the recorded build is network-free, so `--verify-build` enforces hermeticity rather than
> the plan merely asserting it.

## Context

The reproducible-build anchor reproduces each tool's `.host-software` recipe inside the recorded
digest-pinned `toolchain` container and checks the sha256 (`plan/0005`, `plan/0006`). Two gaps
remain: the certified binary is glibc-dynamic and does not run on a host with an older glibc (the
`plan/0028` `GLIBC_2.39` divergence), and the build is not hermetic, since it fetches the
`host-grammar` git dependency and the crates.io deps over the network (the design-review's M5). The
producer release CI separately cross-compiles static musl assets by a different recipe, so the
shipped binary is not the certified one.

`pgs-release` solved the equivalent problem for a heavier dependency layer. Its `build-deps.yml`
builds the static dependency sysroot (zlib, freetype, fribidi, harfbuzz, libass) once per platform
and publishes it as a versioned GitHub release (`sysroot-v2`, with raw dep tarballs under
`deps-v1`); its `ffmpeg-release.yml` then downloads that pinned sysroot and builds against it rather
than rebuilding the dependency chain from upstream each run. The build inputs become one pinned,
hash-verifiable bundle from the project's own release, not many upstream fetches.

For the pure-Rust host-* tools the dependency layer is the cargo dependency set (the tools share
almost all of it). The same pattern applies: vendor the shared dependency sources once, publish them
as a versioned hash-pinned release bundle, and have every build download and verify that bundle and
build offline. Combined with the static musl link and a pinned toolchain image, the build is
hermetic, reproducible, and portable, and the certified artifact is the distributed one.

## Decisions (operator rulings, 2026-06-22)

1. **Distribute equals certify.** Each tool's `x86_64-unknown-linux-musl` release asset is built by
   the recorded recipe in the pinned image and bundle, so it is byte-identical to what
   `--verify-build` reproduces.
2. **Static musl, not an older-glibc image.** Static musl gives a single binary that runs on any
   Linux libc and distro, the distribution property the goal is about; an older-glibc image would
   fix only the dev-host-run symptom and still carry a glibc floor. Recorded and rejected on that
   ground.
3. **All three artifact tools, and host-prove gains a release pipeline.** host-lint and
   host-lifecycle already ship release assets; host-prove ships none, so it gains a release job (the
   musl asset plus a tagged release) and converts too, so all three distribute-equals-certify
   uniformly.
4. **The recorded toolchain is `clux/muslrust:1.95.0-stable`, digest-pinned.** It ships the
   `x86_64-unknown-linux-musl` target and std at Rust 1.95.0.
5. **Hermeticity via a reusable downloadable dependency bundle.** Vendor the host-* dependency set
   once, publish it as a versioned, hash-pinned release bundle (e.g. `vendor-v1`), and consume it
   offline. The build downloads and sha256-verifies the bundle, source-replaces onto the vendored
   crates, and runs `cargo build --release --locked --offline` under `--network none`. This is the
   real resolution of the dropped hermeticity claim.
6. **The pattern is a spine MUST.** `host-template` gains a requirement: a project that ships static
   or hermetic release binaries MUST build its dependency layer once, publish it as a reusable
   versioned hash-pinned downloadable release bundle, and have downstream builds consume that pinned
   bundle offline rather than fetch dependencies at build time. Applied through an `UPGRADING.md`
   ledger entry and the migration onto agentic-host, and made verifiable: the recorded build runs
   with no network, so a build that reaches for the network fails the gate.
7. **The anchor certifies `x86_64-unknown-linux-musl`.** `attest-host` is OS-granular, not
   arch-granular, so the x86_64 scope rests on the amd64 CI runner and the recorded target triple.
   arm64, darwin, and windows assets ship with a checksums manifest and are stated uncertified, an
   explicit trust boundary.

## The dependency bundle (producer, consumer, tooling)

- **Producer.** A workflow runs `cargo vendor` over the three tools' lockfiles (`cargo vendor`
  vendors the crates.io deps and the `host-grammar` git dependency), tarballs the vendor directory,
  computes its sha256, and publishes it as a versioned release (`vendor-vN`) with the tarball and the
  recorded hash. Reusable: one bundle serves all three tools, since their dependency sets overlap.
  Versioned: bump `vendor-vN` only when the dependency set changes, so the input is stable.
- **Consumer.** The build downloads `vendor-vN`, verifies the sha256, extracts it, source-replaces
  crates-io and the git source onto the vendored directory via `.cargo/config.toml`, and builds
  `--release --locked --offline` with no network.
- **Tooling.** `host-lifecycle` gains a `deps-bundle = <url> <sha256>` recipe field; `--verify-build`
  and `release` fetch and verify the bundle on the host (the one controlled, pinned download), stage
  it into the build mount, and run `run_build_in_container` with `--network none`. The
  `HOST_LIFECYCLE_DOCKER_NETWORK` escape is retired for these components, since the build no longer
  needs network. This is the verifiable form of the MUST: the gate proves the build is network-free.

## The spine change (host-template)

`host-template` gains the MUST in its build guidance (the analog of `pgs-release`'s "Static Builds"
rule, raised to the dependency-bundle pattern), an `UPGRADING.md` ledger entry that records the new
requirement and a machine-checkable verify command, and the migration applies it onto agentic-host
(the `.host` baseline advances and is re-recorded). The host-* tools are the first adopters.

## Per-component recipe change

For each of host-lint, host-lifecycle, host-prove, the `.host-software` stanza gains and moves:

- `toolchain` = `clux/muslrust:1.95.0-stable@sha256:<digest recorded in Readiness>`.
- `deps-bundle` = `<vendor-vN release url> <sha256>`.
- `build` = `CARGO_INCREMENTAL=0 cargo build --release --locked --offline --target x86_64-unknown-linux-musl`,
  with the static-linking and build-id flags pinned in the recipe (see Readiness).
- `artifact` = `target/x86_64-unknown-linux-musl/release/<bin> <new sha256>`.

The crates are pure Rust with no C dependencies, so the musl target builds without a C cross-linker.

## Producer-CI convergence (distribute equals certify)

Each producer's release job builds the `x86_64-unknown-linux-musl` asset by the recorded recipe: the
pinned `clux/muslrust:1.95.0-stable` image as a container job, the same downloaded `vendor-vN`
bundle, `--locked --offline`, and the same strip, build-id, and crt-static flags. The uploaded asset
is then byte-identical to the artifact `--verify-build` reproduces and the sha recorded in
`.host-software`. host-prove gains this release job. The arm64, darwin, and windows matrix jobs keep
their mechanism but see the trust boundary in decision 7.

## Readiness (blocking gates, before any hash is recorded)

1. Confirm and digest-pin `clux/muslrust:1.95.0-stable`; record the digest.
2. Produce the `vendor-vN` bundle (`cargo vendor` over the three lockfiles), publish it as a release,
   and record its sha256.
3. Add `deps-bundle` support and the `--network none` offline build to `host-lifecycle`
   (`run_build_in_container`, `software_verify_build`, `release`); unit-test it.
4. Prove a reproducible double-build of each tool in the pinned image, offline against the bundle,
   under `--network none`; `readelf -n` the binary to confirm no `.note.gnu.build-id`. If the image
   shadows `.cargo/config.toml` with a `CARGO_TARGET_*_RUSTFLAGS`, move the build-id and crt-static
   flags into the recorded `build` via `RUSTFLAGS`. No hash is recorded until the offline double-build
   reproduces.
5. Add the release job to host-prove's CI.
6. Author the spine MUST in `host-template` plus its `UPGRADING.md` ledger entry.

## Cutover (atomic re-release round, software-first)

The recipe change moves every artifact hash, so each tool re-releases through
`host-lifecycle release <c> --change-class neither` (patch bumps host-lint 0.8.2, host-prove 0.2.2;
host-lifecycle bumps for both the `deps-bundle` feature and the recipe, a feature, so
`--change-class adds-flag`, a minor bump to 0.20.0). Per component: edit the recipe lines in the
working tree, run `release` (which builds offline against the bundle in the pinned image), push the
producer worktree and tag, then collect the new pin and hash. The musl-and-bundle-edited
`.host-software` is never committed to main with a stale hash or pin: one host commit carries the
toolchain, deps-bundle, build, artifact path and hash, pins, and back-filled receipts together. The
spine migration (the `.host` baseline advance) lands with it or in its own audited commit. The
`plan/0028`-class recurrences carry over: place the musl binary at the new recipe path before
`--install-hooks`, and reinstall the host-lifecycle gate driver from its released commit before the
final green.

## Verification (whole-suite green)

- Each tool's `x86_64-unknown-linux-musl` build reproduces one sha256 on a double build in the
  pinned image, offline against the pinned bundle under `--network none`, build-id-free (confirmed by
  `readelf`).
- `software --verify-build .` green for all three under the released pinned host-lifecycle, with no
  network reachable during the build (the hermeticity gate, the verifiable form of the MUST).
- The producer release job's uploaded `x86_64-unknown-linux-musl` asset byte-matches the recorded
  canonical sha for that tag (distribute equals certify, true by construction).
- `software --install-hooks .` installs the canonical musl host-lint, and the installed `commit-msg`
  hook runs on the dev host.
- `host-lifecycle upgrade .` shows the new baseline (the spine MUST applied); `software --check`,
  `book --check`, the cold-clone CI job, and the commit-hook tell test stay green; whole-suite green
  across every repo.

## Risks / honesty

- **This is a large milestone**, larger than the first draft: it adds a `host-lifecycle` feature (the
  `deps-bundle` field and the offline `--network none` build), a producer bundle workflow, a spine
  MUST with its migration, the producer-CI convergence, and the host-prove release pipeline, on top
  of the static musl conversion and a software-first re-release round. The cost is deliberate, the
  price of a verifiable hermetic distribute-equals-certify build. The `plan/0028` MEMORY lessons
  (atomic re-pin, gate-driver reinstall, the working-dir trap) carry over.
- **`host-lifecycle` consumes its own bundle**, a bootstrap step: the gate driver that runs the
  offline build is seeded from its released commit, and the bundle it downloads is pinned by sha, so
  the controlled download precedes the network-free build, as in the `pgs-release` sysroot download.
- **`cargo vendor` must capture the `host-grammar` git dependency**, not only crates.io; the bundle
  and the source-replacement config must cover the git source, or the offline build fails to resolve
  it. Readiness proves the offline build before any hash is recorded.
- **The bundle is versioned and maintained**: a dependency change requires a new `vendor-vN` and a
  re-pin. The bundle's host location (an agentic-host release or a dedicated deps location) is an
  execution detail settled in Readiness.
- **`attest-host` is OS-granular, not arch-granular**, so the x86_64 scope rests on the CI runner and
  target triple; an arch-level attest is a host-lifecycle feature request, out of scope. Only the
  linux-x86_64-musl asset is reproducibility-certified; the other assets ship with a checksums
  manifest and are stated uncertified.

## Records

This plan, a new `call/` decision recording the hermetic-bundle production-anchor change and the
spine MUST, `PLAN.md`, `MEMORY.md`, the `host-template` `UPGRADING.md` ledger entry and the re-recorded
`.host` baseline; re-pins, receipts, the bundle release, and the producer-CI convergence as the round
lands, each pushed in its own audited commit.
