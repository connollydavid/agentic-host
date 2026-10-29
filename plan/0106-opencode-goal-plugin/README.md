# plan/0106 the opencode goal plugin: the loop as a host surface

**Status: cut 2026-10-29, in build; re-cut the same day by three operator rulings** (the
parity target is the ByBrawe pair's surface and loop discipline only, their verifier
machinery retired as reference; the design must be fully idiomatic to host-*, something
agents reach for naturally; the plugin is V2-native only, and the legacy plugin retires
immediately). Resolves the OpenCode plugin deferral recorded at
[plan/0103](../0103-open-issue-sweep/README.md).

## Why

The operator's opencode carried a plugin: `~/.config/opencode/plugins/opencode-loop.ts`,
a bundled build ("legacy-v1", 4143 lines) that registers goal tools
(`opencode_loop_goal_complete|blocked|progress`), rewrites commands at
`command.execute.before`, survives compaction via `experimental.session.compacting`,
watches `event` for `command.executed`, drives continuations through the SDK's session
command surface, and guards itself with a max-no-progress counter. It is the
opencode-loop way of working with zero host references: its goals, progress, and
completion live in its own state, unreceipted and ungoverned. The host doors
(`/host-goal`, `/host-tasks`, `/host-ci`) are one-shot injections with no loop. The
retired references (the legacy bundle, the community goal plugins, ByBrawe's completion
machinery) each hold a piece; none holds the discipline. This milestone builds the
piece that does: the loop as a host surface.

## The rulings

1. **The host verifier stack is the sole verifier.** ByBrawe's completion pipeline,
   independent verifier session, and contract format are retired as reference: they do
   not combine with the ladder (the verify gate, the obligations and allium specs, the
   kani rungs, the ci receipts, the prose lane, the refs walk, `book --check`,
   `software --check`, and the composed closure gate), and a second, weaker verifier
   beside a complete one is the defect the house exists to refuse.
2. **Fully host-idiomatic.** Not a translation: the command set is the host verb
   family, the tracked surfaces are the only state authority, and the plugin adds no
   vocabulary an agent has not already met in the doors and the verbs.
3. **V2-native only.** Built against the OpenCode 2 plugin API (`Plugin.define`, the
   native `plugins` config, the native hooks). The installed opencode is 1.18.21 with
   @opencode-ai/plugin 1.17.12 (the V1 generation), which cannot load it; the harness's
   live tiers run on an OpenCode 2.x binary pinned into a scratch directory that never
   touches the daily install, or wait for the operator's upgrade; the build node
   records which.
4. **The legacy plugin retires immediately.** Learnings recorded below; the bytes stay
   on disk under a retired name until the swap.

## The design: the loop as a host surface

### One state authority: the tracked surfaces

GOAL.md and the receipt fold are the switch. An active unparked goal arms the loop; a
parked goal holds it; no goal silences it; a completed surface stops it. The plugin
holds no persistent state at all, only an in-memory iteration count and the last
emission; a session restart forgets nothing that matters, and a cold read reconstructs
everything from the surfaces. The Orin and Bly verdicts (reconstructible state, the
version seam) are met structurally, not by discipline.

### The command set is the host verb family

- `/host-goal` (orient; the existing door, injecting the `goal show` emission verbatim)
- `/host-goal set <plan/NNNN>` (declare; free text refused to `goal propose` per
  call/0061: a goal IS a milestone, and the audited declaration is the authority)
- `/host-goal park <reason>` and `/host-goal unpark` (the hold and the resume ARE the
  host verbs; the reason rides the receipt and the frontier reads held)
- `/host-goal complete` (the operator's typed command runs the operator's composed
  gate)
- `/host-tasks` (the frontier; the existing door) and `/host-ci` (the lanes; the
  existing door)

