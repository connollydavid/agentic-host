# plan/0071 host-install-mode: the curl one-liner, the manifest, the receipt, the handoff

This milestone completes plan/0065's remaining `host` install mode. The `host` repo gains
`install.sh`, a `curl -fsSL ... | bash` entry point that downloads the host-* binaries with
verified provenance, scaffolds a new `agentic-<name>` project, detects the operator's agent
harness, and launches it to continue the bringup Q&A. The install manifest, the local receipt,
the platform/shell detection, and the harness allowlist are the substance; the curl script is
the surface.

## Scope: what this completes

plan/0065 shipped the onboarding engine (`host-lifecycle init`/`adopt`, the MCP server, the shims)
as v0.39.0 and locked the install-mode contract in its README (lines 109-280). What remained
was the install mode itself: the manifest, the verified binary download, the receipt, the
platform/shell detection, the harness handoff, and the `install.sh` surface. This plan delivers
all of it.

The design decisions below are grounded in two evidence sources: a neutral Fen classification
probe (the UX conditionals) and a documented landscape survey (the binary names, the star
ordering, the platform matrix, the installer patterns).

## The one-liner

```
curl -fsSL https://raw.githubusercontent.com/connollydavid/host/main/install.sh | bash
```

Named:

```
curl -fsSL https://raw.githubusercontent.com/connollydavid/host/main/install.sh | bash -s -- agentic-acme
```

A short URL (`https://host.david.connol.ly/install.sh`) may redirect here in due course; the
script assumes nothing about it.

## The install/create separation

plan/0065 line 170: "Install and create are two failure domains, so the one-command form does
not fold them into one atomic step." The script honours this as two phases with a clean seam:

1. **Install phase**: detect platform, fetch the install manifest, verify its authenticity
   against the trust root, download each host-* binary, verify each against its recorded hash,
   install all-or-nothing to the path, write the local receipt. A partial install records the
   missing binaries and exits non-zero; nothing lands silently.

2. **Create phase**: prompt for the project name (or accept `$1`), run `host-lifecycle init
   <name>` to scaffold, detect the operator's installed agent harnesses, present a menu (or
   auto-select if one), and `exec` the chosen harness inside the project directory so the
   bringup Q&A continues interactively.

A first-run does both phases in sequence, but the install verifies the full toolset landed
before create begins. "A bootstrap never runs against a partial toolchain" (plan/0065:173).

## The manifest and the trust root

plan/0065 lines 121-132 and 234-243 locked the contract:

- An install manifest records each binary's version and canonical SHA256 hash.
- The hashes are single-sourced from the public per-component release receipts (the GitHub
  release asset digests), never from agentic-host's `.host-software`.
- The manifest is keyed to the template revision, because `host` install is also the upgrade
  route: an adopter on a given revision receives the binaries that revision pins.
- The trust root is the reproducible build itself: every host-* binary is reproducibly built
  from pinned source plus a recorded toolchain, so `software --verify_build` re-derives its
  recorded hash anywhere. The installer treats that hash as the root. No external signer, no
  bootstrap problem, offline by construction. Sigstore keyless is an optional identity layer,
  not the load-bearing root.
- The manifest and the install script are themselves authenticated before they run, so a
  corrupted or substituted manifest cannot present a self-consistent set that the leaf
  hash-check would pass. The trust-anchor material travels into the local install receipt so a
  later verification does not depend on refetching a moving remote.

**Manifest authentication — settled.** HTTPS to GitHub is the transport-layer trust root,
identical to every curl|bash installer in the ecosystem (rustup, homebrew, bun, deno, Claude
Code, Codex CLI all trust HTTPS for first-run). The manifest is served from the same repo over
the same TLS as `install.sh` itself, so the trust boundary for the manifest is the same
boundary the user already crossed to run the script. The reproducible build is the independent
verification path: an adopter can always rebuild any binary from pinned source + toolchain
(`software --verify_build`) and compare hashes, offline, with no external signer. plan/0065:234
already removed cosign as "the wrong layer"; this confirms that ruling. No bootstrap paradox:
first-run trust is HTTPS, durable trust is the reproducible build.

## The local receipt

