# host-lint exempts sanctioned vocabulary via a repo-root allow file

- Status: superseded by the methodology spine (host-template @ 94a1ac7)
- Date: 2026-06-14

## Context and Problem Statement

The migration protocol (`call/0005`) says history is immutable by default and
legacy tells are *acknowledged, not rewritten*. But the audit engine had no way
to *express* an acknowledgement: `host-lint` knew only "is this a tell?", with
repo policy hardcoded in a shell wrapper. So a token that is legitimate
vocabulary in a given repo, a version string (`NT 3.1`, `DOS 6.22`), a release
identity, a cross-repo filename one is forbidden to rename, flagged with no
sanctioned way to clear it short of editing the file.

This bit hard on the first external dogfood. The Agentic-MCP-Win32s migration
(PR #1) chased "zero tells" the only way the tool allowed: by rewriting protected
content (append-only `MEMORY.md` and closed, immutable milestone bodies) which
violated two standing rules and dissolved precise historical identifiers
(review codes, work-item codes) into vague prose. The missing capability, not the
agent's judgement alone, forced the over-reach.

## Considered Options

1. **An acknowledged baseline**: record the existing flagged *occurrences*
   (by file + text), exempt exactly those, keep flagging anything new. Solves
   "acknowledge this historical body" precisely; carries a baseline file that
   must be regenerated as files move.
2. **A sanctioned-token allow-list**: list *phrases* that are legitimate
   vocabulary anywhere in the repo; never flag those tokens. Location-independent;
   simple; does not by itself protect an arbitrary historical line that happens to
   contain a real tell.
3. **Both.**

## Decision Outcome

Chosen option 2: **a sanctioned-token allow-list, and only that, for now.** A
repo-root `.host-lint-allow` file lists one phrase per line (`#` comments, blank
lines ignored). Each phrase is masked out of every line before classification
(case-insensitively, at word boundaries) so the occurrence never flags in any
mode (`--stdin`, files, `--all`, `--log`); a missing file means no allow-list, so
the feature is opt-in and behaviour is unchanged.

The word-boundary rule keeps an entry honest: an entry masks only its exact
phrase, not a longer tell that merely shares its prefix, and a *different* tell on
the same line still flags (the concrete demonstration lives in host-lint's README). Masking
reuses the existing classifier untouched rather than adding a parallel suppress
path.

Baseline (option 1) was **deliberately deferred**, not rejected on the merits.
The Win32s lesson is that the right migration move is to *rename* ordinal
milestone docs to content names, not to baseline their old bodies, so the
acute need is exempting genuine vocabulary, which the token list covers. A
per-site baseline is the correct tool for "this real tell is acknowledged legacy
we will not touch" (the pgs-release history class); add it when a target
concretely needs it, against a real case, rather than speculatively.

This does **not** relax the methodology: the allow-list is for tokens that are
not slop. The standing preference is still to name work after its content
(`host-lint`'s `VOCABULARY.md`); the allow file is the escape hatch for genuine
vocabulary, sized so it cannot quietly silence a real tell.

## Consequences

- Good: a migration can acknowledge legitimate numbered vocabulary instead of
  rewriting protected, append-only, or immutable content, the failure mode that
  produced Win32s PR #1.
- Good: the rule is small and predictable (literal phrase, word-boundaried,
  location-independent) and adds no dependency to a deliberately dependency-free
  binary.
- Cost: an allow file can be abused to hide real tells; mitigated by the
  boundary rule, by keeping it opt-in, and by the documented "not for silencing
  slop" guidance. It remains a trust surface, reviewed like any config.
- Deferred: the per-site acknowledged baseline (option 1) remains unbuilt; the
  pgs-release dogfood is the likely forcing case.
