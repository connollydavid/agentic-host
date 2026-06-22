# A real verdict lifecycle so `allium analyse` bites

## Why

`plan/0012` made both `.allium` specs conform and pass `allium analyse`, but the
prose/naming entities are pure functions with no stateful lifecycle, so the
advanced gate (reachability, terminal states, deadlock) had little to verify:
honest, but a thin example. host-lint's actual flag/warn/clean decision **is** a
state machine (it maps the worst-severity match onto an exit code), so modelling
it gives `analyse` something real to check and makes host-lint.allium a genuine
example of the requirements lane.

## What shipped (host-lint.allium)

A `Check` entity with a `status` transition graph and the rules that drive it:

```
entity Check {
    status: scanning | clean | advisory | blocked   -- exit 0 / 0 / 3 / 1
    saw_flag: Boolean
    saw_warn: Boolean
    transitions status {
        scanning -> blocked     -- a flag-tier match
        scanning -> advisory    -- only warn-tier matches
        scanning -> clean       -- nothing
        terminal: clean, advisory, blocked
    }
}
```

- A boundary `surface LintRun` faces an `Invocation` (the commit hook or CLI run)
  and **provides** the `ScanStarts` / `ScanCompletes` external triggers; without
  this, `analyse` reports the triggers as unreachable.
- `StartScan` assigns the initial `scanning` status; `RecordFlag` / `RecordWarn`
  set `saw_flag` / `saw_warn` as `Match`es are created; `VerdictBlocked` /
  `VerdictAdvisory` / `VerdictClean` settle to exactly one terminal on
  `ScanCompletes`, with mutually exclusive `requires` encoding flag-beats-warn.
- An invariant `FlagBeatsWarn` states a blocked verdict is never downgraded.

This end-to-end chain (`Line.created` to detection rules to `Match.created` to
`Record*` to `ScanCompletes` to verdict) is what `analyse` now traces.

## Verification

- `allium check` and `allium analyse` both exit 0 with **zero findings** on the
  enriched spec; the existing allium CI lane (`plan/0012`) gates it.
- The gate demonstrably bites: an earlier draft without the surface drew an
  `unreachable_trigger` finding, and one without `StartScan` drew
  `status.unreachableValue` for `scanning`, both real, both resolved.

## Methodology

Software-only (host-lint's own spec); no spine change. Commit host-lint, re-pin in
`.host-software` (a spec-only change leaves the build artifact unchanged), record
here and in MEMORY.
