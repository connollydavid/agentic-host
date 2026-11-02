# plan/0108-cold-adopter-improvements: the cast verdicts, implemented

**Status: cut 2026-11-02, in build** (operator-directed: "consult cast on findings,
and plan improvements in detail"; the three rulings taken at cut: accept-required,
the Fen-grade run in the milestone, the recipe teaching tool-carried).

## The findings (plan/0107's cold run, verified)

1. The recipe shape is missing from every published surface an adopter reads: the
   pin-equality rule (the template ledger holds its distributed tools at their own
   pointers) lives in the template's call ledger, reachable only by reading
   history after a refusal bites. The cold session derived the reference-host
   shape by itself; the next adopter should not have to.
2. The docker-owed path worked as documented; the lanes discharged by local test
   runs at the pins. No change beyond recording.
3. The gates taught mid-run (the refs walk caught a cross-repo citation); no
   change.

Adjacent, from plan/0106's loop runs: the floor model fabricates plan directories
and re-aims goals at them (valid_target accepts the fabrication), and the model
invoked `goal complete` itself in both the loop run and the cold demo, with
nothing requiring the operator's semantic acceptance that plan/0101 built.

## The consult (five seats, adversarial where the seat demands)

- **Bly (adopter, primary)**: the fix must be tool-carried, never doc-carried; a
  doc teaches one adopter, the checklist and the HAZARD teach all of them at the
  moment of need. The recipe shape and the pin-equality rule belong in the
  binary's emission.
- **Orin (maintainer)**: concurs and owns it; the checklist and the HAZARD are
  host-lifecycle's emission, and the entrance README carries the same shape. The
  deeper lesson is his recurring defect: the rule existed but was not reachable
  where it was needed.
- **Wren (executor)**: an accept verb nothing requires is the worst of both; if
  the operator's acceptance matters, the machinery must require it. Pressed the
  governance finding into a behavior change.
- **Mara (operator)**: acceptance is semantic and hers by doctrine (plan/0101
  built `goal accept` for exactly this); the gates prove, the operator accepts.
- **Fen (subject)**: the frontier run proved the path; the floor model has not
  walked it, and the floor model is the bar. The Fen-grade cold run belongs in
  the milestone, after the fixes land so the improved path is what gets walked.

**Operator rulings at cut**: accept-required (the machinery enforces the
operator's seat); the Fen-grade run in the milestone; the recipe teaching
tool-carried plus the entrance.

## The changes

1. **Accept-required** (goal.rs): `goal complete` writes the closure receipt and
   the Status suffix `; complete <date>, acceptance owed` and the fold gains the
   pending state; `goal show` reads `NEEDS YOU: the operator's semantic
   acceptance is owed (goal accept)`; `goal accept` performs the final closure.
   The loop and doors stop at pending-accept by construction (NEEDS YOU
   non-none).
2. **The valid_target fabrication guard** (goal.rs): `goal set` refuses a target
   whose plan README lacks the task structure, naming what was missing.
3. **The recipe teaching** (main.rs + the entrance): the init/scaffold checklist
   carries the two-component recipe and the pin-equality rule; the software
   --check pin-equality HAZARD names the rule and the remedy; the entrance
   README's From-nothing section carries the shape.
4. **One release**: v0.63.0 (adds-flag) through the tool-carried cascade; the
   entrance re-pinned, both lanes receipted.
5. **The Fen-grade cold run**: qwen3.5-4b walks the same one-liner after the
   release; receipts and transcript to plan/0107's bench; findings join here.

## Build sequence

### Accept-required {#accept}

- verify: the fold, the emission, and the repair path tested; cargo test green
- inputs: software/host-lifecycle/main/src/goal.rs

### The fabrication guard {#guard}

- verify: the phantom-dir refusal tested; cargo test green
- depends: #accept
- inputs: software/host-lifecycle/main/src/goal.rs

### The recipe teaching {#teach}

- verify: the checklist and HAZARD texts tested; cargo test green
- depends: #accept
- inputs: software/host-lifecycle/main/src/main.rs

### Release v0.63.0 {#release}

- verify: the cascade green (verify gate, clippy bar, obligations, container
  build, tag), the asset equal to the anchor, the host re-pinned, receipts
  recorded
- depends: #guard, #teach

### The entrance shape {#entrance}

- verify: the From-nothing section carries the two-component shape; both lanes
  green and receipted; the host re-pinned
- depends: #release

### The Fen-grade cold run {#fen}

- verify: qwen3.5-4b walks the one-liner; the artifacts land in plan/0107's
  bench; the findings recorded here
- depends: #entrance

### Records {#records}

- verify: PLAN.md row complete, MEMORY entry, the gate green
- depends: #fen
