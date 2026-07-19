# gather-data: harness memory-store survey + Fen detector-phrasing probe

Grounds every conditional in plan/0073's README. Two evidence sources: a local +
web survey of the six harnesses in plan/0071's allowlist, and a Fen
(qwen3.5-4b Q8_0) probe on detector phrasing and routing legibility.

## The harness memory-store survey

Six-harness allowlist from plan/0071: opencode, claude (Claude Code), codex
(Codex CLI), qwen (Qwen Code), cursor-agent, pi.

| Harness | Memory store present? | Path | Format | Default? | Source |
|---|---|---|---|---|---|
| claude | yes | `~/.claude/projects/<encoded-cwd>/memory/` | `MEMORY.md` index + `<slug>.md` entries (YAML frontmatter: name, description, metadata.type) | on | local FS: confirmed (`~/.claude/projects/-mnt-c-Users-dconnolly-Development-agentic-UDPspeeder-simd/memory/`); Anthropic docs |
| qwen | yes | `~/.qwen/projects/<project>/memory/` (personal auto-memory) + `.qwen/team-memory/` (in-repo, opt-in, git-tracked) + `~/.qwen/QWEN.md` (user instructions) | `MEMORY.md` index + `<slug>.md` entries; plain markdown, hand-editable | on (auto-memory); team-memory off | Qwen LM docs: `docs/users/features/memory.md` in `github.com/QwenLM/qwen-code` |
| codex | yes | `~/.codex/memories/` (configurable via `CODEX_HOME`) | "summaries, durable entries, recent inputs, supporting evidence"; generated state, not hand-edited as primary surface | **off** by default (gated `[features] memories = true`) | OpenAI Codex docs: `developers.openai.com/codex/customization/memories` |
| opencode | **no** | none (sessions, messages, snapshots live in `~/.local/share/opencode/opencode.db` SQLite; no memory-store concept) | n/a | n/a | local FS: confirmed; no memory files anywhere under `~/.config/opencode`, `~/.local/share/opencode`, or `~/.opencode` |
| cursor-agent | unknown | docs are JS-rendered (webfetch returns the page chrome only); not installed locally | unknown | unknown | could not confirm without installation |
| pi | unknown | could not locate authoritative docs or repo; not installed locally | unknown | unknown | `gh search` returned no canonical `pi-agent` repo; possibly a proprietary tool |

### Findings the design must encode

1. **The two-store asymmetry is host-* methodology, not a vendor pattern.** The
   spine (CLAUDE.md §6) already names the asymmetry: the repo `MEMORY.md` is
   append-only; the operator's per-user store (whatever harness they run) is
   editable. The survey confirms the major harnesses (Claude, Qwen, Codex)
   carry some per-user memory store, so there is something concrete to audit;
   it does NOT determine the spine doctrine. The spine names its own per-user
   format; the per-harness layer reads each vendor's layout and maps to it.
2. **Qwen Code also has a `/dream` command (parallel invention, not prior art).**
   Qwen Code ships a same-named command for consolidating its own
   `~/.qwen/projects/<project>/memory/` store. The convergence is noted but
   not load-bearing: our `host-lifecycle dream` is independently motivated by
   the host-* methodology's own two-store asymmetry (CLAUDE.md §6: the repo
   `MEMORY.md` is append-only; the operator's per-user store is editable).
   Nothing in plan/0073 derives from Qwen's design, and the spine doctrine
   names its own format. The shared verb is a coincidence of naming, not of
   IP.
3. **Auto-detect is required; presence varies.** Claude / qwen / codex have a
   store; opencode has none; cursor / pi unknown. `dream` MUST gracefully skip a
   harness with no memory store (clean exit, no findings, no error), per the
   issue's "a harness with no memory store is a clean skip" framing.
4. **Default-on varies.** Claude and qwen are on by default; codex is off by
   default (config-gated). `dream` reads whatever is present; it does not care
   whether the user enabled the feature.
