# plan/0065 onboarding-and-mcp-layer: one engine, two human shims, a spawned MCP surface, one dual-mode entrance

This milestone records the design of how a human and an agent start and connect an agentic project.
It is design-stage, not built, and it is deferred as its own initiative behind the open-bug and
dependency-security work so a large new surface never blocks the ready fixes. It absorbs the earlier
adopt-elsewhere design (`plan/0061`) as the `host-adopt` shim described below.

This design was reviewed by the cast and a Fable 5 advisor, and their required changes are folded in
here. The real `qwen3.5-4b` routed the three-route decision twenty of twenty across five scenarios,
so the two-verb split is legible to a weak agent. The cast's Fen remains the acceptance test for the
paths that are built.

## Where it came from

A run of operator refinements in one working conversation. Adoption should start from an arbitrary
folder and elicit the project name. A human should also start a project greenfield from a given name
and have the GitHub repository created. The name Q&A should read authentically across Claude Code,
opencode, and codex, which is one concern across the three clients rather than three separate ones. A
single MCP surface should serve the components rather than each speaking the protocol alone. The human
on-ramp should install as simply as the agent on-ramp reads. The whole human path is aimed at
one-command execution.

The design that answers these keeps one implementation and adds thin, well-named faces over it.

## The one engine and its two shims

`host-lifecycle` is already the generator. Scaffolding a project, stamping it, and generating its book
are its work today, so the create-and-adopt logic lives there rather than in a new library. It grows
two human-facing verbs, `init` and `adopt`, each carrying the name Q&A and the optional GitHub
creation. Because `host-lifecycle` is a single static binary, installing it is one download, so a
human front door does not need a separate lightweight tool underneath.

`host-init` and `host-adopt` are tiny shims over those verbs, the same binary invoked under two names.
They give a human a clean, purpose-named command instead of the internal engine name, and they carry no
logic of their own. On a platform without cheap symlinks the shim is a copy or a small wrapper that
forwards to the engine, so the two names cannot skew from one build.

Adoption keeps the full three-route decision `plan/0061` locked, restated here so absorption drops
nothing.

1. A software repository (a build manifest at its root) keeps the refuse-and-embed path: an agentic
   host is created separately and this repository becomes its subject. `host-adopt` refuses in place.
2. A folder already named `agentic-<name>` and empty adopts in place. The name is the one the operator
   already chose, so there is no Q&A and no handoff. This is the carve-out.
3. Any other folder is arbitrary. `host-adopt` elicits the name, creates the host at `../agentic-<name>`
   (override with `--at`), scaffolds it, seeds a one-line purpose, and requests the operator switch. The
   source folder is untouched.

`host-init <name>` is the fresh-folder path: it takes a given name, creates `agentic-<name>` as a new
directory, and refuses a target that exists. This is the `cargo new` shape against `host-adopt`'s
`cargo init` shape.

The bare `adopt` command name retires in favour of `host-adopt`. That rename is a migration, not only a
naming choice: the live `adopt` skill and the `classify`, `upgrade`, `remap`, and `embed` skills invoke
the command by name. The rename ships with a deprecate-then-retire shim, parallel to the
front-door-to-entrance rename in `call/0027`, and its ledger accounting is in the spine-boundary section.

## The MCP surface: spawned, not resident

The single-surface goal is honoured by a spawned MCP server, not a persistent daemon. The cast and the
Fable advisor converged that a resident service with per-platform units buys a service lifecycle, an
endpoint surface, and a registration protocol to deliver an optional form prompt, when the backstop
already covers every path. So the locked shape is the lighter one: `host-lifecycle` exposes `init` and
`adopt` as MCP tools over stdio, and the client spawns and manages that process for the length of a
session. There is no daemon, no port, no per-platform service, and no runtime registration surface to
secure.

A resident hub that components and plugins register with stays a future option, and it must earn itself.
Before it is built it owes a named list of at least three concrete capabilities that need runtime
registration beyond the name Q&A, a transport choice, and a registration-trust design, because a runtime
registry that any local process can write to would inject tool descriptions into every agent session.
Until then, registration is a declared manifest read at spawn, which also self-describes to a cold read.

