// The plan/0109 tier-1 suite: the realignment onto opencode's native /goal.
// The bridge verbs drive BOTH surfaces (the host verb, then the native goal
// command through the same public-typed surface the TUI widget uses); the four
// belts are a pure decision, tested directly. The definitions are object
// methods so the obligations scanner sees each `name() {` at line start.
import { test } from "node:test"
import assert from "node:assert/strict"
import { makePlugin, beltReason, type LoopIo } from "./index.ts"

// The fake verb runner: the goal show call returns the fixture emission; the
// record and status calls return their house shapes; failComplete makes the
// composed gate refuse (its rc nonzero) so complete must not clear the native.
function fakeIo(emission: string, opts: { failComplete?: boolean; failSet?: boolean; failUnpark?: boolean; failAccept?: boolean } = {}) {
  const calls: string[][] = []
  const io: LoopIo = {
    cap: 25,
    minutes: 30,
    runVerb: async (_root, args) => {
      calls.push(args)
      if (args[0] === "goal" && args[1] === "show") return { ok: true, text: emission }
      if (args[0] === "goal" && args[1] === "complete" && opts.failComplete)
        return { ok: false, text: "REFUSED. Nothing was banked and nothing was cleared." }
      if (args[0] === "goal" && args[1] === "set" && opts.failSet)
        return { ok: false, text: "HAZARD   already-active — plan/0001-smoke is the active goal" }
      if (args[0] === "goal" && args[1] === "unpark" && opts.failUnpark)
        return { ok: false, text: "no parked goal to unpark" }
      if (args[0] === "goal" && args[1] === "accept" && opts.failAccept)
        return { ok: false, text: "HAZARD   nothing-to-accept — no closure receipt names plan/0001-smoke" }
      if (args[0] === "tasks" && args[1] === "--record") return { ok: true, text: `recorded task receipt: ${args[2]} = done` }
      if (args[0] === "tasks") return { ok: true, text: "1 task(s) in the plan room" }
      return { ok: true, text: "ok" }
    },
  }
  return { io, calls }
}

// The fake promise Context: records every native goal command and every
// emission the plugin sends; the goal rpc fake serves the test's current
// native goal state.
function fakeCtx(nativeGoal: { id: string; status: string; rounds: number } | null) {
  const tools: any[] = []
  const commands: any[] = []
  const goalCommands: { name: string; text: string }[] = []
  const prompts: any[] = []
  const changedHandlers: ((ev: any) => void)[] = []
  const ctx = {
    location: { directory: "/fixture" },
    tool: { transform: async (cb: any) => cb({ add: (t: any) => tools.push(t) }) },
    command: { transform: async (cb: any) => cb({ add: (c: any) => commands.push(c) }) },
    session: {
      command: async (req: any) => {
        goalCommands.push({ name: req.name, text: req.text })
        return {}
      },
      prompt: async (m: any) => prompts.push(m),
    },
    rpc: () => ({
      get: async () => nativeGoal,
      events: { on: (_ev: string, cb: (ev: any) => void) => changedHandlers.push(cb) },
    }),
  }
  return { ctx, tools, commands, goalCommands, prompts, changedHandlers }
}

function emission() {
  return [
    "PURPOSE: The fixture purpose.",
    "GOAL: plan/0001-smoke",
    "POSITION: 0 of 2 milestone tasks receipted; PLAN.md row present",
    "NEEDS YOU: none",
    "CI: no receipts",
    "FRONTIER: ready (deps satisfied, may run in parallel): plan/0001#smoke",
    "NEXT: work plan/0001#smoke",
  ].join("\n")
}

const ready = emission()
const activeGoal = { id: "g1", status: "active", rounds: 0 }

async function boot(nativeGoal: typeof activeGoal | null = activeGoal, opts: { failComplete?: boolean; failSet?: boolean; failUnpark?: boolean; failAccept?: boolean } = {}) {
  const f = fakeIo(ready, opts)
  const c = fakeCtx(nativeGoal)
  await makePlugin(f.io).setup(c.ctx)
  const goal = c.commands.find((x: any) => x.name === "host-goal")
  return { ...f, ...c, goal }
}

