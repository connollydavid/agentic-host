# Reserve `agentic-host` for this repository; scrub the collision by a one-time history rewrite

- Status: accepted
- Scope: instance
- Date: 2026-06-16

## Context and Problem Statement

`agentic-host` was used two ways: as the name of *this repository* and as the
generic *kind* a consumer builds. The collision leaked this repository's identity
into the methodology a consumer adopts — and the `.agentic-host` stamp and the
`template-agentic-host` name carried the same ambiguity into shipped software. An
ambiguous name in the artifacts a consumer receives is a consumer-facing defect,
not a cosmetic one. This repository is meta (adopter-zero); consumers never see
its `call/` decisions, so the fix had to land in the software itself.

## Decision Outcome

- **`agentic-host` names *this repository* exclusively** — the project that
  develops `host` and the `host-*` tooling.
- **A repo that adopts the methodology is "an agentic project"** (e.g.
  `agentic-acme`). Two clean namespaces: `agentic-*` for **projects** (this repo,
  plus adopters), `host-*` for the methodology's **reusable artifacts**.
- **Structural renames:** `template-agentic-host` → **`host-template`** (the
  scaffold is a methodology artifact, not a project, so it leaves the `agentic-*`
  namespace), and the `.agentic-host` stamp → **`.host`** (joining the `.host-*`
  config family).
- **Applied as a one-time, archive-first, map-only history rewrite** across all
  four repos (`host`, `host-lifecycle`, `host-template`, `agentic-host`) — the
  sanctioned exception to history-immutability. The literal map:
  `template-agentic-host ==> host-template`, `.agentic-host ==> .host`. Nothing
  outside the map changed byte-for-byte in history.
- **Prose was forward-only** ("an agentic host" → "an agentic project", with a
  bracketed example on first mention; this repository named `agentic-host`; the
  word "forge" banned). Prose is context-dependent — the same phrase meant this
  repository in some files and the kind in others — so it could not be a history
  substitution. Legitimate "agentic" usages were preserved: *agentic tells*
  (host-lint's domain), *agentic LLM* (Wren), *agentic development*, and
  `Agentic-MCP-Win32s` (a correctly-named adopter).
- **Archive:** an `archive/pre-host-rename` tag on every repo preserves the
  pre-rewrite tip verbatim. `host`'s `v0.1.0` and `host-lifecycle`'s `v0.4.1` were
  retagged onto the scrubbed commits.

## Consequences

- Good: the methodology a consumer receives no longer carries this repository's
  name; `agentic-*` (projects) vs `host-*` (artifacts) is a clean dichotomy.
- Cost: every pre-rewrite SHA is invalid; any existing clone must re-fetch. The
  archive tags make the old state recoverable.
- This is a forge-only record. The consumer-facing half — the `agentic-*` /
  `host-*` vocabulary — lives in `host-template`'s own docs, where consumers read
  it.
