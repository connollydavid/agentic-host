# plan/0032: Hermetic static builds, distribute equals certify, via a pinned dependency bundle

> **Goal:** each host-* tool's distributed `x86_64-unknown-linux-musl` binary becomes a statically
> linked build that is also the `.host-software` canonical artifact `--verify-build` reproduces
> (distribute equals certify), and the build is genuinely hermetic: its dependencies come from a
> pinned, hash-verified bundle published as a downloadable release and consumed offline, not fetched
> at build time. The spine gains a MUST on the underlying property, and the host-* family is the
> first adopter. Depends on `plan/0028` and the reproducible-build anchor (`plan/0005`, `plan/0006`).
>
> **Adversarially reviewed twice** (`design-review.md`, then `design-review-2.md` on the bundle and
> spine surface) and re-cut three times. This version resolves the delta review: the MUST attaches to
> the property with a `hermetic-exempt` escape and an honest gate invariant, host-lint owns the
> bundle, host-prove is a no-dependency case, the host-lifecycle staging is specified, and the
> producer git-rev inconsistency is reconciled first.

## Context

The reproducible-build anchor reproduces each tool's `.host-software` recipe inside the recorded
digest-pinned `toolchain` container and checks the sha256 (`plan/0005`, `plan/0006`). Today that
recipe builds a glibc-dynamic `target/release/<bin>` in `rust:1.95.0`. Two gaps: the certified binary
does not run on a host with an older glibc (the `plan/0028` `GLIBC_2.39` divergence), and the build
fetches the `host-grammar` git dependency and the crates.io deps over the network, so it is not
hermetic. The producer release CI separately cross-compiles static musl assets by a different recipe,
so the shipped binary is not the certified one.

The canonical `connollydavid/pgs-release` solved the analogous problem: `build-deps.yml` builds the
static dependency sysroot once and publishes it as the `sysroot-v2` release, and `ffmpeg-release.yml`
downloads that pinned sysroot and builds against it rather than rebuilding from upstream. The build
inputs become one pinned, hash-verifiable bundle from the project's own release.

For the pure-Rust host-* tools the dependency layer is the cargo dependency set. The same pattern
applies: vendor the dependency sources once, publish them as a versioned hash-pinned release bundle,
and have each build download and verify that bundle and build offline. Combined with the static musl
link and a pinned toolchain image, the build is hermetic, reproducible, and portable, and the
certified artifact is the distributed one.

## Decisions (operator rulings, 2026-06-22)

1. **Distribute equals certify.** Each tool's `x86_64-unknown-linux-musl` release asset is built by
   the recorded recipe in the pinned image and bundle, byte-identical to what `--verify-build`
   reproduces.
2. **Static musl, not an older-glibc image.** Static musl gives a single binary that runs on any
   Linux libc and distro; an older-glibc image fixes only the dev-host-run symptom. Recorded and
   rejected on that ground.
3. **All three artifact tools convert; host-prove gains a release pipeline.** host-lint and
   host-lifecycle ship release assets; host-prove gains a release job (the musl asset plus a tagged
   release). All three get the static-musl plus offline `--network none` build.
4. **The recorded toolchain is `clux/muslrust:1.95.0-stable`, digest-pinned.** It ships the
   `x86_64-unknown-linux-musl` target and std at Rust 1.95.0.
