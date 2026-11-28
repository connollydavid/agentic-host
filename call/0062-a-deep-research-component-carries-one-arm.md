# call/0062: a deep-research component carries one arm behind the run contract

- Status: accepted
- Scope: `host-deep-research`, plan/0113
- Date: 2026-11-28
- Relates: plan/0113, call/0010, call/0033, call/0038

## Context and problem

plan/0113 compares four deep-research arms against a null control on one
pinned OpenCode harness, then confirms the locked arm on a sealed held-out
set. The comparison is only useful if the winner can ship as a component the
suite can run and verify, not as a skill copied into a checkout. The component
needs a boundary that keeps the arm's own license, the harness pin, the model
pin and the contract in one reproducible artifact.

The arms are not the same kind of software. The null arm is a frozen prompt
over the harness's built-in tools. `hffmnnj` is an MIT OpenCode plugin that
carries a TypeScript runtime tree and a research library. `weizhena` and
`samber` are skill trees; the selection recorded their ledger gaps. Shipping
any of them as a bare copied directory would put the arm's license, its
native search route and its embedding choice outside the receipt.

## Decision

Ship `host-deep-research` as a single Rust binary whose build embeds the
runner, the contract, the pins and the arm resources.

- The component's own files are Unlicense. The bundled arm keeps its own
  license and notices; the MIT `hffmnnj` tree is vendored unmodified at its
  pin, with its license copied and listed in `THIRD-PARTY.md`.
- The binary verifies the OpenCode v2.4.2 binary digest before a run. The
  receipt records the harness tag and digest, the model provider, route,
  deployment and limits, the search provider, each arm's native search route,
  the budget and the config digests.
- The run contract is one task in; a report, a source ledger with URL, verbatim
  quote and locator, a fetch log with snapshots, a reply ledger and a receipt
  out. A cited page that the run did not fetch is a phantom and voids the run.
- The default arm is the arm the confirmation ships. On a `NO-SHIP`, the
  default is `null`; the selection's incumbent stands. `--arm` selects the
  other bundled arm for replay.
- The `hffmnnj` embedding is off, so the arm uses keyword search and makes no
  local model download. Its native search route is `none`; the null's is
  `exa`. `gptr-mcp` stays out: it has no license at its pin and is an MCP
  server, not a deep-research arm.
- The component is released through `host-lifecycle release`, so the artifact
  hash comes from the recorded musl toolchain, not an ambient build. The
  host recipe pins the released commit and the re-derived artifact hash.

## Consequences

The component can be installed as one binary and run with one command, while
the arm's license and pins travel inside the artifact. The `#component-scaffold`
and `#ship` tasks record the `.host-software` stanza, the release receipt, the
Fen acceptance run and the confirmation verdict. A refinement after a ship
uses the selection set and re-confirms on the held-out set; the component's
default arm changes only through a new release and the operator's approval.
