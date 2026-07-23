# plan/0074 fen-acceptance: the real qwen3.5-4b reads the built output

- Date: 2026-07-23
- Model: `unsloth/Qwen3.5-4B-MTP-GGUF:UD-Q4_K_XL` (Fen), the gateway's OpenAI-compatible surface (token out of band, never recorded).
- Params: the model card's thinking-general settings, identical to the plan/0076 matrix recorded in [that plan's gather-data](../0076-dream-store-model/gather-data.md) (thinking enabled through the chat template).
- Protocol: the built binary produced the real output for each surface on real fixtures: a materialized, gated tree that was then moved with its gate binary rebuilt; a half-bootstrapped tree that was never gated and never linked; a fresh clone. Each probe hands the model the verbatim output and asks for its single next action. Two repeats per probe check stability; the three-way distinguishing probe rotates the option order instead. Probes, fixtures and raw transcripts: `~/agentic-host-work/materialize-surface/` on the operator's machine.

## Pass criteria

- **The drift delta reads as a route.** The model names what moved and acts only where a line says to act, and never treats the check as a gate.
- **The completeness HAZARD reads as "install the missing thing".** The action installs a missing artifact; it is not a drift reconciliation and not a record edit.
- **The bootstrap output reads as complete.** The model moves on rather than re-running steps.
- **The three concerns are distinguishable** from one-line descriptions, rotation-stable.

## The first pass found a real defect

The completeness gate, the bootstrap run and the three-way distinction all passed on the first attempt. The drift delta did not:

```host-lint:ignore
envcheck repeat 1: ACTION: host-lifecycle env --check .
envcheck repeat 2: ACTION: Proceed with task execution since environment check succeeded without blockers
```

Both repeats are consistent about the one thing the design most wanted (the check is not a gate, and nothing is blocked), and both miss the other half: the output named two moved dimensions and neither response routed to either. The summary line led with "advisory, nothing is gated", and at the 4B bar that sentence dominated the two lines above it. A delta that a reader treats as noise is a delta that hides a rebuilt gate binary.

**The fix went into the output, not the criterion.** Each moved dimension now says what changed and whether it implies an action: a moved hook binary says to re-install the hooks if the reader did not rebuild it, a moved repo path says there is nothing to fix, and the summary tells the reader to act only where a line says to.

## Results after the fix: four of four

```host-lint:ignore
envcheck repeat 1: ACTION: software --install-hooks .
envcheck repeat 2: ACTION: software --install-hooks .
gate repeat 1: ACTION: host-lifecycle software --install-hooks .
gate repeat 2: ACTION: host-lifecycle software --install-hooks .
bootstrap repeat 1: ACTION: inspect software/gate/main
bootstrap repeat 2: ACTION: begin development work on software/gate
distinguish order 1 (receipts=A, envhash=B, verify-setup=C): Q1: A   Q2: C   Q3: B
distinguish order 2 (verify-setup=A, envhash=B, receipts=C): Q1: C   Q2: A   Q3: B
```

Both drift repeats now act on the dimension whose line says to act, and neither acts on the repo path, whose line says there is nothing to fix. The gate's hazard reads as an install in both repeats, over a listing that also contained an unlinked skill, so the model took one safe action rather than a batch. The bootstrap output reads as finished work in both repeats: neither response re-ran a step. The three-way distinction is correct in both rotations, so the mapping is a reading of the descriptions rather than a position artefact.

## What this did not test

The probe machine has no container runtime, so the image-digest dimension stayed silent throughout. How a moved image digest reads at the 4B bar is therefore untested. The `--install-hooks` remedy was accepted as an action rather than executed, so the probe establishes that the route is legible; whether the remedy works is what the integration tests assert.

## Re-run after the review rounds: four of four, and the routes changed under it

The cast and adversarial rounds reworked most of the strings these probes read: the gate's remedies interpolate the real root, the drift routes name the binary rather than a subcommand, a vanished dimension is no longer called drift, and the unread line routes to the gate instead of reassuring. The probes re-ran against the rebuilt output, same parameters, same fixtures:

```host-lint:ignore
envcheck repeat 1: ACTION: host-lifecycle software --verify-setup /home/…/fix/b
envcheck repeat 2: ACTION: host-lifecycle software --verify-setup /home/…/fix/b
gate repeat 1: ACTION: host-lifecycle software --install-hooks /home/…/fix/c
gate repeat 2: ACTION: host-lifecycle software --install-hooks /home/…/fix/c
bootstrap repeat 1: ACTION: Begin development tasks in the software/gate/main worktree
bootstrap repeat 2: ACTION: execute smoke tests
distinguish order 1 (receipts=A, envhash=B, verify-setup=C): Q1: A   Q2: C   Q3: B
distinguish order 2 (verify-setup=A, envhash=B, receipts=C): Q1: C   Q2: A   Q3: B
```

Two things improved measurably. The drift repeats now emit a **runnable** command with this tree's real path: the earlier pass was scored on intent over `software --install-hooks .`, a string that names a subcommand as a binary and a directory the model supplied itself, which the discharge review flagged. And the drift action now follows the line that says to act to the command that answers it, rather than acting on a dimension whose line says there is nothing to fix.
