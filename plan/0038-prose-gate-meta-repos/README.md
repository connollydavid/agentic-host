# Prose-gate the meta repos

**Status: complete (landed 2026-06-24).** host-template (`9268d76`) and host (`1dc9cb9`)
are prose-clean and each carries a `Prose` CI gate pinned to host-lifecycle v0.24.2
(host's is its first CI workflow); both gates are green in CI. The agentic-host pointer
and host pin moved in `0813795`; whole-suite CI is green. The one apparent blocker, the
`harness` ai-diction on `` `kani:<harness>` ``, was a density artifact (two occurrences
crossed the gate; one is clean), cleared by rewording the second occurrence, so no engine
change was needed.

## Context

plan/0036 stopped the *instance* docs (this repo's `README`/`CLAUDE`/`STRUCTURE`)
drifting from the spine, and the verify gate already runs `host-lifecycle prose .` over
agentic-host's own tracked markdown. But the two repos that *author* the methodology
prose are not gated, so their docs carry slop the spine itself forbids:

- **host-template** (the spine): 90 prose-trope warnings. plan/0033 cleaned `CLAUDE.md`
  and `STRUCTURE.md`, but the rest were never swept: `UPGRADING.md` 37, `cast/` 26,
  `README.md` 13, the example `plan/` 7, `MIGRATION.md` 3, `call/0000` 3, `CLAUDE.md` 1.
- **host** (the single-file front-door): one `README.md`, 29 warnings, and no CI at all.

The spine states "authored docs carry zero prose tropes, as an ongoing rule"; this
milestone makes the spine and the front-door obey the rule they publish. It is the same
drift root cause as plan/0036, one level up: a rule with no gate on the repo that owns it.

## Approach

**Clean, then gate** (a gate over dirty docs is red on day one). Reword by default, the
methodology's standing disposition. One care-point: `UPGRADING.md`'s `verify =` and
`requires =` lines are machine-checked, so they stay **byte-for-byte** (the plan/0033
precedent); only surrounding prose is reworded. The `cast/` personas and example
`plan/`/`call/` docs are ordinary reword-in-place. This milestone edits the **host** repo,
which agentic-host otherwise treats read-only, an accepted boundary crossing for this work.

No `UPGRADING` ledger entry: an adopted project already runs the prose gate through the
verify phase, so adopters inherit nothing new. This brings the meta repos under the
existing rule via their own CI; it is not a spine rule change.

## Build order

1. Clean **host-template** to zero prose warnings (`UPGRADING` preserving the machine-checked
   lines, `cast/`, `README`, `MIGRATION`, `CLAUDE`, the example `plan/`/`call/`), meaning
   preserved. Verify with `host-lifecycle prose host-template`.
2. Add a **prose-check CI job** to host-template (install the pinned host-lifecycle, run
   `host-lifecycle prose .`, fail on any trope). Commit and push host-template; bump pointer.
3. Clean **host**'s `README.md` to zero warnings and add host's **first CI workflow** with
   the same prose gate. Commit and push host; re-pin `.host-software`.
4. Verify both gates green in CI; agentic-host's own gate stays green; whole-suite green.

## Verification

- `host-lifecycle prose host-template` and `host-lifecycle prose software/host/main` both
  report clean (zero flag and zero warning).
- The host-template prose CI job and the new host prose CI job both pass.
- agentic-host `software --check`, `validate`, `reconcile`, `prose`, and `book --check`
  stay green; whole-suite CI green across the affected repos at close.