5. **host-lint owns the dependency bundle.** host-lint's lockfile is the dependency superset
   (host-lifecycle's third-party set is a subset; host-prove has no third-party dependencies). The
   bundle is published on host-lint's releases as `vendor-vN`. host-lifecycle consumes host-lint's
   bundle (it already depends on host-lint); host-prove vendors nothing and builds offline against an
   empty source set. Hosting the bundle on host-lint, not agentic-host, keeps each tool depending only
   on host-lint and never inverts the host-to-software direction.
6. **The spine MUST is on the property, with an escape and an honest gate invariant.**
   `host-template` requires that a component distributing release binaries MUST be able to reproduce
   them offline from pinned inputs. The downloadable bundle is the recommended mechanism, documented in
   build guidance, not the MUST itself. A `hermetic-exempt = call/NNNN` escape (mirroring the anchor's
   `repro-exempt`) covers a component that cannot vendor offline (a fetching `build.rs`, or a non-Rust
   toolchain). The enforceable gate invariant is specific: a component that records a `deps-bundle`
   MUST build offline under `--network none`, and its staged bundle sha MUST match the recorded hash.
   The MUST is authored in `host-template` first and migrated onto agentic-host; the agentic-host
   `call/` records only the software decision (the `deps-bundle` production-anchor change,
   instance-scoped), never the methodology MUST.
7. **The anchor certifies `x86_64-unknown-linux-musl`.** `attest-host` is OS-granular, not
   arch-granular, so the x86_64 scope rests on the amd64 CI runner and the recorded target triple.
   arm64, darwin, and windows assets ship with a checksums manifest and are stated uncertified, an
   explicit trust boundary.

## The dependency bundle

- **Producer (on host-lint).** `cargo vendor --locked --sync <host-lifecycle>/Cargo.toml <out>` run
  from host-lint's manifest (host-prove contributes nothing) produces one vendor directory covering
  host-lint's superset plus host-lifecycle's git `host-lint` crate. Its full stdout is captured: the
  `[source.*]` block has three keys, `crates-io` and the two git sources (`host-grammar` and
  `host-lint`), whose `?rev=` keys must match the lockfiles byte-for-byte. The directory is tarred
  with normalized metadata (`tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner`, `gzip
  -n`) so the tarball sha is reproducible, published as `vendor-vN` with its sha recorded. The scope is
  `--release`; the vendored `proptest` dev-dependency tree is unused by the release build.
- **Consumer.** The build downloads `vendor-vN`, verifies the sha256, extracts it, merges the
  `[source.*]` stanzas into the existing `.cargo/config.toml` (preserving the build-id rustflags),
  and builds `--release --locked --offline --target x86_64-unknown-linux-musl` under `--network none`.
- **One source of truth for the pin.** The `deps-bundle = <url> <sha256>` pin lives in
  `.host-software`. Each producer CI needs the same url and sha to converge; rather than two
  hand-edited copies, the producer repo commits a `deps-bundle.lock` that `software --check` asserts
  equals `.host-software`, so drift fails the gate.

## The host-lifecycle feature

`host-lifecycle` gains a `deps-bundle` recipe field and a bundle-staging step shared by
`--verify-build` and `release`: fetch the bundle on the host (the one controlled, pinned download),
verify its sha256, extract it into the build worktree's `vendor/`, and merge the vendored-sources
`[source.*]` stanzas into that worktree's `.cargo/config.toml`. `run_build_in_container` gains a
network-mode parameter: a bundle-bearing component builds under `--network none`; a component with no
`deps-bundle` keeps the existing `HOST_LIFECYCLE_DOCKER_NETWORK` behaviour, so the change is additive
for not-yet-converted components. The gate asserts the staged bundle sha matches the recorded hash
before building (the provenance proof; `--network none` is the egress proof). After a `release`
build, the staged config edit is reverted and `vendor/` removed so the canonical worktree is not left
dirty; `vendor/` is gitignored in each producer. `install_hooks` only copies the artifact, so it
stays bundle-unaware. The producer `cargo vendor` job and the gate-driver `cargo install --rev` seed
are network-allowed by design; the MUST scopes only to the per-component container build.

## The spine change (host-template)

`host-template` build guidance gains the property MUST and documents the bundle as the recommended
mechanism, plus the `hermetic-exempt = call/NNNN` escape and the `deps-bundle` recipe field and its
gate invariant. An `UPGRADING.md` ledger entry records the requirement with a machine-checkable verify
command, and the migration applies it onto agentic-host (the `.host` baseline advances and is
re-recorded). The host-* tools are the first adopters; the methodology is authored in the template,
not forked in the instance.

## Per-component recipe change

For host-lint and host-lifecycle (and host-prove for the toolchain and offline build, with no bundle):

- `toolchain` = `clux/muslrust:1.95.0-stable@sha256:<digest recorded in Readiness>`.
- `deps-bundle` = `<host-lint vendor-vN url> <sha256>` (host-lint and host-lifecycle; host-prove omits
  it and builds offline against an empty source set).
- `build` = `CARGO_INCREMENTAL=0 cargo build --release --locked --offline --target x86_64-unknown-linux-musl`,
  with the static-linking and build-id flags pinned in the recipe (see Readiness).
- `artifact` = `target/x86_64-unknown-linux-musl/release/<bin> <new sha256>`.

## Producer-CI convergence (distribute equals certify)

Each producer's release job builds the `x86_64-unknown-linux-musl` asset by the recorded recipe: the
pinned `clux/muslrust:1.95.0-stable` image as a container job, the downloaded `vendor-vN` bundle (per
its committed `deps-bundle.lock`), `--locked --offline`, and the same strip, build-id, and crt-static
flags. The uploaded asset is then byte-identical to the artifact `--verify-build` reproduces. The
arm64, darwin, and windows matrix jobs keep their mechanism but see the trust boundary in decision 7.

## Readiness (blocking gates, before any hash is recorded)

1. **Reconcile** host-lifecycle's `host-lint` git dependency to the certified host-lint pin (it
   currently pins the pre-bump `93a43fa`, not the released `1386e9a`), so the host-lint inside
   host-lifecycle is the certified one and the bundle carries a single host-lint revision.