plan/0065 lines 134-143: the install writes a durable machine-side receipt recording each
installed binary, its version, its verified hash, and the trust anchor used. It is persisted
locally (not in the project's `.host` stamp, which describes a project, not the machine's
binaries) and is re-verifiable offline. A partial install records the missing binaries as
absent or pending and never leaves a silently-missing tool untraceable.

**Receipt location — settled.** `$XDG_DATA_HOME/agentic-<name>/install-receipt` (defaulting to
`~/.local/share/agentic-<name>/install-receipt` when `XDG_DATA_HOME` is unset). Each project
gets its own machine-side receipt — multiple projects on the same machine can be on different
template revisions with different binary versions. XDG-conformant, namespaced by the project
name (not a generic `host/` dir), and distinct from the per-project `.host-receipts` that
plan/0037 established for applied-set receipts.

**Self-update is never an install.sh concern.** plan/0065:142 mentions a self-update that
rewrites the receipt in the same step it swaps the binary, but that is a function of the
agentic harness (the agent running `host-lifecycle upgrade` inside the project), not of this
install script. `install.sh` does first-run install only. Re-running it scaffolds a new
project, not an update.

## Platform and shell detection

Three OS families, two architectures, and the user's login shell for PATH configuration:

**OS detection** (the proven pattern from the opencode installer, verified against the release
asset names):

```
darwin          macOS           → host-lifecycle-darwin-{amd64,arm64}
linux           Linux           → host-lifecycle-linux-{amd64,arm64}
windows         MINGW/MSYS/CYGWIN → host-lifecycle-windows-{amd64,arm64}.exe
```

`uname -s` distinguishes the three; `uname -m` maps `x86_64` to amd64 and `aarch64` to arm64.

