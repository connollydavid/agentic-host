# host-lint reproducible build

Close the follow-on gap from `plan/0005`: this repo's own software, **host-lint**, now
has a recorded, verified reproducible build — so the `.host-software` pin is a true
production anchor for it, not just a source pin. host-lint is greenfield (initiated under
the methodology), so the spine requires this; there is no `repro-exempt` for it.

Surfaced and fixed (software-first, in the host-lint repo, commit `24ecf32`):

- **`Cargo.lock` was gitignored** — a binary with floating dependencies cannot build
  reproducibly. Tracked it (it pins `host-grammar`'s git rev).
- **No pinned toolchain** — added `rust-toolchain.toml` (channel `1.95.0`), the dominant
  source of artifact-hash drift.

Provenance recorded in `.host-software` `[software "host-lint"]`:

- `build` — `CARGO_INCREMENTAL=0 RUSTFLAGS="--remap-path-prefix=$PWD=. --remap-path-prefix=${CARGO_HOME:-$HOME/.cargo}=/cargo" cargo build --release --locked` (path remapping neutralises the build-dir difference between the canonical worktree and `--verify-build`'s throwaway one).
- `toolchain = 1.95.0`, `deploy = host-lint`, `artifact = target/release/host-lint <sha256>`.

Proven: a double-build in two separate worktrees at the pin yields the **same** sha256
(`782a0840…`); `host-lifecycle software --verify-build .` rebuilds from the pin and
reproduces it; `software --check .` attests it. A standing
`.github/workflows/reproducible-build.yml` re-proves it on every push and weekly.

Scope: the `host` component is a README front-door (no compiled artifact), so it carries
no build provenance. **Open hardening:** same-environment reproducibility (pinned
toolchain) is what this milestone guarantees; full container-level environment-independence
is future work — if CI's hash diverges from the recorded one, that divergence is the next
finding to chase (and CI's value becomes canonical).
