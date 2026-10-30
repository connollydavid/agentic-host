// The plan/0106 tier-1 suite: the unit tests against typed fakes of the OpenCode 2
// promise-Context surfaces (packages/plugin/src/promise at the tools/opencode v2.2.2
// pin), asserting the command set, the state authority, and the bounds per stop
// reason. The definitions are object methods so the obligations verb's test scanner
// (resolve_test) sees each `name() {` at line start; the runner is node --test (node
// 26 strips the types; bun is absent on this machine and the port is a promotion
// detail).
import { test } from "node:test"
import assert from "node:assert/strict"
import { makePlugin, type LoopIo } from "./index.ts"

// The fake verb runner: the goal show call returns the fixture emission; the record
// and status calls return their house shapes. The calls are recorded so the command
// tests can assert the verb mappings.
function fakeIo(emission: string, cap: number | undefined = 25) {
  const calls: string[][] = []
  const io: LoopIo = {
    cap,
    runVerb: async (_root, args) => {
      calls.push(args)
      if (args[0] === "goal" && args[1] === "show") return { ok: true, text: emission }
      if (args[0] === "tasks" && args[1] === "--record") return { ok: true, text: `recorded task receipt: ${args[2]} = done` }
      if (args[0] === "tasks") return { ok: true, text: "1 task(s) in the plan room" }
      return { ok: true, text: "ok" }
    },
  }
  return { io, calls }
}

// The fake promise Context: captures every registration and every emission the
// plugin sends, and exposes a push channel for the event subscription.
function fakeCtx() {
  const tools: any[] = []
  const commands: any[] = []
  const hooks: Record<string, (event: any) => Promise<void>> = {}
  const synthetic: any[] = []
  const prompts: any[] = []
  const queue: any[] = []
  let wake: (() => void) | undefined
  const ctx = {
    location: { directory: "/fixture" },
    tool: { transform: async (cb: any) => cb({ add: (t: any) => tools.push(t) }) },
    command: { transform: async (cb: any) => cb({ add: (c: any) => commands.push(c) }) },
    session: {
      hook: async (name: string, cb: (event: any) => Promise<void>) => {
        hooks[name] = cb
      },
      synthetic: async (m: any) => synthetic.push(m),
      prompt: async (m: any) => prompts.push(m),
    },
    event: {
      // The real subscribe returns the AsyncIterable synchronously
      // (packages/plugin/src/promise/event.ts at the pin).
      subscribe: () =>
        (async function* () {
          while (true) {
            if (queue.length === 0) await new Promise<void>((r) => (wake = r))
            yield queue.shift()
          }
        })(),
    },
  }
  return {
    ctx,
    tools,
    commands,
    hooks,
    synthetic,
    prompts,
    send: (event: any) => {
      queue.push(event)
      wake?.()
      wake = undefined
    },
  }
}

function emission(over: Partial<Record<string, string>> = {}) {
  const lines: Record<string, string> = {
    "PURPOSE:": "The fixture purpose.",
    "GOAL:": "plan/0001-smoke",
    "POSITION:": "0 of 2 milestone tasks receipted; PLAN.md row present",
    "NEEDS YOU:": "none",
    "CI:": "no receipts",
    "FRONTIER:": "ready (deps satisfied, may run in parallel): plan/0001#smoke",
    "NEXT:": "work plan/0001#smoke",
    ...over,
  }
  return Object.entries(lines)
    .map(([k, v]) => `${k} ${v}`)
    .join("\n")
}

async function settle() {
  await new Promise<void>((r) => setImmediate(r))
}

async function bootWith(io: LoopIo, options?: any) {
  const f = fakeCtx()
  if (options !== undefined) f.ctx.options = options
  await makePlugin(io).setup(f.ctx)
  return f
}

async function tick(f: ReturnType<typeof fakeCtx>, background: any[] = []) {
  await f.hooks["experimental.idle"]({ sessionID: "s1", background })
  await settle()
}

