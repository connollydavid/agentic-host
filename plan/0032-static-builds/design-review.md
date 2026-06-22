# plan/0032 design-review

> **Verdict: re-scope (proceed only with major revisions).** Five independent adversarial lenses
> (reproducibility, bootstrap/self-cert, re-release ordering, scope/cross-platform,
> altitude/necessity) reviewed the plan. Three returned *re-scope*, one *blocking-incomplete*, one
> *proceed-with-revisions*. The musl-cross image the plan needs does exist and is digest-pinnable,
> and the re-release mechanics are sound, but three headline payoffs are over-claimed or false, two
> execution hazards are unstated, and the simplest alternative was never weighed. The kernel
> survives only once the actual goal is restated.

This review is a frozen record. It captures the findings as of 2026-06-22; the plan is re-cut in
response, and the re-cut supersedes the plan text the findings critique.

## Method

Five lenses, each an independent reviewer reading the plan plus the relevant source
(`host-lifecycle` `run_release`/`software_verify_build`/`install_hooks`/`run_build_in_container`,
`.host-software`, the producer CI workflows, and the `plan/0028` MEMORY lessons). Each returned up
to six findings with evidence and a fix. The findings below are consolidated and de-duplicated
across lenses; the per-lens verdicts are listed at the end.

## Blocking findings

**B1. The motivating breakage is sanctioned by design, not a defect (necessity).** The canonical
binary is *executed* in exactly one place, `install_hooks` copying it into `.git/hooks`;
`--verify-build` and `--check` only *hash* it. The reproducibility anchor never needs the canonical
binary to run on the dev host. The one place that runs it already has a designed fallback: the
local build, whose hash-mismatch note is "informational, not a gate" (the comment at
`install_hooks` ~line 1213, and the `plan/0009` decision that the install gate is worktree-at-pin,
not byte-hash, recorded in MEMORY). So the concrete current breakage the switch removes is
cosmetic: the recorded and runnable binaries become the same file. The plan must name a concrete
non-cosmetic breakage or concede the motivation is aesthetic.

**B2. "Certify the binary we distribute" is false against the producer CI.** `--verify-build`
reproduces the recipe inside the recorded digest-pinned `toolchain` container with `--locked` and
the strip/build-id hardening. Each producer's release CI builds its musl assets with a different,
non-hermetic recipe: `rustup target add` plus a plain `cargo build --release --target` on a stock
`ubuntu-latest`, no `--locked`, no pinned image, no reproducible double-build (host-lint
`ci.yml:42-47`, host-lifecycle likewise; host-prove has no musl build at all). Two different
toolchains do not byte-match. So the recorded canonical artifact will not equal the shipped release
asset, and the "distribute one, certify another" gap does not close, it moves. Delivering this
claim requires converting each producer's release job to build the canonical in the same pinned
image, which the plan never scopes.

**B3. `--install-hooks` MISSes the musl artifact, and a premature recipe push reddens CI.** After
the recipe edit, `install_hooks` reads `worktree.join("target/x86_64-unknown-linux-musl/release/<bin>")`
and exits 1 with `MISSING ... build the component first` unless that file is already in the
canonical worktree. Nothing in the dev flow puts it there: `--verify-build` builds into a throwaway
`.host-verify` worktree it removes immediately, and the `plan/0028` local-build workaround built the
glibc path `target/release/<bin>`, which no longer matches the recipe. Separately, if the
musl-edited `.host-software` (new build/artifact path) is committed and pushed to main while the
recorded hash is still the old glibc sha and the pin is still the old commit, the next push runs
`reproducible-build.yml`, whose `--verify-build` rebuilds at the old pin in the new recipe and
DRIFTs against the stale hash, RED. Both need explicit handling: a step that produces the musl
binary at the new path before `--install-hooks`, and an atomic-sequence rule that the recipe edit,
new hash, new pin, and receipts land in one commit and never split across a push.

## Major findings

**M1. The simpler alternative was never weighed (altitude).** glibc is forward-compatible, so
building the canonical glibc binary in an *older-glibc* base image (an older debian/rust image)
yields a canonical binary that runs on the dev WSL by changing one field, the `toolchain` digest,
with no target flag, no musl-cross image hunt, no host-prove work, and no allocator footnote. The
plan weighs only musl-internal alternatives (pinned image versus in-recipe target-add) and never
records why an older-glibc canonical is rejected. Per the spine's "describe the simpler approach,"
this must be weighed explicitly or adopted.

**M2. Wrong altitude: two concerns folded into one file.** The canonical reproducibility artifact
(the thing `--verify-build` hashes, which wants the simplest deterministic build) and the portable
runnable binary (needed only by the hook install, and already produced by CI as a release asset)
are distinct. Folding portability into the anchor adds a static-musl constraint to a file whose job
is byte-reproducibility and drags in the hermeticity worry the plan then has to defend. If hook
portability is genuinely wanted, fix it at the layer that needs it (have the hook install consume
the verified CI musl asset, or keep the local-build fallback) and leave the anchor the simplest
build.

**M3. host-prove conversion is scope creep.** Only host-lint carries `hooks = pre-commit`;
host-prove and host-lifecycle binaries are never installed as hooks, so the `GLIBC_2.39` motivation
does not apply to them. host-prove additionally ships no release asset today (its CI is a single
smoke job with no release pipeline), so "recorded artifact equals distributed asset" has nothing to
match. Converting host-prove plus building out its musl CI is uniformity-only work smuggled under a
hook-portability headline. Cut it from this plan, or decide and price it as its own line item.

