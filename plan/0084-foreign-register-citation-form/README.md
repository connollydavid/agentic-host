# plan/0084 foreign-register citation form: a citation of another project's register names its repository in a link

Closes the open half of [connollydavid/host#19](https://github.com/connollydavid/host/issues/19), the limitation [plan/0078](../0078-sweep-in-the-verify-gate/README.md) carried as "carried, not closed" and the template's `GATE-refs-in-verify` ledger entry records as a known limit. Both reported halves were fixed in host-template `79c0b71`; what stayed open is that no form the sweep accepts exists for citing a record that lives in another project's register.

## Why

The sweep reads `plan/NNNN` and `call/NNNN` as references into the local rooms wherever the token appears, link text and link target included. The issue's four-form table is the measured statement: bare prose, a prose qualifier (`agentic-host call/0039`), and a markdown link to the other repository's blob URL all report DEAD; the one non-gating form is a code span, which marks an example rather than a reference and renders as literal text. The methodology's own attribution convention ("Recorded as agentic-host plan/0077", six times in the template's upgrade ledger) is flagged by the rule it documents whenever the ledger is swept, which is why the ledger sits outside the sweep and, one list serving both checkers, outside the prose gate with it.

Measured 2026-09-05 against the pinned v0.50.0 source: the six ledger citations are the live population and all are prose form inside the excluded record layer; zero link-form citations exist in any tracked document. The accepted form therefore lands with no remediation wall: it is new capacity, not debt collection, the shape plan/0077's issue half faced with its 374 bare numbers.

Sequencing, operator-approved: this lands before [plan/0079](../0079-spine-is-a-rendered-artifact/README.md) starts its build. The spine rewrite is the form's biggest consumer (the `STRUCTURE.md` provenance citation dropped in the host#19 fix can return as a real citation), and plan/0079 reworks the same verify recheck this gate lives in.

## Decision

The accepted form is link-anchored: a `plan/NNNN` or `call/NNNN` reference inside a markdown link whose target is an absolute forge URL naming the cited record (the path segment `{room}/{number}`) under a repository other than the local origin. The sweep accepts it as a citation, reports it in a counted disclosure, and never gates it.

Boundary cases, each settled in the design:

- the URL's repository equals the local origin: judged as today, so a dead local record stays dead in a link;
- the target is relative: judged as today, this being what `resolve --markdown` emits;
- the URL names a different file than the token claims: DEAD, the false citation being the defect the sweep exists to catch;
- the citation stands in prose, not in a link: DEAD, one rule, link-or-nothing;
- the origin remote is absent: foreign by default, and the disclosure says so.

The check verifies form, never existence: it cannot read another repository, the same honesty limit the issue half already carries. The disclosure is a count on every exit, never an enumeration, per the [call/0048](../../call/0048-the-gate-runs-the-sweep-over-the-record.md) weak-model finding; what captures a weak agent is the per-file list, so the count shape ships again.

A sigil form (`agentic-host!call/0039`) was considered and declined: new grammar for every author and the weak model, a name-to-repository declaration surface to maintain, and no link in the rendered site. The cast round re-examines the rejection with the design on the table.

## Scope

1. **The accepted form** in the sweep's verdict, where the scan already computes link membership for register references.
2. **The disclosure** line, counted, on every exit path of `refs --check` and `refs --gate`.
3. **The doctrine**: the template manual's reference paragraph gains the cross-project form, and a ledger entry succeeds the limitation text in `GATE-refs-in-verify`.

Out of scope, recorded so it is not assumed: rewriting the six ledger prose citations (append-only record layer, and its file stays excluded); the ignore-list separation (one list serving two checkers, owed since the host#19 fix, its own milestone); verifying foreign targets over the network; a `resolve` emission for foreign citations (authorship stays hand-written until a corpus asks for the verb); linkifying commit messages (plan/0077's own out-of-scope row).

A census note, measured on the record: [plan/0082](../0082-suite-zero-open-bugs/README.md)'s `adopter-citation` node carries this issue with the disposition "fix in the template"; it describes the half fixed in host-template `79c0b71` (2026-07-27). That node's own verify, a template clone passing `refs --check`, passes at today's revision `933b7f1`: the `call/0039` citation is gone from `STRUCTURE.md`. What keeps the issue open is the accepted form this milestone closes; the census row predates the issue's closing comment.

## Open questions the gather-data node settles

- The URL well-formedness bar: which absolute shapes name the cited record (`blob` versus `tree`, branch versus commit, the anchor suffix, rendered versus source paths). Settled against real URLs carried in this tree's documents.
- The [call/0057](../../call/0057-a-remedy-must-know-whether-its-artefact-publishes.md) check applied to the new doctrine: the form directs authors to write a URL, which mints nothing on the target repository, and the doctrine and disclosure stay free of forms that publish.
- The exact disclosure lines on each exit, gate and check, so the count never reads as debt.
- Whether origin-absent reads foreign-by-default or skips with disclosure; the spec models whichever the corpus and the adversarial round support.
- The probe kit wording, production legibility and reading safety, written against the plan/0076 corrected protocol before anything runs.

## Build sequence

### The settled conditionals {#gather-data}
- verify: the four-form table re-run on the pinned binary and recorded in gather-data.md; the corpus counted (prose citations, link forms); the URL bar settled against real URLs with a written rule; the probe kit rereads the corrected protocol
- depends: none

### The reference surface {#write-spec}
- verify: the Allium spec models the citation outcome (a register reference in a foreign-naming link is a citation, not a dead pointer), the origin comparison, and the disclosure count on the run outcome; `allium check` and `analyse` exit clean
- depends: #gather-data

### The obligations {#write-obligations}
- verify: every new obligation carries a disposition naming a test that exercises the rule rather than a helper beside it
- depends: #write-spec

### The accepted form {#implement}
- verify: `cargo test` green; a citation in a foreign-naming link is accepted and counted; a dead local record stays dead in label and relative forms; a URL naming another file stays dead; prose citations stay dead
- depends: #write-obligations

### The test matrix {#write-tests}
- verify: the suite covers the issue's four forms plus local-link, relative-target, wrong-file, and origin-absent; mutating the rule reddens its named tests; clippy clean at the pinned toolchain; the exit-paths integration suite green (host-lifecycle's integration lane, not host-lint's script)
- depends: #implement

### Cast consultation {#cast-consult}
- verify: each persona's concern addressed or recorded in design-review.md; the sigil rejection and the disclosure wording re-examined on the record
- depends: #write-tests

### Adversarial review {#adversarial-review}
- verify: an independent multi-lens read of the built diff records every blocking finding fixed or carried, with a dedicated lens for the escape-hazard, a dead local record laundered through a foreign-looking URL
- depends: #cast-consult

### The weak-agent acceptance {#fen-acceptance}
- verify: the real qwen3.5-4b, on the corrected protocol, writes an accepted citation from the doctrine and reads the disclosure without remediating; rotation-stable, transcript recorded; an unreachable channel is labeled and the probes recorded as owed, never simulated silently
- depends: #write-tests

### The spine doctrine {#write-spine-doctrine}
- verify: the template manual's reference paragraph states the cross-project form; the ledger entry succeeding the limitation text records the change and the day-one state
- depends: #adversarial-review

### Release and re-pin {#release-and-re-pin}
- verify: the release cascades clean, `software --check .` clean at the new pin, and connollydavid/host#19 closes with the four-form table re-run as closing evidence; PLAN.md and MEMORY.md record the outcome in their own commits
- depends: #write-spine-doctrine, #fen-acceptance
