# Specs live with the software (dogfood allium, relocate specula)

## The smell (a methodology bug)

The five-room model puts behaviour/timing specs in the **host**, at
`plan/<milestone>/spec/` — quarantined from the software they describe. That is a
bad smell: a spec and the code it constrains should move, version, and break
together, the way a test lives next to its code. The concrete instance:
`ParallelScan.tla` sits in `agentic-host/plan/0008/spec/` while the code it specs
(`scan_chunked`) lives in `host-grammar`. The `.allium` specs were already
correctly co-located in their software repos (`host-grammar.allium`,
`host-lint.allium`), which makes the `.tla` placement the outlier.

**Fix:** specs (`.allium`, `.tla`) live in the **software repo**, beside the code,
and are verified by **that repo's CI**. The host's `plan/<milestone>/` references
a spec by path/pin; it does not contain it. This is a spine change to the
template's "What" room.

## Work

### 1. Dogfood allium for real (the trigger)

Both `.allium` files are hand-written pseudo-syntax that the real
`allium-cli 3.4.2` rejects (no `-- allium: N` version marker; free-form English
clauses are not valid block items). Rewrite each into conformant allium until the
**advanced gate** passes:

- `allium check <spec>` — parse + structural diagnostics (no `error` severity).
- `allium analyse <spec>` — process completeness: data flow, reachability,
  terminal states, deadlock/conflict, invariant verification (no `error`).

Then wire a CI lane in **each software repo** (install `allium-cli@3.4.2`, run
`check` + `analyse`, fail on `error` diagnostics):

- `host-grammar` — has no CI today; add the workflow.
- `host-lint` — add the lane alongside its existing pipeline.

### 2. Relocate specula to the software

- Move `ParallelScan.tla` + `ParallelScan.cfg` from `agentic-host/plan/0008/spec/`
  into `host-grammar` (the software it specs).
- Add a specula/TLC lane to `host-grammar` CI (Temurin `21` + `tla2tools v1.8.0`,
  the versions the host lane proved), mirroring the retired `specula.yml`.
- Retire `agentic-host/.github/workflows/specula.yml`; `plan/0008` references the
  spec's new home.

### 3. Methodology spine fix

The "What" room moves from the host to the software. Update the template spine —
`CLAUDE.md` (the Specs section + the rooms table) and `STRUCTURE.md` — so specs
co-locate with the software and lanes run in the software's CI, with the host
`plan/` referencing them. Add an `UPGRADING.md` ledger entry and bump the
submodule pointer. (Methodology change → recorded in the template spine +
ledger, not an agentic-host `call/`; the `plan/0011` precedent.)

## Verification

- `allium check` **and** `allium analyse` exit clean (no `error`) on both specs,
  proven green in `host-grammar` and `host-lint` CI.
- TLC green in `host-grammar` CI; `agentic-host` no longer hosts a spec or a
  specula lane.
- Template spine reframed; `UPGRADING` entry added; `host-lifecycle validate`
  unaffected.

## Notes / honesty

- `allium analyse` is the advanced gate; if a pure data-flow spec (no stateful
  entity lifecycle) trivially satisfies reachability/terminal checks, that is a
  true result, not a bypass — recorded as such.
- Re-pinning: `host-grammar` is a cargo git dep of `host-lint`; a spec-only change
  does not alter the build artifact, so `host-lint`'s recorded artifact hash is
  unchanged when its `host-grammar` rev bumps.
