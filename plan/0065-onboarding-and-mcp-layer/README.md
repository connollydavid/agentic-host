# plan/0065 onboarding-and-mcp-layer: one engine, two human shims, one MCP hub, one dual-mode entrance

This milestone records the design of how a human and an agent start and connect an agentic project.
It is design-stage, not built, and it is deferred as its own initiative behind the open-bug and
dependency-security work so a large new surface never blocks the ready fixes. It absorbs the earlier
adopt-elsewhere design (`plan/0061`) as the `host-adopt` shim described below.

The cast's Fen (the real `qwen3.5-4b`) is the acceptance test for the weak-agent-facing paths.

## Where it came from

A run of operator refinements in one working conversation. Adoption should start from an arbitrary
folder and elicit the project name. A human should also start a project greenfield from a given name
and have the GitHub repository created. The name Q&A should read authentically across Claude Code,
opencode, and codex, which is one concern across the three clients rather than three separate ones. A single
MCP surface should serve every component and plugin instead of each speaking the protocol alone. The
human on-ramp should install as simply as the agent on-ramp reads. The whole human path is aimed at
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
logic of their own. The split follows the `cargo new` against `cargo init` prior art the initializer
survey confirmed: `host-init <name>` makes a fresh `agentic-<name>` folder and refuses a target that
exists, while `host-adopt` works from an arbitrary source folder, elicits the name, creates the host
elsewhere, and requests the operator switch. Two predictable verbs over one engine read more safely to
a weak agent and a tired human than one command that guesses from context.

The engine's role widens with this. It was the internal development tool; it becomes the human
bootstrapper as well. That widening is deliberate and recorded here so a later reader does not mistake
the human verbs for a separate component.

## The single hub

`host-mcp` is one persistent local MCP hub that the agent's client connects to and that the host
components and plugins register their capabilities with. It implements the cross-client Q&A once. It
speaks MCP Form-mode elicitation where the client declares the capability, and it carries the mandatory
backstop for every client and mode that does not. It generalises the out-of-process plugin boundary
`host-reference` already uses into a uniform registration. Because it is a persistent daemon rather
than a per-session spawn, it ships idiomatic per-platform service affordances: a systemd user unit on
Linux, a launchd agent on macOS, and a service or logon task on Windows.

The client research grounds the layering. Claude Code implements elicitation in its interactive
command-line surface at a recent version. Codex implements it in its interactive surface behind a
config gate. opencode does not implement it and advertises no capability. Every client lacks it in a
headless or print run. So elicitation is the enhanced path and the backstop is load-bearing, never
optional. The reference memory records the per-client detail and the specification link.

The daemon model buys runtime registration, plugins, and one shared endpoint, at the cost of service
lifecycle and a local endpoint's surface. The lighter stdio-spawn transport needs no service at all and
is recorded here as the fallback shape if the daemon proves heavier than its worth.

## The dual-mode entrance

`host` is the single canonical front door in two modes. Read-and-follow is the existing methodology
entrance an agent consumes. Install is the new parallel mode a human or a machine runs to place the
pinned host binaries on the path. The one name an agent reads is the one a human installs from, so
`host` bookends the whole story: it installs the tools, then `host-init` bootstraps a project, then the
agent reads `host` and follows it.

The install mode must preserve provenance or it is a hollow install. The methodology records each
binary's canonical reproducible-build hash, so the installer ships a pinned, signed manifest and
verifies every download against the recorded hash before it lands on the path. An install through
`host` is then byte-identical to the reproducibly-built artifact. The entrance repository serves the
read document and the install script side by side rather than as one fragile polyglot file.

The install mode completes the one-command human run. A single invocation verifies and installs the
tools and then bootstraps the named project, so install and create happen in one shot.

The binary-installer surface (checksum and signature verification, path setup, per-platform placement,
and self-update) is the one part of this design still ungrounded. A survey of the established installer
family is owed before it is built, and it is marked open below.

## The oneshot human run

The human path is one command that ends with a ready, pushed project or a clean error, never a
half-made state. The initializer survey across cargo, the create generators, the template scaffolders,
and the GitHub command-line tool converges on a small set of rules.

- Prompt only for the name. The name carries operator intent that the folder cannot supply, so it is
  the one field elicited when it is absent. Every other choice is a flag with a sensible default, and a
  name-given call runs with no prompt at all.
- Refuse an existing target. A non-empty or already-stamped destination aborts with an actionable
  message, and overwrite lives behind an explicit force flag. This is the universal anti-half-state
  default, and it is cheaper and clearer than a rollback.
