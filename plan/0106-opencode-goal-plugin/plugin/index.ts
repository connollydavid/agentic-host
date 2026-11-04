// host-loop: the host goal loop, realigned onto opencode's native /goal
// (plan/0109). One controller, upstream's: this plugin registers NO idle hook
// and sends NO continuations. It bridges the host verbs (the sole state
// authority: receipts, the Status line, GOAL.md) to the native goal lifecycle
// through ctx.session.command — the same public-typed surface opencode's own
// TUI goal widget drives — and keeps four mechanical belts over the goal RPC
// (get + changed): the round cap, the wall-clock deadline, the NEEDS YOU stop,
// and the native-overwrite guard. Promise-form Plugin.define, zero
// dependencies: the goal RPC is called through a structural definition typed
// against the public Rpc surface (the npm-distributed component cut declares
// @opencode/schema and imports Goal.Definition directly).

// The version seam: the binary the verbs run through, overridable for fixtures.
const HL = process.env.HOST_LIFECYCLE_BIN || "host-lifecycle"

// The objective's doctrine tail, shipped per the A/B confirmation (bench/
// round-1-results.md): the exemplar ACTION block is what the weak model needs
// to land the receipt in the right ledger.
const DOCTRINE = [
  "Work the NEXT line.",
  "If it is a command, run it as printed.",
  "If it says work a task, start that task.",
  "Never invent a command or a flag.",
  "NEEDS YOU non-none means ask the operator and nothing else runs.",
  "Record each done task with the tasks verb, passing the verify output as evidence.",
  "Never hand-edit a state file; the verbs write them.",
  "Then re-orient with goal show.",
  "A correct reply runs the NEXT line's work, records the receipt, and re-orients:",
  "ACTION:",
  "$ <the verify or work the NEXT line names>",
  "$ host-lifecycle tasks --record <the task key> --disposition done --evidence <the verify output> .",
  "$ host-lifecycle goal show .",
].join("\n")

const OBJECTIVE_TAIL = [
  "",
  "Milestone completion runs through the host verbs (host-lifecycle goal",
  "complete <slug> .), never a bare claim: accept nothing less than that",
  "command's output as evidence the milestone is closed. While NEEDS YOU",
  "reads non-none, ask the operator and run nothing.",
].join("\n")

const MAX_OBJECTIVE = 4000

// The injected I/O surface: the verb runner, the round cap, and the deadline
// minutes. The production io spawns the binary (the runtime is Bun); the unit
// suite injects a fake runner and explicit values, so one code path serves
// both.
export interface LoopIo {
  runVerb: (root: string, args: string[]) => Promise<{ ok: boolean; text: string }>
  cap: number | undefined
  minutes: number
}

function optionsInt(options: any, key: string): { has: boolean; value: number } {
  const raw = options?.[key]
  if (raw === undefined) return { has: false, value: 0 }
  const n = typeof raw === "number" ? raw : Number.parseInt(String(raw), 10)
  return { has: true, value: Number.isFinite(n) && n > 0 ? n : 0 }
}

function defaultIo(): LoopIo {
  const int = (name: string, dflt: number): number => {
    const raw = process.env[name]
    if (raw === undefined) return dflt
    const n = Number.parseInt(raw, 10)
    return Number.isFinite(n) && n > 0 ? n : 0
  }
  return {
    cap: int("HOST_LOOP_MAX_ITERATIONS", 25) || undefined,
    minutes: int("HOST_LOOP_MAX_MINUTES", 30) || 30,
    runVerb: async (root, args) => {
      const proc = Bun.spawn([HL, ...args], { cwd: root, stdout: "pipe", stderr: "pipe" })
      const [stdout, stderr, code] = await Promise.all([
        new Response(proc.stdout).text(),
        new Response(proc.stderr).text(),
        proc.exited,
      ])
      return { ok: code === 0, text: (stdout + (stderr ? `\n${stderr}` : "")).trim() }
    },
  }
}

