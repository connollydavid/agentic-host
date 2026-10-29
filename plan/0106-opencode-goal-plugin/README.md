# plan/0106 the opencode goal plugin: the loop under host governance

**Status: cut 2026-10-29, in build** (operator-directed: the installed plugin "is not
powerful enough. we need a full test harness against v2 apis and idiomatic parity with
opencode-loop/opencode-goal's way of working command set, but with host-* idioms and
ledgers"; amended the same hour: the design consults the cast, makes real calls to the
Fen model, targets complete autonomous behaviour governed by the host plan, and dokimi
A/Bs the prompts to confirmation). Resolves the OpenCode plugin deferral recorded at
[plan/0103](../0103-open-issue-sweep/README.md).

## Why

The operator's opencode already carries a plugin: `~/.config/opencode/plugins/opencode-loop.ts`,
a bundled build ("legacy-v1", 4143 lines) that registers goal tools
(`opencode_loop_goal_complete|blocked|progress`), rewrites commands at
`command.execute.before`, survives compaction via `experimental.session.compacting`,
watches `event` for `command.executed`, drives continuations through the SDK's session
command surface, and guards itself with a max-no-progress counter. It is the
opencode-loop/opencode-goal way of working, and it holds **zero host references**: its
goals, progress, and completion live in its own state, unreceipted and ungoverned. The
host doors (`/host-goal`, `/host-tasks`, `/host-ci`) are one-shot injections with no
loop. The gap is exactly the operator's ask: the loop's power with the host's
discipline.

## The autonomy contract

The plugin kicks opencode sessions into complete autonomous behaviour, governed by the
host plan, with every state change landing in a receipt:

- The loop drives unattended across turns: session idle with an active unparked goal
  queues a continuation whose body is the `goal show` emission (PURPOSE, POSITION,
  NEEDS YOU, CI, FRONTIER, NEXT) plus the door doctrine. The emission is the prompt;
  nothing is referenced but absent.
- The model works the NEXT line only, through verbs and tools: run the verify, record
  with `tasks --record`, re-orient. Every autonomous action is auditable in
  `.host-task-receipts`.
- The loop stops, printing its reason, on any of: completion (the composed gates
  banked it), NEEDS YOU non-none (the operator is asked; nothing else runs), the
  iteration cap (default 25, `HOST_LOOP_MAX_ITERATIONS` overrides), a hold
  (`/goal pause`), or three consecutive turns with no receipt and no frontier movement
  (the no-progress guard the legacy plugin already carries).
- Control verbs stay CLI-only (plan/0101): the model can read and record, never
  set, park, complete, or abandon. `/goal clear` stops driving only; abandonment
  remains the operator's CLI act with its OWED row.

## Parity mapping (the /goal family, union shape)

| Command | Plugin behaviour | Host verb and state |
|---|---|---|
| `/goal <plan/NNNN>` | sets the goal; free text is refused with the house refusal shape pointing at `goal propose` | `goal set <target> .` (receipt, Status suffix, sidecar, GOAL.md) |
| `/goal status` / `show` | injects the `goal show` emission verbatim | `goal show .` |
| `/goal pause` / `resume` | loop hold only; the goal state is untouched | plugin-local runtime state |
| `/goal clear` | stops driving only | no host mutation |
| model tools | `goal_show`, `tasks_status` (read); `tasks_record` (the write the doors already direct) | CLI subprocesses, parsed stdout only |

A goal IS a plan/NNNN milestone (call/0061); the audited declaration is the authority,
so no ad-hoc free-text goals. No token budget surface exists in host idiom; the
iteration cap replaces it.

## State discipline

The plugin never touches `.host-*` files: it parses verb stdout only, and a parse
failure is a refusal with the upgrade hint, never a guess (the version seam). Its own
runtime state (hold flag, iteration count) lives in `.opencode/` as gitignored harness
state and is the only plugin-local fact; a cold session reconstructs everything else
from GOAL.md, the ledgers, and the emission. No compaction hook: plan/0101 cut that
hook in favor of the corpus, and GOAL.md (a declared corpus surface) is the recitation
surface.

## Design gates

1. **The cast convenes on the design** (done at the cut; verdicts below and in
   `convening-design.md`): the binding outcomes are folded into the sections above.
