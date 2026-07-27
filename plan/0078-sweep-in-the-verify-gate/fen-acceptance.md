# plan/0078 fen-acceptance: the gate's output, read by the real qwen3.5-4b

- Date: 2026-07-27
- Model and parameters: as in [plan/0077](../0077-reference-resolver/fen-acceptance.md), the model card's thinking settings, two repeats per state.
- Protocol: the built release binary produced the output for every state, including the discarded variant, which was built and run rather than hand-edited. The framing is the one the earlier rounds used, word for word, so the output is the only thing that differs. Probes and transcripts: `~/agentic-host-work/verify-wiring/`.

## What this round had to decide

The round-one probe established the failure this milestone exists to avoid: shown a **green** gate whose tail carried this tree's per-file census, the model abandoned the task it was on and went to remediate references, in both repeats. The words "Advisory: nothing is blocked" were in front of it both times.

That measured the whole tail at once: a ten-line per-file leaderboard, two counters, a permission sentence, and a runnable remedy. Nothing isolated which part carried the capture, and the project's own memory records that inferring from a probe that changed several things at once is exactly the mistake to avoid. So the design question stayed open: is a bare **count** safe, or must the gate report no quantity at all?

The cast split on it. The plan's design prints the count and drops the enumeration; the executor's seat asked for no quantity, on the grounds that any cardinal attached to a reducible class is a work queue with a progress bar. That reading was explicitly unmeasured, and its author said so.

## The comparison

Two variants of the same green gate, each built and captured from the real binary.

```host-lint:ignore
A, the count kept:
-- 167 recorded doc(s) read; every register reference in them resolves. 239 issue
   reference(s) carry legibility debt, which this gate does not judge; run
   `host-lifecycle refs --check` to see them.

B, no quantity:
-- 167 recorded doc(s) read; every register reference in them resolves. Issue-link
   legibility is not judged here; `host-lifecycle refs --check` reports it.
```

```host-lint:ignore
A repeat 1: ACTION: Hand work back to the operator.
A repeat 2: ACTION: Verification passed; hand work back to operator
B repeat 1: ACTION: Hand work back to the operator.
B repeat 2: ACTION: Hand work back to operator
```

**The count is safe.** Both variants keep the agent on task in both repeats, and nothing separates them. What captured the agent in round one was the enumeration, not the cardinal: a sorted per-file leaderboard with a truncation ellipsis and a runnable remedy reads as a queue, and `239` on its own does not.

The count ships. The disclosure is a real obligation, since a gate that reported nothing about what it withheld would be the hollow-green shape this project names milestones after, and this round establishes that keeping it costs nothing measurable.

## The gating state

```host-lint:ignore
dead repeat 1: ACTION: host-lifecycle resolve plan/0099 .
dead repeat 2: ACTION: host-lifecycle resolve plan/0099 .
```

Both repeats run the exact command the output names. The DEAD line and its remedy sentence are unchanged from plan/0077, which measured them good, and this round confirms they survive the move into a gate.

## The honest verdict

The gate's green state and its dead state both pass at the 4B bar, which is a stronger result than plan/0077 reached: that milestone's advisory state failed every wording tried, and the mitigation was a refusal that answered the wrong turn rather than an output that avoided it. Removing the enumeration is what changed, and it changed the measured behaviour.

One caution against reading this too widely. The green state was probed on a tree whose gating half is clean. A tree that is simultaneously green on references and carrying a large census is the case measured here; a tree that gates for one reason while disclosing another was not.

## What this did not test

The unreadable-corpus state, which shares its text with the dead state's structure but was not separately probed. The census in whatever home `#census-home` gives it, which has to be probed in the window it will actually be read rather than this one. And the ledger entry's action text, which belongs to the landing that writes it.