function parseEmission(text: string) {
  const field = (name: string) => {
    const line = text.split("\n").find((l) => l.startsWith(name))
    return line ? line.slice(name.length).trim() : undefined
  }
  return {
    goal: field("GOAL:"),
    position: field("POSITION:"),
    needsYou: field("NEEDS YOU:"),
    frontier: field("FRONTIER:"),
    next: field("NEXT:"),
  }
}

// The structural goal RPC definition (public Rpc.PortableDefinition shape;
// runtime keys off id and method names and passes input through verbatim).
const GOAL_DEF: any = {
  id: "opencode.goal",
  methods: { get: { input: { type: "object" }, output: { type: "object" } } },
  events: { changed: { schema: { type: "object" } } },
}

export interface NativeGoal {
  id: string
  status: "active" | "paused" | "complete"
  rounds: number
}

// The belts, as a pure decision (unit-tested): given the native goal state,
// our emission, the clock, and the bounds, which pause reason fires? "none"
// means the native coordinator keeps driving.
export function beltReason(
  goal: NativeGoal | null,
  needsYou: string | undefined,
  nowMs: number,
  armedAt: number | undefined,
  cap: number | undefined,
  minutes: number,
  expectedId: string | undefined,
): string | null {
  if (!goal || goal.status !== "active") return null
  if (needsYou && needsYou !== "none") return `NEEDS YOU reads non-none (${needsYou})`
  if (cap !== undefined && goal.rounds >= cap) return `the round cap (${cap}) is reached`
  if (armedAt !== undefined && nowMs - armedAt > minutes * 60_000)
    return `the ${minutes}-minute deadline passed`
  if (expectedId !== undefined && goal.id !== expectedId)
    return "the native goal changed under an armed host goal (a native /goal overwrote it)"
  return null
}