2. Confirm and digest-pin `clux/muslrust:1.95.0-stable`; record the digest.
3. Produce the `vendor-vN` bundle (`cargo vendor --locked --sync`), capture and commit the full
   `[source.*]` config, normalize the tarball, and prove the bundle sha double-produces on two
   machines before recording it. Publish it on host-lint with a `deps-bundle.lock`.
4. Add the `deps-bundle` field, the staging step, the config merge, and the `--network none` path to
   `host-lifecycle` (`run_build_in_container`, `software_verify_build`, `release`, and the
   `software --check` sha-and-drift assertions); unit-test it.
5. Prove a reproducible double-build of each tool in the pinned image, offline against the bundle,
   under `--network none`; `readelf -n` confirms no `.note.gnu.build-id`. If the image shadows
   `.cargo/config.toml` via a `CARGO_TARGET_*_RUSTFLAGS`, move the build-id and crt-static flags into
   the recorded `build` via `RUSTFLAGS`. Prove the config merge leaves the artifact hash unchanged.
6. Add the release job to host-prove's CI.
7. Author the spine change in `host-template` first and push it before the migration: the property
   MUST with its recommended-bundle guidance, and the `hermetic-exempt` escape. Define the
   `deps-bundle` gate invariant and add an `UPGRADING.md` ledger entry there as well.

## Cutover (atomic re-release round, software-first)

The recipe change moves every artifact hash, so each tool re-releases through
`host-lifecycle release <c> --change-class <class>` (host-lint and host-prove are fix-only patch bumps,
0.8.2 and 0.2.2; host-lifecycle adds the `deps-bundle` feature, so a minor bump to 0.20.0). Per
component: edit the recipe lines in the working tree, run `release` (which stages the bundle and
builds offline in the pinned image), push the producer worktree and tag, then collect the new pin and
hash. The musl-and-bundle-edited `.host-software` is never committed to main with a stale hash or pin:
one host commit carries the toolchain, deps-bundle, build, artifact path and hash, pins, and
back-filled receipts together. The spine migration (the `.host` baseline advance) lands with it or in
its own audited commit. The `plan/0028`-class recurrences carry over: place the musl binary at the new
recipe path before `--install-hooks`, and reinstall the host-lifecycle gate driver from its released
commit before the final green.

## Verification (whole-suite green)

- The `vendor-vN` bundle tarball sha double-produces on two machines (a verifiable input).
- Each tool's `x86_64-unknown-linux-musl` build reproduces one sha256 on a double build in the pinned
  image, offline against the bundle under `--network none`, build-id-free (confirmed by `readelf`).
