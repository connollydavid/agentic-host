# plan/0065 gather-data: grounding the onboarding-and-MCP build in measured data

The ruled decisions and the install-mode design are grounded here in two measured streams before any
code: a Fen acceptance run on the new weak-agent contracts, and a survey of the established single-binary
installer family. This answers the standing requirement that a decision rest on data, not assertion.

## Fen acceptance (qwen3.5-4b): the new weak-agent contracts are legible

The design names decisions the weak agent must make that the prior three-route run (twenty of twenty) did
not cover. Each was probed on the real qwen3.5-4b (rope API, the qwen sampler with `top_k`, serial on the
single GPU, parsed after the thinking block), three runs each, with the correct option placed at a
different letter per probe so a first-option bias cannot pass spuriously.

| Probe | Contract tested | Correct letter | Result |
|---|---|---|---|
| exit-code re-invoke | on exit `3` name-required with no controlling terminal, re-invoke with `--name` | C | 3/3 |
| shell-verb vs MCP tool | inside an elicitation-capable client with no name, use the MCP tool | B | 3/3 |
| adopt route one (software repo) | a `Cargo.toml`-rooted folder is refused in place | D | 3/3 |
| adopt route three (arbitrary) | an arbitrary folder elicits a name and creates the host elsewhere, source untouched | A | 3/3 |

Twelve of twelve, the correct letters spread across C, B, D, and A, every run genuinely reasoned: the
traces reject the wrong options by name rather than blurting a letter. The exit-code and surface-choice
shapes stand as specified. The one-command run and the agent-driven resolve owe their own runs once the
verbs exist.

## Installer-family survey: what the field actually does

Nine established installers were read at their real install scripts and self-update source (rustup,
cargo-binstall, uv and cargo-dist, deno, starship, ollama, cosign, Homebrew, and the registry-driven
aqua). The load-bearing findings, each tied to a fetched artifact:

- **In-script verification is rare.** Only uv and cargo-dist check integrity in-script (an embedded
  SHA256); the mainstream pipe-to-shell installers trust the transport to the host only, and rustup
  removed its GPG path as buggy. Real in-installer signature verification is on the frontier (basecamp,
  HALO, aqua), so a provenance-verified host install sits ahead of the mainstream, alongside that cohort.
- **The majority cosign pattern** verifies a signed `checksums.txt` with a keyless bundle, then
  `sha256sum -c` checks each binary against it, so one signature covers the whole release.
- **Keyless cosign needs an identity and an issuer.** Since cosign version 2.0, `cosign verify-blob`
  requires `--certificate-identity` (or a regexp) and `--certificate-oidc-issuer`; the identity is the
  signing workflow's ref, pinned to the tag for the tightest guarantee. A `.*` identity is a degenerate
  anti-pattern that proves signed-by-someone, not by-whom.
- **Bootstrapping cosign is a chicken-and-egg**, and nobody verifies cosign with cosign. The honest paths
  are `gh attestation verify` as the primary (GitHub is the trust root, needing no cosign binary) with
  cosign as a fallback, or a pinned SHA256 of the cosign binary checked before it runs.
- **The receipt model** (cargo-dist writes an `<app>-receipt.json`, Homebrew an `INSTALL_RECEIPT.json`)
  records the installed binaries, versions, and hashes. For offline re-verification the receipt also
  stores the verified identity and issuer, the Rekor log pointer (log index, entry UUID, integrated
  time), and the trusted-root snapshot used.
- **Path, platform, and self-update majorities:** the binary lands in `~/.local/bin` with no root, and an
  env script sourced from the shell rc keeps uninstall clean and is skipped under CI or with no
  controlling terminal. A `uname` map selects the target triple, a static musl build is preferred on
  Linux, and an unknown target hard-errors against an allowlist rather than a silent fallback. Self-update
  uses a temp directory, a sanity run, and an atomic rename that first moves a running Windows executable
  aside.

### The verification shape the host install adopts

The signed-checksums majority pattern, pinned to the tag-templated workflow identity (basecamp/HALO):

```bash
cosign verify-blob checksums.txt \
  --bundle checksums.txt.bundle \
  --certificate-identity "https://github.com/connollydavid/host-lifecycle/.github/workflows/release.yml@refs/tags/vX.Y.Z" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
sha256sum -c --ignore-missing checksums.txt
```

Cosign is bootstrapped by `gh attestation verify` as the primary path with a pinned-SHA256 cosign binary
as the fallback, never by cosign itself. Offline re-verification from the receipt runs
`cosign verify-blob --offline` against the stored bundle and the recorded identity and issuer.

### Concrete grounding for the ruled decisions

- The **cosign keyless** trust anchor is confirmed implementable in a shell installer, with a shipping
  majority pattern to copy and a real offline re-verification mode from a receipt-borne inclusion proof.
- The **install receipt** shape is grounded in two production receipts, extended with the Rekor pointer.
- The **all-or-nothing landing** is grounded against ollama's fail-open partial state as the anti-pattern.
- host-lint already ships the canonical static-musl binary and `.host-software` already records the
  canonical hashes, so the musl-first build and the pinned-hash cosign bootstrap fit the existing anchors.

## Sources

- rustup-init.sh and self_update.rs (rust-lang/rustup); cargo-binstall SIGNING.md (cargo-bins).
- uv-installer.sh (releases.astral.sh); axoupdater receipt.rs and lib.rs (axodotdev).
- deno install.sh and upgrade.rs (denoland); starship install.sh; ollama scripts/install.sh.
- cosign verify docs and cosign_initialize.md (sigstore/cosign); Homebrew Bottles docs and the Trail of
  Bits build-provenance writeup.
- Shipping `cosign verify-blob` installers: basecamp/basecamp-cli, context-labs/HALO,
  guidewire-oss/fern-platform, opengrep/opengrep, automagik-dev/genie; the aquaproj/aqua verify path.
- Kubernetes verify-signed-artifacts and the Argo release verification recipes.
