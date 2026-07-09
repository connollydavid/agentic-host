# gather-data: installer survey and harness landscape

Grounds every mechanical conditional in plan/0071's README in how the shipping
majority actually do it. Each row traces a conditional in the README to its
evidence here.

## Installer survey

Surveyed: **rustup** (`sh.rustup.rs`), **opencode** (`opencode.ai/install`),
**deno** (`deno.land/install.sh`), **bun** (`bun.sh/install`). Fetched
2026-07-09.

### Platform and architecture detection

All four use `uname -s` (OS) and `uname -m` (CPU). The patterns:

| Installer | Detection | Edge cases handled |
|---|---|---|
| rustup | `uname -s` + `uname -m` | Rosetta (x86_64→arm64 via `sysctl`), ELF bitness (32-bit userland on 64-bit kernel), LoongArch UAPI, Android, illumos |
| opencode | `uname -s` + `uname -m` | Rosetta, musl/Alpine, AVX2 baseline |
| deno | `uname -sm` combined | none beyond the combined check |
| bun | `uname -ms` combined | Rosetta, musl/Alpine, AVX2 baseline |

**Decision for install.sh:** `uname -s` + `uname -m` with Rosetta detection on
Darwin (the minimum all four agree on). No ELF bitness, no AVX2 baseline, no
LoongArch — our targets are darwin/linux/windows on amd64/arm64 only, matching
the 6 release assets host-lifecycle publishes.

### Hash verification

| Installer | SHA256 in script | Rationale |
|---|---|---|
| rustup | no (delegates to binary) | the `rustup-init` binary does its own verification |
| opencode | no | HTTPS-only trust |
| deno | no | HTTPS-only trust |
| bun | no | HTTPS-only trust |

**The shipping majority do not verify hashes in the install script.** They rely
on HTTPS as the transport-layer trust root. Our install.sh strengthens beyond
the majority by verifying SHA256 digests from the host-lifecycle release
manifest. This is justified because: (1) host-lifecycle already publishes
per-platform digests on the GitHub releases API, (2) we install multiple
binaries and the all-or-nothing invariant requires confirming each landed
correctly, (3) the reproducible-build anchor (plan/0032) makes the digest a
meaningful identity check, not just a transport check.

**Decision for install.sh:** Verify SHA256 after download, before moving any
binary to PATH. Grounded as a strengthening, not as following the majority.

### Manifest

None of the four uses a manifest. They download from URL patterns:
- rustup: `${ROOT}/dist/${arch}/rustup-init`
- opencode: GitHub `releases/latest/download/${filename}`, version from API
- deno: `dl.deno.land/release/${version}/deno-${target}.zip`, version from
  `release-latest.txt`
- bun: GitHub `releases/latest/download/bun-${target}.zip`

**Decision for install.sh:** We need a manifest because we coordinate binaries
across multiple repos (host-lint, host-lifecycle, host-prove). The manifest
format: plain text, one line per binary (`name <url> <sha256>`), generated from
the host-lifecycle release receipts. This is simpler than TOML/JSON and parseable
in pure bash (no `jq`/`toml` dependency).

### Trust root

All four use HTTPS to their download origin. None uses GPG, cosign, or an
external signer. rustup additionally enforces TLS 1.2+ and negotiates strong
cipher suites (with graceful fallback for older curl/wget).

**Decision for install.sh:** HTTPS to GitHub (`raw.githubusercontent.com` for
the script, `api.github.com` for the manifest/digests, `github.com` for release
assets). Enforce `curl --proto '=https' --tlsv1.2`. No GPG, no cosign (settled
in plan/0065:234 — wrong layer for a reproducible-build project).

### Shell configuration

All four detect `$SHELL` and write export commands to the appropriate config
file. The pattern is uniform:

| Shell | Config file | Line written |
|---|---|---|
| zsh | `~/.zshrc` | `export PATH=$DIR:$PATH` |
| bash | `~/.bashrc` or `~/.bash_profile` | `export PATH=$DIR:$PATH` |
| fish | `~/.config/fish/config.fish` | `fish_add_path $DIR` |

