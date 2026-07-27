# plan/0078 the sweep runs in the verify gate, and the clauses beside it stop failing open

Decided by [call/0048](../../call/0048-the-gate-runs-the-sweep-over-the-record.md), after two cast review rounds and a question round. Closes the gap [plan/0077](../0077-reference-resolver/README.md)'s adversarial round named as its largest: the reference sweep is correct and nothing invokes it.

## Why

The `verify` phase's recheck is the gate that re-derives a `done` receipt, and it is step one of `host-lifecycle release`. It chains `validate`, `prose` and `reconcile`. plan/0077 hardened a fourth checker against a defect none of those three is hardened against, and then left it unwired.

So the accurate statement of the gap is not that a good tool goes unused. It is that **the gate's existing clauses can report clean over a corpus with a hole in it, and the one walk that was fixed is the one nothing runs.** Reproduced: a tracked document carrying a real tell, made unreadable, yields `prose: clean` at exit 0.

Two more defects sit on the same path. The document walk includes the working tree, so an uncommitted note blocks a release over a file no clone contains. And the ledger entry that would ship any of this would, under the convention the ledger already uses, carry a verify condition its own command's precondition makes true.

## What the convening measured

Real qwen3.5-4b, two repeats per state, on output the built binary produced.

- Shown a **green** gate whose tail carried this tree's advisory census, the model abandoned its task to remediate references, in both repeats. The gate must not print the enumeration.
- Shown a **dead pointer**, both repeats ran the exact command the output named. That text is measured-good and is kept byte for byte.
- The naming probe failed on position and was redesigned as a comprehension probe. Both rule-legal spellings read correctly; neither invented a third exit code.

## Build sequence

Three landings, because pre-existing fixes, a behaviour change, and a template revision have different blast radii. Landings that share a blast radius may merge; these do not. Each ends in something recorded.

Prerequisite, ahead of landing one: the owed ledger entry for the host-lint v0.15.0 pin, which reserved two words in the bare-argument position and made the canonical build produce a second binary, and which shipped as a bare pointer bump with no entry.

**Landing one: the walks tell the truth, and a verify can fail.**

### A walk reports what it could not read {#walk-reports-what-it-could-not-read}
- verify: a tracked document made unreadable turns `prose` non-zero with a line naming the document, rather than reporting clean; the same holds for host-lifecycle's own walk; a walk that fails outright never becomes an empty document set
- depends: none

### The gate reads the record, the hook reads the working tree {#corpus-selector}
- verify: the document walk takes a corpus selector; an untracked file carrying a tell is reported by the hook and ignored by the gate path; the walk exists once, so no second walk drifts from it
- depends: #walk-reports-what-it-could-not-read

### A directory argument is honoured or refused {#argument-is-honoured}
- verify: `--all <dir>` and `--docs <dir>` audit the named directory rather than the tree resolved from the working directory, or exit as a usage error; a fixture under a different root proves which tree was read
- depends: none

### The printed remedy names something real {#remedy-names-a-real-reference}
- verify: no emission attaches a guessed repository to a bare issue number, and none prints a placeholder shape either; a test asserts the remedy names a reference that exists in the tree, and mutating it fails that test
- depends: none

### The recheck runs, or says it could not {#recheck-runs-everywhere}
- verify: the recheck chooses its shell per platform rather than assuming one, and a shell that cannot be spawned reports that it could not run, distinctly from a condition that did not hold
- depends: none

### A capability answers for itself {#capability-probe}
- verify: one command with no shell operators reports whether the running binary carries a named capability, reads no tree, refuses an unknown name, and draws from the same constant the feature is gated on; the engine version appears wherever the naming and prose surfaces speak
- depends: none

### The version floor is enforced or the deferral is recorded {#floor-enforced-or-owed}
- verify: either a tool below an entry's floor is refused at record time with the floor named, or an issue records the deferral and the ledger says the floor is advisory
- depends: #capability-probe

