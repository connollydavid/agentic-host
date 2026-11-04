# plan/0110: the doctrine reminder rides the context hook

**Status: cut 2026-11-04, in build** (the operator's go on the Q&A round's
recommendations; the open review item plan/0109 left). The finding it answers
is measured: under the native coordinator the 4B drifts off the doctrine after
kickoff (their continuation template carries the objective but drops the
exemplar block), which produced a wrong-ledger receipt and a
reviewer-accepted false stop; the plan/0106 A/B had already measured the
exemplar as load-bearing per turn under our own controller.

## The design

A reminder belt in host-loop that injects the compact doctrine tail (the
never-invent rule, the exact `tasks --record ... --evidence` command, the
NEEDS YOU rule) into the model's context near the tail, before each request,
**without persisting a message and without admitting a turn**: the
`ctx.session.hook("context", ...)` mutation surface, the exact mechanism the
native goal plugin itself uses for its post-compaction objective reminder
(splice near the tail; the cached prefix stays warm; the reminder stops once
a continuation re-carries the doctrine). This answers the plan/0109 caveat
head-on: the reminder is not an admission and never wakes the session; it is
context, not a driver.

Guardrails: the reminder fires only while the native goal is active; it is
suppressed when the recent window already carries the record command (no
stacking); it is disabled by default until the A/B confirms it (the plugin
entry's `options.reminder` or `HOST_LOOP_REMINDER` enables it), per the ship
gate doctrine.

## The A/B protocol (pre-declared, the plan/0100 shape)

Subject qwen3.5-4b on rope, the existing rubric (six mechanical points, the
zero-invented hard gate). Selection on the ready-frontier state: R0 (no
reminder, the shipped default) versus R1 (reminder on), three draws each,
interleaved. Confirmation on the held-out needs-you and parked states with
the winner, pre-declared criteria: R1 must hold zero-invented on every draw,
violate no state gate, and beat R0's pooled mean by at least one point. Ship
gate: on confirmation, the reminder becomes the default and host-loop ships
0.2.0; on failure, it stays option-gated and the refusals record.

## Build sequence

### The reminder belt {#belt}

- verify: the context-hook reminder implemented with its guardrails; the
  suite extended (injection when active, suppression when the window carries
  the command, silence when paused or absent or disabled); node --test green;
  the spec gains the prose guarantee DoctrineRidesContext (no new obligations
  beyond the suite's tests)
- inputs: software/host-loop/main/index.ts, suite.test.ts, host-loop.allium

### The A/B {#ab}

- verify: the selection and confirmation rounds run on the real 4B with the
  pre-declared criteria; tables in this plan's bench
- depends: #belt
- note: hour-scale draws; the kit is the plan/0106 one extended with the
  reminder arm

### Ship or record {#ship}

- verify: the verdict recorded; on confirmation host-loop 0.2.0 publishes
  with the reminder default-on; otherwise the option stays and the refusals
  land here
- depends: #ab

### Records {#records}

- verify: the PLAN.md row, MEMORY, the gate
- depends: #ship