bun is the most thorough: it also checks `$XDG_CONFIG_HOME` variants and handles
`.profile` fallback. opencode writes to `$GITHUB_PATH` in CI.

**Decision for install.sh:** Detect `$SHELL`, write the export to the
appropriate config file. Support zsh/bash/fish/profile. Check `$XDG_CONFIG_HOME`.
Write to `$GITHUB_PATH` in CI. All match the majority pattern.

### Install location

| Installer | Location |
|---|---|
| rustup | `~/.cargo/bin` (via the binary) |
| opencode | `~/.opencode/bin` |
| deno | `~/.deno/bin` (or `$DENO_INSTALL/bin`) |
| bun | `~/.bun/bin` (or `$BUN_INSTALL/bin`) |

Pattern: `~/.<app>/bin`. Our install.sh uses `~/.local/bin` (XDG data dir for
receipt, local bin for binaries) because the tools are shared across projects,
not per-project.

### Receipt

None of the four writes a receipt. This is unique to our approach.

**Decision for install.sh:** Write
`$XDG_DATA_HOME/agentic-<name>/install-receipt` (default
`~/.local/share/agentic-<name>/install-receipt`). Justified by idempotency: the
receipt records what landed, when, at what version, so re-running the script is
deterministic (skip what's installed, install what's missing, fail if a hash
diverged).

### TTY handling for curl-pipe-bash

rustup and deno both use `< /dev/tty` to read interactive input when the script
is piped (stdin is owned by curl). This is the standard pattern.

**Decision for install.sh:** All interactive reads go through `< /dev/tty`.
Grounded in the rustup and deno precedent.

### Shell dialect

| Installer | Dialect | Rationale |
|---|---|---|
| rustup | POSIX `sh` (dash-compatible) | maximum portability |
| opencode | bash (`set -euo pipefail`) | progress bar needs bash |
| deno | POSIX `sh` | maximum portability |
| bun | bash (`set -euo pipefail`) | arrays for config-file list |

**Decision for install.sh:** bash with `set -euo pipefail`. The harness
allowlist, menu logic, and string manipulation are cleaner in bash. We require
`bash` explicitly in the shebang (`#!/usr/bin/env bash`). The opencode and bun
precedent justifies this.

**Critical constraint: macOS bash 3.2 compatibility.** macOS ships bash 3.2.57
at `/bin/bash` — the last GPLv2 release. Apple froze it when bash 4.0 switched
to GPLv3, and has never updated it. Every macOS user has bash 3.2 and only 3.2
unless they installed a newer one via Homebrew. Confirmed via Apple TN2065:
`/bin/sh` on macOS is bash in POSIX mode. Since Catalina (10.15, 2019), zsh is
the default interactive shell, but `/bin/bash` is present on every macOS
release including current Tahoe (26) and Golden Gate (27 beta).

This pins install.sh to **bash 3.2-safe constructs only**:

| Safe in 3.2 (use these) | bash 4+ only (avoid these) | Replacement |
|---|---|---|
| `set -euo pipefail` | `mapfile` / `readarray` (4.0) | `while read -r line; do ...` |
| `[[ ]]` test | `declare -A` assoc arrays (4.0) | parallel arrays + `case` dispatch |
| `read -rp` | `${var^^}` / `${var,,}` (4.0) | `tr '[:lower:]' '[:upper:]'` |
| `${var//pattern/replacement}` | `\|&` pipe shorthand (4.0) | `2>&1 \|` |
| `local` variables | `coproc` (4.0) | named pipes or `&` + `wait` |
| `case` / `select` | `${var:i:n}` substring (4.2) | `cut -c` or `expr substr` |
| arrays `arr=(a b c)` `${arr[@]}` | `${!name@}` indirect (4.3) | `eval` or `case` |
| `printf '%s'` | `declare -g` (4.2) | avoid global declaration in functions |
| `< /dev/tty` redirect | | |
| `trap` / `exit` / `return` | | |

