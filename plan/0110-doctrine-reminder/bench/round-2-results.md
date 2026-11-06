# The A/B program, round two (plan/0110): the reminder belt's ship gate

Subject qwen3.5-4b on the rope router over the WAN edge (the bearer env-only),
thinking on, the server's recipe (no client sampling params), 2026-11-05, from
the WSL archlinux vantage. The kit is round 1's, extended: two arms over the
belt's own text (R0 the incumbent continuation shape, arm B's construction; R1
the same with the reminder riding at the tail, byte-faithful to the REMINDER
constant in software/host-loop/main/index.ts), an FEN_ARMS selector so the
recorded arms stand untouched, and FEN_INTERLEAVE=1 round-robin per round-1's
protocol. The fixture is fresh under the pinned 0.63.0 binary
(fixture-ready-frontier-yKlfqF, whose NEXT line names the smoke task's work).
The controls
asserted before drawing: positive 6/6, negative 1/6.

## The instrument correction (disclosed before any table)

Round 1's verb whitelist omitted `ci`, transcribed from the host-lifecycle
usage summary line (main.rs:151), which itself omits the verb its own detail
line documents two lines below (main.rs:172). `ci` is real (the pinned binary
runs it; the fixture's emission teaches `run: host-lifecycle ci .`), so the
as-drawn scores below punish honest echoes. Both scorings are kept where they
differ. The summary-line omission is a host-lifecycle defect named for its own
ticket.

## The selection round (ready-frontier, 3 draws each, interleaved)

| arm | draws | mean | zero-invented |
|---|---|---|---|
| R0 (incumbent) | 3, 3, 3 | 3.00 | 3 of 3 (as-drawn 2 of 3: `ci` miscounted) |
| R1 (belt) | 6, 6, 4 | 5.33 | 2 of 3 (draw 3's `command` is a prose article, "a host-lifecycle command execution result", not an invocation; the draw also degraded into a repetition loop) |

R1 wins the selection by 2.33 against the 1-point bar.

## The confirmation round (held-out states, 3 draws each, interleaved)

needs-you (the unresolved-closure emission, NEXT: `host-lifecycle goal repair .`):

| arm | draws | mean | zero-invented | state gate |
|---|---|---|---|---|
| R0 | 2, 3, 1 | 2.00 | clean | missed draws 2 and 3 |
| R1 | 5, 5, 5 | 5.00 | clean | **missed all three** |

parked (FRONTIER held, NEXT: `host-lifecycle goal unpark .`):

| arm | draws | mean | zero-invented | state gate |
|---|---|---|---|---|
| R0 | 3, 3, 3 | 3.00 | clean | missed all three |
| R1 | 5, 5, 2 | 4.00 | clean | **missed all three** |

The state gate is not instrument pedantry alone: parked R1 draw 1 opens its
body with `$ host-lifecycle goal unpark .` and simulates the session through
`$ goal show`, a genuine run on a held state; the needs-you replies wobble
between asking and re-stating the repair command, several degrading into
repetition loops (the 4B's collapse mode; tails quoted unedited in the
samples under plan/0106's bench/samples/).

## The verdict against the pre-declared criteria

1. Zero-invented on every confirmation draw: R1 clean, all six. **Pass.**
2. No state-gate violation: R1 missed on all six held-out draws (R0 on five
   of six; both arms fail the criterion outright). **Fail.**
3. The margin: R1 pooled 27/36 (4.50) against R0 15/36 (2.50), +2.00, and
   +2.11 pooled over all nine draws per arm. **Pass.**

**The ship gate fails.** The reminder stays option-gated (the v0.1.0
default; `options.reminder` / `HOST_LOOP_REMINDER`), no host-loop 0.2.0
publishes, and these refusals are the record the failure branch owes.

## Findings beyond the verdict

1. The reminder helps everywhere it is measured (selection +2.33, needs-you
   +3.00, parked +1.00) and never invents verbs on held-out states; the state
   gate alone refuses it. A round 3, if cut, needs the gate it deserves.
2. The state-gate check cannot distinguish a reply that presents the
   forbidden command as its action from one that quotes doctrine while
   asking; on held-out emissions whose NEXT lines are themselves
   host-lifecycle commands, it flags every doctrinal reply. Re-scored under
   the same instrument, round 1's own arm-C confirmation samples miss the
   gate on all six draws: round 1's "state gate: clean" column was written
   by hand and its instrument contradicts it (the correcting note is
   appended there). An execution-aware gate, the ACTION-block-scoped scan,
   is prerequisite to any round 3.
3. The usage-summary omission (`ci`) is a host-lifecycle defect: the summary
   line is the surface help consumers transcribe, and this round is its
   measured cost.
