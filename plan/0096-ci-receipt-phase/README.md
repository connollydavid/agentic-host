# plan/0096 ci-receipt-phase: the lane outcome becomes a receipt

The build milestone plan/0095 recommended (the design survives review; the
operator ruled go). Host-lifecycle gains the `ci` surface, the judge joins
`software --check`, the template carries the per-turn duty and the two
documentation gaps, and the forge adopts its own receipts — the gate that
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
   no workflows prints the named absence line — a component with no spec-driven
   lane states its absence instead of being implied away.
3. **Run-anchored evidence.** `software --verify-build` cites the `ci` receipt's
   run beside the digest when one exists at the built revision.
4. **The template landing.** The manual gains the per-turn duty clause; the
   `[software]` `toolchain` key documentation names a digest-pinned container
   image; the ledger entry carries the duty with its verify.
5. **The forge adopts.** The ledger entry is recorded through the tool, and the
   forge records its own lanes' receipts at the released pins — the receipts
   this plan creates are the first ones the judge consumes.

## Results

Recorded at closure.
