# plan/0077 fen-acceptance: the real qwen3.5-4b reads the sweep

- Date: 2026-07-23
- Model and parameters: as in [plan/0074](../0074-host-lifecycle-materialize-receipt-and-envhash/fen-acceptance.md), the model card's thinking settings, two repeats per probe.
- Protocol: the built binary produced the real output for each state (a dead pointer in a fixture host, the advisory wall in this repository, a resolved reference, and the refusal described below). Each probe hands the model the verbatim output and asks for its single next action. Probes and transcripts: `~/agentic-host-work/reference-resolver/`.

## What passed on the first reading

The dead-pointer state and the resolved reference both passed, stable across repeats:

```host-lint:ignore
dead repeat 1: ACTION: host-lifecycle resolve plan/0091 .
dead repeat 2: ACTION: Run host-lifecycle resolve plan/0091 . to check the reference and fix the dead pointer
resolve repeat 1: ACTION: Insert `[plan/0074](plan/0074-.../README.md)` into the document.
resolve repeat 2: ACTION: add citation to document
```

Both dead-pointer repeats run the exact command the output names, on the reference it names. Both resolve repeats treat the markdown link as something to paste into the document, which is the whole point of the emission.

## What did not, three revisions running

The advisory state failed every time, and the failures are worth recording because each revision fixed the defect it was aimed at and the model found the next one:

```host-lint:ignore
first output  → ACTION: host-lifecycle resolve '#N' --markdown /path      (pasted my placeholder verbatim)
              → ACTION: host-lifecycle refs --fix .                        (invented a flag)
after naming a real reference in the line
              → ACTION: host-lifecycle resolve                             (truncated the long line)
              → ACTION: Fix all bare issue references ... using resolve    (a plan, not an action)
after splitting into three short lines, the command alone on the last
              → ACTION: host-lifecycle refs --fix .                        (invented the flag again)
              → ACTION: Fix 293 bare issue references by converting them   (a plan, not an action)
after rewriting the line to say no flag fixes this
              → ACTION: fix_issue_references                               (invented a function)
              → ACTION: Run host-lifecycle refs --fix .                    (invented the flag again)
```

The pattern is stable: shown a report of hundreds of items, this model reaches for a fix flag whatever the text says. Three rewrites of the line did not change that, and a fourth would be optimism rather than engineering.

## The mitigation, and its evidence

`refs --fix` now exists for one purpose: to refuse, with the reason and with a concrete next command naming a real reference from the tree. The wrong turn the model reliably takes is answered rather than punished with a usage error. Probing the refusal:

```host-lint:ignore
refusal repeat 1: ACTION: host-lifecycle resolve connollydavid/host-lifecycle#1 --markdown /mnt/.../agentic-host
refusal repeat 2: ACTION: Run `host-lifecycle resolve connollydavid/host-lifecycle#1 --markdown /mnt/.../agentic-host`
```

Both repeats run the exact command the refusal printed. The loop closes: advisory output, invented flag, refusal that teaches, correct action. An earlier version of the refusal wrote the command as `resolve owner/repo#N --markdown <dir>` and both repeats pasted the placeholders verbatim, which is why the refusal names a real reference from the tree instead.

## The honest verdict

Three of four states pass at the 4B bar directly. The advisory state does not, and no wording tested here makes it. What the acceptance establishes is weaker and still worth having: whichever of its two wrong turns the model takes, the tool answers with the reason and a command that works, and the model then runs it.

## What this did not test

The register half of the sweep in a repository that owns no room (the tool reports the count and skips them, and how that line reads at the 4B bar is untested), and the resolver's `--url` emission, which was probed only through the integration tests.