const suite = {
  the_registry_never_provides_complete() {
    // never provides complete: the tool registry carries exactly the three doors'
    // tools and no model-facing completion.
    return (async () => {
      const f = await boot()
      const names = f.tools.map((t) => t.name).sort()
      assert.deepEqual(names, ["goal_show", "tasks_record", "tasks_status"], "never provides complete")
    })()
  },

  tool_results_carry_content_not_output() {
    // The v2.2.2 bridge contract (core/src/tool/runtime.ts): a schemaless tool's
    // execute returning an `output` key dies; `content` is the shape the bridge
    // joins and passes verbatim. The record passthrough carries the evidence.
    return (async () => {
      const f = await boot()
      for (const tool of f.tools) {
        const result = await tool.execute(
          tool.name === "tasks_record" ? { key: "plan/0001#smoke", evidence: "smoke-ok" } : {},
        )
        assert.ok("content" in result, `${tool.name} returns content`)
        assert.ok(!("output" in result), `${tool.name} never returns a bare output key`)
      }
      assert.ok(f.calls.some((c) => c[0] === "tasks" && c[6] === "smoke-ok"), "the evidence reaches the verb")
    })()
  },

  the_command_set_is_the_verb_family() {
    // The family is the bridge: set, park, unpark, complete, accept, show; free
    // text is refused to goal propose.
    return (async () => {
      const f = await boot()
      const names = f.commands.map((c) => c.name).sort()
      assert.deepEqual(names, ["host-ci", "host-goal", "host-tasks"], "the family is three doors")
      await f.goal.execute({ sessionID: "s1", prompt: { text: "make me a sandwich" } })
      assert.match(f.prompts.at(-1).text, /Refused: a goal IS a plan\/NNNN milestone/, "free text is refused")
    })()
  },

  set_drives_the_verb_then_arms_the_native_goal() {
    // The bridge's set: the host verb first (the state authority), then the
    // native goal created with the emission plus the confirmed doctrine as the
    // objective, through the same command surface the TUI widget uses.
    return (async () => {
      const f = await boot(activeGoal)
      await f.goal.execute({ sessionID: "s1", prompt: { text: "set plan/0001-smoke" } })
      assert.ok(f.calls.some((c) => c[0] === "goal" && c[1] === "set" && c[2] === "plan/0001-smoke"), "the verb ran first")
      const created = f.goalCommands.find((g) => g.name === "goal" && !["pause", "resume", "clear"].includes(g.text))
      assert.ok(created, "a native goal command was issued")
      assert.match(created.text, /GOAL: plan\/0001-smoke/, "the objective carries the emission")
      assert.match(created.text, /Never invent a command or a flag/, "the objective carries the doctrine")
      assert.match(created.text, /Milestone completion runs through the host verbs/, "the objective carries the evidence rule")
    })()
  },

  park_pauses_the_native_goal() {
    // park drives the host verb and pauses the native goal.
    return (async () => {
      const f = await boot(activeGoal)
      await f.goal.execute({ sessionID: "s1", prompt: { text: "park operator hold" } })
      assert.ok(f.calls.some((c) => c[1] === "park" && c.at(-2) === "operator hold"), "the verb ran")
      assert.ok(f.goalCommands.some((g) => g.text === "pause"), "the native goal was paused")
    })()
  },

  unpark_resumes_a_paused_native_goal() {
    // unpark drives the verb and resumes a paused native goal.
    return (async () => {
      const f = await boot({ id: "g1", status: "paused", rounds: 3 })
      await f.goal.execute({ sessionID: "s1", prompt: { text: "unpark" } })
      assert.ok(f.calls.some((c) => c[1] === "unpark"), "the verb ran")
      assert.ok(f.goalCommands.some((g) => g.text === "resume"), "the native goal was resumed")
    })()
  },

  unpark_rearms_when_no_native_goal_exists() {
    // unpark after the native goal is gone (server restart, clear) re-arms it
    // with a fresh objective rather than resuming nothing.
    return (async () => {
      const f = await boot(null)
      await f.goal.execute({ sessionID: "s1", prompt: { text: "unpark" } })
      assert.ok(f.calls.some((c) => c[1] === "unpark"), "the verb ran")
      const created = f.goalCommands.find((g) => !["pause", "resume", "clear"].includes(g.text))
      assert.ok(created, "a fresh native goal was created")
      assert.match(created.text, /GOAL: plan\/0001-smoke/, "the fresh objective carries the emission")
    })()
  },

  complete_banks_then_clears_the_native_goal() {
    // A banked closure clears the native goal (their status is a driver
    // detail); a refused gate clears nothing.
    return (async () => {
      const ok = await boot(activeGoal)
      await ok.goal.execute({ sessionID: "s1", prompt: { text: "complete" } })
      assert.ok(ok.goalCommands.some((g) => g.text === "clear"), "a banked closure clears the native goal")
      const refused = await boot(activeGoal, { failComplete: true })
      await refused.goal.execute({ sessionID: "s1", prompt: { text: "complete" } })
      assert.ok(!refused.goalCommands.some((g) => g.text === "clear"), "a refused gate clears nothing")
      assert.match(refused.prompts.at(-1).text, /REFUSED/, "the refusal reached the session")
    })()
  },

  accept_closes_the_host_goal() {
    // accept joins the family: the operator's semantic acceptance is a command.
    return (async () => {
      const f = await boot(null)
      await f.goal.execute({ sessionID: "s1", prompt: { text: "accept plan/0001-smoke" } })
      assert.ok(f.calls.some((c) => c[0] === "goal" && c[1] === "accept" && c[2] === "plan/0001-smoke"), "the accept verb ran")
    })()
  },

  an_oversized_objective_refuses_the_native_arm() {
    // Over the native 4000-char objective cap the native goal is not armed and
    // the refusal is logged; the host goal stands (the verb already ran).
    return (async () => {
      const long = emission().replace("The fixture purpose.", "P".repeat(4200))
      const f = fakeIo(long)
      const c = fakeCtx(activeGoal)
      await makePlugin(f.io).setup(c.ctx)
      const goal = c.commands.find((x: any) => x.name === "host-goal")
      await goal.execute({ sessionID: "s1", prompt: { text: "set plan/0001-smoke" } })
      assert.ok(f.calls.some((x) => x[1] === "set"), "the host verb still ran")
      assert.ok(!c.goalCommands.some((g) => !["pause", "resume", "clear"].includes(g.text)), "no native goal was armed")
    })()
  },

  the_needs_you_belt_pauses_the_native_goal() {
    // Belt: our surface reading NEEDS YOU non-none pauses the native goal.
    return (async () => {
      assert.equal(
        beltReason({ id: "g", status: "active", rounds: 1 }, "the tree is dirty", 0, 0, 25, 30, "g"),
        "NEEDS YOU reads non-none (the tree is dirty)",
      )
    })()
  },

  the_cap_belt_pauses_at_the_round_limit() {
    // Belt: the native rounds reaching our cap pauses (theirs is a fixed 50;
    // ours is ours).
    return (async () => {
      assert.equal(
        beltReason({ id: "g", status: "active", rounds: 25 }, "none", 0, 0, 25, 30, "g"),
        "the round cap (25) is reached",
      )
      assert.equal(beltReason({ id: "g", status: "active", rounds: 24 }, "none", 0, 0, 25, 30, "g"), null)
    })()
  },

  the_deadline_belt_pauses_past_the_clock() {
    // Belt: the wall-clock deadline passes; the native goal pauses however long
    // the individual turns run.
    return (async () => {
      const armed = 1_000_000
      const late = armed + 31 * 60_000
      assert.equal(
        beltReason({ id: "g", status: "active", rounds: 1 }, "none", late, armed, 25, 30, "g"),
        "the 30-minute deadline passed",
      )
      assert.equal(beltReason({ id: "g", status: "active", rounds: 1 }, "none", armed + 29 * 60_000, armed, 25, 30, "g"), null)
    })()
  },

  the_overwrite_belt_pauses_a_foreign_native_goal() {
    // Belt: a native /goal typed over an armed host goal changes the goal id;
    // the belt pauses the foreign loop rather than letting it drive blind.
    return (async () => {
      assert.equal(
        beltReason({ id: "other", status: "active", rounds: 1 }, "none", 0, 0, 25, 30, "g"),
        "the native goal changed under an armed host goal (a native /goal overwrote it)",
      )
    })()
  },

  the_belts_hold_fire_on_a_paused_goal() {
    // The belts never fire on a paused or absent native goal: the coordinator
    // is already stopped; the belts bound the active loop only.
    return (async () => {
      assert.equal(beltReason({ id: "g", status: "paused", rounds: 99 }, "the tree is dirty", 1e9, 0, 25, 30, "g"), null)
      assert.equal(beltReason(null, "the tree is dirty", 1e9, 0, 25, 30, "g"), null)
    })()
  },

  a_refused_set_arms_nothing() {
    // The negative half of the bridge's set: a refusing verb arms no native
    // goal, and the refusal reaches the session.
    return (async () => {
      const f = await boot(activeGoal, { failSet: true })
      await f.goal.execute({ sessionID: "s1", prompt: { text: "set plan/0002-other" } })
      assert.match(f.prompts.at(-1).text, /already-active/, "the refusal reached the session")
      assert.ok(!f.goalCommands.some((g) => !["pause", "resume", "clear"].includes(g.text)), "a refused set arms nothing")
    })()
  },

  park_pauses_even_without_a_native_goal() {
    // The negative half of the bridge's park: with no native goal at all the
    // pause is still issued (idempotent by their handler's design).
    return (async () => {
      const f = await boot(null)
      await f.goal.execute({ sessionID: "s1", prompt: { text: "park holding" } })
      assert.ok(f.goalCommands.some((g) => g.text === "pause"), "the pause was issued")
    })()
  },

  a_refusing_unpark_runs_no_native_command() {
    // The negative half of the bridge's unpark: a refusing verb drives no
    // native resume and no rearm.
    return (async () => {
      const f = await boot({ id: "g1", status: "paused", rounds: 3 }, { failUnpark: true })
      await f.goal.execute({ sessionID: "s1", prompt: { text: "unpark" } })
      assert.ok(!f.goalCommands.some((g) => g.text === "resume"), "no native resume")
      assert.ok(!f.goalCommands.some((g) => !["pause", "resume", "clear"].includes(g.text)), "no native rearm")
    })()
  },

  a_refused_accept_drives_no_closure() {
    // The negative half of accept: with nothing to accept the verb refuses and
    // the refusal reaches the session.
    return (async () => {
      const f = await boot(null, { failAccept: true })
      await f.goal.execute({ sessionID: "s1", prompt: { text: "accept plan/0001-smoke" } })
      assert.match(f.prompts.at(-1).text, /nothing-to-accept/, "the refusal reached the session")
    })()
  },
}

for (const [name, fn] of Object.entries(suite)) test(name, fn)
