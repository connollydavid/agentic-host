# plan/0096 ci-receipt-phase: the lane outcome becomes a receipt

The build milestone plan/0095 recommended (the design survives review; the
operator ruled go). Host-lifecycle gains the `ci` surface, the judge joins
`software --check`, the template carries the per-turn duty and the two
documentation gaps, and the forge adopts its own receipts; the gate that
certifies the design is the design working.

## Scope

1. **The `ci` verb.** `host-lifecycle ci <dir>` discovers the lanes
   (`.github/workflows/*` at the host root and each materialized component) and
   judges offline: every discovered lane at the current revision (host root) or
   the recorded pin (components) must carry a `ci` receipt whose revision
   matches and whose conclusion is success. Absence, failure, and a stale
   revision each HAZARD, carrying the remedy. `host-lifecycle ci <dir>
   --record <label>/<lane> --run <url> [--revision <sha>] [--conclusion
   <c>]` writes the receipt; `--conclusion` defaults to success, `--revision`
   to the component's pin or the host HEAD, and `--all` records every
   discovered lane in one invocation for the per-turn duty.
2. **`software --check` integration.** A `ci` section after the component
   walk: discovered lanes are named, receipts are judged, and a component with
   no workflows prints the named absence line; a component with no spec-driven
   lane states its absence instead of being implied away.
3. **Run-anchored evidence.** `software --verify-build` cites the `ci` receipt's
   run beside the digest when one exists at the built revision.
4. **The template landing.** The manual gains the per-turn duty clause; the
   `[software]` `toolchain` key documentation names a digest-pinned container
   image; the ledger entry carries the duty with its verify.
5. **The forge adopts.** The ledger entry is recorded through the tool, and the
   forge records its own lanes' receipts at the released pins; the receipts
   this plan creates are the first ones the judge consumes.

## Results

Recorded at closure.

## Results

Recorded 2026-09-26, same session. The `ci` surface landed in host-lifecycle
v0.55.0 (34a6bd8, artifact fa8ae1bd1a24baeb2b88b28cd2368ec0d5189071ea4ad8871cddefcb60f60f5c,
feature class, suite 312 plus 40, clippy clean): `discover_ci_lanes` from
`.github/workflows/`, `ci_lane_problems` judged offline, the `ci` verb with
`--record/--run/--revision/--conclusion`, the check integration with the named
absence line, and the verify-build run citation. The template landed the per-turn
duty in the manual, the `toolchain`-is-a-digest-pinned-image documentation, and
the ledger entry `fbdb176` (verify: the duty text in the manual), which this host
recorded through the tool at **zero pending**. The embed-equality chain rode the
same landing: lint v0.22.2 (grammar at 6cd41c3) with the vendor-v19 bundle, and
lifecycle v0.55.0 carrying both through the vendor-v11 bundle, so the recipe pins
match the embedded engines at every level (call/0052).

The forge then recorded its own receipts: thirteen lanes discovered across the
host root and eight components; twelve discharged with success receipts citing
their run URLs. The thirteenth; host-lint's own lane at v0.22.2; waits on its
kani rung at the writing of this section and records the moment the run
concludes. The judge's first honest findings were exactly the design's point:
lanes that had run green for months were absent from every receipt until this
plan wrote them down.
