# The host-* static-musl releases build hermetically against a pinned dependency bundle

- Status: accepted
- Date: 2026-06-22
- Scope: host-lint, host-lifecycle, host-prove (the artifact-bearing Where-room software)
- Relates: the spine MUST authored in `host-template` (`ecce498`, the methodology home for
  "a component shipping static release binaries reproduces them offline from pinned inputs");
  `plan/0032` (the milestone); `plan/0028` (the `GLIBC_2.39` divergence this retires);
  `call/0010` (the `.host-software` recipe); `call/0018` (discharge is re-derivation in a
  pinned toolchain, to which this adds offline hermeticity).

## Context and Problem Statement

The recorded canonical artifact for each host-* binary was a glibc-dynamic
`target/release/<bin>` built in `rust:1.95.0`, with the `host-grammar` git dependency and the
crates.io deps fetched over the network during the build. Two gaps followed:

- **Not portable.** The certified binary linked `GLIBC_2.39`, so it did not run on an older-glibc
  host. `plan/0028`'s `--install-hooks` had to fall back to a local build that differed from the
  canonical hash (sanctioned by `plan/0009`, but a standing divergence).
- **Not hermetic.** A network fetch at build time means the build inputs are not pinned, so the
  re-derivation `call/0018` relies on is not reproducible from a fixed input set.

The producer release CI separately cross-compiled a static-musl asset by a *different* recipe, so
the distributed binary was not the certified one (distribute did not equal certify).

## Decision

**The host-* artifact tools record a static `x86_64-unknown-linux-musl` canonical artifact, built
in a digest-pinned `clux/muslrust` image, offline against a pinned hash-verified
vendored-dependency bundle.**

- The `.host-software` recipe for each tool records the musl `toolchain` digest, a `build` that
  passes `--offline --target x86_64-unknown-linux-musl` (with `RUSTUP_TOOLCHAIN=stable`, the image
  std's toolchain name), and the musl `artifact` path and sha256.
- **host-lint owns the bundle.** Its dependency set is the superset, so it publishes the versioned
  hash-pinned `vendor-vN` release; host-lint and host-lifecycle record `deps-bundle = <url> <sha256>`
  and build under `--network none` after a verified download. Hosting the bundle on agentic-host
  would invert the host-to-software direction. (**Superseded in part by call/0043:** the shared-superset
  ownership is retired once host-lifecycle's dependencies diverge from host-lint's, so each artifact
  component self-owns its bundle on its own releases repo. The staged, hash-verified, no-egress build
  mechanism this decision records is unchanged.)
- **host-prove has no third-party dependencies**, so it builds `--offline` against an empty source
  set with no bundle (hermetic by emptiness, not by `--network none`).
- The methodology MUST is in the template, not here. This decision records only the host-* family
  adopting the production anchor as its first adopter, an instance-scoped software change.

## Consequences

- **Distribute equals certify.** Each producer release job builds the musl asset by the recorded
  recipe in the pinned image, so the shipped asset is byte-identical to the `--verify-build`
  artifact.
- **The `plan/0028` local-build workaround retires.** The canonical musl binary is static-pie and
  runs on any glibc, so `software --install-hooks` installs the canonical binary itself, verified
  against its recorded hash.
- **The bundle is a maintained, versioned input.** A dependency change requires a new `vendor-vN`,
  a re-pin in `.host-software` and the producer `deps-bundle.lock`, and a re-release.
  `software --check` enforces the drift between the two pins; `software --verify-build` enforces the
  two-part hermeticity (the staged-bundle sha matches *and* the build runs with no egress).
- **Reproducibility certification stays OS-granular** (`attest-host`): only linux-x86_64-musl is
  certified; other-platform assets ship with a checksums manifest, stated uncertified.

## Alternatives considered

- **A simpler older-glibc canonical image** (portability without musl): a single static binary on
  any libc was preferred over chasing a glibc floor, and musl is what the producer CI already
  distributed.
- **Fetch-at-build with a committed `Cargo.lock` only**: the lock pins versions but the build still
  reaches the network, so it is reproducible-ish but not hermetic; `--verify-build` could pass while
  consuming an upstream that later changes.
- **Vendoring the sources into each repo (no bundle)**: bloats every producer with the same tree and
  has no shared, hash-verifiable anchor; one published `vendor-vN` is checked once and consumed by
  both bundle-bearing tools.
