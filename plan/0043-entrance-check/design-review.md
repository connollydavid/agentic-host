# plan/0043 design review: the entrance check

Three independent adversarial reviewers read the milestone, `gather-data.md`, the spine
(`host-template/CLAUDE.md`, `host-template/UPGRADING.md`, `STRUCTURE.md`), the reconcile and
entrance code in `software/host-lifecycle/main/src/main.rs`, and `call/0023` and `call/0027`.
One read with a simplicity bias (is this premature and over-built?), one with an integrity
bias (does coverage actually hold the new documents complete?), and one with a
weak-agent-ergonomics bias (can an adopter and a weak agent author and apply it without a
silent break?). They converged on the same core findings and a re-scope.

The operator decisions recorded so far stand: the capability is opt-in and reusable in
principle, the name is `entrance`, and it is the standalone sibling of reconcile. The review
interrogated the declaration form, the concept-set model, the reconcile relationship, and the
spine reconciliation, and found the generalization premature and one mechanism broken as
drawn.

## The convergent blocking finding: the value form breaks the shared marker

The `entrance` marker is overloaded. `parse_project_facts` sets a member apart as the entrance
only when the value is exactly `true` (`main.rs:1352`, `val.trim() == "true"`). That one
predicate feeds two checks at once: `facts.entrance` is the entrance check's target, and
`facts.components` is every member except the entrance, the set reconcile holds the
`STRUCTURE.md` components home to (`main.rs:1362`, the coverage bite at `main.rs:1607`).

So the gathered Style A value, `entrance = phases tools`, does not generalize the flag. It
silently un-marks the entrance: the value is not `true`, the `host` member loses its set-apart
status, `facts.entrance` goes empty, and `host` falls back into `facts.components`. The next
reconcile run then demands the `STRUCTURE.md` components home name `host`, the exact silent
demotion `call/0027` was written to forbid, reintroduced through the value rather than the key.
No test covers a non-boolean `entrance` value, so the regression would ship green. The
integrity and ergonomics reviews both proved this from the code.

The lesson is plan/0040's, one rung along: a fact is only safe through the tool when the tool
actually reads it. The concept list in `entrance = phases tools` is read by nothing today
(`entrance_problems` checks all phases and all tools and the stamp unconditionally,
`main.rs:1750`), so the declared set is unverifiable sugar that also breaks the marker.

## The generality is unfounded: the new documents restate doctrine with no home

The milestone's headline is that the check generalizes to a standalone `SKILL.md` and an
operator-and-agent landing page. The entrance check holds three facts: the lifecycle phases
(home: the manifest), the wired tools (home: `.host-software`), and the `.host` stamp block (a
fixed format). `entrance_spine_facts` returns the full manifest and the full driver set every
time (`main.rs:1795`); `entrance_problems` looks for the phases, the tools, and a `## The
stamp` block (`main.rs:1750`).

A standalone skill or a landing page restates teaching doctrine: the disposition rules, the
point-over-restate principle, the conditional-lane MUST. None of that has a structured home
the tool reads, so the check cannot hold it complete. plan/0040 settled exactly this class:
the lanes rule and the tool prose have no structured home and stay authored, and the milestone
says so plainly rather than claiming a drift-proofing it cannot deliver
(`plan/0040/design-review.md:69`, `:112`). The simplicity review also found that the one
concrete candidate, `software/host-lint/main/SKILL.md`, restates neither the phases nor the
tools, so the motivating second user does not exist in the repo, and the check resolves a
member's `README.md` by filename (`main.rs:1809`), so a differently-named skill doc could not
even be declared.

So the entrance check holds, honestly, any document that restates the phase, tool, and stamp
facts, which in practice is the front-door `README.md` and little else. The broader pitch is
not delivered by the design.

## The real, finishable payload: the spine reconciliation