Nothing else: no contract, audit, budget, doctor, queue, history, edit, or restore.
Each is either a projection the emission already carries or a host act the CLI owns.
The model-facing surface is the same three tools the doors direct: `goal_show` and
`tasks_status` (read) and `tasks_record` (the write the doors already direct). No
model-facing complete tool; the legacy plugin's `opencode_loop_goal_complete` is the
named anti-pattern, and completion is never model-claimable: the loop stops when the
tracked surface says complete, and only `goal complete`, operator-invoked, writes that
surface.

### The loop and its bounds

On session idle with an armed goal, the continuation body is the `goal show` emission
plus the door doctrine: work the NEXT line; if it is a command, run it as printed; if
it says work a task, start it; never invent a command or a flag; NEEDS YOU non-none
means ask the operator and nothing else runs. The emission is the prompt; nothing is
referenced but absent. Bounds, each printing its stop reason: the iteration cap
(default 25, `HOST_LOOP_MAX_ITERATIONS`, unknown values fail closed), three consecutive
turns with no receipt and no frontier movement (counted mechanically, never assessed,
Wren's verdict), a no-tool-call turn, a verb refusal, NEEDS YOU, parked, complete.
Resuming after any stop is the operator's hand: a new user turn or an unpark. One
controller per session by construction: the single plugin owns the loop, so the
two-controller hazard the references document never arises.

### Zero new verification

The plugin adds no checks, no digests, no verifier session, no second contract format.
The ladder already runs; the loop's only job is to keep the agent on the NEXT line
until the ladder or the operator speaks. Every autonomous action lands in a receipt,
so the ledger is the audit trail of an unattended session, and the operator's surfaces
(the emission, the receipts, the lanes) are the trust surface, never a chat claim.

## The retirement and its learnings

The legacy bundle retires immediately by ruling; the bytes stay on disk under a
retired name until the swap. Learnings taken before removal:

- The live-proven V1 surfaces (tool registration, `command.execute.before`, `event`,
  `experimental.session.compacting`, the SDK session-command surface), all on opencode
  1.18.21 with @opencode-ai/plugin 1.17.12; the V2 gap this ruling accepts is recorded
  at discovery.
- The no-progress counter (three turns), which the loop adopts mechanically: receipt
  stanzas and frontier movement are counted, never assessed.
- The two continuation registers (a goal-mode and a loop-mode prompt), which the A/B
  arms inherit as variants.
- The cost that justified retirement: an unreviewable bundle governing an unreviewable
  loop, with state the host ledgers never saw.

From the community set, also retired as references: conservative continuation (a turn
with no tool calls stops the loop; adopted), the budget concept (becomes the iteration
cap), and evidence-mapped completion (the composed gates are the stronger form).

## Design gates

1. **The cast convened at the cut** (`convening-design.md`); an addendum records the
   three rulings above. Superseded verdict note: the plugin-local hold and its
   persisted runtime state are gone; the hold is `goal park` and the only runtime
   facts are in-memory. The discipline verdicts stand: the ship gate, the cap at 25
   with printed reasons, the version seam, the tool surface, no compaction hook.
2. **Real Fen calls are the acceptance bar, not a lens** (operator ruling 2026-10-20):
   qwen3.5-4b runs the probes through dokimi. The operator handed the direct LAN
   channel the same day (no API key; the endpoint, the capacity, and the gotchas the
   kit respects are recorded in `bench/README.md`). Reachability from this host is
   refused by the deliberate UFW scope: the rope box answers ICMP across the routed
   path, but 8080 and 4001 are scoped to 192.168.21.0/24 while this host sits on
   192.168.178.0/24, and the WAN edge returns 401 without the bearer; the kit is
   endpoint-driven and runs unmodified from a host inside the scope or once the
   bearer is handed over, the plan/0088 one-command pattern.
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
  emission plus the door doctrine (the four rules including never-invent); C B plus
  one exemplar ACTION block; D B with the negative rule leading.
- Rubric per draw (deterministic): ACTION line present; the ACTION command equals the
  NEXT line's command; a receipt stanza appended where the task ran; the re-orient
  command present; no state-file hand-edits; zero commands run on the NEEDS YOU and
  parked states. Score six points per draw.
- Ship gate: the continuation prompt ships only after confirmation passes; until then
  the loop runs the incumbent prompt (the door doctrine text).

## Build sequence

### Discover the installed surface {#discover}

- verify: the installed opencode version recorded here with the hook surfaces it
  carries, and the legacy-v1 bundle's source located or its absence recorded
- inputs: the operator's opencode config and plugins directory
- Landed at the cut (2026-10-29): opencode 1.18.21 with @opencode-ai/plugin 1.17.12;
  the bundle's V1 surfaces are all proven live by the installed plugin itself. The
  legacy-v1 source is not located on this machine. The V2-only ruling accepts the gap:
  the plugin targets OpenCode 2, and the live tiers await a 2.x binary in a scratch
  install or the operator's upgrade.

### Convene the cast {#convene}

- verify: five seat ballots recorded with the adversarial constraint, binding verdicts
  folded into this README, the addendum recording the re-cut rulings
- inputs: cast/
- Landed at the cut: `convening-design.md`, verdicts folded, addendum recorded.

### Stage the A/B kit {#stage-kit}

- verify: `bench/run-ab.py` and the state fixtures exist; a dry run scores one fixture
  without network
- depends: #convene
- Landed 2026-10-29: `bench/` (make-fixture.sh, rubric.py, run-ab.py, the controls,
  the channel document); the dry run is green offline, the positive control 6/6 and
  the negative 1/6 with the invented verb named. The fixture's real emission is
  captured from the canonical binary; NEXT is the work-key form.

### The dokimi program {#ab-program}

- verify: the confirmation stage passes its pre-declared criteria, or the incumbent
  stands with the refusals recorded; every round's table in `bench/`
- depends: #stage-kit
- note: blocked on the Fen credential; runs the moment the channel exists

### Plugin prototype {#prototype}

- verify: the plugin (Plugin.define, V2-native) loads in a real OpenCode 2.x session
  from the plan room; the /host-goal family drives the verbs through subprocesses; the
  loop fires once on idle with an armed goal and stops on a no-tool-call turn; no
  persistent plugin state exists
- depends: #discover, #convene
- note: runs the incumbent prompt; the confirmed prompt lands after #ab-program

### Tier 1 suite {#tier1}

- verify: the bun unit suite is green against typed fakes of the OpenCode 2 hook
  surfaces, asserting the command set, the state authority, and the bounds per stop
  reason
- depends: #prototype

### Tier 2 harness {#tier2}

- verify: real headless OpenCode 2.x runs (the pinned scratch install) assert the
  host-ledger effects (receipt stanzas, GOAL.md, the sidecar), the loop bounds, and
  the printed stop reasons
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

- The parity target (the operator: "specifically good"):
  [ByBrawe/opencode-goal](https://github.com/ByBrawe/opencode-goal) (the /goal family,
  the fail-closed posture, one controller, the resume whitelist) and
  [ByBrawe/opencode-loop](https://github.com/ByBrawe/opencode-loop) (due-versus-safe
  admission, the bounds, doctor and logs, session-bound state). Their command surface
  and loop discipline are studied; their verifier machinery is retired as reference.
- Retired as references: [watzon/opencode-goal](https://github.com/watzon/opencode-goal),
  [wejick/opencode-goal](https://github.com/wejick/opencode-goal), the legacy-v1
  bundle, the loop feature requests
  [anomalyco/opencode#23578](https://github.com/anomalyco/opencode/issues/23578) and
  [anomalyco/opencode#27162](https://github.com/anomalyco/opencode/issues/27162).
- House surfaces: the door family and goal verbs (goal.rs), the tasks verb family
  (plan/0042), the MCP pair (plan/0101), the teaching-layer protocol (plan/0100), the
  weak-model kit pattern (plan/0088).
