# plan/0106 the opencode goal plugin: the loop as a host surface

**Status: cut 2026-10-29, in build; re-cut the same day by three operator rulings** (the
parity target is the ByBrawe pair's surface and loop discipline only, their verifier
machinery retired as reference; the design must be fully idiomatic to host-*, something
agents reach for naturally; the plugin is V2-native only, and the legacy plugin retires
immediately). Resolves the OpenCode plugin deferral recorded at
[plan/0103](../0103-open-issue-sweep/README.md).; active goal since 2026-10-30

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
5. **The V2 lifecycle and its autonomous coordinator are the continuation owners**
   (operator ruling, mid-cut): the plugin registers as the coordinator's client on
   OpenCode 2's V2 lifecycle (native prompt admission, the durable inbox,
   session-idle recovery); it never hand-rolls a competing loop, which is what makes
   one controller per session structural rather than promised.

## The design: the loop as a host surface

### One state authority: the tracked surfaces

GOAL.md and the receipt fold are the switch. An active unparked goal arms the loop; a
parked goal holds it; no goal silences it; a completed surface stops it. The plugin
holds no persistent state at all, only an in-memory iteration count and the last
emission; a session restart forgets nothing that matters, and a cold read reconstructs
everything from the surfaces. The Orin and Bly verdicts (reconstructible state, the
version seam) are met structurally, not by discipline.

### The command set is the host verb family

- `/host-goal` (orient; the existing door, with the `goal show` emission injected
  verbatim)
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

## The spec and its obligations

The plugin's behavior is spec'd in allium beside the prototype code
(`plugin/host-loop.allium`, validated green by the allium CLI): the GoalSurface state
machine, the admission rules over the coordinator's safe ticks (ArmOnReadyGoal,
HoldWhenParked, SilentWithoutGoal, HoldWhenBusy, StopOnComplete), the tool registry
with its no-completion invariant, and the surface @guarantees for the string-level
facts (EmissionIsPrompt, StopPrintsReason, CapFailsClosed, NoPersistentState,
HonestTelemetry, OneControllerPerSession). Every derived obligation is dispositioned
in `plugin/host-loop.obligations`: structural for shape facts, and the tier-1 suite's
test names declared as the discharge contract for everything behavioral; every shipped
test exercises its token. Until #tier1 lands the test
dispositions read ABSENT, the honest interim state. Placement note (plan/0012): the
spec lives beside the prototype in the plan room and travels with the promotion, the
lemgate precedent; software without its spec beside it is the defect plan/0012 exists
to refuse.

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
   structure and answer capture from dokimi (no LLM judge on this endpoint; the
   plan/0100 verdict); the score comes from the mechanical rubric. Protocol per
   plan/0100: selection
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

### Materialize the OpenCode 2 source {#materialize}