The one part with a real, non-speculative obligation is the spine reconciliation that the
pre-generalization audit surfaced. The spine still teaches the old spelling:
`host-template/CLAUDE.md:281` and `host-template/UPGRADING.md:207` both document
`front-door = true`, while the tool prefers `entrance = true` and a deprecation shim absorbs
the gap (`call/0027`). This is live debt `call/0027` deferred, fixable now, and it needs none
of the declaration-form or concept-set machinery.

The integrity review added a sharp constraint: the shim retirement adds a hard fail on a
surviving `front-door = true`, but the spine prose that teaches `front-door = true` has no
structured home and nothing gates it. Retire the shim while the spine still teaches the old
spelling, and the spine teaches the very spelling the tool now rejects. So a `front-door` grep
over host-template is a release gate of the retirement, not an afterthought. The ergonomics
review added that the adopter ledger entry is a pure boolean rename (`front-door = true` to
`entrance = true`), which stays a safe literal substitution precisely because `entrance = true`
still parses, and its verify post-condition must hold reconcile and `software --check` green,
not only `entrance --check`.

## The decisions, settled

### The declaration form: keep `entrance = true`, defer the value form

`entrance = true` stands. It marks the front door, which restates every concept, and it already
parses, so the spine rename stays a safe no-op substitution. The concept-list value (Style A)
is deferred with the generalization: introducing it now breaks the shared marker for a feature
no document needs yet. The Fen leaning to a member-level concept list is recorded in
`gather-data.md` for that future decision, with the caveats the review added: a `true` or `all`
sentinel for the restates-everything case so the full front door never types an enumeration, a
closed concept vocabulary the tool validates at parse time, and the marker keyed on presence
with a non-empty value rather than on `== "true"`.

### The concept-set model: deferred, with its homes named

Deferred with the declaration form. The only concepts with a structured home are the phases and
the tools, and the front door restates both, which `entrance = true` already covers in full. A
partial entrance (a document restating a subset) has no consumer yet, and a routed concept set
is unimplemented (`entrance_problems` checks all concepts unconditionally). When a real partial
entrance exists, the set must be a closed vocabulary aligned with reconcile's concept names,
rather than a third overlapping word list.

### The reconcile relationship: settled, a separate subcommand

Already settled by plan/0040 (the entrance check ships as a sibling of reconcile) and confirmed
in every review here. reconcile resolves links and checks anchors over tracked markdown;
entrance reads a materialized README, covers the manifest phases, and generates the stamp
byte-exact. Folding entrance into reconcile would put a generator inside a checker. They share
only `parse_project_facts`, and that shared marker is the real coupling point, to be kept a
single, tested primitive. This leaves the open list.

### The spine reconciliation: the milestone's core, do it now

Rename `front-door = true` to `entrance = true` in `host-template/CLAUDE.md` and
`host-template/UPGRADING.md`, ship an adopter `UPGRADING` ledger entry for the rename, and
retire the deprecate-then-retire shim with a hard fail on a surviving `front-door = true`. Gate
the retirement on a `front-door` grep over host-template, so the spine never teaches the
spelling the tool rejects, and gate the ledger entry's verify post-condition on reconcile and
`software --check` green, not only `entrance --check`. Fold in the exit-code convention comment
that `gather-data.md` validated.

## Verdict

Re-scope. The opt-in generalization for documents unlike the front door is deferred until a real
second entrance exists, one that restates a concept with a structured home, since the headline
`SKILL.md` and landing-page use cases restate doctrine the tool cannot hold complete, and the
gathered value form breaks the shared marker for a feature no document needs yet. The
milestone's deliverable becomes the spine reconciliation it already owes: rename the spine flag,
ship the adopter ledger entry, retire the shim behind a host-template `front-door` grep gate,
and fold in the exit-code comment, with the marker parse left on `entrance = true` so
reconcile's component model stays intact. The entrance check's honest scope is recorded: it
holds any document that restates the phase, tool, and stamp facts, which today is the front
door.
