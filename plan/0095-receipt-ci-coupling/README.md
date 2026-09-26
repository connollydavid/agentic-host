# plan/0095 receipt-ci-coupling: a lane's outcome enters the receipts

**Status: cut, design-only, go recommended** (operator-directed "let's do the
work" on the named next cut). The design record starts from
[connollydavid/host#21](https://github.com/connollydavid/host/issues/21), whose
measurements are the problem statement: an adopter's reproducibility lane failed
on 64 of 67 runs over two and a half days while every local gate stayed green, a
component with no spec carried no CI obligation at all, and three hashes
described one component with only two agreeing; a release input no receipt
could vouch for. This session supplied three live instances in the forge itself:
v0.54.3 and v0.54.4 shipped with red CI, and the red sat outside every receipt.

## Scope

Design only, the plan/0075 pattern: the tool boundary against the existing
receipt and verify machinery, the receipt shape, and a go or no-go. The build
milestone is cut only if this design survives review; the operator rules on that
cut.

## The designed resolution

**D1. The receipt cites the run; verification splits by network truth.** A new
receipt phase `ci`, one per repository and lane:
`[receipt "ci" "<repo>/<lane>"]` carrying `evidence = <run-url>`,
`revision = <head-sha>`, and `conclusion = success|failure`, authorized per
call/0050. The writer runs where network exists: the forge's own CI records its
conclusion after the lanes, and `host-lifecycle ci --record` records it locally
on demand. The reader is offline and always runs inside `software --check`: it
judges the receipts, never the network; every lane declared at the pinned
revision must carry a receipt whose revision matches the pin and whose
conclusion is success. This is upstream-drift's own split applied to outcomes:
the fetch happens in the workflow, the judgment happens offline, and no offline
gate depends on a credential.

**D2. Absence fails; discovery is mechanical.** Lanes are discovered from the
tree (`.github/workflows/` at the component and the host; name-presence), and
the receipt provides the discharge. A discovered lane with no receipt at the pin
is a HAZARD (`declared, never discharged`), so a repository with no runs reads
red the honest verdict, and a hand-typed lane list is never needed. The
pairing is the spine's own rule in two parts: name-presence is not discharge.

**D3. The per-turn duty is a spine clause, at its own layer.** The manual gains:
before a turn reports done, the default branch's most recent runs are read, and
every non-green conclusion is fixed in that turn or receipted as a blocker
carrying the run URL. The gate clause judges the pin's revision; the manual duty
watches main. The two layers are stated separately so neither inherits the
other's blind spot.

**D4. Run-anchored re-derivation.** `obligations --rederive --record-digests`
and `software --verify-build` record the discharging run alongside the digest,
and `software --check` reports "reproduced on the pinned host, run 35454897584".
The adopter's chain closed exactly once and its only durable evidence was a run
URL no receipt held; this closes that.

**D5. The two documentation gaps.** The `[software]` `toolchain` key is
documented as a digest-pinned container image (a target triple is the natural
misreading, and the cost is a lane that never runs). A component with no spec of
any kind states the absence explicitly in the recipe, and `software
--check` prints the named line; the absence is written down, and the rule leaves silence for nobody.

## The cast consult

- **Bly, the cold auditor**: the receipt must be checkable with no network and
  no history; the run URL is printed for the one-command read-back, and absence
  HAZARDs so silence never reads clean. Bly's fear; a hand-typed lane list
  going stale; is answered by D2's tree discovery.
- **Orin, the methodology maintainer**: the duty is written once in the manual
  and the receipt shape is versioned with the template; adopters receive it
  through a ledger entry keyed to the template commit. D5's gaps are his to
  close in the same landing.
- **Fen, the weak executor**: recording must be one command whose output names
  the next move, and the offline judge needs no credentials; a token-dependent
  gate would exclude Fen's local runner. D1's split is what makes that hold.
- **Mara, the human operator**: trust but verify cheaply; the per-turn read is
  one command and every HAZARD carries the run URL, so triage is one click.
- **Wren, the executor**: the loop needs a terminal state; every declared lane
  green at the pin is checkable, not aspirational.

## The adversarial pass

- *"The receipt can lie."* call/0050's answer holds: forging means authoring a
  run URL that does not exist on the forge, the read-back is one command, and
  the authorization field makes the claim attributable. The receipt cites; the
  forge is the truth.
- *"The gate's verdict becomes environment-dependent."* The #23 lesson, answered
  by D1's split: the offline judge reads receipts only, so the verdict is
  deterministic on every machine; the network refresher is a separate, disclosed
  surface.
- *"A fresh clone goes red."* It does, until CI runs on the pin; which is the
  design working: absence is the finding. The remedy line names the command that
  records the run outcome once the run exists.

## Go/no-go

**Go.** The three asks sit inside the existing receipt and verify machinery, the
offline/online split follows the house's own upstream-drift pattern, and the
session supplied three live instances of the gap. The build milestone
(host-lifecycle: the `ci` receipt phase, the discover-and-judge clause, the
run-anchored evidence; host-template: the manual duty, the ledger entry, the two
doc gaps) is recommended for cut on the operator's ruling.