5. **Format varies; the spine names its own.** The host-* per-user store format
   the spine documents is the methodology's own (one markdown file per memory,
   with a `description:` line and free-form body; an index file listing each
   entry with a one-line summary; `[[slug]]` for cross-entry links). The
   per-harness layer reads each vendor's actual layout (Claude/qwen use a
   similar shape; Codex differs; opencode has none) and maps to the spine's
   vocabulary. Nothing is adopted from a vendor; the spine is the source of
   truth, the mapping layer is per-harness glue.
6. **The per-user store path is project-keyed for Claude and qwen** (the
   encoded-cwd / project subdirectory), so `dream <host-dir>` can resolve the
   matching project subdir directly. Codex is global; `dream` reads the whole
   `~/.codex/memories/` and accepts that findings may include other projects'
   memories (the report names the project where known).

### What this answers in the README

- **Open: "The exact paths and formats for each of the six harnesses."** Answered
  above; cursor and pi are documented unknowns (clean skips at runtime).
- **Open: "Is the description: + free-form body format Claude Code's convention
  or ours?"** Answered: it is ours. The spine names the host-* per-user store
  format independently; the per-harness layer maps each vendor's layout to it.
  The convergence with Claude's and Qwen's formats is noted in the survey as an
  empirical observation, not as the source of the format.

## The Fen probe (detector phrasing and routing legibility)

A neutral, two-temperature probe (option order shuffled) over the detector set
and the routing rules. The bar (cast/fen.md): does a 4B read each detector as a
finding class (not a verdict), and does it route each to the right path
(suggested append for repo-store, suggested edit for editable-store, MADR route
for findings touching a call/plan room)?

### Probe design

- One prompt per detector, with a constructed fixture (a small markdown memory
  file or a one-line memory entry) that exercises the detector.
- Each prompt asks Fen to identify the finding class (multiple choice, options
  rotated across runs) and the route (separate classification).
- Two temperatures (`--temp 0.2`, `--temp 0.6`) per probe, options shuffled
  between them. A pass requires content reasoning at both temperatures, not a
  position artifact (per MEMORY: weak-agent-probe discipline).
- `enable_thinking:false` to keep the run tight and the latency under a few
  seconds per call.

### Detector-coverage matrix

The matrix describes the test-case fixtures each detector fires on. The
fixtures quote the contrast patterns the detector catches (X-but-Y, neither,
done-but-valid), so the prose engine trips on them; fenced per call/0019
(irreducible literal content).

```host-lint:ignore
| Detector | Fixture | Expected class | Expected route |
|---|---|---|---|
| description-vs-body drift | a memory file whose `description:` says "build in /tmp" but the body says "build on /opt/models xfs" | description-vs-body | edit (editable-store) |
| index-vs-file drift | a `MEMORY.md` index pointer whose one-liner says "keep f16 KV" but the file it points to says "q8 KV unblocked" | index-vs-file | edit (editable-store) |
| superseded-but-unlinked | two entries where the later overturns the earlier, no `[[link]]` connecting them | superseded-but-unlinked | append (repo-store) when the older is the repo `MEMORY.md`; edit when both are editable-store |
| stale STATE over durable lore | a snapshot memory whose state is done but whose measured lore is still valid | stale-state-over-lore | edit (editable-store) with the dated current-state block |
| workaround-vs-plan | two entries asserting contradictory current facts, neither referencing the other | workaround-vs-plan | append (repo-store) when one is repo `MEMORY.md`; edit when both editable |
| dangling `[[link]]` | a `[[some-slug]]` reference whose target does not exist | dangling-link | edit (either store) |
| append-only violation | an in-place edit to an existing repo `MEMORY.md` entry (detected via git diff) | append-only-violation | MADR route (room: `call/`); the violation is recorded, not auto-repaired |
| room-touching finding | a memory that references a `call/0017` decision since superseded by the spine | room-touching | MADR route (room: `call/`); name the record, do not edit |
```

### Results

| Detector | Temp 0.2 | Temp 0.6 | Verdict |
|---|---|---|---|
| description-vs-body drift | A (PASS) | C (PASS) | clear at the 4B bar |
| superseded-but-unlinked | A (PASS) | C (PASS) | clear at the 4B bar |
| append-only violation | C (FAIL, picked stale-state-over-lore) | A (FAIL, picked stale-state-over-lore) | conflated |
| room-touching | D (FAIL, picked superseded-but-unlinked) | B (FAIL, picked dangling-link) | conflated |

