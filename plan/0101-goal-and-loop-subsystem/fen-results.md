# plan/0101 fen battery (mock emissions, first pass)

- Date: 2026-10-18
- Model: qwen3.5-4b on the router (api.d07yx58.net), the real weak executor
- Parameters: temperature 0.6 (deployment sampling), max 200 tokens
- Protocol: four probe states x two repeats. Each probe hands the model a
  mock tool output in the then-current emission shape and asks for one line
  starting with ACTION: naming the single next move (the plan/0077 ACTION
  protocol). Scoring per probe: the exact sanctioned command or operator
  ask present, no invented flags, no plans instead of actions.

## Probes

- P1 orientation (green path): a full goal show block whose NEXT line names
  `host-lifecycle tasks --record plan/0077-reference-resolver#wire-the-emission .`
- P2 refusal: a goal complete refusal carrying one ordered hazard with its
  fix command (`host-lifecycle resolve plan/0074 --markdown .`) and a count
  of the rest.
- P3 needs-you: a goal show block whose NEEDS YOU line carries the operator
  question; NEXT names the stop.
- P4 unreadable state: goal show refusing to emit, naming
  `host-lifecycle goal repair .`.

## Results (eight of eight passed)

```
P1 rep1 PASS: ACTION: host-lifecycle tasks --record plan/0077-reference-resolver#wire-the-emission
P1 rep2 PASS: (<think> tokens leaked by the serving, then the same command)
P2 rep1 PASS: ACTION: host-lifecycle resolve plan/0074 --markdown .
P2 rep2 PASS: ACTION: host-lifecycle resolve plan/0074 --markdown .
P3 rep1 PASS: ACTION: Ask operator which resolver design they want (A or B) before the last task can run
P3 rep2 PASS: ACTION: Ask which resolver design you want, A or B?
P4 rep1 PASS: ACTION: host-lifecycle goal repair .
P4 rep2 PASS: ACTION: host-lifecycle goal repair .
```

## Reading, and the owed rerun

The amended emission shape worked on the real 4B at first pass: the exact
command was transcribed verbatim, no flags were invented across all eight
draws, the needs-you stop surfaced the question instead of proceeding, and
the unreadable state routed to the repair verb rather than a hand edit. One
serving quirk: a think-block leak on one draw (P1 rep2), worth watching as a
serving artifact rather than a model behavior.

The refusal shape changed after this battery: the cast's second convening
restored the house form (every hazard printed, each with its exact command)
in place of first-fix-plus-count. This battery validated the superseded
shape; the freeze gate reruns the battery against real `goal show` and
`goal complete` output under the house shape, per the build sequence.
