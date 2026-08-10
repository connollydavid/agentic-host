# call/0055: upstream artefacts are referenced, not embedded

- Status: accepted
- Scope: how `host-lint-openwrt` obtains an upstream artefact it checks against; the line between a rule source the pack vendors and a live artefact it must resolve; what a temporary cache may and may not stand in for
- Date: 2026-08-10

## Context and problem

[plan/0072](../plan/0072-ffmpeg-commit-rule-pack/README.md) established pin-and-vendor for the
FFmpeg pack: every upstream source is copied in and pinned by whole-file digest, so the corpus is
provable offline and drift localises to the section that moved. [plan/0081](../plan/0081-openwrt-style-pack/README.md)
inherited that shape, and the fourth style manual broke it.

Three of the four manuals describe habits measured from the tree and from history. The fourth
describes a pull request body, and its rules key to `.github/pull_request_template.md`, a file
`openwrt/packages` ships and GitHub prefills. That is not a measurement. It is a live artefact
owned by another project, and it changes without asking. The manual's own figures say so: template
adoption runs 0.0% in 2024, 44.0% in 2025 and 71.6% in 2026, because the template in this form
landed mid-2025 and replaced a plainer one.

A vendored copy of that file would be wrong the moment upstream edits it, and wrong silently. The
pack would keep reporting a confident verdict against headings the project no longer ships, which
is the same failure mode as a checker whose completeness test passes over what it happened to see.

There is a second, quieter path to the same fault. `openwrt-pr-style.md` quotes the template in
full inside a fenced block. That quote is vendored, because the manual is vendored. If the checker
read its expected headings out of that fence, the pack would embed the upstream artefact by the
back door, through a file that looks like the project's own.

## The distinction that settles it

Two kinds of input were being treated as one.

- A **rule source** states what the pack enforces. The four manuals are rule sources. They are
  project-authored measurements, they are the pack's own, and freezing them is correct: a rule
  that changes without the registry changing is exactly what the digest pin exists to catch.
- A **checked-against artefact** is something the pack compares a submission to, owned and moved
  by someone else. `.github/pull_request_template.md` is one. Freezing it is not conservatism; it
  is a wrong answer with a long shelf life.

Pin-and-vendor is right for the first and wrong for the second.

## Decision

Upstream artefacts are **referenced and resolved at check time**, never embedded.

1. The pack carries no copy of `.github/pull_request_template.md`. It records the artefact's
   canonical location and resolves it per run, preferring a local `openwrt/packages` checkout when
   one is given and falling back to the published raw file.
2. A **temporary cache is permitted** and is expected, so a sweep does not refetch per invocation.
   It is bounded by a short lifetime, it is gitignored and never tracked, and it is a cache in the
   strict sense: it may only hold what was fetched from the canonical location, and its presence
   may never change a verdict from what a live fetch would have produced.
3. When the artefact cannot be resolved and no live cache entry stands, the template-keyed rules
   **do not run and say so**. A degraded path states what it did not check. It never falls back to
   the manual's quoted fence, and it never reports clean for a rule it could not evaluate.
4. The last-seen digest is recorded so a moved template is **reported as drift**, not absorbed.
   Drift on a checked-against artefact is news about upstream, not a defect in the pack.
5. The quoted template inside `openwrt-pr-style.md` is illustration. No checker may read expected
   headings, labels or box wording from it. The manual is a rule source; the fence inside it is not
   a copy of the artefact for the pack's purposes.

The four style manuals stay vendored and digest-pinned under `fixtures/manuals/`, unchanged by this
decision.

## Consequences

The `pr` lane gains a resolution step the other three do not have, and with it a failure mode they
do not have: it can be unable to check. That is accepted, and it is why point three is written as a
floor rather than a preference. A lane that quietly passes because it could not read the thing it
compares against is worse than a lane that refuses, and this pack already carries one refusal of
that shape, since the `pr` lane also refuses a directory argument rather than sweeping a clone for
a body that is not in it.

Offline reproducibility is now partial by construction. The three tree-facing lanes remain fully
offline; the `pr` lane's template-keyed rules do not, and the release gate must not treat that as a
regression to be engineered away. The measured rules of the `pr` lane, those about *filling* the
headings rather than matching them, stay offline and keep working when resolution fails, which is
where most of that manual's findings live: a template body keeps the testing lines about 95% of the
time and supplies a value only about two thirds of the time.

This decision is scoped to artefacts the pack checks against. It does not reopen pin-and-vendor for
rule sources, and it does not apply to the FFmpeg pack, whose pinned documents are prose that states
rules rather than a form a submission is matched to.
