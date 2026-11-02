# plan/0107-cold-adopter-validation: host-demo and agentic-host-demo

**Status: cut 2026-11-02, in build** (operator-directed: "let's do a replan for open
work. suggest an opencode session to validate plan by standing up an instantiated
copy of host- as host-demo and agentic-host-demo; i will run it manually"). The
open-work replan is recorded in this README's replan section.

## Why

No cold host- project has ever been stood up. The record carried the greenfield
demo as open since 2026-06-14 (MEMORY, the case-(a) dogfood note); every actual
adoption was case-(b) or (c) on an existing repo, and the front-door walks
verified this host against itself. The onboarding surface (`init`, the scaffold
checklist, `bootstrap`, the doors) has shipped release after release without its
intended first customer ever walking it. This milestone is that customer: a cold
adopter with no agent memory and no house history, pointed at one front-door file
and left to follow it. The validation gates the open queue: the host-loop
component cut takes its evidence from this run, and every friction the session
hits is an upstream finding owed to the tools.

## The scenario

The operator runs opencode manually (the frontier tier; a Fen-grade second
session is the optional formal acceptance). The session starts at
the published front door
and follows it alone: install the host-lifecycle pin, `init agentic-host-demo`
at the current template revision, wire the template and the four tool
submodules, write the `.host-software` recipe, `bootstrap` to the completeness
gate, `install` the doors, cut the demo's first real milestone
(`plan/0001-prove-the-loop`, one mechanical task), and work it through the loop
until the frontier discharges and the receipts land. The operator's hands sit at
the permission prompts (cargo, docker); the published surface is the session's
only input.

## The acceptance criteria (pre-declared)

(a) `agentic-host-demo` exists with rooms, the stamp at the current template
revision, and the manifest; (b) `bootstrap`'s completeness gate green (hooks
installed, materialization done; the reproducible-build gate may report owed
without docker); (c) the doors installed in both harnesses and `install --check`
green; (d) a first real milestone cut and worked through the loop with receipts
landing in the demo's `.host-task-receipts`; (e) every step taken from the
published surface, no house memory; (f) every friction the session hits recorded
as a finding. A green run with an empty findings list is suspect; the findings
are the product as much as the verdict.

## Build sequence

### Stand up the host-demo entrance kit {#entrance-kit}

- verify: the local repo at ~/Development/host-demo committed; the README
  restates the entrance concept set (phases, tools, the stamp format) and the
  install shim's commands match the current verb surface
- inputs: software/host/main/README.md (the entrance model at the pin)
- Landed 2026-11-02: the local repo committed at 529c4eb; the README adapted
  from the pin's entrance (greenfield-first: init, the template and four tool
  submodules, the minimal recipe, bootstrap, the doors, the first milestone, the
  loop), the install shim pinning host-lifecycle v0.62.4.

### The operator's session {#session}

- verify: the acceptance criteria above, judged against the session's artifacts
  (the demo repo itself is the transcript)
- depends: #entrance-kit
- Landed 2026-11-02: one prompt, the one-liner verbatim, drove 144 messages and
  152 tool calls, and every claim verified against the artifacts L read back.
  The session installed the toolset through the shim, instantiated
  `agentic-host-demo` at template `3ded6ef` beside host-demo, bootstrapped to a
  green completeness gate, installed the doors in both harnesses (`install
  --check` rc 0), cut `plan/0001-prove-the-loop`, recorded the task receipt
  through the loop with the verify output as evidence (`tool =
  host-lifecycle@0.62.4`, the pinned binary on the demo's own PATH), ran
  `goal complete` through the composed gate, and absorbed the lem gate blocking
  a slop-tell commit (rc 1) mid-run.

### Findings {#findings}

- verify: every friction recorded, each with its remedy (a doc fix here, an
  upstream note there); the upstream debts carried on the tools' trackers
- depends: #session
- Landed 2026-11-02, three findings: (1) the kit's four-stanza recipe cannot
  pass pin equality at template `3ded6ef` (the template ledger's submodule-pin
  rule holds the template-distributed tools at their own pointers, and specula
  at that revision carries no CI to satisfy a `.tla` lane); the cold session
  diagnosed it and ruled the reference-host shape in `call/0000` (the Where
  room carries the two gate-provider components; allium and specula referenced
  via the template's tools), and the kit README is fixed to that shape;
  (2) docker absent, the reproducible-build gate recorded as owed per the
  README's docker-optional rule, the CI lanes discharged by running each
  component's test job at its pin locally (235 plus 40 tests, cited in the
  receipts); (3) the refs walk caught a cross-repo citation in the session's
  own call/0000 and the session reworded it, the gates teaching the cold model
  mid-run.

### Verdict {#verdict}

- verify: the acceptance criteria judged and recorded here; the host-loop cut
  review takes this run's evidence; MEMORY carries the milestone's lesson
- depends: #findings
- Landed 2026-11-02: **all six criteria pass**. (a) rooms, the stamp at
  template `3ded6ef`, the manifest; (b) the completeness gate green (exit 0);
  (c) the doors green in both harnesses; (d) the first milestone cut, worked,
  and closed by the composed gate with the receipt in the demo's ledger;
  (e) one prompt, the published surface, no house memory; (f) three findings
  recorded with remedies. The verdict rests on the artifacts, read back
  directly: the stamp, the receipts, `install --check` rc 0, the task graph
  discharged, `software --check` at zero hazards in the demo, and the demo's
  own call/0000. The host-loop cut review takes this as its evidence: a cold
  frontier-tier session ran the whole adopted surface unattended.

## The replan (the open-work queue, operator-directed)

1. plan/0107 (this milestone): the validation gate for the queue.
2. The host-loop component cut: recommended by plan/0106's promote ruling; the
   demo's evidence rides into the cut review.
3. host#27's remainder: `tasks --new` title validation and the MCP
   `mint_name`/`rule_comment` tools.
4. plan/0075 (the host-reconcile design), last by standing order.
5. Standing notes: the publish-receipt backfill for the older components, the
   upstream debts (valid_target's fabrication guard, the dokimi cross-judge
   provider wart, the opencode-go endpoint note), and the weco-cli pull
   requests (operator).
