# Adoption is a clean break to a pristine state; upgrade is a Shallow delta

- Status: accepted
- Date: 2026-06-14
- Refines: `call/0005` (does not supersede it — the cased/moded protocol stands; this corrects how mode is chosen and fixes a factual error in a target audit).

## Context and Problem Statement

`call/0005` made **Shallow the universal default** and treated history as
immutable-by-default, gating any rewrite behind a provenance prohibition. Two
problems surfaced while applying it.

1. **The token ledger.** A clean break costs *more* at migration time but *less*
   per future session: one naming system, `host-lint --all` exiting 0 outright,
   no dictionary to consult, no "clean-modulo-acknowledged-legacy" subtraction to
   re-derive each session. For an *active* repo the recurring saving dominates.
   Shallow's real home is the small, frequent case — a stamped repo bumping the
   template revision — exactly like `copier update`. Treating Shallow as the
   universal default mis-priced first-time adoption.
2. **A wrong audit premise.** `call/0005` and the pgs-release brief recorded that
   pgs-release carries *external* FFmpeg patch-series provenance forbidding a
   rewrite. Examination (2026-06-14) showed otherwise: pgs-release is **not a
   fork** (567 KB, no parent) — it is planning docs (`PHASE1–14` + variants) plus
   four vendor submodules; the FFmpeg fork (`connollydavid/FFmpeg`) and its patch
   series are **ours**; the host repo's own history is ~199 commits, **100%
   authored by us**, with tells in only a minority of `docs:` subjects. The
   prohibition rested on a misattribution.

## Decision Outcome

**Correlate mode with intent, and define a clean break as three risk tiers.**

- **Adoption** (first-time — case (a)/(b), or a first-stamping case (c)): a
  *transformation* of what the repo is → **clean break to a pristine live state.**
- **Upgrade** (a stamped case (c) bumping template revision X→Y): a *delta* →
  **Shallow.** Small, frequent, non-disruptive.

A **clean break** is unbundled by risk, because the tiers are not equally safe:

1. **Live files** (structure, governance, plan docs, skills): rewrite freely to
   content names. No ceremony. This is where most of the recurring saving lives.
2. **Owned append-only record** (`MEMORY.md`, closed milestone bodies): may be
   rewritten at adoption **only archive-first + map-only + recorded** — the
   document analog of a Deep history rewrite, governed by `CLAUDE.md` §6. Original
   archived verbatim; only mapped rename tokens substituted; unmapped identifiers
   (`finding #7`, `rmcp 1.7`, work-item codes) left byte-for-byte; the diff shows
   nothing but substitutions. Never free-form, never self-authorized.
3. **Git commit history**: **acknowledged, not rewritten, by default** — even in a
   clean break. Re-shaing every commit (re-pointing tags, diverging branches,
   stale refs) rarely beats the value of de-numbering old subjects. Reserve Deep
   for the exceptional case where history coherence genuinely matters *and* the
   history is ours.

**Provenance test, corrected.** The bar is "history whose shas external consumers
depend on," **not** "touches a patch series." A patch series we author (e.g.
`connollydavid/FFmpeg`) is ours and rewrite-tolerant: rebasing is its native
lifecycle, and a local rewrite produces a normal v2/v3 — it cannot corrupt an
already-submitted series. So no target is categorically Deep-forbidden merely for
having patches; the decision is cost + ownership, per `call/0005`'s selection rule.

## Consequences

- Good: the model matches how scaffolding tools actually work — clean *generate*,
  incremental *update* — and stops mis-pricing adoption as a minimal diff.
- Good: corrects the pgs-release provenance error before it hardened into doctrine.
- Good: the one dangerous operation (rewriting the owned record) is gated by an
  explicit, verifiable discipline (archive-first, map-only, recorded) rather than
  forbidden outright or — as in Agentic-MCP-Win32s PR #1 — done free-form under a
  self-invented authorization.
- Cost: "adoption = clean break" raises the one-time spend and the tier-2
  fabrication risk; mitigated by the map-only discipline and by preferring the
  deferred `host-lint` baseline (`call/0006`) to carry `--all`-cleanliness when a
  record rewrite is not worth its cost.

### Per-target consequences (correcting the `call/0005` audit)

- **Agentic-MCP-Win32s** (adoption): clean break. Live PHASE docs → content homes
  freely; `MEMORY.md` + closed bodies rewritten **map-only, original archived**;
  host git history acknowledged; record the authorization in a `call/`.
- **pgs-release** (adoption): **Staged-Shallow for the host migration — by cost,
  not prohibition.** ~199 owned commits, 11 release tags (`n*-pgsN.N`) and two
  branches make a host-history Deep rewrite not worth it. Clean-break the live
  PHASE docs → content homes (tier 1); acknowledge host git history (tier 3); keep
  the release tags as identities; submodules untouched. Cleaning the ffmpeg patch
  subjects for upstream is a separate, **permitted** rebase in our fork, out of
  scope for the host migration.
