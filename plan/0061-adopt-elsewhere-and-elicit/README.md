# plan/0061 adopt-elsewhere-and-elicit: adopt from an arbitrary folder by creating the host elsewhere and eliciting its name

This milestone extends adoption so an agent can start an agentic project in whatever folder it is
already working in. Today `adopt` takes a directory and a revision and scaffolds in place, and the arbitrary-folder
case is only half-served by the `refuse-adopt-in-place` message, which tells the operator to make a
separate host by hand. The feature builds the active path: elicit the project name, create the host in
a fresh `agentic-<name>` folder, scaffold it, and request that the operator switch to it. The source
folder is never written to.

The cast's Fen (the real `qwen3.5-4b`) is the acceptance test.

## Where it came from

A feature request from the operator: an agent should start an agentic project from an arbitrary folder,
create the host elsewhere on the machine, and ask the operator to switch to it. Two refinements landed
in the same conversation. The source folder may be a large aggregate directory or the home directory,
so the tool must be defensive and touch nothing within it. And a folder that already matches
`agentic-<name>` exactly is a carve-out that adopts in place. The operator flagged the question of
how an authentic name Q&A works across Claude Code, opencode, and codex, as a major concern and a
skill-related item.

## The three routes

Adoption becomes a decision on the current directory:

1. A software repository (a manifest at its root) keeps the existing refuse-and-embed path: become the
   Where room of a separate host. Unchanged.
2. A folder already named `agentic-<name>` and empty adopts in place; the name is the `<name>` the
   operator already chose, so there is no Q&A and no handoff. The carve-out.
3. Any other folder is arbitrary. The tool elicits the name, creates the host at `../agentic-<name>`
   (override with `--at`), scaffolds it, seeds a one-line purpose, and requests the operator switch.
   The source folder is untouched.

## The name Q&A across Claude Code, opencode, and codex (the operator's major concern)

The name carries operator intent, so it is elicited rather than read off the folder; a folder named
`pdf-notes` never becomes a project named `pdf`. The elicitation must read authentically in whatever
host drives the agent. The mechanism is layered.

- MCP elicitation (Form mode) where the client supports it. The June 2025 MCP specification added an
  `elicitation/create` request: the server names the fields it needs (here `name`, plus a one-line
  `purpose` for the seed), the client renders the prompt in its own native surface, the operator
  answers or declines, and the tool resumes. A URL mode covers sensitive input. The reference memory
  records the specification link.
- A stdout contract as the universal backstop. Where a client does not implement elicitation, `adopt`
  exits with a distinct code and names the missing field, so the agent asks the operator through its
  own native surface and re-runs with `--name`. This is the path validated on the real 4B.

The Q&A belongs to the tool, and the skill only points at it. Each host has its own skill format, so an
elicitation authored into skill markdown would not travel; the tool's protocol and stdout contract keep
it portable.

## The cast's throughline

- **Mara** (operator, final say): the name and the switch are hers. No agent, in any host, can relocate
  her session, so the switch is a request she performs. The tool proposes a name and a path and never
  invents them. She added the load-bearing constraint: assume the source may be the home directory, and
  touch nothing in it.
- **Wren** (amnesiac executor): the agent that creates the host and the agent that continues in it are
  separate sessions with total amnesia between them. The handoff must be written into the new host's
  files, because the creating session's context does not survive the switch. Hence the seeded purpose
  note.
- **Orin** (maintainer): express the behaviour once and make it fail safe when followed literally. If
  the operator never switches, nothing is left half-built, because the source stays pristine and only
  the new host exists.
- **Bly** (writes now, reads cold): the new host self-describes to a memoryless read through the stamp
  and the adopt checklist, which re-list the next steps and so over-report. The source carries no
  ambiguous breadcrumb that a later cold read could mistake for a half-adopted host.
- **Fen** (acceptance test, driven not simulated): the real `qwen3.5-4b` routed all three decision
  points correctly on the corrected scenario, six of six each. It asks the operator for the name rather
  than reading it off the folder, it requests the operator switch rather than relocating itself, and it
  adopts in place in the carve-out. The condition is that the tool output carries the routed next move,
  which the design is built to do.

## Locked decisions (operator)

- The name Q&A is carried by MCP elicitation with the stdout contract as the universal backstop.
- An arbitrary folder relocates in one command: elicit, create `../agentic-<name>` (`--at` to
  override), scaffold, request the switch.
- The source folder is touched by nothing, even when it is the home directory.
- The new host is seeded with a one-line purpose so the amnesiac next session is not cold.

## Open questions

- How host-lifecycle speaks MCP. It is a CLI today, and Form-mode elicitation needs it to answer an MCP
  client. Whether that is a `host-lifecycle` server mode, a separate thin MCP surface, or the adopt
  verb made MCP-callable is unsettled, and it is the largest piece of work here.
- Where the behaviour lives. The active relocate-and-handoff extends an existing methodology rule
  (adopt into a separate host) rather than adding a new one, so it reads as host-lifecycle software.
  Whether any part is spine doctrine that needs a host-template ledger entry is for the milestone to
  settle, gated by the anti-ouroboros scope rule.
- The seed's shape. A seeded purpose is a `plan/` entry or a MEMORY line; the milestone picks one and
  defines what a declined purpose does (the seed is optional, the name is not).

## Verification

Ships as one host-lifecycle release, then re-vendor and propagate to consumers, with the whole-suite
verify gate green and the Fen probe passing on all three routes. The cheap-verification bar: a run in
an arbitrary folder writes nothing there and creates a well-formed `agentic-<name>` host elsewhere; a
run in a pattern folder adopts in place; a run in a software repository still refuses.