**Shell detection** (for PATH config modification, since the script runs as bash via curl|bash
but writes to the user's login shell config):

The script reads `$SHELL` and writes the idiomatic PATH line to the right config file:
`~/.zshrc` (zsh, macOS default since Catalina), `~/.bashrc` (bash), `~/.config/fish/config.fish`
(fish, using `fish_add_path`), or `~/.profile` (fallback). The opencode installer's
`current_shell` case block is the proven reference pattern.

**Git Bash on Win32** (git-scm): `uname -s` returns `MINGW*` or `MSYS*`, which maps to the
windows platform. The script downloads the `.exe` binary, installs to the MSYS2 bin dir, and
`command -v` in Git Bash resolves `.exe`-suffixed binaries transparently, so the harness
allowlist needs no platform-specific logic.

## Prerequisite checks: fail early, fail loudly

Before any work, the script checks its own prerequisites and exits with an actionable message
if any is missing:

- `git` — host-lifecycle clones the template during scaffold
- SHA256 verifier — `sha256sum` (Linux/Git Bash), `shasum -a 256` (macOS), or `certutil`
  (native Windows). Detected before the verify step, not at it.
- `curl` — inherently present (`curl | bash`), but checked if re-run from a local file.

`cargo` and `rustup` are NOT prerequisites of the install script (it downloads pre-built
binaries), but the harness-driven bringup inside the scaffolded project will eventually need
them. The script notes this in its final handoff block, not as a gate.

## Harness detection and the allowlist

After scaffolding, the script detects installed agent harnesses and offers to launch one so
the bringup Q&A continues interactively inside the project. The allowlist is strict: only
known harness binaries are probed, ordered by GitHub star count (a data signal, not an
opinion), not alphabetically and not by PATH order (which varies by machine).

The 6-harness allowlist (star-ordered, binary names confirmed from official docs and the
harnesscli unified meta-tool):

| # | Binary | Harness | Stars | Confidence |
|---|---|---|---|---|
| 1 | `opencode` | opencode | 184k | confirmed |
| 2 | `claude` | Claude Code | 137k | confirmed |
| 3 | `codex` | Codex CLI | 96.5k | confirmed |
| 4 | `qwen` | Qwen Code | 25.9k | confirmed |
| 5 | `cursor-agent` | Cursor Agent | unquantified | confirmed binary; `agent` fallback too generic for a strict allowlist — skip |
| 6 | `pi` | Pi Agent | unquantified | confirmed binary |

Dropped from consideration:
- `cheetahclaws` — PyPI package name confirmed, but the console-script entry point is
  unconfirmed. Re-evaluate when the binary invocation is documented.
- `zcode` — no official CLI binary; only a third-party wrapper (zCode-CLI-X). The official
  distribution is a GUI installer.

No `HARNESS` environment variable: research confirmed no cross-vendor standard exists (each
tool self-identifies via its own native var, e.g. `CLAUDECODE`). The closest to a standard is
the third-party `detect-coding-agent` crate reading native vars, which is for detecting a
*running* harness, not an *installed* one. Our script detects installed harnesses via
`command -v`, which is correct regardless.

**Selection logic:**
- `$1` is the project name, not the harness. The harness is never a positional arg.
- Zero harnesses detected: scaffold anyway, print "install opencode or claude, then `cd
  <name>`." The project is ready regardless.
- One harness detected: auto-select, no menu.
- Multiple detected: numbered menu via `read -rp ... < /dev/tty` (curl owns stdin). The
  numbering follows the star order above, which is deterministic across machines.
- `exec <harness>` in the project dir replaces the script process; the harness reads the
  scaffolded CLAUDE.md as its entrance and continues the bringup Q&A. Because `curl | bash`
  runs bash as a child of the user's shell, `exec` replaces that child, not the parent shell.
  When the harness exits, the user is back in their original directory. The script prints
  `cd <name>` as its final line before `exec` so the command is in scrollback. This is the
  curl-pipe-bash pattern's natural behavior, not a workaround.

## Name resolution

plan/0065 lines 99-107 locked the name backstop: the verb accepts the name by flag or
environment, else prompts on a controlling terminal, else exits with code 3 and a
machine-parseable stderr line naming the missing field.

For `install.sh`, the name resolves in this order:
1. `$1` if provided (`bash -s -- agentic-acme`)
2. `read -rp 'Project name (agentic-<name>): ' name < /dev/tty` if no arg and a TTY is
   available
3. Exit 3 with a machine-parseable message if neither

The name is validated: it must match `^[a-zA-Z0-9][a-zA-Z0-9_-]*$` and is prefixed with
`agentic-` if it does not already start with it. Path traversal (`../`), shell
metacharacters, and empty strings are rejected before reaching `host-lifecycle init`.
`agentic-host` is reserved (it is the name of this project's own development host) and
refused with an actionable message; the script exits non-zero and suggests choosing a
different name.

## The Allium specification

The install state machine is genuinely complex (platform detect, manifest fetch, trust
verify, per-binary download and hash-check, all-or-nothing, receipt, then name prompt,
scaffold, harness detect, launch), so it earns a spec, not just tests.

The spec lives in the `host` repo (specs-live-with-software, plan/0012) and models the
surface `InstallRun` with states and transitions:

- `Prerequisites` → `Detecting` (all met) | `MissingPrereq` (any absent, exit 1)
- `Detecting` → `FetchingManifest` (platform identified) | `UnsupportedPlatform` (exit 1)
- `FetchingManifest` → `VerifyingManifest` (fetched) | `FetchFailed` (exit 5)
- `VerifyingManifest` → `Downloading` (trust root verified) | `ManifestUntrusted` (exit 1)
- `Downloading` → `VerifyingBinary` (per-binary) | `DownloadFailed` (exit 5)
- `VerifyingBinary` → `Downloading` (hash matches, next binary) | `HashMismatch` (exit 1,
  all-or-nothing) | `AllVerified` (last binary matches)
- `AllVerified` → `WritingReceipt` → `InstallDone`
- `InstallDone` → `NamePrompt` (create phase begins)
- `NamePrompt` → `Scaffolding` (name resolved) | `NameRequired` (no TTY, exit 3) | `NameReserved` (`agentic-host`, exit 4)
- `Scaffolding` → `HarnessDetect` (project created) | `TargetExists` (exit 4)
- `HarnessDetect` → `Launching` (resolved) | `NoHarness` (print message, exit 0)
- `Launching` → `Done` (`exec harness`)

Invariants:
- No binary lands on PATH before its hash is verified.
- No project is scaffolded before the full toolset is installed and verified.
- The receipt is written before the create phase begins.
- The name is never empty when it reaches `Scaffolding`.
- The name is never `agentic-host` (reserved).

## Verification

**Integration tests** exercise every branch:
- Prerequisites: missing `git` → exit 1 with actionable message
- Platform: darwin/linux/windows detection from mocked `uname`
- Manifest: trust-root failure → exit 1 before any download
- Binary: hash mismatch → exit 1, nothing on PATH, receipt records the failure
- Binary: all match → receipt written, all binaries on PATH
- Name: from arg, from TTY prompt, from neither (exit 3)
- Name: path-traversal rejected, shell-metacharacter rejected, empty rejected
- Name: `agentic-host` refused (reserved), actionable message, exit 4
- Harness: zero detected (print + exit 0), one detected (auto-select), multiple (menu),
  invalid menu selection (re-prompt)
- Scaffold: existing target → exit 4
- Shell config: correct file written for zsh/bash/fish/profile

**Fen probe** (gather-data.md) validates the UX conditionals:
- Name prompt legibility: does `(agentic-<name>)` produce `agentic-acme`, not `acme`?
- No-harness message: does the print-and-exit read as actionable to a weak agent?
- Manifest authentication pattern: which of the surveyed installer patterns reads as
  trustworthy to a cold read?
- Star-ordered menu: does a weak agent read a numbered star-ordered menu without position
  bias?

**Installer survey** (gather-data.md) grounds the mechanical patterns:
- The hash-check-and-verify pattern (opencode, rustup, homebrew, deno, bun, Claude Code,
  Codex CLI) — what do the shipping majority do?
- The manifest format — TOML (host-lifecycle's idiom) vs JSON vs plain text
- The trust-root mechanism — reproducible build hash vs external signer vs GitHub-digest-only
- The receipt location — `~/.host-receipts` vs XDG vs home-dir dotfile

## Build sequence

The tasks are anchored receipted nodes (plan/0042), built as a forward graph:

### gather-data
Grounds every conditional in data: the Fen probe (UX), the installer survey (mechanical
patterns), and the binary-name/harness landscape confirmation.
- verify by: every conditional in this README traces to a gather-data.md row
- depends: none

### write-install-sh
The tight bash script, zero third-party deps. Implements the full state machine: prerequisites,
platform/shell detection, manifest fetch, trust verify, per-binary download and hash-check,
all-or-nothing, receipt, name resolution, scaffold, harness detect, launch.
- verify by: `bash -n install.sh` (syntax), `shellcheck install.sh` (lint; requires adding a
  shellcheck job to the host repo's CI, which currently has only a prose gate per plan/0038),
  integration tests pass
- depends: gather-data

### write-manifest
The install manifest keyed to the template revision, single-sourced from public release
receipts. Generated or declared; its format settled by the installer survey.
- verify by: manifest hashes match the public release asset digests for every host-* binary
- depends: gather-data

### write-allium-spec
The `InstallRun` surface with states, transitions, and invariants as specified above.
- verify by: `allium check` + `allium analyse` exit 0, zero findings
- depends: gather-data

### write-obligations
Every `allium plan` obligation dispositioned in a `<spec>.obligations` manifest, discharged by
the integration tests.
- verify by: `host-lifecycle obligations <spec> --tests tests --strict-discharge` clean
- depends: write-allium-spec

### write-tests
Integration tests covering every branch listed in Verification above. The test harness mocks
`uname`, `command -v`, `/dev/tty`, and the network (manifest fetch, binary download) so tests
run offline and deterministic.
- verify by: full test suite green, every spec obligation exercised
- depends: write-install-sh, write-allium-spec

### host-repo-release
Ship `install.sh`, the manifest, the spec, and the tests in the `host` repo. The entrance
ships through its own release authority (plan/0065:192-194).
- verify by: `host-lifecycle entrance --check` green, `software --check` clean, CI green
- depends: write-install-sh, write-manifest, write-obligations, write-tests

### re-pin-and-receipt
Re-pin `host` in agentic-host's `.host-software`, record the release receipt.
- verify by: `software --check .` clean at the new pin
- depends: host-repo-release

### fen-acceptance
The real `qwen3.5-4b` runs the one-liner end-to-end (or as close as the sandbox allows) and
the harness-detection menu, confirming the UX conditionals hold at the weak-agent bar.
- verify by: Fen routes the install flow and the harness selection correctly
- depends: host-repo-release
