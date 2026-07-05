# plan/0057 implementation

The two operator rulings settled the design fork: the verb is `software --lock <name>`, and the
graduation commit answers to **release-grade** authority (it drives a normal producer release, so
`.host-software` keeps pinning a released, tagged commit; dual-release-authority is unchanged and no
gate is loosened).

## The owed third state (`software --check`)

`provenance_problems` (src/main.rs:4823) already prints the onboarding `note` and returns it as a
non-fault (it does not add to `bad`, so onboarding stays green). It gains a `&mut Vec<String> owed`
out-parameter; the onboarding branch pushes the component name. `software_check` (src/main.rs:4477)
declares the `owed` list, threads it through, prints an enumerated summary, and returns `(bad, owed)`.

The `software --check` caller (src/main.rs:3370) then reports a distinct verdict at the exit-code
layer, so a cold-read auditor or CI gate can tell clean from clean-but-owed:

- `bad > 0` — a HAZARD or failed gate. Exit 1 (unchanged).
- `bad == 0` and `owed` non-empty — clean but a graduation is owed. Print
  `N deps-bundle graduation(s) owed: <names> (run: host-lifecycle software --lock <name> <dir>)`
  and exit 3 (advisory, the same convention host-lint uses for a warn: not a fault, but not silent).
- otherwise — fully clean. Exit 0.

The owed set is derived from repo state on every run (declares a `deps-bundle`, no matching lock on
disk), so it is idempotent and self-re-listing: a partial graduation re-lists the remainder, and a
truncated window never buries owed work behind a green exit.

## The graduation verb (`software --lock <name>`)

`--lock <name>` takes the component name as its value and reuses the `--item` filter path. It:

1. Resolves the component. If it declares no `deps-bundle`, error (exit 2). The worktree must be
   materialized and at its pin (the existing gate).
2. Reads the state and fails loud on the wrong one:
   - lock on disk equals the pin — already locked, a no-op success (exit 0), so the verb is
     idempotent.
   - lock on disk differs from the pin — producer drift, refuse (exit 1) and name the drift; never
     overwrite a disagreeing lock.
   - no lock — the onboarding case, proceed.
3. Writes `deps-bundle.lock` as the recorded `<url> <sha>` (never hand-typed), asserts it equals the
   pin, and stages it (`git add`).
4. Drives `run_release(root, name, Some("neither"), preview=false)` (src/main.rs:7955): the verify
   gate, the tool-computed version bump (a fix-only `neither` bump), the container rebuild that
   re-derives the byte-identical artifact hash (the lock is provenance, never compiled in), and the
   printed operator-run outward steps (commit the staged lock and the bump, tag, push, re-pin
   `.host-software`, record the receipt). The outward steps stay operator-run, consistent with the
   existing `release` verb; the local mechanical work is tool-carried, and the single next action is
   named at each step (the Fen bar).

Writing the lock before the gate is safe: the check reads the lock from disk, so the just-written
lock reads `ok` (not owed) during the gate.

## Spec, obligations, tests

- `host-lifecycle.allium`: model the component provenance state (onboarding, locked, drifted) and the
  `--lock` transition; disposition the new obligations in the `.obligations` manifest.
- Rust unit tests: owed detection (a bundled component with no lock is owed; a matching lock is not; a
  differing lock is a HAZARD, not owed); the `--lock` state machine (refuse a non-bundle component,
  no-op on an already-locked one, refuse a drifted one); the `(bad, owed)` return and the exit-3
  verdict.

## Cascade (after the code is green)

1. Release host-lifecycle (the new verb plus the owed verdict is a feature; change class decided at
   release, leaning `adds-flag`). Re-derive the artifact, tag, re-pin, receipt.
2. Re-vendor and propagate to consumers per the recorded recipe.
3. Graduate the three onboarding components with the new verb — `software --lock host-reference`,
   `host-reference-ocr`, `host-reference-openscad` — each a `neither` producer release, then re-pin.
   They are the ramp's first customer.
4. Whole-suite verify green, `software --check` at exit 0 with zero owed, receipts recorded.

## Acceptance

Fen (the real `qwen3.5-4b`) is handed the one-command graduation and must complete it, and, as the
baseline, must fumble the manual hand-write-and-release form. The cast review gates the design.
