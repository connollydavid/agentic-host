# plan/0057 implementation

The two operator rulings settled the design fork: the verb is `software --lock <name>`, and the
graduation commit answers to **release-grade** authority (it drives a normal producer release, so
`.host-software` keeps pinning a released, tagged commit; dual-release-authority is unchanged and no
gate is loosened).

## The owed advisory summary (`software --check`)

`provenance_problems` already prints the onboarding `note` and returns it as a non-fault (it does not
add to `bad`, so onboarding stays green). It gains a `&mut Vec<String> owed` out-parameter, and the
onboarding branch pushes the component name. `software_check` threads the `owed` list through, and
the `software --check` caller prints a counted, enumerated summary that names the next action:

```
-- N deps-bundle graduation(s) owed: <names>; run: host-lifecycle software --lock <name> <dir>
```

Owed stays **exit 0**, deliberately. Turning onboarding into a fault is the retro-red trap plan/0051
rejected, and it would deadlock the graduation: `--lock` drives a release whose verify gate re-runs
`software --check` (a `HOST_LIFECYCLE_IN_CHECK` re-entrancy guard sits on exactly that path), so a
non-zero owed exit would block graduating one component while the others are still legitimately owed.
The fix for the under-report is loudness, not a fault: a counted, enumerated line, re-listed every
run, derived from repo state (declares a `deps-bundle`, no matching lock on disk). That makes it
idempotent and self-re-listing, so a partial graduation re-lists the remainder, and a cold read
surfaces the debt rather than a green that hides it (Bly's over-report direction).

## The graduation verb (`software --lock <name>`)

The component name is the flag's value rather than a positional, so it never collides with `<dir>`.
The verb:

1. Resolves the component. If it declares no `deps-bundle`, it errors (exit 2). The worktree must be
   materialized at its pin.
2. Reads the on-disk lock and fails loud on the wrong state:
   - a lock equal to the pin is already locked, a no-op success (exit 0), so the verb is idempotent.
   - a lock that differs from the pin is producer drift; the verb refuses (exit 1) rather than
     overwrite a disagreeing lock.
   - no lock is the onboarding case, which proceeds.
3. Writes `deps-bundle.lock` as the recorded `<url> <sha>` (so the content is never hand-typed) and
   stages it.
4. Drives `run_release(root, name, Some("neither"), false)`: the verify gate, the tool-computed
   fix-only version bump, the container rebuild that re-derives the byte-identical artifact hash (the
   lock is provenance, never compiled in), and the operator-run outward steps (commit the staged lock
   and the bump, tag, push, re-pin `.host-software`, record the receipt). The outward steps stay
   operator-run, consistent with the existing `release` verb, so the local mechanical work is
   tool-carried and the single next action is named at each step (the Fen bar).

Writing the lock before the gate is safe: the check reads the lock from disk, so the just-written
lock reads `ok` (not owed) during the gate.

## Spec, obligations, tests

- `host-lifecycle.allium`: the owed state is a first-class advisory `Owed` entity, a
  `DetectOwedGraduation` rule (`bundle_owed` implies an `Owed` record, never a `Finding`), and an
  `OwedNeverHazards` invariant (an owed component's pin vacuously matches, so onboarding never
  hazards). The `--lock` verb is a mutation at the altitude of `materialize`/`release`, so the
  check-spec models the owed state it surfaces, not the verb. Five new obligations dispositioned.
- Rust unit tests: owed detection (a bundled component with no lock is owed; a matching lock is not; a
  differing lock is a fault, not owed). The `--lock` fail-loud branches are exercised by the actual
  graduation and the Fen probe.

## As-built status (local, green)

The code and spec are implemented and green locally: `software --check` prints the counted owed
summary at exit 0; `--lock` guards resolve, refuse a non-bundle component, refuse a drift, and drive
`run_release`; `allium check`/`analyse` clean; all 41 obligations dispositioned; 132 tests pass;
clippy clean. What remains is outward: the Fen acceptance probe, then the release cascade (release
host-lifecycle, re-vendor, propagate, graduate the three components), each pushing to a producer
repo.

## Cascade (after the code is green)

1. Release host-lifecycle (the new verb plus the owed summary is a feature; change class likely
   `adds-flag`). Re-derive the artifact, tag, re-pin, record the receipt.
2. Re-vendor and propagate to consumers per the recorded recipe.
3. Graduate the three onboarding components with the new verb (`software --lock host-reference`,
   `host-reference-ocr`, `host-reference-openscad`), each a `neither` producer release, then re-pin.
   They are the ramp's first customer.
4. Whole-suite verify green, `software --check` at exit 0 with zero owed, receipts recorded.

## Acceptance

Fen (the real `qwen3.5-4b`) is handed the one-command graduation and must complete it, and, as the
baseline, must fumble the manual hand-write-and-release form. The cast review gates the design.
