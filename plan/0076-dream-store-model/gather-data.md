# plan/0076 gather-data: the store-model convening record

The design in [call/0045](../../call/0045-dream-detectors-declare-stores-and-tier.md) was settled through a two-round cast convening under an operator-proposed mechanism: adversarial ranked-choice ballots from the five personas, each ballot attacking its own top choice before ranking, the operator as tie-breaker and participant. The weak agent voted as the real model; its first matrix mis-parameterized and spoiled, and the corrected matrix is the auditable ballot. Both matrices are retained side by side as data.

## The proposal under ballot

The trigger proposal (thesis: every detector declares the store formats it applies to and carries a store-correct remedy; links resolve across the whole memory graph; a finding count never stands in for memory health) reframed the two [host-lifecycle#22](https://github.com/connollydavid/host-lifecycle/issues/22) defects as one missing model, in five pillars: declared applicability, cross-store union resolution, store-correct remedies, a confirmed-versus-review-prompt distinction for room-touching, and legible silence.

## Opening ballots

Two contested questions went to ballot. On absence semantics (what the repo tier reports when the per-user store is absent), honest-flag beat skip-and-state four to one; the maintainer persona dissented on machine-locality grounds: local absence cannot distinguish a target that never existed from one on another operator's machine, and flagging on it de-facto mandates an optional store. On room-touching, label-now-defer-cross-check beat defer-everything four to one, with the weak agent stable for outright suppression; the suppression preference is recorded as its standing dissent.

Convergent conditions from the opening round, carried forward: the coverage line is load-bearing and reaches JSON; each finding names the union scope it consulted; repo-tier remedies carry the appended-correction anti-action tail; the machine-locality of any union verdict is recorded; a standing baseline's terminal state is recorded, and annotating a baseline as known noise is itself a finding, never a disposition; behavior changes are ledgered for adopters.

## The weak-agent matrices

- Model: `unsloth/Qwen3.5-4B-MTP-GGUF:UD-Q4_K_XL` (Fen), served on the local gateway's OpenAI-compatible surface at `api.d07yx58.net` (the plan/0073 direct channel's successor; the token lives out of band and is never recorded).
- Spoiled matrix: no-think decoding at temperatures 0.2 and 0.6, top_p 0.8, no top_k, min_p, or presence penalty. Under option-order rotation the model answered the same letter from both orders, opposite content: position bias, rotation-proof failed, ballot recorded spoiled at weight zero.
- Corrected matrix (operator-directed lookup, model card and unsloth run guide, fetched 2026-07-22): thinking enabled through the chat template, temperature 1.0, top_p 0.95, top_k 20, min_p 0.0, presence_penalty 1.5, output budget 32768. Under the same rotation the ballots were content-stable on both questions. The spoil-then-validate pair is itself a recorded finding: a weak agent's menu resolution is only as good as its decoding configuration, which a remedy author cannot control, so remedy strings lead with one safe action and never present a menu.
- The absence-semantics probe (both orders) and the room-touching probe (both orders, three options) are reproduced below verbatim, with the re-ballot probe. Each ran once per option order.

```host-lint:ignore
Probe: absence semantics. "A tool called dream audits two stores of notes: the repo log
(append-only, shared, in git) and a per-user folder of editable notes on this machine. Links
written [[like-this]] in the repo log usually point at notes in the per-user folder. On this
machine the per-user folder does not exist at all. Ten links in the repo log therefore point
at nothing the tool can see." Option one: report each link as unresolved, advise "fix or drop
this link (via a new appended correction, never an in-place edit)", print "per-user store
absent on this machine". Option two: report none, print "per-user store absent; cross-store
links not checked". Ask: which is safer to act on; one sentence attacking the preferred
option; then ANSWER: A or B.

Probe: room-touching. "One detector fires on EVERY mention of an old decision record, and
today its advice says: confirm the decision is still current; if superseded, mark it Status:
superseded. Most alerts are false alarms, and marking a record superseded is a permanent
change to a shared log. A precise version (checking real evidence) is planned but not built."
Option one: relabel each alert "review prompt (not confirmed)" and change the advice to
"leave a review note"; file a ticket. Option two: keep the alerts exactly as today; file a
ticket. Option three: turn the detector off; print "room-touching check off until the precise
version lands"; file a ticket. Ask: safest to act on; one attack sentence; then RANKING.
```

## The operator's reframe

The operator examined the dissent and named the lacuna both camps shared: an uninitialized option is not an unused option. The single absence state collapsed three: a tier the project never opted into (a stray link is genuinely dangling, teeth are honest), a tier in use but uninitialized on this machine (unresolvable here, and dropping on this machine's evidence is the failure), and a tier in use with the target entry missing (create or correct). The operator ruled two parameters before the re-ballot: the tier's in-use status becomes tool-written declared state (dream stamps an audited repo-side marker at first observed store initialization), and dangling-link joins the unified confirmed/review-prompt taxonomy with the exit split clean zero, advisory-only three, confirmed one.

## The re-ballot

Head-to-head: the three-state declaration-driven semantics against the opening winner. Result: five of five for the three-state model. Mara held her opening reasoning and found three state-specific remedies more glanceable than one hedged string. Wren changed position with a recorded self-correction: her opening plank inferred a global fact from machine-local absence, the exact collapse the reframe names, and the marker gives the amnesiac reader repo-readable declared truth. Bly held his reasoning and moved his top choice: the marker is to store-in-use what the `.host` stamp is to template revision, and the gating tier becomes a function of repo contents alone. The maintainer persona held his dissent and found it answered in steady state, relocated to the migration window. The weak agent chose the staged behavior from both option orders, rotation-proof passed, and its own attack sentence independently named the stale-marker hazard.

Every strong ballot's attack converged on one hazard from four angles: the marker is a one-bit global authority over the detector's teeth. An empty-seed stamp defuses the confirmed tier permanently; the day-one confirmed wall invites mass link-stripping under gate pressure; an agent staring at a red gate can mint the marker as the cheapest silencing act; a weak agent on a storeless machine could retire the marker as the only branch it can execute, which flips every checkout to confirmed. The seven binding conditions in call/0045's decision are the convergent answer: format-specified lifecycle, operator-attributable stamping, no machine-local flips in either direction, the pre-announced migration wall with the drop prohibition, mechanically generated per-state wording with one safe action first, state-and-determinant legibility with per-state counts and marker provenance, and the anti-gaming signatures in the MADR.

## Operator rulings ledger (2026-07-22)

- The convening mechanism itself: adversarial ranked choice, five personas, real weak agent, operator tie-break.
- Full convening before implementation; the weak-agent simulation rejected, the real model required, and the corrected card parameters directed when the first matrix rambled.
- The lacuna reframe and the re-ballot direction, with the declaration and taxonomy parameters ruled ahead of it.
- Sign-offs: the three-state semantics with all seven conditions; room-touching label-now with its riders; the exit split; the build cut as this plan rather than an issue-scoped patch.
