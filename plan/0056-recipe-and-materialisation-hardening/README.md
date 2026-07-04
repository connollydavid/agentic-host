# plan/0056 recipe-and-materialisation-hardening: host-lifecycle legible and fail-safe to a heavily-quantized operator

This milestone gathers a superset of host-lifecycle defects that share one root: **the tool
trusts input, state, and on-disk layout that a heavily-quantized operator mis-authors, or that
fights git tooling and its own docs.** Each is a place where host-lifecycle should normalize the
input, fail safe on a degenerate state, or present a layout that neither git nor a cold reader can
misread. The cast's Fen (the real `qwen3.5-4b`) is the acceptance test.

## Where it came from

A cross-project read-only audit for a single quote-leak class (opened as
[connollydavid/host-lifecycle#6](https://github.com/connollydavid/host-lifecycle/issues/6)) found the
reported `worktrees = "main"` leak was one symptom of a systemic raw-value read across the whole
`.host-software` parser, and the same class recurring fail-safe in host-lint and latent in host-prove.
Probing that result, the operator surfaced three more defects of the same family: `remap` bailing on an
empty dictionary rather than a fail-safe no-op
([#7](https://github.com/connollydavid/host-lifecycle/issues/7)), and the bare-store layout naming a
bare repo `.git` inside the component dir, which git tooling misreads as a working tree
([#8](https://github.com/connollydavid/host-lifecycle/issues/8)), and the template pinning an outdated
host-lifecycle that no release bumps ([#9](https://github.com/connollydavid/host-lifecycle/issues/9)).
Four defects, one root: the tool is not yet robust to the weak-agent author, the degenerate state, and
the release drift the methodology explicitly serves.

## The superset

| # | Defect | Decided direction | Class |
|---|---|---|---|
| [#6](https://github.com/connollydavid/host-lifecycle/issues/6) | `.host-software` value lines read raw; ordinary ASCII quotes leak into refs, paths, hashes, URLs | Normalize value lines on the existing `stamp_value_after_eq` model (unquote a `"…"` wrapper, reject a stray quote); cover every value field and both parsers; regression fixture | recipe parsing |
| [#7](https://github.com/connollydavid/host-lifecycle/issues/7) | `remap` exits 2 on an empty or absent `.host-remap` | Fail-safe no-op: `--apply` no-op exit 0; `--check` still scans with zero rules and exits on the tells; informational status lines, not error; keep malformed-dictionary errors; anti-hollow test | control-flow fail-safe |
| [#8](https://github.com/connollydavid/host-lifecycle/issues/8) | Bare store named `.git` inside `software/<name>/` fights git tooling; docs describe a third layout | Adopt `.bare` + `.git`-file per component; reconcile the stale docs; re-materialize; supersede plan/0029's bare-store placement | on-disk layout + doc reconcile |
| [#9](https://github.com/connollydavid/host-lifecycle/issues/9) | Template pins an outdated host-lifecycle that no release bumps | A tool release bumps the template's pin, and a gate fails on a stale pin (durable policy `call/0038`) | release process |

The detailed per-defect implementation plan is in [implementation.md](implementation.md); the durable
policy for #9 is recorded in `call/0038`.

## The cast's throughline

Fen (qwen3.5-4b, Q8_0) is the milestone's acceptance test, not a lens: the design is validated by
driving the real 4B to author a `.host-software` value, operate `remap` on an empty dictionary, and
read the materialized layout, and confirming it succeeds where the un-hardened forms fumble it. Two
persona demands run across all three defects:

- **Fen:** the tool must carry the process and name the single next action; silence and a
  red-error-on-benign both fail it. This shapes #7's status lines and #6's split between a loud error
  on a malformed value and a benign no-op on a merely-empty one.
- **Bly (writes now, reads cold; its own auditor):** the record and the layout must fail safe and
  never over-report. An empty remap says "nothing to do", not "done" (#7); the docs must match the
  code so a cold read is not misled (#8); a normalized value must not silently launder a corrupt pin
  (#6).

Because these touch tool behaviour the spine relies on, the milestone is gated on a cast review
(`cast/applying-personas.md`).

## Supersedes and owes

- #8 supersedes plan/0029's bare-store placement (`software/<name>/.git` becomes
  `software/<name>/.bare` plus a `.git` file). A `call/` decision records the change and its migration.
- #8 also surfaces a reconcile gap: the reconcile pass does not cover the recipe's on-disk layout, so
  the plan/0029 doc drift stood undetected. Whether reconcile should is an open question, out of scope
  here.

## Verification

Ships as one host-lifecycle release, then re-vendor and propagate to consumers, with the whole-suite
verify gate green across host-lifecycle and every consumer, and the Fen probe passing on the three
flows. Each defect carries its own regression test; #7 and #8 additionally assert the anti-hollow and
the tool-legibility properties.

## Open questions

- Whether #6, #7, #8 ship as one release or a small series (they are independent fixes with a shared
  root; one release is simpler for the pin bookkeeping).
- The migration path for already-materialized components under #8 (re-materialize from `url` + `pin`,
  or an in-place move of `.git` to `.bare` plus writing the `.git` file).
- Whether the `--check` empty-dictionary scan (#7) should honor `.host-lintignore` for `MEMORY.md` the
  way the full `--all` path does (it already collects via `is_target` / `path_ignored`, so likely yes;
  confirm).