The elicitation path is explicit. MCP elicitation is a server-to-client request inside a session, so it
exists only when `init` or `adopt` run as MCP tools on the spawned server, not when they run as a shell
command. A client that invokes the shell verb gets the backstop; a client that invokes the MCP tool and
declares the capability gets the Form-mode prompt. That the agent must choose the shell verb or the MCP
tool is a new weak-agent decision, and it joins the Fen acceptance set.

The client research grounds the layering. Claude Code implements elicitation in its interactive
command-line surface at a recent version. Codex implements it in its interactive surface behind a config
gate. opencode does not implement it and advertises no capability. Every client lacks it in a headless
or print run. So elicitation is the enhanced path and the backstop is load-bearing. The reference memory
records the per-client detail and the specification link.

## The backstop belongs to the verb

The name backstop is a per-invocation contract on `host-lifecycle init` and `host-lifecycle adopt`, and
it holds whenever no MCP client answers, which is every headless run, every client without the
capability, and every plain shell call. The verb accepts the name by flag or environment, else prompts
on a controlling terminal, else exits with a distinct code and a machine-parseable message naming the
missing field so the caller re-invokes with the name supplied. The exit-code set and the message shape
are the load-bearing contract for every scripted and agent caller, so they are specified with the verb
rather than left as an implementation detail. The real 4B is driven through this path.

## The dual-mode entrance

`host` is the single canonical front door in two modes. Read-and-follow is the existing methodology
entrance an agent consumes. Install is the new parallel mode a human or a machine runs to place the
pinned host binaries on the path. The entrance is a repository and a URL, and its install mode is a
script served beside the read document; no executable named `host` is placed on the path, so it does not
collide with the system `host` lookup tool. The install script installs the named tools, `host-lifecycle`
with its `host-init` and `host-adopt` shims, and it does not install a resident service.

Install preserves provenance or it is a hollow install, and the trust chain is anchored at the root, not
only at the leaves.

- The install manifest records each binary's version and canonical hash, and the installer verifies
  every download against the recorded hash before it lands on the path.
- The manifest and the install script are themselves authenticated before they run, so a corrupted or
  substituted manifest cannot present a self-consistent set that the leaf hash-check would pass. The
  trust root, a signing key or an equivalent anchor, is named in the design and its material travels
  into the local install receipt so a later verification does not depend on refetching a moving remote.
- The manifest's hashes are single-sourced from the public per-component release receipts, `host-lint`,
  `host-lifecycle`, `host-prove`, and the rest, never from agentic-host's `.host-software`. The dev
  environment is neither referenced nor leaked, and the two records cannot drift.
- The manifest is keyed to the template revision, because `host` install is also the upgrade route. An
  adopter on a given revision receives the binaries that revision pins, so the spine and the binaries
  cannot drift out of step.

The install writes a durable machine-side receipt: each installed binary, its version, its verified
hash, and the trust anchor used, persisted locally and re-verifiable offline. A memoryless later read
learns what is installed and at what verified hash from this receipt, which is the machine analog of the
dev host's release receipts. The per-project `.host` stamp describes a project, not the machine's
binaries, so the receipt carries this record, not the stamp.

Install is all-or-nothing on the path. A partial install, where some binaries verify and one fails,
records the missing binaries as absent or pending in the receipt and never leaves a silently-missing
tool untraceable. A self-update rewrites the receipt to the new version and hash in the same step it
swaps the binary, so a later read never reports an old hash for a new binary.

## The oneshot human run

The human path is one command that ends with a ready, pushed project or a clean error, never a half-made
state. The initializer survey across cargo, the create generators, the template scaffolders, and the
GitHub command-line tool converges on a small set of rules.

- Prompt only for the name. The name carries operator intent that the folder cannot supply, so it is the
  one field elicited when it is absent. Every other choice is a flag with a sensible default, and a
  name-given call runs with no prompt at all.