2. **Real Fen calls are the acceptance bar, not a lens** (operator ruling 2026-10-20):
   qwen3.5-4b runs the probes through dokimi. The channel is credential-refused today
   (the rope router serves qwen3.5-4b at the recorded baseURL, but `ROPE_BEARER`
   resolves only in the operator's own sessions); the kit below runs the moment the
   credential is handed over, the plan/0088 one-command pattern.
3. **dokimi A/Bs the prompts to confirmation** (tools/dokimi, adopted 691c007): arms
   structure and answer capture from dokimi, scoring by the mechanical rubric (no LLM
   judge on this endpoint; the plan/0100 verdict). Protocol per plan/0100: selection
   rounds are exploratory with in-round re-baselines, cross-round numbers never
   compare; the winner then faces the locked confirmation stage against the incumbent
   with held-out states untouched by selection, fresh interleaved draws, a pre-declared
   margin, a per-state floor, and the zero-invented hard gate. The program iterates
   until confirmation passes or the operator stops it; every round's table lands in
   `bench/`.

### The A/B program (staged)

- Subject: qwen3.5-4b on the rope router, thinking on through the chat template, the
  plan/0076 protocol parameters (the plan/0088 kit's shape).
- States (the emission battery, each a scratch-project fixture with real ledgers):
  ready frontier with a mechanical task; an attested task; NEEDS YOU non-none;
  parked; complete pending accept; goal-less.
- Arms (continuation-body variants): A bare emission plus "Work the NEXT line."; B
  emission plus the door doctrine (four rules including never-invent); C B plus one
  exemplar ACTION block; D B with the negative rule leading.
- Rubric per draw (deterministic): ACTION line present; the ACTION command equals the
  NEXT line's command; a receipt stanza appended where the task ran; the re-orient
  command present; no state-file hand-edits; zero commands run on the NEEDS YOU and
  parked states. Score six points per draw.
- Ship gate: the continuation prompt ships only after confirmation passes; until then
  the loop runs the incumbent prompt (the door doctrine text).

## Build sequence

### Discover the installed surface {#discover}

- verify: the installed opencode version recorded here with the hook surfaces it
  carries (command.execute.before, event, experimental.session.compacting, the SDK
  session-command surface, tool registration), and the legacy-v1 bundle's source
  located or its absence recorded
- inputs: the operator's opencode config and plugins directory
- Landed at the cut (2026-10-29): opencode 1.18.21 with @opencode-ai/plugin 1.17.12;
  the bundle's surfaces (tool registration, command.execute.before, event,
  experimental.session.compacting, the SDK session-command surface) are all proven
  live by the installed plugin itself. The legacy-v1 source is not located on this
  machine; the prototype rebuilds from the live surfaces, not the bundle.

### Convene the cast {#convene}

- verify: five seat ballots recorded with the adversarial constraint, binding verdicts
  folded into this README
- inputs: cast/

### Stage the A/B kit {#stage-kit}

- verify: `bench/run-ab.py` and the state fixtures exist; a dry run scores one fixture
  without network
- depends: #convene

### The dokimi program {#ab-program}

- verify: the confirmation stage passes its pre-declared criteria, or the incumbent
  stands with the refusals recorded; every round's table in `bench/`
- depends: #stage-kit
- note: blocked on the Fen credential; runs the moment the channel exists

### Plugin prototype {#prototype}

- verify: the plugin loads in a real opencode session from the plan room; the /goal
  family drives the verbs; the loop fires once on idle and stops on a no-tool-call
  turn
- depends: #discover, #convene
- note: runs the incumbent prompt; the confirmed prompt lands after #ab-program

### Tier 1 suite {#tier1}

- verify: the bun unit suite is green against typed fakes of the hook surfaces,
  asserting the mapping table and the guardrails per state
- depends: #prototype

### Tier 2 harness {#tier2}

- verify: real headless opencode runs assert the host-ledger effects (receipt stanzas,
  GOAL.md, the sidecar), the loop bounds, and the printed stop reasons
- depends: #tier1

### Tier 3 Fen acceptance {#fen}

- verify: qwen3.5-4b completes a bounded loop in a scratch project, working the
  frontier, recording receipts, and stopping at NEEDS YOU; transcript and rubric table
  in `bench/`
- depends: #tier2, #ab-program

### Promotion ruling {#promote}

- verify: the component-versus-template-payload ruling recorded (proposed component
  name host-loop, the lemgate-to-host-voice arc), the recipe and release cascade
  scoped, and the deferral resolution noted on plan/0103's record
- depends: #fen

## References

- The parity targets: [watzon/opencode-goal](https://github.com/watzon/opencode-goal)
  (the /goal family with budget and idle-event continuation) and
  [wejick/opencode-goal](https://github.com/wejick/opencode-goal) (the session-inbox
  continuation and the four goal tools; OpenCode 2 beta or newer).
- The standing loop discussion:
  [anomalyco/opencode#23578](https://github.com/anomalyco/opencode/issues/23578)
  (a native /loop) and
  [anomalyco/opencode#27162](https://github.com/anomalyco/opencode/issues/27162)
  (native session goals).
- House surfaces: the door family and goal verbs (goal.rs), the tasks verb family
  (plan/0042), the MCP pair (plan/0101), the teaching-layer protocol (plan/0100), the
  weak-model kit pattern (plan/0088).
