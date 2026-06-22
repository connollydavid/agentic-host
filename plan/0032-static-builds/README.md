# plan/0032: Static musl artifacts, the binary we ship is the binary we certify

> **Goal (re-cut to distribute-equals-certify, operator ruling 2026-06-22):** each host-* tool's
> distributed `x86_64-unknown-linux-musl` binary becomes a statically linked build that is also the
> `.host-software` canonical artifact `--verify-build` reproduces. The release asset and the
> certified artifact become one file, built by one recorded recipe in one digest-pinned image. A
> static musl binary also runs on any Linux host regardless of libc or distro, which retires the
> `plan/0028` hook-portability divergence as a side effect. Depends on `plan/0028` and the
> reproducible-build production anchor (`plan/0005`, `plan/0006`).
>
> **Adversarially reviewed** (`design-review.md`, 5 lenses, re-scope) and re-cut to this goal. The
> review's findings are resolved below. The decisive change from the first draft: converging each
> producer's release CI onto the recorded recipe is now an in-scope deliverable, so
> distribute-equals-certify holds by construction rather than by claim.

## Context

The reproducible-build anchor reproduces, for each artifact-bearing tool, the `.host-software`
recipe inside the recorded digest-pinned `toolchain` container and checks the sha256 (`plan/0005`,
`plan/0006`). Today that recipe builds a glibc-dynamic `target/release/<bin>` in `rust:1.95.0`. Two
consequences:

- The certified binary is not the distributed one. Each producer's release CI already
  cross-compiles static musl assets (host-lint and host-lifecycle ship the full musl plus darwin
  and windows matrix), but it builds them on a stock runner with `rustup target add` and a plain
  `cargo build --release --target`, a different recipe from the one `--verify-build` reproduces. The
  project ships binaries the anchor never reproduced: the shipped artifact carries no
  reproducibility guarantee.
- The certified glibc binary does not run on a host with an older glibc (the dev WSL:
  `GLIBC_2.39 not found`), which is why `plan/0028`'s `--install-hooks` installed a local build
  instead of the canonical one.

The goal makes the distributed binary and the certified binary one file. A statically linked musl
binary is the right form: it is reproducible, it carries no glibc dependency so it runs on any Linux
host and in a distroless or Alpine image, and it is what the producer CI already ships. The work is
to build that one binary by the one recorded recipe in both places, the orchestration's
`--verify-build` and the producer's release job.

## Decisions (operator rulings, 2026-06-22)

1. **Distribute equals certify.** Each tool's `x86_64-unknown-linux-musl` release asset is built by
   the recorded `.host-software` recipe in the pinned image, so it is byte-identical to what
   `--verify-build` reproduces. This is the load-bearing deliverable the first draft omitted.
2. **Static musl, not an older-glibc image.** An older-glibc base image would fix only the
   dev-host-run symptom with a one-field change, and it still depends on a glibc floor, so it gives
   no distribution-portable binary. Static musl gives a single binary that runs on any Linux libc
   and distro, the distribution property the goal is about. The older-glibc option is recorded and
   rejected on that ground.
3. **All three artifact tools, and host-prove gains a release pipeline.** host-lint and
   host-lifecycle already ship release assets; host-prove ships none, so distribute-equals-certify
   is vacuous for it until it does. The plan adds a release job to host-prove's CI (the musl asset
   plus a tagged release), so all three distribute-equals-certify uniformly. This is the priced
   uniformity the review asked for, not unscoped padding.
4. **The recorded toolchain is `clux/muslrust:1.95.0-stable`, digest-pinned.** It ships the
   `x86_64-unknown-linux-musl` target and std at Rust 1.95.0. (`messense/rust-musl-cross` has no
   1.95.0 tag, so it is not a candidate.) The pinned digest is recorded in Readiness. The image is
   chosen for a deterministic toolchain version, not for hermeticity: the build still fetches the
   git and registry dependencies over the network, so it is not hermetic, and that claim is dropped.
5. **The anchor certifies `x86_64-unknown-linux-musl`.** That is the primary distributable and the
   CI gate's host arch. `attest-host` is OS-granular, not arch-granular, so x86_64 scope is enforced
   by the amd64 CI runner and the recorded target triple, not by the recipe. The other shipped
   assets are handled under "Cross-platform trust boundary" below.

## Per-component recipe change

For each of host-lint, host-lifecycle, host-prove, three `.host-software` lines move:

- `toolchain` = `clux/muslrust:1.95.0-stable@sha256:<digest recorded in Readiness>`.
- `build` = `CARGO_INCREMENTAL=0 cargo build --release --locked --target x86_64-unknown-linux-musl`,
  with the static-linking and build-id flags pinned in the recipe (see Readiness) rather than left
  to `.cargo/config.toml`, which a per-target image env var can shadow.
- `artifact` = `target/x86_64-unknown-linux-musl/release/<bin> <new sha256>`.

The crates are pure Rust with no C dependencies, so the musl target builds without a C cross-linker.

## Producer-CI convergence (the distribute-equals-certify deliverable)

