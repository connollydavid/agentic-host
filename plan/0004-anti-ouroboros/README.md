# Anti-ouroboros: methodology to the spine

Self-migration to `host-template @ 94a1ac7` — adopter zero applies the
anti-ouroboros upgrade to itself.

The Why room must not feed on its own methodological tail. The methodology is
owned by the template spine (`CLAUDE.md` + `STRUCTURE.md`), inherited by
copy-at-version; it is not re-litigated as this project's `call/` decisions. A
settled methodology decision is retired the MADR way — `Status: superseded by the
spine`, in place — keeping the immutable log intact.

What landed:

- **host-lifecycle v0.7.0** — `validate <call-dir>` scope gate: an accepted
  decision must carry a `Scope:` header and must not be `Scope: methodology`.
- **host-template spine** — states the anti-ouroboros principle and the
  inherit-from-the-source rule; de-references the `call/NNNN` authority pointers
  (the rules stand on their own); reduces the template's `call/` to one worked
  example; UPGRADING ledger entry keyed at `6db01f3` (requires v0.7.0).
- **agentic-host (this repo)** — superseded its methodology decisions
  (`call/0000`–`0012`, `0014`) in place, kept as immutable history; kept `0013`
  (this repo's own name reservation) live with `Scope: instance`; added a root
  `README.md` / `STRUCTURE.md` stating the adopter boundary.

Resolves issue #9 (methodology vs instance-decision conflation). Issues #7 and #8
(`host-lifecycle book`) remain open and follow separately.
