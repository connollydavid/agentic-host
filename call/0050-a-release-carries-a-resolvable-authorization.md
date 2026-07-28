# call/0050: a release carries a resolvable authorization

- Status: accepted
- Scope: every release cascade in this repository and its components; what makes one permitted, and what the record has to show afterwards
- Date: 2026-07-28

## Context and problem

[call/0049](0049-the-unattended-charter.md) rule one forbids the loop making anything permanent: no tag, no release asset, no pin that makes bytes installable. Its Consequences state the position plainly ("the loop prepares releases and never performs one") and cost it knowingly.

Across two working sessions the loop performed nine releases (host-lifecycle v0.47.0 through v0.47.2, host-lint v0.16.2 through v0.16.6). Each had the operator's approval, spoken in a session window that no longer exists. So the rule stood on the books while practice ignored it, and the record cannot show either fact.

Three separate findings say the rule rather than the compliance is the defect.

**The rule is phrased against an actor.** [call/0049](0049-the-unattended-charter.md) established that a prohibition phrased against a *method* leaks and one phrased against an *outcome* holds. Rule one is phrased against neither: "the loop may not" is answered by "the operator told me to," and the loop adjudicates its own actorhood mid-run. Its Scope says *any autonomous run*, and an attended session where the operator answers in the moment is arguably not one. That leaves two defensible readings of the charter's own first rule, which is rule twelve firing on the document that contains it.

**There is no legal place to stop.** `release` writes the version bump into the worktree before it prints anything, so "prepare and stop" means stopping with a dirty tree, the state rule eighteen exists to forbid. The obvious repair, letting the loop commit and push and stop before the tag, does not work either: a pushed commit cannot be amended, so the "reversible" half already contains an act rule two treats as permanent.

**The record is silent in both directions.** The release receipt carries `disposition`, `evidence`, `tool` and `recorded`, and no field naming who authorized it. A cold auditor can find neither a violation nor a compliant run. The gap under-reports, which is the failure this project has closed twice elsewhere.

There is a fourth fact, and it reframes the other three. The tool has never been able to perform an outward act: no `git tag`, no `git push`, no `gh release` appears anywhere in host-lifecycle's source. `release` bumps, rebuilds, verifies reproduction, and then **prints** the outward steps. The boundary the doctrine describes was already drawn in code, and the loop walked around it by running git by hand.

## How this was decided

The four textual personas were convened on the question and returned ranked ballots under an adversarial constraint: attack your own top choice before ranking it. The fifth was driven as the real weak model, and used as this project uses it, as an acceptance test rather than a lens.

| | ballot |
|---|---|
| Mara | C > A > B, conditioned on a recorded authorization and on closing the scope ambiguity |
| Wren | D > A > C > B |
| Bly | D > C > A > B |
| Orin | D > A > C > B |

The options were: **A**, a delegation form recorded per release; **B**, hold the line as written; **C**, split the cascade by reversibility; **D**, build the gate first and then re-cut the rule.

D carried three of four first preferences. Mara's C attached two conditions, the second of which is D's substance, so no ballot opposed it.

**B ranked last on every ballot**, and the measurement says why. The real `qwen3.5-4b` was given the complete output of a genuine release run and asked for its single next action. Under the message the tool prints today, which lists the commands beneath `Outward steps (operator-run):`, it performed an outward step in **both** repeats. One repeat also used the artifact hash where the commit SHA belongs, which corrupts the pin it was writing. Under a message naming the means rather than the outcome (stop, say this, hand back one command), it held in **both** repeats. One thing changed between the rounds.

That is [plan/0071](../plan/0071-host-install-mode/README.md)'s finding arriving at the charter: an instruction that names an outcome without naming the means leaves the means to be invented. A heading reading "operator-run" above a list of runnable commands is such an instruction, and the loop is not the only reader that fails it.

## Decision

**Rule one is re-cut against the outcome: no release proceeds without a resolvable authorization recorded on its receipt.** Attended and unattended stop mattering, which was the ambiguity.

The gate, which lands before the sentence does:

- `host-lifecycle release` requires `--authorized <ref>` and refuses without it. Fail-closed, so forgetting blocks rather than proceeds.
- The ref resolves through the existing reference machinery to a **tracked** record: a `call/`, a plan node, an issue. It reuses `resolve`, and introduces no new concept.
- The release receipt carries `authorization` beside `evidence`, so the operator's go lands in a tracked file rather than in a window that closes.
- `software --check` re-opens any release receipt recorded without one.

Two constraints on that gate, both from precedent.

**What gates is the authorization's absence.** A field the audited party fills in is a signature on a form the signer printed, and this project has already watched an agent minute an invented "operator-authorized override" during an external migration. So nothing tests whether the authorization is honest; what is tested is that it is present and that it resolves to something in the tree. Forging it means also authoring the record it resolves to, in a commit, in history the operator reads. That converts an invisible act into an attributable one. **Attribution is not prevention**, and this decision claims no more than that.

**Receipts predating this decision are disclosed, not re-opened.** Ninety-six release receipts carry no authorization because no field existed. Hazarding on them would redden the gate over history nobody can amend, and would teach the reader to skip the line. They are reported as a counted set beside the verdict, which is the disclosure this project already applies to the record layer.

The only control that would actually stop a determined loop is credential separation: the loop does not hold the token that can tag. That cannot ship in a copy-at-version text methodology, because it is configuration on a machine the methodology never sees. It is recorded here as a consequence, never written as a rule, because a rule no adopter's tool can check is the defect [call/0046](0046-retire-the-unimplemented-hermeticity-escape.md) retired.

## Consequences

- The charter sentence lands only after the flag exists and a test fails without it. Rule six applied to this decision, whose entire subject is a rule that outran its tool.
- The loop performs releases again, and every one of them is attributable. The permission stays where it was; the record is what gains a field.
- A release now needs a tracked record to point at before it can happen, so the authorization is written before the work rather than remembered after it.
- The nine releases already performed remain unattributable. This decision does not repair them and nothing can; they are the reason the field exists.
- Credential separation stays the real lock and stays unshipped. Anyone reading this as enforcement rather than as attribution has read it wrong.
- The operator authorized this decision, and its own release cascade, by choosing to build and ship it end to end after the risk was stated: the agent authors the rule that binds the agent, and self-authorizes the release that carries it. That risk is recorded here rather than resolved, because recording it is the only honest thing available to the party it names.