**M4. "Any Linux" conflates OS with architecture.** A static musl x86_64 binary runs on any Linux
with an x86_64 kernel, not on aarch64 Linux, darwin, or windows. `attest-host` gates on
`std::env::consts::OS` only (linux/macos/windows), with no arch dimension, and the current flat
stanza form (no `attest-host`) attests on *any* host. So on an aarch64 Linux dev or CI host the
recorded x86_64-musl recipe would attempt an x86_64 build and DRIFT rather than skip, and the
producer's shipped aarch64/darwin/windows assets are never reproducibility-certified. The plan must
scope the anchor to x86_64 Linux explicitly and decide the fate of the other shipped assets (record
per-platform builds with their own shas, or declare them uncertified at the release surface).

**M5. The "hermetic / no network fetch" rationale for the image is largely false.** The build
already fetches the `host-grammar` git dependency and the crates.io deps over the network (no
vendor dir, no `--offline`, and `run_build_in_container` deliberately omits `--network none` and
exposes `HOST_LIFECYCLE_DOCKER_NETWORK` precisely because network is needed). Preinstalling the
musl std removes only the `rustup target add` fetch, a tiny slice of the network surface. Either
drop the hermeticity claim and pick the image on the honest grounds (it ships the musl target), or
actually vendor the deps and assert `--network none`.

**M6. musl reproducibility is asserted, not proven.** `--build-id=none` is injected via
`.cargo/config.toml` scoped to `cfg(target_os = "linux")` (which includes musl), but a musl-cross
image can set `CARGO_TARGET_X86_64_UNKNOWN_LINUX_MUSL_RUSTFLAGS`, which fully *replaces* the config
`target.*.rustflags` (cargo does not merge), silently dropping the flag; and static linking depends
on `+crt-static` and static-PIE defaults that have varied by rustc version and image. The Readiness
step must double-build in the candidate image and `readelf -n` the binary to confirm no build-id and
a stable hash *before* recording it, and pin the full linking configuration, not just the target
triple.

## Confirmed (what survives)

- The image exists and is digest-pinnable: `clux/muslrust:1.95.0-stable` (last built 2026-05-27).
  `messense/rust-musl-cross` has no 1.95.0 tag (rolling stable), so it is not a co-equal candidate.
- `--change-class neither` is the correct class for a build-recipe change; it yields patch bumps
  (host-lint 0.8.2, host-lifecycle 0.19.3, host-prove 0.2.1 to 0.2.2), and `current_version` reads
  the last tag, so a re-run is version-idempotent.
- `run_release` reads the on-disk recipe, so editing `toolchain`/`build` first makes `release`
  build the musl artifact and compute the right hash; the per-component interleave (edit recipe in
  the working tree, release, push the producer tag, then re-pin) is sound.
- host-lifecycle re-releasing itself works (the container build is independent of the glibc-local
  driver); the gate driver must be reinstalled from the released commit before the final green.
- Adding a toolchain to the three artifact tools and not to repo-only `host`/`host-grammar` raises
  no gate inconsistency.

## The pivotal question for the re-cut

The findings converge on one decision the plan never settles: **what is the actual goal?**

- **G1, hook portability only.** Make the canonical binary run on the dev host so the hook install
  stops diverging. Then the cheapest correct move is an older-glibc canonical image (M1), a
  one-field change, or doing nothing (B1, the local-build path is green by design). musl,
  all-three, and host-prove are unnecessary.
- **G2, distribute-equals-certify.** Make the shipped binary and the certified binary the same. The
  load-bearing work is converting each producer's release CI to build the canonical in the pinned
  image (B2); only then is musl-static the right choice, for distribution portability across any
  Linux x86_64. This is larger than the plan scoped and must be priced.

## Recommended re-cut decisions

1. State the goal (G1, G2, or both) before anything else; it determines the whole shape.
2. If G1: prefer the older-glibc image (or status quo); drop musl, drop host-prove, drop the
   byte-match claim.
3. If G2: scope in producer-CI convergence onto the recorded recipe; keep musl for portability;
   price the producer work.
4. Either way, scope the anchor to x86_64 Linux explicitly (M4) and decide the other assets' fate.
5. Cut host-prove unless G2 uniformity is chosen and priced (M3).
6. Make the musl-image digest confirmation and a reproducible double-build (build-id `readelf`
   check) a blocking Readiness gate, not a risk bullet (M6); pin the full linking config.
7. Fix or drop the hermeticity claim (M5).
8. Document the atomic re-pin sequence: recipe edits stay uncommitted until the producer tag is
   pushed, and one host commit carries toolchain, build, artifact path and hash, pin, and receipts
   (B3); add the explicit step that places the musl binary at the new path before `--install-hooks`.

## Per-lens verdicts

- Reproducibility and toolchain hermeticity: proceed-with-revisions (image confirmed; F1 hermeticity,
  F3 asset byte-match, and F4 build-id survival must be fixed before recording any hash).
- Bootstrap, self-cert, install-hooks: re-scope (install-hooks MISSes the musl path; the
  divergence-retires and asset-byte-match payoffs are over-claims).
- Re-release ordering: blocking-incomplete (the RED-window and the install-hooks musl-path
  precondition need explicit atomic sequencing).
- Scope and cross-platform: proceed only after scoping host-prove out, scoping to x86_64, and making
  the multi-platform trust boundary explicit.
- Altitude and necessity: re-scope (the breakage is sanctioned by design, the older-glibc fix was
  never weighed, and a second full re-release round the same day as the cutover is the wrong cost
  at the wrong time for a cosmetic benefit).
