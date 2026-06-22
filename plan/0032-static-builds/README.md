# plan/0032: Static musl canonical artifacts for the host-* tools

> **Goal:** the recorded `.host-software` artifact for each host-* binary becomes a statically
> linked `x86_64-unknown-linux-musl` build, so the reproducible canonical binary runs on any Linux
> host (including the dev WSL), `software --install-hooks` installs that canonical binary rather
> than a local rebuild, and the recorded artifact is the same binary the producer CI distributes.
> Depends on `plan/0028` (the host-* family is now uniform Where-room software) and the
> reproducible-build production anchor (`plan/0005`, `plan/0006`).
>
> **Adversarially reviewed** (`design-review.md`, 5 lenses, **re-scope**): three payoffs are
> over-claimed (the install-hooks divergence is sanctioned by design, the canonical will not
> byte-match the producer CI asset unless producer CI is converted to the pinned recipe, and "any
> Linux" conflates OS with architecture), host-prove conversion is scope creep, and a simpler
> older-glibc image was never weighed. The body below is the pre-review plan; it is re-cut once the
> operator settles the pivotal goal (portability for the hook versus distribute-equals-certify).

## Context

`.host-software` records each artifact as `target/release/<bin>`, built by
`CARGO_INCREMENTAL=0 cargo build --release --locked` in `rust:1.95.0`. That is a glibc-dynamic
binary linked against the image's glibc (2.39), so it does not run on a host with an older glibc.
`plan/0028` hit this directly: the cutover's `software --install-hooks` could not run the canonical
container binary on the dev host (`GLIBC_2.39 not found`), so it installed a local
`cargo build --release` instead and reported "local build (differs from the canonical hash)". The
runnable hook binary and the reproducible canonical artifact diverged.

There is a second split. Each producer's release CI already cross-compiles static musl binaries
(host-lint and host-lifecycle ship the full `x86_64`/`aarch64` musl plus darwin and windows matrix
as release assets), yet `.host-software` records, and `--verify-build` reproduces, the glibc
binary. The project distributes one binary and certifies another.

A statically linked musl binary carries no glibc dependency, so it runs on any Linux host. A musl
static canonical artifact closes both gaps: the certified binary is portable, `--install-hooks`
installs it directly, and the recorded artifact equals the distributed one.

## Decisions (operator rulings, 2026-06-22)

1. **All three artifact-bearing tools convert.** host-lint, host-lifecycle, and host-prove each
   record a static musl canonical artifact. host-prove's producer CI also gains a musl build; today
   its CI produces only the glibc `target/release/host-prove`.
2. **The recorded toolchain is a digest-pinned musl-cross image.** The image ships the
   `x86_64-unknown-linux-musl` target and its std preinstalled, so the build recipe needs no
   `rustup target add` and makes no network fetch. This keeps the build hermetic, the property the
   reproducibility anchor rests on. The rejected alternative (`rust:1.95.0` plus an in-recipe
   `rustup target add`) fetches the musl std at build time, a hermeticity dent the anchor should
   not carry.

## Per-component change

For each of host-lint, host-lifecycle, host-prove, the `.host-software` stanza changes three lines:

- `toolchain` = the digest-pinned musl-cross image at Rust 1.95.0.
- `build` = `CARGO_INCREMENTAL=0 cargo build --release --locked --target x86_64-unknown-linux-musl`.
- `artifact` = `target/x86_64-unknown-linux-musl/release/<bin> <new sha256>`.

The existing reproducibility hardening (`strip = true`, `.cargo/config.toml`
`-C link-arg=--build-id=none`) carries over unchanged. These crates are pure Rust with no C
dependencies (pulldown-cmark, getopts, unicode-*, bitflags, memchr, unicase), so the musl target
builds without a C cross-linker.

| Component | Current canonical | Becomes |
|-----------|-------------------|---------|
| host-lint | glibc `target/release/host-lint` | static musl `target/x86_64-unknown-linux-musl/release/host-lint` |
| host-lifecycle | glibc `target/release/host-lifecycle` | static musl, same path shape |
| host-prove | glibc `target/release/host-prove` | static musl; producer CI gains the musl build |

## The migration: a re-release round (software-first)

Changing `build` and `toolchain` changes every artifact hash, so each tool is re-released through
the tool-carried `host-lifecycle release <component> --change-class neither` (a build-recipe change
is not a public-flag change). The producer tag is the release; the orchestration re-pins
`.host-software` and records the receipt, the same shape as the `plan/0028` cutover. host-grammar
is untouched (repo-only, no artifact). host-lint, host-lifecycle, and host-prove each re-release
software-first, then agentic-host re-pins and re-records in one coherent commit so the receipt gate
is never RED on a push to main.

The payoff is checkable at the gate: after the re-pin, `software --install-hooks` installs the
canonical musl binary itself (it runs on the dev host), so the "local build (differs from the
canonical hash)" divergence from `plan/0028` retires, and `--verify-build` reproduces the same
static binary the producer CI distributes.

## Verification (whole-suite green)

- A double build of each tool in the pinned musl-cross image reproduces one sha256 (musl static
  drops the dynamic-loader and build-id variability, so it is at least as reproducible as the
  current glibc build); the hash is recorded as the canonical artifact.
- `software --verify-build .` green for all three under the released pinned host-lifecycle.
- `software --install-hooks .` installs the canonical binary, reports it verified against the
  canonical hash, and the installed `commit-msg` hook runs on the dev host (the `plan/0028`
  workaround retires).
- The canonical recorded artifact byte-matches the producer CI's `x86_64-unknown-linux-musl`
  release asset for that tag.
- `software --check`, `book --check`, the cold-clone CI job, and the commit-hook tell test stay
  green; whole-suite green across every repo.

## Risks / honesty

- **The musl-cross image must exist at Rust 1.95.0 and be digest-pinnable.** A Readiness step
  confirms a tag (a `clux/muslrust` or `messense/rust-musl-cross` build at 1.95.0) and records its
  digest. If none matches 1.95.0 exactly, the fallback is the rejected in-recipe target-add, taken
  only with the hermeticity cost noted; the plan does not assume the image without confirming it.
- **A second full re-release round**, with the same software-first and atomic-receipt discipline as
  the cutover. The `plan/0028` MEMORY lessons apply, with one inversion to confirm: the
  local-build-for-hooks step should no longer be needed once the canonical binary is portable.
- **The musl allocator is slower than glibc's**; for these short-lived CLIs the difference is
  immaterial.
- **The canonical artifact stays single-platform** (`x86_64-unknown-linux-musl`, the dev and CI
  host arch). The darwin, windows, and aarch64 binaries remain producer-CI release assets, not
  `.host-software` canonical artifacts; the reproducibility gate certifies the one host arch.

## Records

This plan, `PLAN.md`, `MEMORY.md`; a `call/` decision if the design-review judges the
production-anchor recipe change warrants its own MADR; re-pins and receipts as the round lands,
each pushed in its own audited commit.