- Scaffold locally, wire the remote last. The order is resolve, then preflight before any write, then
  scaffold, then commit, then create and push the remote. A remote failure after the commit leaves a
  valid local project and prints the exact manual remote command, and it never discards good local
  work.
- Treat GitHub as optional and fully flagged. The tool probes for the command-line tool and a live
  token, drives it with explicit flags rather than its prompts, and degrades to a local-only success
  when either is absent.
- Hand off explicitly. The final block names the created path, the remote if any, and the next command,
  and it is machine-readable so the same output serves a scripted or agent-driven caller. That output
  is the stdout backstop doing double duty.

`host-adopt` adds one invariant to this. The source folder is read-only. Every write goes to the target
host elsewhere, the source is never touched even when it is the home directory, and the run ends by
requesting the switch rather than working in place.

The whole run is one flow: resolve, preflight, scaffold, commit, remote, hand off. The only difference
between a human at a terminal and an agent under a client is how the resolve step fills a missing name:
a terminal prompt, an MCP elicitation through `host-mcp`, or the stdout backstop. That keeps the pattern
single and testable.

## The layered name Q&A

The name is elicited rather than read off the folder, so a folder named `pdf-notes` never yields a
project named `pdf`. The elicitation reads natively in whatever client drives the agent through the
hub. Where the client declares the capability, `host-mcp` sends a Form-mode request naming the fields
it needs. Where the client does not, or the run is headless, the backstop accepts the name by flag or
environment, else prompts on a controlling terminal, else exits with a distinct code and a
machine-parseable message so the caller re-invokes with the name supplied. The backstop is the path the
real 4B is driven through.

## The cast's throughline

- **Mara** (operator, final say): the name, the visibility, and the switch are hers. No agent can
  relocate her session, so the switch is a request. The tool proposes and never invents. Her standing
  constraint holds: the source folder is touched by nothing.
- **Wren** (amnesiac executor): the creating session and the continuing session share no memory, so the
  handoff is written into the new host's files. A seeded one-line purpose keeps the next session from
  starting cold.
- **Orin** (maintainer): the onboarding doctrine that ships in the template is expressed once and fails
  safe when followed literally. An install that skips hash verification, or a create that leaves a half
  state, is the failure-unsafe shape he rejects.
- **Bly** (writes now, reads cold): the installed binaries and the created host self-describe to a
  memoryless read through the stamp and the pinned manifest. A provenance-verified install is the record
  a later cold read can trust; an unverified download is not.
- **Fen** (acceptance test, driven not simulated): the real `qwen3.5-4b` is handed the one-command run
  and the agent-driven resolve, and it must complete them through the tool's named next move. The prior
  adopt-routing run already routed six of six on the corrected scenario. The new paths owe their own runs.

## Locked decisions

- `host-lifecycle` is the one engine. `host-init` and `host-adopt` are tiny shims over its `init` and
  `adopt` verbs, and there is no separate scaffolding library.
- The bare `adopt` command name retires in favour of `host-adopt`, parallel to `host-init`. Adoption
  stays the methodology concept.
- `host-mcp` is one persistent registration hub for every component and plugin, built as the general
  hub rather than scoped to a single client, with per-platform service affordances.
- `host` gains a parallel install mode that verifies every binary against the recorded canonical hash.
- The human run defaults are private visibility, name-only prompting, a `agentic-<name>` target that
  refuses an existing folder, and local-first remote-last with no rollback of good local work.

## Open questions

- The binary-installer surface. A survey of the established installer family (verification, path setup,
  per-platform placement, self-update) is owed before the install mode is built.
- How `host-mcp` discovers registrations. A declarative manifest it reads against a runtime protocol is
  unsettled, and it sets the registration contract for every component and plugin.
- The spine boundary. The onboarding and adoption doctrine that ships in the template is methodology and
  needs a host-template ledger entry; the component code is software. The milestone that builds each
  piece settles which half is which, gated by the anti-ouroboros scope rule.
- The seed's shape, carried over from `plan/0061`: whether the seeded purpose is a `plan/` entry or a
  memory line, and what a declined purpose does.

## Verification

Each piece ships through its own lifecycle release with the whole-suite verify gate green. The Fen probe
runs on the one-command human path and the agent-driven resolve. The cheap-verification bar for the
human run: a fully-flagged call creates a well-formed, committed, pushed host and prints a
machine-readable handoff; a name-absent call at a terminal prompts only for the name; an existing target
refuses; a missing GitHub tool degrades to a local-only success with the manual remote command printed.
The cheap bar for the install mode: a download whose hash does not match the manifest is rejected before
it lands on the path.