export function makePlugin(io: LoopIo = defaultIo()) {
  return {
  id: "host-loop",
  setup: async (ctx: any) => {
    const root = ctx.location?.directory ?? process.cwd()
    const optCap = optionsInt(ctx.options, "maxIterations")
    const optMin = optionsInt(ctx.options, "maxMinutes")
    const cap = optCap.has ? (optCap.value || undefined) : io.cap
    const minutes = optMin.has ? (optMin.value || 30) : io.minutes

    const goalShow = () => io.runVerb(root, ["goal", "show", "."])
    const tasksStatus = () => io.runVerb(root, ["tasks", "."])
    const tasksRecord = (key: string, evidence: string) =>
      io.runVerb(root, ["tasks", "--record", key, "--disposition", "done", "--evidence", evidence, "."])

    // The native bridge: drive the /goal lifecycle exactly as the TUI widget
    // does (packages/client session.command; the plugin Context exposes the
    // same method, typed-public).
    const native = (sessionID: string, text: string) =>
      ctx.session.command({ sessionID, name: "goal", text }).catch((e: unknown) => {
        console.error(`[host-loop] native goal command failed (${text.split(" ")[0]}): ${e}`)
      })

    const rpcGoal = () => {
      try {
        return ctx.rpc?.(GOAL_DEF)
      } catch {
        return undefined
      }
    }
    const getNative = async (sessionID: string): Promise<NativeGoal | null> => {
      try {
        const g = await rpcGoal()?.get?.({ sessionID })
        return g && typeof g === "object" ? (g as NativeGoal) : null
      } catch {
        return null
      }
    }

    // The belts' runtime state: the goal id we created per session, and when
    // that session's host goal was armed.
    const createdId = new Map<string, string>()
    const armedAt = new Map<string, number>()

    const runBelts = async (sessionID: string) => {
      const goal = await getNative(sessionID)
      if (!goal) {
        createdId.delete(sessionID)
        armedAt.delete(sessionID)
        return
      }
      const show = await goalShow()
      const needsYou = show.ok ? parseEmission(show.text).needsYou : undefined
      const reason = beltReason(
        goal,
        needsYou,
        Date.now(),
        armedAt.get(sessionID),
        cap,
        minutes,
        createdId.get(sessionID),
      )
      if (reason) {
        console.error(`[host-loop] belt: ${reason}; pausing the native goal`)
        await native(sessionID, "pause")
      }
    }

    // Belt triggers: the changed event when the rpc surface allows the
    // subscription, and a light interval as the belt-and-braces path.
    try {
      rpcGoal()?.events?.on?.("changed", (ev: any) => {
        const sessionID = ev?.sessionID
        if (typeof sessionID === "string") void runBelts(sessionID)
      })
    } catch {
      // The interval below carries the belts alone.
    }
    const beltTimer = setInterval(() => {
      for (const sessionID of createdId.keys()) void runBelts(sessionID)
    }, 60_000)
    beltTimer.unref?.()

    const objective = (emission: string) => `${emission}\n${DOCTRINE}${OBJECTIVE_TAIL}`

    const orient = async (sessionID: string) => {
      const show = await goalShow()
      const body = show.ok ? `${show.text}\n\n${DOCTRINE}` : `${show.text}\n\nThe verb refused; run it in a terminal and read the remedy. Never invent a command or a flag.`
      await ctx.session.prompt({ sessionID, text: body, delivery: "queue" })
    }

    // The model-facing tools (the doors' surface; there is no complete and never will be).
    // The result shape is the v2.2.2 bridge's contract for schemaless tools
    // (core/src/tool/runtime.ts: an `output` key without a declared output schema
    // dies; `content` is joined and passed to the model verbatim).
    await ctx.tool.transform((editor: any) => {
      editor.add({
        name: "goal_show",
        description: "The host goal orientation: PURPOSE, POSITION, NEEDS YOU, CI, FRONTIER, NEXT. The emission is the instruction.",
        parameters: { type: "object", properties: {}, additionalProperties: false },
        execute: async () => ({ content: (await goalShow()).text }),
      })
      editor.add({
        name: "tasks_status",
        description: "The receipted task graph with the ready frontier.",
        parameters: { type: "object", properties: {}, additionalProperties: false },
        execute: async () => ({ content: (await tasksStatus()).text }),
      })
      editor.add({
        name: "tasks_record",
        description: "Record a done task receipt: run the task's verify first, then pass its output as evidence. Key is plan/NNNN#anchor.",
        parameters: {
          type: "object",
          properties: {
            key: { type: "string", description: "the task key, e.g. plan/0106#prototype" },
            evidence: { type: "string", description: "the verify command's output; the verb refuses a done record without it" },
          },
          required: ["key", "evidence"],
          additionalProperties: false,
        },
        execute: async (input: { key: string; evidence: string }) =>
          ({ content: (await tasksRecord(input.key, input.evidence)).text }),
      })
    })

    // The /host-goal family: the bridge. Each control verb runs the host verb
    // (the state authority) and then drives the native lifecycle to match.
    await ctx.command.transform((editor: any) => {
      editor.add({
        name: "host-goal",
        description: "Orient on the active goal: /host-goal [set <plan/NNNN-slug> | park <reason> | unpark | complete | accept]",
        execute: async (input: any) => {
          const sessionID = input.sessionID
          const arg = (input.prompt?.text ?? "").trim()
          const [verb, ...rest] = arg.split(/\s+/)
          if (!verb || verb === "show") return orient(sessionID)
          if (verb === "set") {
            const target = rest[0]
            if (!target || !/^plan\/\d{4}-/.test(target)) {
              await ctx.session.prompt({
                sessionID,
                text: `Refused: a goal IS a plan/NNNN milestone (call/0061). Propose one instead:\n\nNEXT: ${HL} goal propose <plan/NNNN-slug> .`,
                delivery: "queue",
              })
              return
            }
            const out = await io.runVerb(root, ["goal", "set", target, "."])
            if (!out.ok) {
              await ctx.session.prompt({ sessionID, text: out.text, delivery: "queue" })
              return
            }
            const show = await goalShow()
            const obj = objective(show.ok ? show.text : `Work the milestone ${target} through the host verbs.`)
            if (obj.length > MAX_OBJECTIVE) {
              console.error(`[host-loop] the objective is ${obj.length} chars, over the native ${MAX_OBJECTIVE}; the native goal is not armed (the host goal stands)`)
            } else {
              await native(sessionID, obj)
              const g = await getNative(sessionID)
              if (g?.id) {
                createdId.set(sessionID, g.id)
                armedAt.set(sessionID, Date.now())
              }
            }
            return orient(sessionID)
          }
          if (verb === "park") {
            const reason = rest.join(" ") || "operator hold"
            const out = await io.runVerb(root, ["goal", "park", "--reason", reason, "."])
            await native(sessionID, "pause")
            await ctx.session.prompt({ sessionID, text: out.text, delivery: "queue" })
            return
          }
          if (verb === "unpark") {
            const out = await io.runVerb(root, ["goal", "unpark", "."])
            if (out.ok) {
              const g = await getNative(sessionID)
              if (g && g.status === "paused") {
                await native(sessionID, "resume")
              } else if (!g) {
                const show = await goalShow()
                const obj = objective(show.ok ? show.text : "Continue the host goal through the host verbs.")
                if (obj.length <= MAX_OBJECTIVE) {
                  await native(sessionID, obj)
                  const g2 = await getNative(sessionID)
                  if (g2?.id) {
                    createdId.set(sessionID, g2.id)
                    armedAt.set(sessionID, Date.now())
                  }
                }
              }
            }
            return orient(sessionID)
          }
          if (verb === "complete") {
            const out = await io.runVerb(root, ["goal", "complete", "."])
            await ctx.session.prompt({ sessionID, text: out.text, delivery: "queue" })
            if (out.ok) {
              await native(sessionID, "clear")
              createdId.delete(sessionID)
              armedAt.delete(sessionID)
            }
            return
          }
          if (verb === "accept") {
            const target = rest[0]
            const out = await io.runVerb(root, ["goal", "accept", ...(target ? [target] : []), "."])
            await ctx.session.prompt({ sessionID, text: out.text, delivery: "queue" })
            return
          }
          await ctx.session.prompt({
            sessionID,
            text: `Refused: a goal IS a plan/NNNN milestone (call/0061). The family is set, park, unpark, complete, accept, show; propose a goal instead:\n\nNEXT: ${HL} goal propose <plan/NNNN-slug> .`,
            delivery: "queue",
          })
          return
        },
      })
      editor.add({
        name: "host-tasks",
        description: "The receipted task graph and the ready frontier.",
        execute: async (input: any) => {
          const out = await tasksStatus()
          await ctx.session.prompt({ sessionID: input.sessionID, text: out.text, delivery: "queue" })
        },
      })
      editor.add({
        name: "host-ci",
        description: "The CI lanes' receipted verdicts and their remedies.",
        execute: async (input: any) => {
          const out = await io.runVerb(root, ["ci", "."])
          await ctx.session.prompt({ sessionID: input.sessionID, text: out.text, delivery: "queue" })
        },
      })
    })

    // The boot probe: the version seam and the emission parser exercised once at
    // startup, model or no model. A refusing verb logs its remedy; the probe
    // never mutates anything.
    const boot = await goalShow()
    if (boot.ok) {
      const em = parseEmission(boot.text)
      console.error(`[host-loop] boot: seam ok; ${em.goal ?? "(no active goal)"}; ${em.position ?? "position unknown"}`)
    } else {
      console.error(`[host-loop] boot: the verb refused (${boot.text.split("\n")[0]}); the bridge stays silent until it is repaired`)
    }
  },
  }
}

export default makePlugin()