Each producer's release job builds the `x86_64-unknown-linux-musl` asset by the recorded recipe: the
same `clux/muslrust:1.95.0-stable@sha256:...` image as a container job (not `rustup target add` on a
stock runner), `--locked`, `CARGO_INCREMENTAL=0`, and the same strip, build-id, and crt-static
flags. The uploaded asset is then byte-identical to the artifact `--verify-build` reproduces and the
sha recorded in `.host-software`. host-prove gains this release job (it has none today). The
darwin, windows, and arm64 matrix jobs keep their mechanism but see the trust boundary below.

## Readiness (blocking gates, before any hash is recorded)

1. Confirm and digest-pin `clux/muslrust:1.95.0-stable`; record the digest.
2. Prove a reproducible double-build of each tool in that image, and `readelf -n` the binary to
   confirm no `.note.gnu.build-id` section. If the image sets a
   `CARGO_TARGET_X86_64_UNKNOWN_LINUX_MUSL_RUSTFLAGS` that shadows `.cargo/config.toml`, move
   `--build-id=none` (and pin `+crt-static` and the static-PIE choice) into the recorded `build` via
   `RUSTFLAGS`, so the flags survive. No hash is recorded until the double-build reproduces.
3. Add the release job to host-prove's CI.

## Cutover (atomic re-release round, software-first)

The recipe change moves every artifact hash, so each tool re-releases through
`host-lifecycle release <c> --change-class neither` (a build-recipe change; patch bumps host-lint
0.8.2, host-lifecycle 0.19.3, host-prove 0.2.2). `current_version` reads the last tag, so a re-run
is version-idempotent. Per component: edit the three recipe lines in the working tree only (so
`release` reads them and builds the musl artifact), run `release`, push the producer worktree and
tag, then collect the new pin and hash. The musl-edited `.host-software` is never committed to main
with a stale hash or pin: one host commit carries the toolchain, build, artifact path and hash, pin,
and back-filled receipts together, or `--verify-build` reddens CI at the old pin.

Two `plan/0028`-class steps recur:

- Before `--install-hooks`, the musl binary must exist at the new recipe path in
  `software/host-lint/main`. Produce it by the recorded recipe (the `release` or `--verify-build`
  container build, copied into the canonical worktree, or a local musl build), since the old
  `target/release/host-lint` workaround path no longer matches the recipe. The installed canonical
  musl binary then runs on the dev host, so the `plan/0028` local-build divergence retires for the
  hook binary.
- After host-lifecycle's own re-release, reinstall the gate driver from the released 0.19.3 commit
  before the final whole-suite green.

## Cross-platform trust boundary

`x86_64-unknown-linux-musl` is reproducibility-certified by `--verify-build`.
`aarch64-unknown-linux-musl` may be added as a second recorded build with its own sha (the CI matrix
already produces it) if an arm gate host is available; until then it is a shipped-but-uncertified
asset. The darwin and windows assets are cross-OS and stay distributables, not anchor artifacts;
reproducing them needs platform runners, a separate and larger effort. The release publishes a
checksums manifest for every asset, and the plan states plainly that only the linux-x86_64-musl
asset is reproducibility-certified, so the trust boundary is explicit at the release surface rather
than implied.

## Verification (whole-suite green)

- Each tool's `x86_64-unknown-linux-musl` build reproduces one sha256 on a double build in the
  pinned image (build-id-free, confirmed by `readelf`), recorded as the canonical artifact.
- `software --verify-build .` green for all three under the released pinned host-lifecycle.
- The producer release job's uploaded `x86_64-unknown-linux-musl` asset byte-matches the recorded
  canonical sha for that tag (the distribute-equals-certify check, true by construction).
- `software --install-hooks .` installs the canonical musl host-lint, and the installed
  `commit-msg` hook runs on the dev host.
- `software --check`, `book --check`, the cold-clone CI job, and the commit-hook tell test stay
  green; whole-suite green across every repo.

## Risks / honesty

- **The build is not hermetic** (the git and registry dependencies fetch over the network); the
  pinned image buys a deterministic toolchain version, not network isolation. Vendoring plus
  `--network none` is a possible later hardening, out of scope here.
- **A second full re-release round** so soon after the `plan/0028` cutover, and it now also covers
  the producer-CI convergence and the host-prove release pipeline. The cost is real, and it is the
  price of distribute-equals-certify. The `plan/0028` MEMORY lessons still apply: atomic re-pin,
  gate-driver reinstall, and the working-dir trap.
- **`attest-host` is OS-granular, not arch-granular**, so the anchor's x86_64 scope rests on the CI
  runner and target triple, not the recipe; an arch-level attest is a host-lifecycle feature
  request, out of scope.
- **Only the linux-x86_64-musl asset is reproducibility-certified**; arm64, darwin, and windows
  ship with a checksums manifest and are stated as uncertified, an explicit trust boundary.
- **musl reproducibility is proven in Readiness, not assumed** (the double-build and `readelf`
  gate); the build-id and crt-static flags are pinned in the recipe so an image env var cannot
  shadow them.

## Records

This plan, a new `call/` decision recording the distribute-equals-certify production-anchor change,
`PLAN.md`, `MEMORY.md`; re-pins, receipts, and the producer-CI convergence as the round lands, each
pushed in its own audited commit.
