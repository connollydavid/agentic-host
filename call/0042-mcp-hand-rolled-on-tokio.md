# call/0042: the MCP surface is hand-rolled on tokio, not the rmcp SDK

- Status: accepted
- Scope: host-lifecycle
- Date: 2026-07-07

## Context and problem

plan/0065 adds a spawned MCP server exposing the `init` and `adopt` verbs over stdio, with a
server-initiated elicitation request for the project name. The server is async on tokio (an operator
directive, and the elicitation request naturally wants an async request-response). The official Rust SDK,
rmcp, supports exactly this and provides server elicitation. But host-lifecycle is a lean binary with a
hash-pinned musl reproducible build against a vendored dependency bundle, so every added dependency is a
re-vendor and re-hash cost that the release must carry and re-derive.

## Decision

Hand-roll the protocol on tokio and serde_json rather than depend on the rmcp SDK. The wire surface is
small and static: newline-delimited JSON-RPC over stdio, the `initialize` handshake echoing the protocol
version and advertising a `tools` capability, the `notifications/initialized` follow-up, `tools/list`,
`tools/call`, and one server-initiated `elicitation/create`. Two fixed tools plus one elicitation Form is
about five methods, so the SDK's macro ergonomics buy little, while a stdio-only rmcp still pulls schemars,
tokio-util, url, and a support set on the order of dozens of transitive crates, from a crate that shipped a
major version bump on a one-to-two-week cadence. The reproducible build would vendor, pin, and re-derive
all of it on every bump. The hand-roll adds only tokio to the vendored set; serde_json is already present.

The server elicits only when the client declared the `elicitation` capability in `initialize`, per the
spec, and it correlates the elicitation response by its JSON-RPC id while a tool call is in flight. That
correlation is the one non-trivial piece and is the part to test hardest. The data grounding the SDK
capabilities and the wire shapes is in plan/0065 gather-data.md.

## Consequences

Good: the reproducible-build dependency surface stays lean and stable, and we hold full control of the
wire behaviour and the name backstop it wraps. Bad: we own protocol correctness, bounded because the
`2025-06-18` stdio, tools, and elicitation surface is small and stable, and we absorb a future spec change
rather than riding an upstream. Sunset: adopt rmcp if the tool set grows enough that its ergonomics and
spec-tracking outweigh the vendored-dependency tax.

## Relates

plan/0065 (the onboarding and MCP layer this serves); plan/0032 and call/0021 (the reproducible re-vendor
recipe every host-lifecycle dependency change runs); the elicitation client-support matrix recorded in the
project memory.
