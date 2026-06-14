# TEMPLATE-REWRITE — rewrite host-template into the canonical agentic host

Plan for the parked "template content rewrite" work. The template scaffold exists
(`tools/` submodules, `.claude/skills`, `cast`/`plan`/`call` seed, `STRUCTURE.md`);
what remains is replacing the **inherited Karpathy-guidelines skin** with our own
canonical methodology, retiring the inherited artifacts, and flipping the license
to Unlicense. This is the coupled CLAUDE.md-rewrite → Unlicense-flip.

## Anchors (heads at time of writing, 2026-06-14)

- template `host-template` @ `0e5dd7f`
- host-lint `c0b19f4` · host-grammar `342f507` (v0.1.1) · host-lifecycle `6dac2fc`
- host `agentic-host` @ `7ad7e8e`

## Inherited artifacts still on the template (to replace/retire)

- `README.md` — titled "Karpathy-Inspired Claude Code Guidelines"; has a plugin
  install section.
- `CLAUDE.md` — the four Karpathy principles only (swept to say `host-lint`); no
  agentic-host methodology.
- `skills/karpathy-guidelines/` — the inherited single skill.
- `.claude-plugin/{plugin.json,marketplace.json}` — plugin/marketplace metadata.
- `LICENSE` — MIT, © "Jiayuan Zhang and the andrej-karpathy-skills contributors".

## Steps

1. **Retire inherited artifacts (mechanical).** `git rm -r skills/karpathy-guidelines
   .claude-plugin`; remove the plugin-install section from `README.md`.
2. **Rewrite `CLAUDE.md` as the canonical methodology** — our own words (this is
   what makes the content ours and enables the Unlicense flip). **Tight framing
   (D1): write for weaker LLMs and lesser harnesses — crisp, explicit, directive;
   clarity over cleverness; never rely on a strong model to infer intent.** Outline:
   - What an agentic host is — host = externalized *thought*, software = *action*;
     the five-W rooms (`cast`/`spec`/`plan`/Where-slot/`call`/tools).
   - The four working principles — think-before-coding, simplicity-first,
     surgical-changes, goal-driven-execution — Karpathy-inspired, rewritten,
     credited in Provenance.
   - The three verification lanes — host-lint (hygiene), allium (requirements +
     property-based testing), Specula (timing/concurrency via TLA+) — plus
     reference-not-vendor and instruct-not-patch.
   - The `host-*` tools — host-grammar (rules), host-lint (checker), host-lifecycle
     (token-free generator/validator); generator and checker share host-grammar.
   - Names/numbers/milestones (`plan/`), decisions (`call/`, MADR from the `0000`
     bootstrap), specs (`spec/` `.allium`/`.tla`), personas (`cast/`, XP-Persona).
   - Audited plans + append-only MEMORY discipline.
   - Provenance — Karpathy's observations via Jiayuan Zhang (@forrestchang);
     personas via Powell, Keenan & McDaid (2007).
3. **Reframe `README.md`** → "the agentic-host template": what it is, how to
   instantiate (clone → `git submodule update --init` → replace `cast/` examples →
   add the software submodule), Provenance, Unlicense.
4. **Flip `LICENSE` MIT → Unlicense** (the content is then ours; Provenance carries
   the credit, not an obligation).
5. **Commit + push** the template.

## Decisions (resolved)

- **D1 — CLAUDE.md scope → full cut, tightly framed.** Write the full methodology
  (the rewrite below), but for **weaker LLMs and lesser harnesses**: crisp, explicit,
  directive framing; clarity over cleverness; never rely on a strong model to
  infer intent. The doc must be followable by a weak agent — that is the success
  criterion.
- **D2 — Host ↔ template sole-source → defer liberally.** The host builds the
  template whose methodology the host itself follows — a self-hosting bootstrap
  (a C compiler compiling a C compiler). Defer the host-sync; reconcile later.
  This pass touches only the template's identity.

## Follow-up tidy-ups (separate, not blocking the rewrite)

- Bump `tools/host-lint` submodule pointers (template + host) `a9a7cd3` → `c0b19f4`
  to pick up the host-grammar refactor.
- Refresh the host's **installed** git hooks — they still call the `no-phase`
  binary (per-clone, local); point them at `host-lint`.
- Update or close host issue #1 — its phase-naming topic is superseded by the
  cast/spec/plan/call + three-lane design.