The constructs we need (the state machine, harness allowlist, name validation,
menu, SHA256 verification, manifest parsing) are all expressible in 3.2-safe
bash: `case` dispatch, indexed arrays, `while read` loops, `[[ ]]` tests, and
string operators. No associative arrays or `mapfile` required.

### Downloader

All four prefer curl, with wget as a fallback. rustup additionally detects the
broken snap-curl and handles it.

**Decision for install.sh:** Prefer `curl`, fail with a clear message if neither
curl nor wget is available (but do not implement wget fallback — curl is
ubiquitous on the platforms we target, and the complexity is not justified for 6
platforms).

### Two-stage vs fat script

rustup is thin: the shell script detects platform, downloads the
`rustup-init` binary, and execs it. The binary does the real work (installing
toolchains, configuring PATH, etc.). The others are fat: the shell script does
everything (download, extract, configure PATH, print success message).

**Decision for install.sh:** Fat script. We install multiple binaries (not one
self-installing binary like rustup), and the scaffold step runs `host-lifecycle
init` after the binaries are on PATH. The fat approach matches opencode, deno,
and bun.

## Harness landscape confirmation

The allowlist (6 harnesses, star-ordered) was confirmed during planning and
re-verified here:

| # | Binary | Harness | Stars | Confidence |
|---|---|---|---|---|
| 1 | `opencode` | opencode | 184k | confirmed |
| 2 | `claude` | Claude Code | 137k | confirmed |
| 3 | `codex` | Codex CLI | 96.5k | confirmed |
| 4 | `qwen` | Qwen Code | 25.9k | confirmed |
| 5 | `cursor-agent` | Cursor Agent | unquantified | confirmed binary |
| 6 | `pi` | Pi Agent | unquantified | confirmed binary |

Dropped: `zcode` (no CLI binary), `cheetahclaws` (entry point unconfirmed).

The ordering is the star ordering. The menu shows names and numbers only — no
star counts, no popularity labels. This keeps the menu clean and avoids implying
a recommendation beyond ordering.

No `HARNESS` environment variable: research confirmed no cross-vendor standard
exists. Detection is via `command -v <binary>`.

## Fen probe

The Fen probe (weak-model UX validation) runs at the `fen-acceptance` build step
(the last task in the build sequence), where the real install.sh output is
available to probe against. The probe validates:

1. **Name prompt**: does `(agentic-<name>)` produce `agentic-acme`, not `acme`?
2. **No-harness message**: does the print-and-exit read as actionable?
3. **Ordered menu**: does a weak agent read a numbered ordered menu (names only)
   without position bias?
4. **Manifest trust**: does the trust message read as trustworthy to a cold
   read?

Deferred from gather-data to fen-acceptance because probing requires the actual
script output, not a mock.

## Conditional traceability

Every conditional in the README traces to a gather-data row:

| README conditional | gather-data row |
|---|---|
| Platform: `uname -s`/`uname -m` + Rosetta | Platform detection table |
| SHA256 verification after download | Hash verification (strengthening) |
| Manifest: plain text, one line per binary | Manifest (none use one; we need one) |
| Trust root: HTTPS to GitHub | Trust root (all four use HTTPS) |
| Shell config: zsh/bash/fish/profile | Shell configuration table |
| Install location: `~/.local/bin` | Install location (XDG vs `~/.<app>/bin`) |
| Receipt: per-project XDG | Receipt (unique to us; justified by idempotency) |
| TTY: `< /dev/tty` for interactive reads | TTY handling (rustup, deno precedent) |
| Dialect: bash, `set -euo pipefail` | Shell dialect (opencode, bun precedent) |
| bash 3.2-safe constructs only | macOS ships 3.2.57 (last GPLv2; never updated) |
| Downloader: curl, no wget fallback | Downloader (curl ubiquitous on 6 targets) |
| Fat script, not two-stage | Two-stage vs fat (opencode/deno/bun precedent) |
| Harness allowlist: 6 binaries, ordered | Harness landscape table |
| No `HARNESS` env var | Harness landscape (no standard exists) |
| Menu: names and numbers only | Harness landscape (ordering without star counts) |