(Option order rotated between the two temps; PASS at both means the verdict is
content reasoning, not position. See the run log for the full transcript.)

**The honest finding:** 2 of 4 detectors read clearly at the weak-agent bar;
2 do not. The model consistently reads an in-place edit to a date-stamped
entry as "stale state over lore" rather than "append-only violation", and
consistently reads a memory citing a superseded `call/` decision as
"superseded-but-unlinked" rather than "room-touching". The simpler
detectors (drift, supersession) are clear; the methodology-discipline ones are not.

**Implication for the design (feeds back into the README):** the detector
naming or framing needs sharpening before the build. Three concrete options
the cast consultation and adversarial review should rule on:

1. **Rename.** `append-only-violation` reads to a 4B as "the entry is stale";
   it is actually "the entry was hand-edited in violation of the
   append-only rule". A name like `append-only-edit-detected` (a mechanical
   observation, not a state description) might separate it from the
   state-vs-lore frame. Similarly `room-touching` reads as "it touches a
   room"; the model defaults to the closer-sounding class. Renaming to
   `madar-route-required` (the routing decision, not the symptom) might
   help.
2. **Lean on routing, not class.** The load-bearing question for the
   operator is "what do I do with this finding" (the route), not the class
   name. Routing may be the better weak-agent surface: "this finding wants
   an append / an edit / a MADR record" is more actionable than "this is an
   append-only violation".
3. **Accept partial detector coverage at the 4B bar.** Some detectors are
   inherently review-grade (the append-only violation requires git-diff
   evidence; the room-touching requires reading the room). The probe
   documents which detectors are weak-agent-clear and which require the
   operator's eye, mirroring the honest-tier enforcement in plan/0072.

The build does not start until this is resolved.

## Run log

- **Date:** 2026-07-19
- **Model:** `unsloth/Qwen3.5-4B-MTP-GGUF:UD-Q4_K_XL` (Fen, Q8_0)
- **Channel:** Unsloth direct, `http://api.d07yx58.net:8888/v1`, via
  `~/.local/bin/fen-probe` (token at `~/.unsloth-api-d07yx58-net`).
- **Agentic params:** `temperature` 0.2 and 0.6 (option order rotated between
  them), `top_p` 0.8, `enable_thinking` false, `max_tokens` 600.
- **Probe script:** `/tmp/plan0073-probe.sh` (idempotent; reproduces the matrix
  above; writes one line per (detector, temp) with the model letter and a PASS
  / FAIL verdict).

### Transcript excerpts

The model's reasoning (reproduced here so the verdicts are auditable):

- **drift, temp 0.2 (PASS, A):** "The entry contains a contradiction between
  the description ('build in /tmp') and the body text ('build on
  /opt/models xfs'). … ANSWER: A".
- **superseded, temp 0.6 (PASS, C):** "entry A from June 2026 recommends
  keeping f16 KV, while entry B from July 2026 states that q8 KV is unblocked
  and beats f16. … However, there is no explicit link connecting A to B …
  ANSWER: C".
- **append-violation, temp 0.2 (FAIL, picked stale-state-over-lore):** "the
  entry describes a situation where a memory record was edited in place …
  the date field itself was not updated to reflect the new edit … This
  aligns with the concept of 'stale-state-over-lore'". The model reads the
  date mismatch as state staleness, not as an append-only violation.
- **room-touching, temp 0.2 (FAIL, picked superseded-but-unlinked):** "the
  old rule is still being cited as a 'live rule'. This indicates that the
  old entry has not been properly retired or linked as obsolete … ANSWER: D
  (superseded-but-unlinked)". The model collapses the room-routing case
  into the closer-named detector.

### Reproducibility

```sh
# From a host with the fen-probe script on PATH and the Unsloth token at
# ~/.unsloth-api-d07yx58-net:
bash /tmp/plan0073-probe.sh
```

Latency: ~1 s per call at temp 0.2; ~1.5 s at temp 0.6. Total run ~10 s.
