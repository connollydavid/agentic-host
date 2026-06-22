# host-lint reproducible build

Close the follow-on gap from `plan/0005`: this repo's own software, **host-lint**, now
has a recorded, **environment-independently reproducible** build, so the `.host-software`
pin is a true production anchor for it. host-lint is greenfield (initiated under the
methodology), so the spine requires this; there is no `repro-exempt` for it.

Driving it through the methodology surfaced the real defects and the genuine difficulty,
software-first in the host-lint repo:

1. **`Cargo.lock` was gitignored** (`24ecf32`): a binary with floating dependencies
   cannot reproduce. Tracked it (it pins `host-grammar`'s git rev).
2. **No pinned toolchain** (`24ecf32`), added `rust-toolchain.toml` (channel `1.95.0`).
3. **Build metadata embedded the host** (`2361ae0`): the release binary carried the
   `.note.gnu.build-id` and a `.comment` section naming the build host's toolchain/distro.
   Set `[profile.release] strip = true` and `--build-id=none` (`.cargo/config.toml`), in
   source. (Path remapping was tried and shown to be a no-op; paths were not the diff.)
4. **The build environment itself differed**: even with the above, a local (WSL) build
   and a GitHub-CI build diverged, because `ld`/`gcc`/distro differ. Bit-for-bit identity
   needs a **fixed build environment**, so the canonical environment is pinned to the
   `rust:1.95.0` image **by digest** (`sha256:f49565f1…`).

Provenance recorded in `.host-software` `[software "host-lint"]`: `build = CARGO_INCREMENTAL=0
cargo build --release --locked` (determinism config lives in the host-lint source),
`toolchain = rust:1.95.0@sha256:f49565f1…` (the pinned environment), `deploy = host-lint`,
`artifact = target/release/host-lint a7e276c0…`.

Proven: a double-build in the pinned container yields the same sha (`a7e276c0…`); the
`reproducible-build.yml` CI job runs in that same digest-pinned image and
`host-lifecycle software --verify-build .` reproduces it (green). `software --check .`
attests the artifact.

Scope: the `host` component is a README front-door (no compiled artifact), so it carries
no build provenance. Reproducibility is now environment-independent **given the pinned
image**: the legitimate standard (anyone with that image reproduces the binary).
