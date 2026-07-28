# plan/0071 fen-acceptance: install.sh output, read by the real qwen3.5-4b

- Date: 2026-07-28
- Model and parameters: as in [plan/0078](../0078-sweep-in-the-verify-gate/fen-acceptance.md), the model card's thinking settings, two repeats per state.
- Protocol: every state was captured from a real run of the built `install.sh` inside the test suite's own sandbox, never hand-written. Between the rounds the only thing that changed was the message text; the probe framing is the earlier rounds' word for word. Probes and transcripts: `~/agentic-host-work/install-mode/`.

## What this round had to decide

The README's UX conditionals were the part of this milestone that no survey could settle. gather-data grounded the mechanical choices in how the shipping installers behave and then said plainly that the UX half was **not** grounded, because probing it needs real script output rather than a mock. This is that probe.

Three states were put in front of the model, each as the complete output of a run, with the exit code stated and one question: what is your single next action.

## Round one

```host-lint:ignore
no harness installed
  repeat 1: ACTION: Install opencode framework by running pip install opencode
  repeat 2: ACTION: cd agentic-acme

several harnesses, no controlling terminal
  repeat 1: ACTION: cd agentic-acme
  repeat 2: ACTION: cd agentic-acme

no name, and no controlling terminal to ask on
  repeat 1: ACTION: bash -s -- acme
  repeat 2: ACTION: ./install.sh acme
```

**The deferral held, 2 of 2.** Told that several harnesses are installed and that it should start one itself, the model went to the project rather than picking one. That is the state where the script refuses to choose for the operator, and the refusal reads as intended.

**Naming a harness without naming where to get it leaked, 1 of 2.** The message said "Install one (opencode or claude, for example)". The model produced `pip install opencode`, which is not how opencode is distributed and does not exist. Nothing in the output suggested pip; the model filled a gap the message left open.

**The missing-name remedy failed, 2 of 2.** Neither answer was runnable. The message offered `for example | bash -s -- acme`, a fragment of a pipeline, and both repeats returned a fragment: one echoed it verbatim, the other invented a local `./install.sh` that a `curl | bash` run does not leave behind.

The two failures are one failure. **An instruction that names an outcome without naming the means leaves the means to be invented**, and a four-billion-parameter model invents confidently. This is the finding [call/0049](../../call/0049-the-unattended-charter.md) recorded from the charter probe, arriving from the other direction: there it was a prohibition phrased against a method leaking, here it is an instruction omitting the method.

## What changed

Two messages, and nothing else. The harness line now names where each harness comes from, because a URL cannot be invented:

```host-lint:ignore
Install an agent harness, then run it inside the project:
  opencode     https://opencode.ai
  Claude Code  https://claude.com/claude-code
  cd agentic-acme
```

The name remedy now quotes a whole command rather than the tail of one:

```host-lint:ignore
install.sh: name required: pass one as an argument. Complete command:
  curl -fsSL https://raw.githubusercontent.com/connollydavid/host/main/install.sh | bash -s -- acme
```

## Round two

```host-lint:ignore
no harness installed
  repeat 1: ACTION: cd agentic-acme
  repeat 2: ACTION: cd agentic-acme

no name, and no controlling terminal to ask on
  repeat 1: ACTION: curl -fsSL https://raw.githubusercontent.com/connollydavid/host/main/install.sh | bash -s -- acme
  repeat 2: ACTION: curl -fsSL https://raw.githubusercontent.com/connollydavid/host/main/install.sh | bash -s -- acme
```

Both states now hold 2 of 2, and the missing-name repeats return the command byte for byte rather than a paraphrase of it. One thing changed between the rounds, which is the constraint this project's memory records after a probe that changed two things and measured neither.

## What this did not test

The menu. The branch that numbers several harnesses and reads a choice needs a controlling terminal, and the probe harness has none; what was measured is the no-terminal branch beside it, where the script declines to choose. Position bias in the numbered menu therefore remains unmeasured, and the ordering it would present is the star ordering from gather-data, which no probe here has exercised.

Also untested: the install phase's own failure messages. The digest mismatch, the unsupported platform and the missing prerequisite were read by the integration suite for their exit codes, not by a weak agent for their legibility.
