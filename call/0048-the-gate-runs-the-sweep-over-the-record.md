# call/0048: the gate runs the reference sweep, over the record rather than the working tree

- Status: accepted
- Scope: the `verify` phase's recheck in `host-template/lifecycle.manifest`, host-lint's document walk, host-lifecycle's embedded engine, the upgrade ledger's verify convention
- Date: 2026-07-27

## Context and problem

[plan/0077](../plan/0077-reference-resolver/README.md) shipped a reference resolver and a sweep that nothing invokes. Its adversarial round named that the largest remaining gap: the capability is correct and surfaces nowhere. No lane runs it, no skill calls it, and the verify gate does not know it exists.

The first proposal was to append it to the `verify` phase's recheck in `lifecycle.manifest`, which the tool reads live from the host-template submodule, so a pointer bump delivers it to every adopter with no per-project file to migrate. Because the recheck is an `&&` chain in which any non-zero result breaks the chain, and because the sweep exits 3 over this tree's several hundred advisory references, the proposal carried a shell fragment to tolerate that one code:

    && (host-lifecycle refs --check . || [ $? -eq 3 ])

That fragment is correct POSIX and it was refused. What follows is why, and what replaced it.

## How this was decided

Two review rounds with the five personas, the fifth realized as the real weak model rather than simulated, then a question round in which the operator ruled. Every persona returned wire-with-changes in both rounds; none defended the fragment; none argued for leaving the sweep uninvoked.

The weak-agent probes settled two things and failed at a third, which is recorded because the failure is the useful part.

- **The census captures the agent.** Shown a *green* gate whose tail carried this tree's advisory block, the model abandoned the task it was on and went to remediate references, in both repeats. The words "Advisory: nothing is blocked" were in front of it both times. This reproduces plan/0077's recorded finding: shown a report of hundreds of items, the model acts on them whatever the text says.
- **The blocking half is legible.** Shown a dead pointer, both repeats ran the exact command the output named.
- **The naming probe failed on position, and the failure exposed a second defect.** Four candidate spellings presented as a list, rotated: the model chose the first-listed candidate in one rotation and the second-listed in the other. That is position bias rather than a preference for a word, so the probe settled nothing against [call/0047](0047-the-reproducibility-waiver-is-named-for-its-record.md)'s standard. Worse, the candidate it chose from the second rotation named a quality rather than a thing, which the naming rule forbids, so an unscreened list let the probe hand back a name the rule rejects. Redesigned as a comprehension probe, one spelling per prompt with nothing to compare against, both rule-legal spellings were read correctly in every repeat, and neither invented a third exit code.

## What the rounds found

Four findings changed the design, and each was verified in the tree rather than taken on report.

1. **The proposed verify condition was tautological.** It grepped the fetched template, and `upgrade` refuses to run unless that template is checked out at the target revision, so the condition is a post-condition of the command's own precondition. It can never refuse a false record, and it can never detect a revert. The class is not confined to the new entry: of 49 ledger entries, 30 carry a `verify` and 26 of those grep a file under `host-template/`.
2. **The gate corpus included the working tree.** The sweep walks tracked and untracked markdown alike, so an uncommitted scratch note naming a record that does not exist turns the sweep red, which re-opens the verify receipt, which stops a component release at its first step.
3. **The recheck's other clauses fail open.** host-lint's document walk reads each file with `if let Ok(content)` and no else branch, so a document it cannot read is silently dropped and the run still reports clean. Reproduced: a tracked document carrying a real tell, made unreadable, yields `prose: clean` at exit 0. host-lifecycle's own walk carries the same shape, and two of its call sites turn a failed walk into an empty document set. This is the coverage class plan/0077 spent a milestone closing for one checker, alive in the clauses that actually run.
4. **The ledger's version floor is printed and never enforced.** It is parsed and stored, and nothing ever compares it to the running tool. An adopter who moves the template pointer while pinned to an older tool gets a usage failure that reads as a defect in their documents.

## Decision

1. **The gate calls a mode of the tool, never a shell fragment.** The manifest line stays one verb per clause. The exit partition belongs where the tool's own tests can bite on it rather than in an unlinted string in a config file, and positional exit arithmetic is a trap for whoever extends the chain next, because the next clause appended binds to the wrong command.
2. **The asymmetry is stated with its reason wherever it is read.** A prose warning gates and a reference advisory does not, and the two sit in the same chain. Left unexplained it reads as an inconsistency, and the obvious repair is to tolerate the prose warning too, which would disarm a gate that an entire ledger entry exists to install. The reason is that a prose trope is the author's own text and always rewordable, while only the author knows which tracker a bare number meant.
3. **The gate judges the record; the hook scans the working tree.** A gate that reddens over an uncommitted note asserts something about a record that does not contain the note, which no one can re-derive from any clone. The hook keeps the wider corpus, because catching a document before it is staged is its job.
4. **A walk that cannot read a document says so.** Failing closed is right and blaming the file is not. This applies to every walk in the chain rather than the one that was fixed.
5. **A verify condition that the command's own preconditions make true is not a verify.** The new entry tests a capability of the adopter's own binary, in one command with no shell operators so it survives a non-POSIX shell, and it accepts a tree that the gate would redden, because requiring a clean tree would wedge an adopter whose one dead pointer sits in a record they must not rewrite.
6. **The census keeps a home, away from the gate.** The blocking half reports in the gate; the per-file enumeration answers a question someone asked, so the debt stays visible without ambushing a session that asked something else.

## Consequences

- The reference sweep runs in the `verify` recheck, so a reference naming a record that does not exist re-opens the verify receipt and stops a release at its first step, over tracked documents only.
- host-lint gains a corpus selector and a walk that reports what it could not read; host-lifecycle's embedded engine moves to that release, which closes a divergence in which two engines gave two verdicts over one file while neither named which had spoken.
- The upgrade ledger gains its first entry whose verify tests something the adopter did. The other 26 are a finding of their own and are not swept here; they need a documented map and their own milestone, on the same discipline the append-only exception requires.
- The reference discipline lands in this repository's own operating manual before the entry that ships it is recorded, because an entry whose author never applied it is the defect the upstream seat is worst at seeing.
- Nothing in this decision retires the shell fragment as a technique elsewhere. It is refused for the recheck, where the manifest is the one spine file whose contents are executed and no test has ever executed one.
