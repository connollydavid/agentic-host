// host-loop: the opencode goal loop under host governance (plan/0106).
//
// Promise-form Plugin.define contract, zero dependencies: the default export is
// `{ id, setup }` and nothing is imported, so the loader needs no node_modules.
// The tracked surfaces are the only state authority (GOAL.md and the receipt fold,
// read through the verbs); this module holds no persistent state, only the
// in-memory iteration and progress counters below. The host verifier stack is the
// sole verifier: the plugin adds no checks and claims no completion.

// The version seam: the binary the verbs run through, overridable for fixtures.
const HL = process.env.HOST_LIFECYCLE_BIN || "host-lifecycle"

// The continuation body's doctrine, SHIPPED per the A/B confirmation (bench/
// round-1-results.md): arm C, the door doctrine plus the exemplar ACTION block,
// confirmed against the incumbent on the held-out needs-you and parked states
// (C 5.0 vs B 1.83 pooled, the zero-invented hard gate clean, the incumbent
// violating the state gate). The exemplar is the plan/0100 finding measured in
// the loop's own context: the exact record command in the prompt is what the
// weak model needs to land the receipt in the right ledger.
const DOCTRINE = [
  "Work the NEXT line.",
  "If it is a command, run it as printed.",
  "If it says work a task, start that task.",
  "Never invent a command or a flag.",
  "NEEDS YOU non-none means ask the operator and nothing else runs.",
  "Record each done task with the tasks verb.",
  "Then re-orient with goal show.",
  "A correct reply runs the NEXT line's work, records the receipt, and re-orients:",
  "ACTION:",
  "$ <the verify or work the NEXT line names>",
  "$ host-lifecycle tasks --record <the task key> --disposition done .",
  "$ host-lifecycle goal show .",
].join("\n")

// The injected I/O surface: the verb runner and the iteration cap. The production
// io spawns the binary (the runtime is Bun); the unit suite injects a fake runner
// and an explicit cap, so one code path serves both.
export interface LoopIo {
  runVerb: (root: string, args: string[]) => Promise<{ ok: boolean; text: string }>
  cap: number | undefined
}

