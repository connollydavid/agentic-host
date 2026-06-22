# Agentic-tell grammar engine

Extend the verification surface so it covers *prose* tells, not just *naming* tells: a
token-free English adaptation of the tropes catalogued at tropes.fyi (Ossama).
The engine lives in **host-grammar** (the shared rules crate); **host-lint**
calls it. Every prose finding is advisory (warn, exit 3); any one device is
legitimate rhetoric, so the signal is density, never a single use.

## What shipped

- **host-grammar `tells` module** (v0.2.0): three layers, all token-free.
  1. **Lexical**: phrase/character rules (AI diction, filler transitions,
     pedagogical hooks, signposted conclusions, typographic polish: em-dash,
     smart quotes, arrows).
  2. **Structural**: windowed equations: negative parallelism, tricolon,
     anaphora (`Σ_runs max(0,L−2)²`), countdown, self-answered question,
     listicle, participial tail, false range, plus paragraph-shape tells
     (punchy fragments, bold-first bullets).
  3. **Composite**: a per-document density `Score`; over-threshold needs high
     absolute weight *and* high density (conservative gates).
  Public API: `scan_prose(text)` and `tell_score(text)`. One zero-transitive
  dependency (`unicode-segmentation`) for tokenizing; the reproducible-build
  anchor is untouched.
- **host-lint** (v0.3.0): `--stdin` runs prose tells alongside naming tells
  (so an agent self-checking a gh title or commit subject sees both), and
  `--prose <files>` scans documents on demand. `--json` gained a `cite` field.
  Naming tells keep their flag tier; prose tells are warn-only.

## Engine choice: lighter NLP crate, not Harper

The plan picked Harper as a "SoTA grammar engine" on the premise it was pure-Rust
and lightweight. By implementation time `harper-core` v2.5.0 pulled ~490 transitive
crates including the `burn` deep-learning framework, far too heavy for a CLI
linter and a real cost to bit-for-bit reproducibility. None of the equations need
a model or even POS tags; they are token/window heuristics. Decision: drop Harper,
use `unicode-segmentation` (zero transitive deps) for sentence/word boundaries and
hand-roll the corpus and equations.

## Verification lanes

Per `call/0002` (lanes by property type, now in the spine), the equations are
**functional invariants**, allium's lane, not TLA+ (which is reserved for
timing/concurrency).

- **host-grammar.allium** specifies the prose-tell entities, every structural
  equation, the composite gate, and the invariants.
- **tests/prose_properties.rs** is the property-based lane: one proptest property
  per invariant, black-box over `scan_prose`/`tell_score`, plus a **refinement
  property**: the engine's total anaphora weight equals an independent
  declarative sum over maximal runs, with the end-of-stream tail explicitly
  exercised (the run-accumulator's tail-flush is the classic off-by-one site).
  Writing it surfaced that anaphora detection relies on standard sentence
  capitalization (UAX#29 only breaks `". "` before a capital), true of real
  prose. TLA+ was considered and declined: there is no interleaving or timing to
  model, so the escalation bridge does not fire.
- **host-lint.allium** records the checker-side contract: `ScanProse` maps every
  tell to warn, and the `ProseTellsAreAdvisory` invariant (never flag).

## Comment hygiene

The engine's own comments are the dogfood: terse single-line or proper rustdoc
API form, no motivating prose, the waffle the prose engine itself flags.

## Reproducible build re-pin

host-grammar `aec090c` to host-lint `43b8ccd` (v0.3.0) to `.host-software` pin
`43b8ccd`, artifact `600e5c97…`, double-build reproducible in the digest-pinned
`rust:1.95.0` container. CI `reproducible-build.yml` rebuilds and verifies.

## Interface: idiomatic for agents, not MCP

The agent interface is the existing CLI: `echo "$draft" | host-lint --stdin --json`
before committing, plus the git hook and the `.claude/skills/host-lint` skill. No
MCP server, over the top for a fast CLI linter.
