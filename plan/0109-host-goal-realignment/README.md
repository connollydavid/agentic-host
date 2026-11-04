# plan/0109: realign /host-goal onto opencode's native /goal

**Status: complete 2026-11-04** (every node landed and verified; the plugin is
the host-loop component, wired into the daily harness; the reminder-belt
remedy for the live finding stays an open review item, its own milestone if
built) (operator-directed: "opencode 2.2 has its
own /goal system we will uninstall all the plugins ByBraw versions, and realign
/host-goal to opencode upstream"). The exploration record: the native system
verified in the materialized pin (`tools/opencode`, goal.ts byte-identical
v2.2.2 through the daily v2.2.5; announced v2.2.1); the public-API audit
(`ctx.session.command` typed-public and first-party-practiced; the goal RPC
readable cross-plugin; structural definition for the dependency-free local
plugin; the npm-distributed component retires the shim).

## The design

One controller, upstream's, by construction: the plugin registers NO idle hook
and sends NO continuations. The bridge maps the verb family onto the native
lifecycle through the same command surface opencode's own TUI goal widget
drives:

| host verb | native lifecycle |
|---|---|
| `goal set` | then `goal <objective>` (the emission plus the confirmed doctrine plus the evidence rule; refused over 4000 chars with the host goal standing) |
| `goal park` | then `pause` |
| `goal unpark` | then `resume` (a missing native goal is re-armed fresh) |
| `goal complete` (banked) | then `clear` (their status is a driver detail; accept-required leaves ours pending) |
| `goal accept` | the family gains `accept` (the v0.63.0 gap closes) |

The four belts stay ours, mechanical, over the goal RPC (`get` + `changed`):
the round cap (default 25; theirs is a fixed 50), the wall-clock deadline
(default 30 minutes), the NEEDS YOU stop (our surface non-none pauses the
native goal), and the native-overwrite guard (a foreign goal id under an armed
host goal pauses the loop). Each pause prints its reason.

The tracked surfaces remain the sole state authority and the sole record: a
native reviewer `done` is a recoverable stop that writes nothing to the
receipts, the Status line, or GOAL.md. The reviewer becomes the turn-tick, not
the verifier; the operator's open question on that trade is answered by the
belts keeping every mechanical stop ours.

## Build sequence

### Uninstall ByBrawe {#uninstall}

- verify: the singular `plugin` entry gone from ~/.config/opencode/opencode.jsonc,
  the retired bundle deleted, the stale V1 `@opencode-ai/plugin` dependency and
  its lock/node_modules pruned, and the config still loading
- Landed 2026-11-04: all three edits applied and verified (`opencode models`
  loads clean; zero bybrawe references; an empty plugins dir).

### The pin {#pin}

- verify: tools/opencode at v2.2.5; the pin equals the daily binary
- Landed 2026-11-04: 9bbb8ce (v2.2.5).

### The bridge and the belts {#bridge}

- verify: node --test green (19 tests: the bridge verbs, the four belts as a
  pure decision, the negative halves, the tools contract);
  `obligations --strict-discharge` green over the re-scoped host-loop.allium
- Landed 2026-11-04: 19/19 green; the spec re-scoped (the admission rules
  become bridge rules; guarantees: UpstreamIsTheOnlyController,
  TrackedSurfacesAreTheAuthority, WrongDoneWritesNothing, BeltsAreMechanical,
  NoPersistentState, HonestTelemetry); all 31 obligations dispositioned with
  zero findings under strict-discharge.

### The live run {#live}

- verify: a rope/qwen3.5-4b run on the daily binary through
  `/host-goal set`: the receipts land in the right ledger under the pinned
  binary; no idle controller of ours fires; the native bridge never errors;
  the boot probe fires
- depends: #bridge
- Landed 2026-11-04, an honest split. The bridge held: the boot probe fired,
  the native goal armed (the model referenced the goal state across turns and
  worked multi-turn under the native coordinator with zero admissions of
  ours), the native bridge never errored, and the receipt the model did land
  carries `tool = host-lifecycle@0.63.0` (the pinned binary on the session
  PATH). But the receipts landed in the WRONG ledger again: the 4B invented a
  `tasks record done` form and wrote a stray `[receipt "tasks"]` stanza into
  the operational ledger, then claimed completion; the native reviewer
  accepted the claim on the visible (wrong) file contents and stopped the
  loop. Nothing false landed in the record (the task graph shows no receipt;
  our surface still reads active; the stray stanza is a pollution our own
  gates flag, not a false closure); a recoverable stop, exactly the designed
  worst case. The finding replicates the A/B's measurement in the realigned
  setting: the doctrine-with-exemplar is load-bearing for the 4B on EVERY
  turn, and the native continuation template (their text, the objective plus
  reviewer feedback) drops it after the kickoff. Remedies named, not built:
  a doctrine-reminder belt (a short synthetic reminder riding the changed
  event; it blurs the no-plugin-messages line),
  or drift-tolerance for floor models while the frontier tier (whose cold
  run held the surface) drives daily. The operator's call at the review.

### Records {#records}

- verify: PLAN.md row, the plan/0106 supersession addendum, MEMORY, the gate
- depends: #live

### Daily wiring {#daily}

- verify: the plugins entry in the operator config pointing at the
  materialized component worktree
  (file:///mnt/c/Users/dconnolly/Development/agentic-host/software/host-loop/main),
  `opencode plugin list` reads host-loop, and one boot-probe line in a
  real session under the daily 2.2.5
- depends: #records
- Superseded shape (the operator, 2026-11-04): the plugin never wires from a
  plan room; plan/0106's plugin directory is deleted and the component
  connollydavid/host-loop (ac83d1cf, the host-grammar precedent: a repo-only
  source at a pin) is its home, materialized under software/host-loop/main
  with its spec, suite, and CI lanes beside the code (plan/0012).

## Named risks

`ctx.session.command` is typed-public but undocumented (first-party TUI
practice; pin-matched to the daily binary to bound drift). The dependency-free
local plugin calls the goal RPC through a structural definition (typed against
the public Rpc surface; retired at the npm component cut). The native
reviewer's verdicts pause and complete THEIR storage only; the worst case is a
recoverable stop, and the belts bound it.
