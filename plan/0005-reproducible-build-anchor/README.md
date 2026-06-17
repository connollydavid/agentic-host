# Reproducible-build production anchor

Make the `.host-software` pin a *true* production anchor, resolving the deployed-anchor
finding (issue #10): `software --check` was green while being materially wrong about
what runs in production — it audited only `canonical HEAD == pin` (source SHAs), never
that the deployed artifact derives from that pin, and the line production shipped from
could be excluded from the recipe.

The fix is a requirement, not just a check: **software initiated under the methodology
has reproducible builds** — its deployed artifact is byte-reproducible from the pinned
source plus a recorded build recipe, so a clean rebuild from the pin equals what is
deployed. Pre-existing/migrated software (not initiated under the methodology) converges
toward that goal and may carry a `repro-exempt = call/NNNN` **case decision** (a
software-scoped `call/` decision) until it does.

What landed (host-lifecycle **v0.8.0**, template `e49d8d9`):

- `.host-software` gains optional per-component provenance: `build`, `toolchain`,
  `deploy` (which line ships), `artifact = <worktree-path> <sha256>`, `repro-exempt`.
- `software --check` adds the cheap attestation: the `deploy` line must be a recorded
  worktree, a `repro-exempt` must cite an existing decision, and a present `artifact`
  must hash to the record.
- `software --verify-build` is the proof: materialize a throwaway worktree at the pin,
  run `build`, and fail unless `artifact` reproduces — an exempt component (citing a
  real decision) is warned and skipped. Reference CI workflow shipped in the template.
- Spine states the requirement + the migrated-software escape clause; `UPGRADING.md`
  entry `e3b174d` (requires v0.8.0).

Follow-on (not in this milestone): wiring host-lint's *own* reproducible build into
this repo's `.host-software` (real determinism work — pinned toolchain, reproducible
release artifact). This milestone delivers the mechanism and the requirement; applying
it to our software is its own task.

Resolves issue #10.