- verify: the source pinned, the pin recorded, the plugin API package version named
- inputs: tools/opencode
- Landed 2026-10-29: `tools/opencode` is an external-by-source submodule pinned at
  anomalyco/opencode `v2.2.2` (098aa7fd), the ref where the repo tag and the
  `@opencode/plugin` package (2.2.2, "authoring interfaces and runtime loader support
  for OpenCode V2 plugins") agree. The pin is the API authority for every harness
  tier, and the tier-2 binary builds from it into the scratch install.

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
- Landed 2026-10-30 (the rope channel opened by the operator): the selection round
  on the ready-frontier state returned a unanimous winner at n=3 — arm C, the door
  doctrine plus the exemplar ACTION block, 6/6 on every draw while every other arm
  scored 1-2/6 inventing the `ci` verb — and the locked confirmation on the held-out
  needs-you and parked states confirmed it on all three pre-declared criteria
  (C pooled 5.00 vs the incumbent 1.83; C zero-invented on all 12 draws; the
  incumbent violated the state gate on NEEDS YOU, running commands where nothing
  may run). The ship gate passed: the exemplar prompt is the loop's DOCTRINE as of
  this node's commit, and `bench/round-1-results.md` carries both tables and the
  protocol. The subject was real qwen3.5-4b end to end (the rope WAN edge, the
  bearer env-only).

### Plugin prototype {#prototype}

- verify: the plugin (Plugin.define, V2-native, the coordinator's client) loads in a
  real OpenCode 2.x session from the plan room; the /host-goal family drives the verbs
  through subprocesses; the loop fires once on idle with an armed goal and stops on a
  no-tool-call turn; no persistent plugin state exists
- inputs: plugin/, ../tools/opencode (the API authority at the pin)
- depends: #discover, #convene
- note: runs the incumbent prompt; the confirmed prompt lands after #ab-program
- Built 2026-10-29, the live proof partial: `plugin/index.ts` and
  `plugin/package.json` are the promise-form Plugin.define contract, zero
  dependencies (the default export needs no node_modules), carrying the three
  tools (goal_show, tasks_status, tasks_record), the /host-goal family (set takes
  a plan/NNNN-slug, free text refused to goal propose; park, unpark, complete
  drive their verbs and re-orient), and the loop as the coordinator's client: the
  `experimental.idle` hook admits at most one synthetic continuation per safe
  tick, admission decided by the emission alone, the cap default 25 failing
  closed on an unknown value, the three-stall mechanical guard, and the
  no-tool-call turn guard. The live load proof in a real opencode 2.2.2 session
  (the scratch binary over the fixture): `opencode plugin list` reads
  `host-loop  local  <the plan-room path>`, and the standalone server log
  carries the load line plus the boot probe "[host-loop] boot: seam ok;
  plan/0001-smoke; 0 of 1 milestone tasks receipted; PLAN.md row present" — the
  verb subprocess and the parser exercised at startup, model or no model. The
  command turn, the model-driven tool calls, and the idle continuation need a
  live model turn: every channel is exhausted tonight (tokenhub's package
  disabled on both models, rope bearerless and LAN-scoped, the direct Fen
  endpoint LAN-scoped), so the loop half of this node's verify stays unproven
  and the task stays unreceipted; `bench/verify-plugin.sh` is the one-command
  harness the moment a channel opens. The event subscription floats its
  iterator (the promise form); the promotion decides the Effect-form port.
- Live continuation proof, same day (the free gateway model, opencode/glm-5.3-flash-free,
  the channel the auth store already held): with a two-task fixture whose second task
  cannot pass (`verify: false`, the deliberate ready-but-failing state), the server log
  reads "[host-loop] admit #1" naming the second task's work key — the idle hook
  admitted a
  continuation with an armed goal and remaining work, and the model's continuation turn
  began from the synthetic. The model ran the failing verify, refused to false-record,
  and named the fixture's design in its own report; the loop's silence rules held at
  every boundary. Two warts recorded for #tier1: the tool bridge no-ops plugin tools
  in this environment (three silent tasks_record attempts; the model fell back to the
  CLI, the house's primary surface), and the fixture PATH binary is the stale 0.60.4
  (the plugin's own calls carry HOST_LIFECYCLE_BIN). The no-tool-call stop did not
  arise live (a diligent model makes tool calls); its discharge is the tier-1 suite's.

### Tier 1 suite {#tier1}

- verify: the bun unit suite is green against typed fakes of the OpenCode 2 hook
  surfaces (built against the materialized pin's types, never from memory), asserting
  the command set, the state authority, and the bounds per stop reason; and
  `host-lifecycle obligations plugin/host-loop.allium --tests plugin
  --strict-discharge` is green
- depends: #prototype, #materialize
- Landed 2026-10-29: `plugin/suite.test.ts`, twenty tests green, the fakes typed to
  the promise Context's real shapes (one API correction the fakes caught: the event
  subscription returns its AsyncIterable synchronously). The runner deviation is
  recorded: bun is absent on this machine, so the suite runs under node --test (node
  26 strips the types natively); the bun port is a promotion detail. The test
  definitions are object methods so the obligations scanner sees each `name() {` at
  line start; every stop reason has a test (armed, parked, no-goal, busy,
  complete, needs-you, cap, unknown-cap, three stalls, no-tool-call), the command
  set asserts the three doors and the verb mappings, and the free-text refusal got
  sharper because the suite demanded it: any non-family argument now reads the
  goal-propose refusal shape. The discharge check reads all 24 obligations
  dispositioned with zero findings under --strict-discharge.

### Tier 2 harness {#tier2}

- verify: real headless OpenCode 2.x runs (the pinned scratch install) assert the
  host-ledger effects (receipt stanzas, GOAL.md, the sidecar), the loop bounds, and
  the printed stop reasons
- depends: #tier1
- Built 2026-10-29, the battery partial: `bench/tier2.sh` runs four scenarios
  (the success path, the parked hold, the cap failing closed, the
  ready-but-failing integrity) with per-assertion ok/MISS lines, a 1G watchdog on
  the server storage, and the server data dir OUTSIDE the fixture worktree. That
  last one is a harness-design lesson paid for twice: the snapshot machinery
  commits the observed tree per step, so a data dir inside the worktree feeds
  itself (one run wrote 23G before the disk filled; the git-spawn count in the
  run log is the storm's signature). The first corrected run proved the decisive
  assertions before the free gateway's quota ran out ("Free usage limit reached"):
  the admit printed, GOAL.md and the sidecar carried the goal, the parked hold
  passed in full, and the boot probe exercised the seam in every scenario. The
  receipt-stanza and stop-reason asserts are written and correct but await a
  living model channel; the task stays unreceipted until the battery completes.
  Also recorded: in headless run mode the loop admits once per run (the process
  exits after the continuation turn), so the multi-admission bounds are tier-1's
  deterministic ground and the TUI's long-session behavior.
- Battery completed 2026-10-30 (the free quota reset at midnight): **16 of 17
  green**, scenario A in full (the loop admitted; both done receipt stanzas in the
  ledger; GOAL.md and the sidecar carrying the goal; the probe exercised), B in
  full (the parked hold dispatches nothing, every surface standing), D in full
  twice (the admission onto the failing frontier; the failing verify reported; no
  false receipt; exactly one honest receipt; the goal uncompleted). The one miss
  is a real finding, not a harness defect: scenario C's env-plumbed cap
  (`HOST_LOOP_MAX_ITERATIONS=0`) never reached the plugin under
  `opencode run --standalone` on the pin — the loop admitted six times and the
  refusal line never printed, so the environment contract between the CLI and the
  standalone server does not pass through arbitrary plugin env. The remedy is the
  config-plumbed cap (the `plugins` entry's `options`, which the schema carries)
  with the env kept as the fallback; the fail-closed rule itself is tier-1-proven
  and unaffected. Corrected note: run-mode sessions DO admit multiple times in
  one process (A showed four admissions, C six); the earlier one-admission
  reading was the throttled runs, and the cap and stall guards are what bind a
  long session — exactly what the config cap fixes.
- Addendum, same night: the env-contract finding is fixed at the source. The
  plugin now reads the cap from the plugins entry's `options.maxIterations`
  (the path that reaches the plugin), falling back to the env, an explicitly
  invalid value failing closed; two tier-1 tests pin the override and the
  refusal (22/22 green), and the discharge check stays green. Scenario C's
  harness assert became outcome-based twice over: the config cap demonstrably
  reached the plugin in the first fixed run (zero admissions where the env cap
  had admitted six), and the refusal line's print was re-aimed at a fixture
  whose frontier holds work at the idle boundary — the line prints only then,
  behind the frontier checks. The free tier's daily allowance is roughly one
  battery; the re-run died mid-A, so the 17/17 completion run awaits a fresh
  quota or a sturdier channel. The scenario-A assert also became outcome-based:
  the model may discharge both tasks in the command turn itself, and the
  receipt stanzas, not the admit line, are the success claim.

### Tier 3 Fen acceptance {#fen}

- verify: qwen3.5-4b completes a bounded loop in a scratch project, working the
  frontier, recording receipts, and stopping at NEEDS YOU; transcript and rubric table
  in `bench/`
- depends: #tier2, #ab-program
- Landed 2026-10-30, both halves, on real qwen3.5-4b: the work run under the
  confirmed prompt completed the bounded loop — both receipts in the RIGHT ledger
  (`tasks --record` into .host-task-receipts, the task graph reading both done, the
  frontier discharged, two admissions), where the pre-A/B run under the incumbent
  prompt had recorded into the wrong ledger and claimed a completion the surface
  refuted (the finding the A/B was run to fix, fixed). The stop run on the
  NEEDS YOU state held: Fen tried the no-op tool bridge, got nothing, asked the
  operator, and ran nothing — zero commands, zero state changes. The acceptance
  also surfaced two findings recorded for the ladder: the floor model will
  fabricate a plan directory and re-aim the goal at it (valid_target's existence
  check accepted the fabrication; the deep fix is upstream), and every loop bound
  lived between turns while a weak model's single turn can run unboundedly long —
  the wall-clock deadline (HOST_LOOP_MAX_MINUTES / options.maxMinutes, default 30)
  is the bound that closes it, pinned in tier 1.

### Promotion ruling {#promote}

- verify: the component-versus-template-payload ruling recorded (proposed component
  name host-loop, the lemgate-to-host-voice arc), the recipe and release cascade
  scoped, and the deferral resolution noted on plan/0103's record
- depends: #fen
- Ruled 2026-10-30: **the component wins** (proposed `host-loop`, the
  lemgate-to-host-voice arc). The reasons, recorded: the plugin has its own release
  cadence (the prompt ships on A/B confirmation, not on template revisions), its
  own verification surface (23 tier-1 tests, the obligations manifest, the tier-2
  battery), and its own API dependency (the tools/opencode pin) — a template
  payload would couple all three to the spine's revision train and deny adopters
  pinned releases, the exact coupling plan/0104 rejected for host-voice. The
  recipe, scoped: a TypeScript component (node-compatible, the bun question open at
  the build milestone) in a `connollydavid/host-loop` repo, the `.host-software`
  stanza pinning it with the plugin directory as the deploy artifact, CI lanes for
  the tier-1 suite plus the obligations strict-discharge (the tier-2 battery a
  manual lane against a living channel), and the publish receipt from day one
  (lc#30). The deferral resolution is noted on plan/0103's record. The build
  milestone is recommended for cut on the operator's ruling.

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