- Refuse an existing target. A non-empty or already-stamped destination aborts with an actionable
  message, and overwrite lives behind an explicit force flag.
- Scaffold locally, wire the remote last. The order is resolve, then preflight before any write, then
  scaffold, then commit, then create and push the remote. A remote failure after the commit leaves a
  valid local project and prints the exact manual remote command, and it never discards good local work.
- Treat GitHub as optional and fully flagged. The tool probes for the command-line tool and a live
  token, drives it with explicit flags, and degrades to a local-only success when either is absent.
- Hand off explicitly and machine-readably. The final block names the created path, the remote if any,
  and the next command, and the same output serves a scripted or agent caller. That output is the
  stdout backstop doing double duty, so its shape is part of the specified contract.

`host-adopt` adds one invariant: the source folder is read-only. Every write goes to the target host
elsewhere, the source is never touched even when it is the home directory, and the run ends by requesting
the switch rather than working in place. The declined-name case aborts clean and writes nothing; the
name is required, the seeded purpose is optional.

Install and create are two failure domains, so the one-command form does not fold them into one atomic
step. A first-run install that then bootstraps a project runs the install to completion, verifies the
whole toolset landed, and only then runs create, so a bootstrap never runs against a partial toolchain.
A first-run install does not drive a token-bearing GitHub creation inside the install channel; the create
step, with its own remote handling, is the place the live token is used.

## The spine boundary, drawn now

The boundary is what fans out to adopters, so it is drawn here rather than deferred to each build. Each
element is diff-visible spine prose (which owes no ledger entry), a structural migration (which owes a
revision-keyed ledger entry), or pure software (no spine change).

- Spine prose: the onboarding narrative, the refuse-existing-target and source-read-only invariants, and
  the provenance-verified install contract. These ship as template doctrine and are read by adopters;
  they owe no ledger entry on their own.
- Structural migration, ledger entry owed: the `adopt`-to-`host-adopt` rename, carrying a
  deprecate-then-retire shim and a `requires` host-lifecycle version, keyed to the doctrine commit, with
  an independent flag so a late adopter can take it alone. Whether an adopter must place the spawned MCP
  tools is a second possible entry, and it is decided by the mandatory-or-optional question below.
- Software, no spine change: the shim binaries, the install receipt format, the manifest verification,
  and the engine's `init` and `adopt` internals.

The entrance ships its install mode through the entrance's own release authority, because `host` is the
`[entrance]` member set apart from the components, so the phrase about each piece shipping through its
own lifecycle release does not apply literally to it.

## The cast's throughline

- **Mara** (operator, final say): the name, the visibility, and the switch are hers, and the tool
  proposes and never invents. Her standing constraint holds: the source folder is touched by nothing.
  Her review cut the daemon back to the spawned surface and restored the three routes.
- **Wren** (amnesiac executor): the creating session and the continuing session share no memory, so the
  handoff is written into the new host's files. The seeded one-line purpose is the one artifact crossing
  the boundary, so its shape is settled in the open questions before build, not left implicit.
- **Orin** (maintainer): the onboarding doctrine that ships in the template fails safe when followed
  literally. An install that skips root authentication, a manifest that drifts from the release receipts,
  or a rename with no shim is the failure-unsafe shape he rejects, and each is closed above.
- **Bly** (writes now, reads cold): the installed binaries self-describe to a memoryless read through the
  local install receipt, and a partial install over-reports the missing tool rather than hiding it. The
  receipt, not the per-project stamp, is the machine-side record.
- **Fen** (acceptance test, driven not simulated): the real `qwen3.5-4b` routed the three-route decision
  twenty of twenty. The one-command run, the shell-verb-against-MCP-tool choice, and the agent-driven
  resolve owe their own runs at build.

## Locked decisions

- `host-lifecycle` is the one engine. `host-init` and `host-adopt` are tiny shims over its `init` and
  `adopt` verbs, and there is no separate scaffolding library.
- The bare `adopt` command retires in favour of `host-adopt` through a deprecate-then-retire shim, and
  the skills that call it migrate.