- `software --verify-build .` green for all three under the released pinned host-lifecycle: the staged
  bundle sha matches the recorded hash and the build runs with no network (the two-part hermeticity
  proof, provenance plus egress).
- The producer release asset byte-matches the recorded canonical sha for that tag (distribute equals
  certify), and `software --check` confirms the producer `deps-bundle.lock` equals `.host-software`.
- `software --install-hooks .` installs the canonical musl host-lint, which runs on the dev host.
- `host-lifecycle upgrade .` shows the new baseline (the property MUST applied); `software --check`,
  `book --check`, the cold-clone CI job, and the commit-hook tell test stay green; whole-suite green
  across every repo.

## Risks / honesty

- **This is a large milestone**: a `host-lifecycle` feature (the `deps-bundle` field, the staging,
  the config merge, the network-mode threading, the sha-and-drift gate), a producer bundle workflow on
  host-lint, a spine MUST with its migration, the producer-CI convergence, the host-prove release
  pipeline, the static musl conversion, and a software-first re-release round. The cost is deliberate,
  the price of a verifiable hermetic distribute-equals-certify build.
- **The hermeticity proof is two-part, not one.** `--network none` proves no egress; the staged-bundle
  sha match proves provenance. Both are gate assertions, since `--network none` alone could pass while
  consuming an image-baked cache.
- **`host-lifecycle` consumes host-lint's bundle**, a controlled pinned download that precedes the
  network-free build; the producer `cargo vendor` and the gate-driver seed are network-allowed by
  design and are not gated.
- **The bundle is versioned and maintained**: a dependency change requires a new `vendor-vN`, a re-pin
  in `.host-software` and the producer `deps-bundle.lock`, and a re-release. The `software --check`
  drift assertion keeps the two pins in step.
- **`attest-host` is OS-granular, not arch-granular**; only the linux-x86_64-musl asset is
  reproducibility-certified, the others ship with a checksums manifest and are stated uncertified. An
  arch-level attest is a host-lifecycle feature request, out of scope.

## Records

The `host-template` build guidance, its `UPGRADING.md` ledger entry, and the re-recorded `.host`
baseline (the methodology MUST, authored in the template first); `call/0021` recording only the
software `deps-bundle` production-anchor change (instance-scoped); this plan, `PLAN.md`, `MEMORY.md`;
re-pins, receipts, the host-lint bundle release, and the producer-CI convergence as the round lands,
each pushed in its own audited commit.

## Landed (2026-06-22)

The software-first re-release round and the atomic agentic-host change shipped:

| component | tag | pin | static-musl artifact sha256 |
|---|---|---|---|
| host-lint | `v0.8.2` | `ba479258` | `a099c27d8ce3912bec11f4f7e2140ef37b5c8d03f320aad2a882244e98f8bac8` |
| host-prove | `v0.2.2` | `3ca95fc0` | `520cdd109d96c8996402792065cd9c0198f13f97ebefd62ff15edb8c0030f366` |
| host-lifecycle | `v0.20.0` | `a38b0c07` | `7d0903340be787183661c4cb933af82886f22af436a179e8a856117386d950d0` |

Each artifact reproduced offline in `clux/muslrust:1.95.0-stable@sha256:15a72a4a…` against the pinned
`vendor-v1` bundle (sha `f1141763…`), host-prove against an empty source set. One atomic commit
(`86e19db`) re-pinned `.host-software`, back-filled the three release receipts, recorded `ecce498`
applied, and bumped the `host-template` pointer to `455fba8`. The released `0.20.0` binary gated
green: `software --check`, `software --verify-build` (reproduces all three offline under
`--network none`), `book --check`, and the commit-hook tell test; `--install-hooks` installed the
canonical musl host-lint, retiring the `plan/0028` local-build workaround. agentic-host CI re-pinned
to the certified `0.20.0` (`eff82b8`).