### The embedded engine matches the pinned one {#engine-bump}
- verify: the vendored bundle is cut and published, the embedded revision moves to the released one, and one tree yields one verdict from both surfaces where two verdicts were demonstrated
- depends: #corpus-selector, #argument-is-honoured, #remedy-names-a-real-reference, #capability-probe

**Landing two: the gate mode.**

### The two corpora in the model {#spec-the-two-corpora}
- verify: the spec models both walks, the corpus each judges, and the gate's exit partition, so an obligation can bite on a verdict claiming more than its walk read; `allium check` and `analyse` exit 0
- depends: #engine-bump

### The gate mode {#gate-mode}
- verify: exit 0 with no blocking finding, advisory included; exit 1 on a dead pointer, an unreadable document, or a corpus the walk could not produce, each with a line naming its own cause; the advisory is counted and never enumerated; the coverage line names which corpus it read; the empty-corpus case is specified rather than inherited
- depends: #spec-the-two-corpora

### The composition is executed {#composition-test}
- verify: a fixture host with a `done` verify receipt and a dead pointer re-opens the receipt under `software --check` and exits non-zero; this is the first test that executes a manifest recheck string
- depends: #gate-mode

### The recheck stays cheap {#cost}
- verify: the budget is stated before the measurement; the chain is measured before and after; if the budget is exceeded the disposition is recorded rather than noted
- depends: #composition-test

### The weak agent stays on task {#fen-acceptance}
- verify: two repeats per state on real output; the count-only gate is compared against a gate printing no quantity, and the comparison decides which ships; a spoiled probe is recorded as protocol data
- depends: #gate-mode

### The gate ships {#release-the-gate}
- verify: released by the tool-carried sequence, re-pinned, and the binary on the path is the released one
- depends: #cost, #fen-acceptance

**Landing three: the revision adopters receive.**

### The manifest calls the mode, in a vocabulary every platform runs {#template-wiring}
- verify: the recheck line is one verb per clause with no exit arithmetic; a comment above the stanza states why a reference advisory passes while a prose warning gates; and the four `test -f` conditions become portable, since a shell branch alone leaves them failing wherever `test` is not a builtin. `host-lifecycle version .` is an exact stand-in for the two `.host` conditions (exit 1 with no readable stamp, 0 with one); the two `.host-software` conditions need one, and inventing a verb for them is a decision this node owns
- depends: #release-the-gate

### The spine says where it runs {#spine-bullets}
- verify: the existing reference section names the gate, the corpus it judges, and the asymmetry with its reason; an adopter who reads only the spine learns that something gates and what
- depends: #template-wiring

### The entry an adopter can fail {#ledger-entry}
- verify: the condition is the capability probe, and a tree that SHOULD fail it does, meaning an environment whose binary predates the floor rather than a tree carrying a dead pointer, which must record as applied; the action text opens with the two facts a cold reader needs first
- depends: #spine-bullets

### The census has a home {#census-home}
- verify: the enumeration is reachable by one documented command and appears in no gate path; the chosen home is probed in the window it will actually be read
- depends: #gate-mode

### It is applied here before it is shipped {#walk-it-here}
- verify: this repository's own operating manual carries the reference discipline, the pending entry is recorded honestly rather than on a condition its own precondition satisfies, and the new entry is applied here
- depends: #ledger-entry

### The record {#record-the-outcome}
- verify: the PLAN.md row and the MEMORY.md entry are written and pushed, each in its own commit
- depends: #walk-it-here

## Out of scope, recorded so it is not assumed

- **The ledger's verify convention.** Of 49 entries, 30 carry a condition and 26 grep the fetched template, which `upgrade` requires present before it will run. Those cannot refuse a false record nor detect a revert. This milestone fixes the shape for its own entry and sets the precedent; sweeping 26 shipped entries needs a documented map and its own milestone, on the discipline the append-only exception requires.
- **The remaining findings of the FFmpeg pack review**, which stay with their own milestone: the pack here is a skeleton and nothing in it is calibrated.
- **A fix flag for the advisory half.** plan/0077 refused one because only the author knows which tracker a bare number meant, and that refusal stands.