function defaultIo(): LoopIo {
  // The iteration cap; unknown values fail closed (never guessed).
  let cap: number | undefined = 25
  const raw = process.env.HOST_LOOP_MAX_ITERATIONS
  if (raw !== undefined) {
    const n = Number.parseInt(raw, 10)
    cap = Number.isFinite(n) && n > 0 ? n : undefined
  }
  return {
    cap,
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

// The options cap: the config entry's options.maxIterations overrides the env
// (the tier-2 finding: the env var does not reach the plugin under `opencode run
// --standalone` on the pin). An explicitly invalid value refuses; an absent one
// falls back to the io's cap.
function optionsCap(options: any): { has: boolean; cap: number | undefined } {
  const raw = options?.maxIterations
  if (raw === undefined) return { has: false, cap: undefined }
  const n = typeof raw === "number" ? raw : Number.parseInt(String(raw), 10)
  return { has: true, cap: Number.isFinite(n) && n > 0 ? n : undefined }
}

// The wall-clock bound: every other guard lives between turns, and a weak model's
// single turn can run unboundedly long (the Fen acceptance exposed it: a 4B
// thinking-mode turn ran past fifty minutes). The loop stops admitting once its
// per-session deadline passes; HOST_LOOP_MAX_MINUTES and options.maxMinutes
// override the 30-minute default.
function optionsMinutes(options: any): { has: boolean; minutes: number } {
  const raw = options?.maxMinutes
  if (raw === undefined) return { has: false, minutes: 0 }
  const n = typeof raw === "number" ? raw : Number.parseInt(String(raw), 10)
  return { has: true, minutes: Number.isFinite(n) && n > 0 ? n : 30 }
}

function deadlineMinutes(options: any): number {
  const env = process.env.HOST_LOOP_MAX_MINUTES
  if (env !== undefined) {
    const n = Number.parseInt(env, 10)
    if (Number.isFinite(n) && n > 0) return n
  }
  const opt = optionsMinutes(options)
  return opt.has ? opt.minutes : 30
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

export function makePlugin(io: LoopIo = defaultIo()) {
  return {
  id: "host-loop",
  setup: async (ctx: any) => {
    const root = ctx.location?.directory ?? process.cwd()
    const opt = optionsCap(ctx.options)
    const cap = opt.has ? opt.cap : io.cap

    // The verbs, wrapped once: every surface reads through them.
    const goalShow = () => io.runVerb(root, ["goal", "show", "."])
    const tasksStatus = () => io.runVerb(root, ["tasks", "."])
    const tasksRecord = (key: string) => io.runVerb(root, ["tasks", "--record", key, "--disposition", "done", "."])
    const orient = async (sessionID: string) => {
      const show = await goalShow()
      const body = show.ok ? `${show.text}\n\n${DOCTRINE}` : `${show.text}\n\nThe verb refused; run it in a terminal and read the remedy. Never invent a command or a flag.`
      await ctx.session.prompt({ sessionID, text: body, delivery: "queue" })
    }

    // The model-facing tools (the doors' surface; there is no complete and never will be).
    await ctx.tool.transform((editor: any) => {
      editor.add({
        name: "goal_show",
        description: "The host goal orientation: PURPOSE, POSITION, NEEDS YOU, CI, FRONTIER, NEXT. The emission is the instruction.",
        parameters: { type: "object", properties: {}, additionalProperties: false },
        execute: async () => ({ output: (await goalShow()).text }),
      })
      editor.add({
        name: "tasks_status",
        description: "The receipted task graph with the ready frontier.",
        parameters: { type: "object", properties: {}, additionalProperties: false },
        execute: async () => ({ output: (await tasksStatus()).text }),
      })
      editor.add({
        name: "tasks_record",
        description: "Record a done task receipt by key (plan/NNNN#anchor). The receipt pulls the task's own verify and inputs.",
        parameters: {
          type: "object",
          properties: { key: { type: "string", description: "the task key, e.g. plan/0106#prototype" } },
          required: ["key"],
          additionalProperties: false,
        },
        execute: async (input: { key: string }) => ({ output: (await tasksRecord(input.key)).text }),
      })
    })

    // The /host-goal family: the operator's typed commands are the operator's hand
    // on the verbs. Free text is refused to goal propose (a goal IS a milestone).
    await ctx.command.transform((editor: any) => {
      editor.add({
        name: "host-goal",
        description: "Orient on the active goal: /host-goal [set <plan/NNNN-slug> | park <reason> | unpark | complete]",
        execute: async (input: any) => {
          const arg = (input.prompt?.text ?? "").trim()
          const [verb, ...rest] = arg.split(/\s+/)
          if (!verb || verb === "show") return orient(input.sessionID)
          if (verb === "set") {
            const target = rest[0]
            if (!target || !/^plan\/\d{4}-/.test(target)) {
              await ctx.session.prompt({
                sessionID: input.sessionID,
                text: `Refused: a goal IS a plan/NNNN milestone (call/0061). Propose one instead:\n\nNEXT: ${HL} goal propose <plan/NNNN-slug> .`,
                delivery: "queue",
              })
              return
            }
            await io.runVerb(root, ["goal", "set", target, "."])
            return orient(input.sessionID)
          }
          if (verb === "park") {
            const reason = rest.join(" ") || "operator hold"
            await io.runVerb(root, ["goal", "park", "--reason", reason, "."])
            return orient(input.sessionID)
          }
          if (verb === "unpark") {
            await io.runVerb(root, ["goal", "unpark", "."])
            return orient(input.sessionID)
          }
          if (verb === "complete") {
            const out = await io.runVerb(root, ["goal", "complete", "."])
            await ctx.session.prompt({ sessionID: input.sessionID, text: out.text, delivery: "queue" })
            return
          }
          await ctx.session.prompt({
            sessionID: input.sessionID,
            text: `Refused: a goal IS a plan/NNNN milestone (call/0061). The family is set, park, unpark, complete, show; propose a goal instead:\n\nNEXT: ${HL} goal propose <plan/NNNN-slug> .`,
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

    // The loop: the V2 autonomous coordinator's client. The host owns due-versus-
    // safe (this hook fires only when the session would go idle with nothing
    // pending); the tracked surface alone decides admission. No second controller.
    const iterations = new Map<string, number>()
    const progressSig = new Map<string, string>()
    const stalled = new Map<string, number>()
    const usedTools = new Set<string>()
    const startedAt = new Map<string, number>()
    const minutes = deadlineMinutes(ctx.options)

    // A turn with no tool calls is the anti-runaway guard: count them per session.
    const events = ctx.event.subscribe({ types: ["session.tool.called", "session.deleted"] })
    ;(async () => {
      for await (const event of events) {
        if (event.type === "session.deleted") {
          for (const m of [iterations, progressSig, stalled]) m.delete(event.data.sessionID)
          usedTools.delete(event.data.sessionID)
        } else {
          usedTools.add(event.data.sessionID)
        }
      }
    })()

    await ctx.session.hook("experimental.idle", async (event: any) => {
      const sessionID = event.sessionID
      // HoldWhenBusy: the coordinator ticks only at safe boundaries, and pending
      // background work (a subagent or an image job) is not one; the reference
      // goal plugin in the pin skips the same shape.
      if (event.background?.some((w: any) => w.kind === "subagent" || w.kind === "image")) return
      const show = await goalShow()
      const em = parseEmission(show.text)
      // NoGoalSilent: no goal or a refusing verb silences the loop.
      if (!show.ok || !em.goal || !em.next || em.next === "(none)") return
      // StopOnComplete: a banked completion is the surface's to carry, not ours.
      if (em.frontier?.includes("(none")) return
      // ParkedHolds: a parked goal holds the loop.
      if (em.frontier?.includes("held while parked")) return
      // NEEDS YOU non-none means ask the operator and nothing else runs.
      if (em.needsYou && em.needsYou !== "none") return
      // CapFailsClosed: an unknown cap refuses to arm.
      if (cap === undefined) {
        console.error("[host-loop] HOST_LOOP_MAX_ITERATIONS is not a positive integer; refusing to arm")
        return
      }
      // The wall-clock bound: the loop stops admitting once the per-session
      // deadline passes, however long the individual turns run.
      const start = startedAt.get(sessionID) ?? Date.now()
      startedAt.set(sessionID, start)
      if (Date.now() - start > minutes * 60_000) {
        console.error(`[host-loop] stop: the ${minutes}-minute deadline passed for ${sessionID}`)
        return
      }
      const count = (iterations.get(sessionID) ?? 0) + 1
      if (count > cap) {
        console.error(`[host-loop] stop: cap (${cap}) reached for ${sessionID}`)
        return
      }
      // The no-progress guard, counted mechanically: the same position and frontier
      // on consecutive admissions, three in a row, stops the loop.
      const sig = `${em.position}|${em.frontier}`
      if (progressSig.get(sessionID) === sig) stalled.set(sessionID, (stalled.get(sessionID) ?? 0) + 1)
      else stalled.set(sessionID, 0)
      progressSig.set(sessionID, sig)
      if ((stalled.get(sessionID) ?? 0) >= 3) {
        console.error(`[host-loop] stop: three consecutive turns with no receipt and no frontier movement (${sessionID})`)
        return
      }
      // The no-tool-call guard: a turn that called nothing stops the loop.
      if (!usedTools.has(sessionID)) {
        console.error(`[host-loop] stop: the last turn made no tool calls (${sessionID})`)
        usedTools.add(sessionID) // the stop itself is the answer; a fresh user turn re-arms
        return
      }
      usedTools.delete(sessionID)
      iterations.set(sessionID, count)
      console.error(`[host-loop] admit #${count}: ${em.next}`)
      // EmissionIsPrompt: the continuation body is the emission verbatim plus the
      // doctrine; nothing is referenced but absent.
      await ctx.session.synthetic({ sessionID, text: `${show.text}\n\n${DOCTRINE}`, metadata: { source: "host-loop" } })
    })

    // The boot probe: the version seam and the emission parser exercised once at
    // startup, model or no model. A refusing verb logs its remedy and the loop
    // stays silent until it is repaired; the probe never mutates anything.
    const boot = await goalShow()
    if (boot.ok) {
      const em = parseEmission(boot.text)
      console.error(`[host-loop] boot: seam ok; ${em.goal ?? "(no active goal)"}; ${em.position ?? "position unknown"}`)
    } else {
      console.error(`[host-loop] boot: the verb refused (${boot.text.split("\n")[0]}); the loop stays silent until it is repaired`)
    }
  },
  }
}

export default makePlugin()
