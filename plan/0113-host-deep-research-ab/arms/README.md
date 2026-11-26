# plan/0113 arm snapshots: pins, dates, and licenses

- Read 2026-11-26 over the GitHub REST API (`gh api`, authenticated as
  `connollydavid`), and materialized the same day under this directory.
- Committer dates are GitHub's commit object dates in UTC. A pin is the full
  40-character commit; the root tree is the commit's tree object, so it commits
  to every path and blob in the snapshot.
- One snapshot directory holds every arm: `arms/<arm>/`. The run harness built
  by the next task draws from the arm's own subdirectory, never from an
  installed skill, plugin or note library. The materialized trees are
  gitignored by [`.gitignore`](.gitignore); the pins in this file are the
  reproducibility anchor, so a cold reader re-creates the bytes rather than
  trusting a tracked copy.

## The qualifying arms

| Arm | Repository | Pin | Committer date | License file | SPDX | License blob | License sha256 |
|---|---|---|---|---|---|---|---|
| `weizhena` | `Weizhena/Deep-Research-skills` | `6ce38f60e3f8b22502c29873f96503a4e0c5addb` | 2026-08-23T03:25:07Z | `LICENSE` | MIT | `57d6df8dfc71cd3e6b35fd6c2776084843f2d73b` | `1883a89d5fe9b87f5137eb7f2755df95a95c6c75aaf8eb1d9eec2cb794471c72` |
| `hffmnnj` | `hffmnnj/opencode-deep-research` | `d9773015b5388868c2ff560148ec37857170e7ef` | 2026-11-13T19:35:59Z | `LICENSE` | MIT | `edae5d338158d7a55daec0f56d56674f1c9c9d3a` | `b560f06c8fc467bf0524b1b467b1cbac5b76a4093769b6790c5a1cc0b0e196f8` |
| `kanatami` | `Kanatami/opencode-deep-research` | `9f4696850df46e168f2d6d0b970bd8b362a351f0` | 2026-07-06T13:31:26Z | `LICENSE` | MIT | `14fac913ccf80234b1848540089a3bbcb6e5283d` | `1126322e2cc8d165adc4c792eeb195717de2bcc7b39be1ce77959d78e87ef685` |
| `samber` | `samber/cc-skills` | `50a33836b20f690c668af557bd9ef9d07a8c7ef2` | 2026-11-01T07:26:22Z | `LICENSE` | MIT | `e01f008a1febe41946345c425832c6aa093731d3` | `a6735e3815503be2fc1ae4813758cb3d0c24a5309df508309ce180cf5a4ead58` |

Every license file was read at the pin and begins `MIT License`; the digest
covers the exact bytes at that commit. The root trees, in the same arm order:

| Arm | Root tree |
|---|---|
| `weizhena` | `476c2298e23d6c9493f468d8d9fe336c8c4c6939` |
| `hffmnnj` | `a6d0795b9dbb94b157d7fb9945f8781fa547c906` |
| `kanatami` | `e5a4948c711abd8da88f3a23be1d3eef5e8b91d0` |
| `samber` | `9fca485fe8005f3e2ce89ef54eabda327a7c55ca` |

## What each snapshot holds

The path list names the files the arm runs, so the run harness can mount the
arm and nothing else.

| Arm | The arm's paths | Recorded note |
|---|---|---|
| `weizhena` | `skills/research-en/` (the `research`, `research-deep`, `research-report`, `research-add-items` and `research-add-fields` skills), `agents/web-search-opencode.md`, `agents/web-search-modules/` | Upstream's OpenCode recipe copies the skills into `~/.claude/skills/`, the agent into the config's `agents/` directory, and needs `pyyaml`; web search needs `OPENCODE_ENABLE_EXA=1`. |
| `hffmnnj` | `index.ts`, `package.json`, `bun.lock`, `content/skills/deep-research/`, `content/agents/researcher.md`, `content/agents/librarian.md`, `content/agents/verifier.md` | An OpenCode plugin with a notes library; `bun.lock` pins the runtime tree. |
| `kanatami` | `SKILL.md`, `agents/web-search-worker.md` | One skill and one worker agent; the repository's only commit is the pin. |
| `samber` | `skills/deep-research/` | The licensed origin of the fourth candidate; the skill declares `license: MIT` and version `1.3.0` in its frontmatter, and the repository's `LICENSE` is the same MIT text. |

## The optional sixth

The plan names two candidates for the optional sixth, and they are not
interchangeable in role.

- `199-biotechnologies/claude-deep-research-skill` at
  `f2f2c0fa4e7617ca84c86b63f4bb40f77a746933` (2026-04-11T22:18:07Z, root tree
  `37178a659db57adb5d5a8eafff3a50bae98aafb3`) is the verification pipeline:
  its `scripts/verify_citations.py` and `scripts/verify_claim_support.py`
  are the citation and claim checks the `verify` row describes. A recursive
  tree read at the pin finds no `LICENSE`, `LICENCE`, `COPYING`, `NOTICE` or
  `UNLICENSE` path, and the repository API reports no license. **Excluded**
  under the arm qualification rule. It enters only if upstream adds a license
  file before the selection round, and then at a commit that carries it, so
  this pin would be replaced rather than amended.
- `assafelovic/gptr-mcp` at
  `63884773685b1f12c7f0d9e283b3d71a5b9b5fda` (2025-11-07T07:46:52Z, root tree
  `d697e78a3b84ba501dc2c2220656e5420619ccb2`) carries `LICENSE`, MIT, blob
  `a469b2e36f12dcc7f724f66cc480d167d23d45f1`, sha256
  `1d2dfdf1d659afad94a97139b7e12511b09af981967d4f7b194bb0a91dcb4ae4`. It
  qualifies on license and is snapshotted as the named alternative. It is an
  MCP server around GPT Researcher, not the scripted verification pipeline, so
  whether the sixth slot is run as a server, and on which model, is a
  selection-round question, not a license one.

The fourth roster arm's unlicensed predecessor, `Thomashighbaugh/opencode`, is
not a candidate: the plan's ruling replaced it with the licensed `samber`
origin because the copy carries no license file and dropped the upstream MIT
notice.

## Re-creating the snapshots

```sh
cd plan/0113-host-deep-research-ab/arms
git clone https://github.com/Weizhena/Deep-Research-skills.git weizhena
git -C weizhena checkout --detach 6ce38f60e3f8b22502c29873f96503a4e0c5addb
# ...the same two commands per arm, at the pin in the table above.
git -C weizhena rev-parse 'HEAD^{tree}'   # 476c2298e23d6c9493f468d8d9fe336c8c4c6939
```

A tree hash that does not equal the table's root tree is a different snapshot
and does not belong to this record.

## What this record does not settle

- Whether the optional sixth enters; the qualification evidence is here, the
  roster decision is the selection round's.
- Runtime and toolchain fit. The `pyyaml` dependency, the notes library's
  SQLite index, and the MCP server's Python environment are recorded as arm
  facts; the run contract and the harness pin test them.
- Upstream drift after the pins. A newer commit is a new pin, not an edit to
  this table.