async function withTools(f: ReturnType<typeof fakeCtx>) {
  f.send({ type: "session.tool.called", data: { sessionID: "s1" } })
  await settle()
}

const ready = emission()
const parked = emission({ "FRONTIER:": "(held while parked)" })
const complete = emission({
  "FRONTIER:": "(none; every task discharged, or blocked on an undischarged dep)",
  "NEXT:": "host-lifecycle goal repair .",
})
const goalless = emission({ "GOAL:": "", "NEXT:": "host-lifecycle goal set <plan/NNNN-slug> ." })
const needsYou = emission({ "NEEDS YOU:": "the tree is dirty; commit or stash" })

const suite = {
  armed_goal_admits_one_continuation() {
    // armed goal admits: one safe tick on an active goal dispatches exactly one
    // continuation, the emission verbatim plus the doctrine.
    return (async () => {
      const f = await bootWith(fakeIo(ready).io)
      await withTools(f)
      await tick(f)
      assert.equal(f.synthetic.length, 1, "armed goal admits one continuation")
      assert.match(f.synthetic[0].text, /NEXT: work plan\/0001#smoke/, "the emission is the prompt")
      assert.equal(f.synthetic[0].metadata.source, "host-loop")
    })()
  },

  parked_goal_holds_the_loop() {
    // parked holds: a parked goal keeps the loop from dispatching.
    return (async () => {
      const f = await bootWith(fakeIo(parked).io)
      await withTools(f)
      await tick(f)
      assert.equal(f.synthetic.length, 0, "parked holds the loop")
    })()
  },

  no_goal_is_silent() {
    // silent without goal: no active goal means no dispatch and no noise.
    return (async () => {
      const f = await bootWith(fakeIo(goalless).io)
      await withTools(f)
      await tick(f)
      assert.equal(f.synthetic.length, 0, "silent without goal")
    })()
  },

  busy_tick_never_stacks_a_turn() {
    // busy never stacks: an idle boundary carrying pending background work is not
    // a safe tick; the coordinator will call again when it is.
    return (async () => {
      const f = await bootWith(fakeIo(ready).io)
      await withTools(f)
      await tick(f, [{ kind: "subagent", sessionID: "s1", childSessionID: "c1", agent: "x", description: "d" }])
      assert.equal(f.synthetic.length, 0, "busy never stacks a turn")
    })()
  },

  banked_completion_stops_the_loop() {
    // stop on complete: a banked completion is the surface's to carry; the loop
    // dispatches nothing after it.
    return (async () => {
      const f = await bootWith(fakeIo(complete).io)
      await withTools(f)
      await tick(f)
      assert.equal(f.synthetic.length, 0, "stop on complete")
    })()
  },

  goal_surface_reaches_parked_and_back() {
    // park and unpark: the loop follows the surface through the transition, holding
    // while parked and re-arming when the unpark lands.
    return (async () => {
      const f1 = await bootWith(fakeIo(ready).io)
      await withTools(f1)
      await tick(f1)
      assert.equal(f1.synthetic.length, 1, "park and unpark: active admits")
      const f2 = await bootWith(fakeIo(parked).io)
      await withTools(f2)
      await tick(f2)
      assert.equal(f2.synthetic.length, 0, "park and unpark: parked holds")
      const f3 = await bootWith(fakeIo(ready).io)
      await withTools(f3)
      await tick(f3)
      assert.equal(f3.synthetic.length, 1, "park and unpark: active admits again")
    })()
  },

  goal_surface_activates_from_absent() {
    // goal set: a goal-less tree silences the loop, and the surface activating
    // (the goal set command) arms it again.
    return (async () => {
      const f1 = await bootWith(fakeIo(goalless).io)
      await withTools(f1)
      await tick(f1)
      assert.equal(f1.synthetic.length, 0, "goal set: silent while absent")
      const f2 = await bootWith(fakeIo(ready).io)
      await withTools(f2)
      await tick(f2)
      assert.equal(f2.synthetic.length, 1, "goal set: active arms")
    })()
  },

  goal_surface_reaches_complete_and_back() {
    // complete and re-set: a completed surface stops the loop, and a re-set goal
    // arms it again.
    return (async () => {
      const f1 = await bootWith(fakeIo(complete).io)
      await withTools(f1)
      await tick(f1)
      assert.equal(f1.synthetic.length, 0, "complete and re-set: complete stops")
      const f2 = await bootWith(fakeIo(ready).io)
      await withTools(f2)
      await tick(f2)
      assert.equal(f2.synthetic.length, 1, "complete and re-set: re-set arms")
    })()
  },

  a_parked_or_absent_goal_never_arms() {
    // never arms: the admission rule's negative half, parked and absent together.
    return (async () => {
      const f1 = await bootWith(fakeIo(parked).io)
      await withTools(f1)
      await tick(f1)
      const f2 = await bootWith(fakeIo(goalless).io)
      await withTools(f2)
      await tick(f2)
      assert.equal(f1.synthetic.length + f2.synthetic.length, 0, "never arms on parked or absent")
    })()
  },

  an_active_goal_does_not_hold() {
    // does not hold: the negative of the parked rule; an active goal dispatches.
    return (async () => {
      const f = await bootWith(fakeIo(ready).io)
      await withTools(f)
      await tick(f)
      assert.equal(f.synthetic.length, 1, "an active goal does not hold")
    })()
  },

  an_active_goal_is_not_silent() {
    // is not silent: the negative of the no-goal rule.
    return (async () => {
      const f = await bootWith(fakeIo(ready).io)
      await withTools(f)
      await tick(f)
      assert.ok(f.synthetic.length > 0, "an active goal is not silent")
    })()
  },

  an_idle_tick_dispatches() {
    // idle tick: the safe boundary itself dispatches for an armed goal.
    return (async () => {
      const f = await bootWith(fakeIo(ready).io)
      await withTools(f)
      await tick(f)
      assert.equal(f.synthetic.length, 1, "the idle tick dispatches")
    })()
  },

  an_incomplete_goal_keeps_the_loop() {
    // keeps the loop: an incomplete goal with a moving frontier stays armed across
    // consecutive ticks; each tick may dispatch again.
    return (async () => {
      const f = await bootWith(fakeIo(ready).io)
      for (let i = 0; i < 2; i++) {
        await withTools(f)
        await tick(f)
      }
      assert.equal(f.synthetic.length, 2, "keeps the loop across ticks")
    })()
  },

  the_registry_never_provides_complete() {
    // never provides complete: the tool registry carries exactly the three doors'
    // tools and no model-facing completion.
    return (async () => {
      const f = await bootWith(fakeIo(ready).io)
      const names = f.tools.map((t) => t.name).sort()
      assert.deepEqual(names, ["goal_show", "tasks_record", "tasks_status"], "never provides complete")
      assert.ok(!f.tools.some((t) => t.name === "complete"), "never provides complete")
    })()
  },

  the_command_set_is_the_verb_family() {
    // The command set is the host verb family: three doors, and the /host-goal
    // handler maps set/park/unpark/complete to their verbs and refuses free text
    // to goal propose.
    return (async () => {
      const { io, calls } = fakeIo(ready)
      const f = await bootWith(io)
      const names = f.commands.map((c) => c.name).sort()
      assert.deepEqual(names, ["host-ci", "host-goal", "host-tasks"], "the family is three doors")
      const goal = f.commands.find((c) => c.name === "host-goal")
      await goal.execute({ sessionID: "s1", prompt: { text: "make me a sandwich" } })
      assert.match(f.prompts.at(-1).text, /Refused: a goal IS a plan\/NNNN milestone/, "free text is refused to goal propose")
      await goal.execute({ sessionID: "s1", prompt: { text: "set plan/0001-smoke" } })
      assert.ok(calls.some((c) => c[0] === "goal" && c[1] === "set" && c[2] === "plan/0001-smoke"), "set drives the verb")
      await goal.execute({ sessionID: "s1", prompt: { text: "park operator hold" } })
      assert.ok(calls.some((c) => c[0] === "goal" && c[1] === "park" && c.at(-2) === "operator hold"), "park drives the verb")
      await goal.execute({ sessionID: "s1", prompt: { text: "unpark" } })
      assert.ok(calls.some((c) => c[0] === "goal" && c[1] === "unpark"), "unpark drives the verb")
    })()
  },

  the_cap_stops_the_loop() {
    // The bounds: an iteration cap stops the loop after its last permitted
    // continuation.
    return (async () => {
      const f = await bootWith(fakeIo(ready, 2).io)
      for (let i = 0; i < 3; i++) {
        await withTools(f)
        await tick(f)
      }
      assert.equal(f.synthetic.length, 2, "the cap stops the loop at two")
    })()
  },

  an_unknown_cap_fails_closed() {
    // CapFailsClosed: an unknown cap value refuses to arm at all.
    return (async () => {
      const base = fakeIo(ready)
      const io = { ...base.io, cap: undefined }
      const f = await bootWith(io)
      await withTools(f)
      await tick(f)
      assert.equal(f.synthetic.length, 0, "an unknown cap fails closed")
    })()
  },

  the_options_cap_overrides_the_env_cap() {
    // The config-plumbed cap governs: the plugins entry's options.maxIterations
    // overrides the env-derived cap (the tier-2 env-contract finding's remedy).
    return (async () => {
      const f = await bootWith(fakeIo(ready, 25).io, { maxIterations: 1 })
      for (let i = 0; i < 2; i++) {
        await withTools(f)
        await tick(f)
      }
      assert.equal(f.synthetic.length, 1, "the options cap stops the loop at one")
    })()
  },

  an_invalid_options_cap_fails_closed() {
    // CapFailsClosed through the options: an explicitly invalid options cap
    // refuses to arm even when the env cap is valid.
    return (async () => {
      const f = await bootWith(fakeIo(ready, 25).io, { maxIterations: 0 })
      await withTools(f)
      await tick(f)
      assert.equal(f.synthetic.length, 0, "an invalid options cap fails closed")
    })()
  },

  three_stalls_stop_the_loop() {
    // The no-progress guard: three consecutive turns with the same position and
    // frontier stop the loop mechanically.
    return (async () => {
      const f = await bootWith(fakeIo(ready).io)
      for (let i = 0; i < 4; i++) {
        await withTools(f)
        await tick(f)
      }
      assert.equal(f.synthetic.length, 3, "three stalls stop the loop")
    })()
  },

  a_no_tool_call_turn_stops_the_loop() {
    // The anti-runaway guard: a turn that called no tools stops the loop instead
    // of spinning it (the tier-1 discharge of the live run's unobserved half).
    return (async () => {
      const f = await bootWith(fakeIo(ready).io)
      await tick(f)
      assert.equal(f.synthetic.length, 0, "a no-tool-call turn stops the loop")
    })()
  },

  a_needs_you_emission_stops_the_loop() {
    // NEEDS YOU non-none means ask the operator and nothing else runs.
    return (async () => {
      const f = await bootWith(fakeIo(needsYou).io)
      await withTools(f)
      await tick(f)
      assert.equal(f.synthetic.length, 0, "a NEEDS YOU emission stops the loop")
    })()
  },

  the_deadline_stops_a_long_loop() {
    // The wall-clock bound: the clock stubs 31 minutes ahead before the first
    // tick (the baseline), the first tick admits, and past 62 minutes the second
    // tick refuses — the deadline binds however long the turns run.
    return (async () => {
      const f = await bootWith(fakeIo(ready, 25).io)
      const realNow = Date.now
      Date.now = () => realNow() + 31 * 60_000
      try {
        await withTools(f)
        await tick(f)
        Date.now = () => realNow() + 62 * 60_000
        await withTools(f)
        await tick(f)
      } finally {
        Date.now = realNow
      }
      assert.equal(f.synthetic.length, 1, "the deadline admits once, then stops the loop")
    })()
  },
}

for (const [name, fn] of Object.entries(suite)) test(name, fn)