- The full three-route adoption decision from `plan/0061` stands, with the `--at` override.
- The MCP surface is a stdio-spawned server exposing `init` and `adopt` as tools, not a resident daemon.
  A hub must earn itself with named capabilities and a trust design.
- The name backstop is a per-invocation contract on the engine verb, and it holds when no MCP client
  answers.
- `host` gains a parallel install mode with a root-anchored, revision-keyed, receipt-recording,
  all-or-nothing install; no executable named `host` lands on the path.
- The human run defaults are private visibility, name-only prompting, an `agentic-<name>` target that
  refuses an existing folder, and local-first remote-last with no rollback of good local work.

## Decisions ruled (2026-07-07, operator)

The four questions the design left open are ruled, so the build proceeds against fixed contracts.

- **Trust anchor: Sigstore keyless (cosign).** The install manifest and script are signed keylessly
  through cosign (an OIDC identity recorded in the Rekor transparency log), and the installer runs
  `cosign verify-blob` against the Fulcio and Rekor roots before anything lands on the path. The verifying
  identity and the Rekor log reference travel into the local install receipt, so a later read re-verifies
  without trusting a moving remote. The heavier, network-bound option, chosen for keyless operation and
  public transparency over a held key.
- **MCP is optional, backstop-covered.** The spawned MCP tools are the enhanced path, never mandatory: the
  per-invocation verb backstop covers every client without elicitation (opencode, every headless run) and
  every plain shell call. No second UPGRADING ledger entry is owed, so the only migration is the `adopt`
  rename.
- **Seed shape: a MEMORY.md purpose line.** The seeded one-line purpose is written as a MEMORY.md project
  line, the cross-session handoff a cold continuing session reads first. A declined purpose leaves the
  default MEMORY untouched. The name is required; the seed is optional.
- **Exit codes and handoff: line-based `key: value`.** Success prints a final stdout block of `key: value`
  lines (`host-path`, `remote`, `next`); the codes are `0` success, `2` usage error, `3` name-required
  with no controlling terminal (a machine-parseable stderr line names the missing field), `4`
  target-exists or refuse, `5` remote-failed-after-local-commit (the local project is intact and the
  manual remote command is printed). The line-based shape is chosen over JSON for weak-agent legibility.

These rulings are grounded, not asserted, in `gather-data.md`: a Fen acceptance run on the qwen3.5-4b
(twelve of twelve, position-bias controlled, genuinely reasoned) shows the exit-code and shell-verb-vs-MCP
contracts are legible to a weak agent, and a survey of nine established installers grounds the cosign
trust anchor in a shipping majority pattern (verify a signed `checksums.txt` keyless bundle, then check
each hash). The survey refined the install-mode implementation: cosign is bootstrapped by
`gh attestation verify` as the primary with a pinned-SHA256 cosign binary as the fallback, never by cosign
itself, and the receipt stores the verified identity, issuer, and Rekor pointer for offline re-verification.

## Open questions

The operator-gated questions are ruled above. What remains is installer implementation detail, pinned
during the build rather than owed to the operator: the per-platform path setup and binary placement, the
self-update mechanics, and the survey of the established installer family that grounds them.

## Verification

Each software piece ships through its own lifecycle release with the whole-suite verify gate green; the
entrance ships through its own release authority. The Fen probe runs on the one-command run, the
shell-verb-against-MCP-tool choice, and the agent-driven resolve. The cheap-verification bar for the
human run restates all three routes: a fully-flagged `host-init` creates a well-formed, committed, pushed
host and prints a machine-readable handoff; a name-absent call at a terminal prompts only for the name; a
`host-adopt` in a pattern folder adopts in place; a `host-adopt` in a software repository refuses; a
`host-adopt` in an arbitrary folder writes nothing there and creates the host elsewhere. The bar for the
install mode: a download whose hash does not match the manifest is rejected before it lands on the path,
a manifest that fails root authentication is rejected before any download, and an interrupted install
leaves a receipt that re-lists the missing binaries rather than hiding them.
