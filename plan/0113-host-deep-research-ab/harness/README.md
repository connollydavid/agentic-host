# plan/0113 harness pin: OpenCode v2.4.2

- Pinned 2026-11-27 from the release's own publication, installed into
  `.prefix/` and checked by digest and version before every draw.
- The binary is local and gitignored (`.gitignore`); `install.sh` recreates it
  from the release, and the pin below is the reproducibility anchor.

## The pin

| Field | Value |
|---|---|
| Release tag | `v2.4.2` |
| Asset | `opencode-linux-x64.tar.gz` |
| Archive sha256 | `452912288f934d1771bd5bd0d8611ba3a6adc3db3ac3333c37facf373770ba66` |
| Binary sha256 | `523b1502d1d556998b0904235cef65eb1d8cf8362b4e2faa7ae7a170c9a44cd4` |
| Version line | `opencode v2.4.2` |

The archive digest is the line the release's `SHA256SUMS` carries, and
`install.sh` verifies it before extraction. The extracted binary's digest is
the value `preflight.sh` reads; it also equals the daily
`~/.opencode/bin/opencode` at the cut, so the pin names the release the host
already runs rather than a second engine.

## The draw environment

`probe.py` builds every draw under `/tmp/opencode/plan0113/probes/`, outside
any tree that carries a manual, and starts the pinned binary's server there:

- a scratch `HOME` and scratch `XDG_CONFIG_HOME`, `XDG_DATA_HOME`,
  `XDG_CACHE_HOME` and `XDG_STATE_HOME`, one set per draw;
- `OPENCODE_DISABLE_AUTOUPDATE=1` and `OPENCODE_DISABLE_MODELS_FETCH=1`;
- one work directory per draw, so no project config or `AGENTS.md` above it is
  discovered;
- the arm's own files planted under the draw's native config directory:
  `$XDG_CONFIG_HOME/opencode/skills/<id>/` and
  `$XDG_CONFIG_HOME/opencode/agents/<id>.md`, or the plugin entry in
  `$XDG_CONFIG_HOME/opencode/opencode.json`.

## Install and pre-flight

```sh
cd plan/0113-host-deep-research-ab/harness
./install.sh          # download, verify SHA256SUMS, extract, preflight
./preflight.sh        # digest and version, the draw gate
python3 probe.py      # the checks below
```

`preflight.sh --check digest` proves the digest branch alone;
`preflight.sh --check version` proves the version branch alone; the default
checks both against `pin.env`. A draw that fails either line does not run.

## The probe output

```
PASS pin: preflight: ok v2.4.2 digest=523b1502d1d556998b0904235cef65eb1d8cf8362b4e2faa7ae7a170c9a44cd4 version=opencode v2.4.2
PASS pin: preflight rejects a wrong digest
PASS pin: preflight rejects a wrong version
PASS pin: preflight rejects a tampered binary under the default check
PASS null: resolved config lists no skill, plugin or instruction; catalog is the binary's built-ins only (skills: opencode, report, browser)
PASS weizhena: loaded under the pinned binary (skills: research, research-deep, research-report, research-add-items, research-add-fields; agents: web-search)
PASS kanatami: loaded under the pinned binary (skills: web-search-deep; agents: web-search-worker)
PASS samber: loaded under the pinned binary (skills: deep-research)
PASS hffmnnj: plugin, skill and three agents loaded under the pinned binary
PASS isolation: leak control loads the planted skill and discovers the planted manual
PASS isolation: the planted skill and manual in the host home are absent from the draw
probe: 11 checks passed
```

## What each check proves

- **The pin.** The good binary passes; a copy with one appended byte fails the
  digest branch; a fake binary that reports `opencode v9.9.9` fails the
  version branch; the tampered copy fails the default check.
- **The null arm.** Its resolved configuration is the scratch global config
  directory and nothing else: no document, no `skills`, `plugins` or
  `instructions` key, and no manual in the scratch tree. Its skill, plugin and
  agent sets equal the binary's built-in set from the baseline draw.
- **The arms.** Each arm draws in its own root and loads under the pinned
  binary with no other arm's skills, plugins or agents: Weizhena's five skills
  and its `web-search` agent, Kanatami's `web-search-deep` skill and its
  `web-search-worker` agent, samber's `deep-research` skill, and the hffmnnj
  plugin with its skill and three agents.
- **Isolation.** A decoy home carries a planted skill under
  `~/.config/opencode/skills`, a planted skill under `~/.claude/skills` and
  `~/.agents/skills`, and a planted manual at
  `~/.config/opencode/AGENTS.md` and `~/AGENTS.md`. The leak control runs
  the same binary with that home as `HOME`: the native skill loads and the
  instruction plugin discovers the manual. The draw runs with the scratch
  home: none of the planted skills appears in its catalog and its log carries
  no reference to the decoy home.

## Measured facts worth carrying

- The built-in skills `opencode`, `report` and `browser` are the binary's own
  and appear in every draw. The null arm's **configuration** carries none of
  them; the catalog holds only the binary's built-ins.
- Under the pinned v2.4.2 server, the native
  `$XDG_CONFIG_HOME/opencode/skills` path is the one that loads arm skills.
  The Claude and agents compatibility roots (`~/.claude/skills`,
  `~/.agents/skills`) did not contribute in the server's draw; the leak
  control's positive result comes from the native global path. The scratch
  `HOME` still matters because the global config directory and the manual
  discovery live under it, and the retired research skills are planted under
  the home.
- The hffmnnj plugin loads from the bare snapshot at its pin with no
  dependency install; the pinned binary resolves its `@opencode/plugin`
  import.
- **The operator ruled 2026-11-27: consider only `v2.4.2`.** The experiment's
  harness is the pinned release for every draw and check; the house
  `tools/opencode` pin is not part of this milestone's harness decision.
- The optional `verify` arm stays excluded (no license at its pin), and
  `gptr-mcp` is an MCP server whose draw belongs to the run contract and the
  selection round, not to this probe.
