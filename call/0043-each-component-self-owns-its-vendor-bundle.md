# call/0043: each artifact component self-owns its vendor bundle

- Status: accepted
- Scope: host-lifecycle
- Date: 2026-07-07

## Context and problem

call/0021 established that host-lint owns a superset vendored-dependency bundle, shared with
host-lifecycle: host-lint's dependency closure was a superset of host-lifecycle's, so one bundle served
both. plan/0065 (call/0042) added tokio and serde_json to host-lifecycle for the MCP surface. host-lint
uses neither, so its closure is no longer a superset, and no host-lint-derived bundle can carry
host-lifecycle's offline dependencies. Meanwhile host-reference and its out-of-process helpers already
self-own their bundles on their own releases repos, so the shared-superset arrangement is the lone special
case in the tree.

## Decision

Retire the special case. Each artifact component self-owns its vendor bundle, vendored from its own
`Cargo.lock` and hosted on its own releases repo. host-lifecycle publishes its own `vendor-v1`; host-lint
keeps its own bundle for itself. The hermetic-build mechanism of call/0021 is unchanged: the bundle is
staged, hash-verified, and built against under no egress; only that decision's ownership clause (host-lint
owns the superset, shared) is superseded here. The result is one uniform rule, a component self-owns its
bundle, in place of two.

The migration is a one-time, atomic re-pin: re-vendor host-lifecycle's own dependencies, publish the
bundle, and flip the single `deps-bundle` line in `.host-software` and host-lifecycle's own
`deps-bundle.lock` from the shared host-lint pin to the self-owned one. The old shared bundle stays live
until the pin flips in the release commit, so no build breaks mid-transition.

## Consequences

Good: a uniform, decoupled model with no cross-component superset relationship to preserve; a dependency
change in one component never forces a re-vendor of another. No adopter is affected, because the deps-bundle
is a per-component reproducibility anchor and an adopter carries its own components and bundles. host-lint is
untouched, and its orphaned shared bundle retires with its single consumer. Bad: host-lifecycle now carries
its own bundle to maintain, the same per-component cost host-reference already pays. This is the natural
price of host-lifecycle's dependency set diverging.

## Relates

call/0021 (the hermetic-build mechanism, whose shared-ownership clause is superseded here); call/0042 (the
tokio addition that diverged host-lifecycle's dependencies); plan/0065; plan/0032 (the reproducible
re-vendor recipe).
