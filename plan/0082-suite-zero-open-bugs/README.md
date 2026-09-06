# plan/0082 suite-zero-open-bugs: every open issue across the suite closed or deferred with a reason

This milestone drives the whole `connollydavid/host-*` suite to zero open bugs. It is a
closing milestone rather than a building one: nothing new is designed here except where an
open issue's remedy has no design yet, and the deliverable is an empty tracker across nine
repositories plus one recorded deferral for each thing that is not a bug.

The census below was taken on 2026-08-10 and is the whole population. `host-template` has
issues disabled, so its defects are carried on `connollydavid/host`; that is a standing
condition of the suite and not something this milestone changes.

## The census

Six issues are open. Two of them are already fixed and were confirmed so by measurement, not
by reading the fix direction and assuming it landed.

| Issue | State on 2026-08-10 | Disposition |
|---|---|---|
| [connollydavid/host-lifecycle#24](https://github.com/connollydavid/host-lifecycle/issues/24) | resolved | verify and close |
| [connollydavid/host-lint#27](https://github.com/connollydavid/host-lint/issues/27) | resolved | verify and close |
| [connollydavid/host#19](https://github.com/connollydavid/host/issues/19) | live defect | fix in the template |
| [connollydavid/host-lint#26](https://github.com/connollydavid/host-lint/issues/26) | live defect | **Done 2026-09-06** (plan/0086): the grammar decides block structure before the mask, shipped in host-lint v0.19.0, verified against the pinned binary and closed with the transcript |
| [connollydavid/host-lifecycle#23](https://github.com/connollydavid/host-lifecycle/issues/23) | owed work, not a defect | defer with a recorded reason |
| [connollydavid/host#18](https://github.com/connollydavid/host/issues/18) | design handover, not a defect | defer to plan/0075 |

Four further defects have no issue and will not get one. The operator directed that these findings
fold into the work rather than the tracker, so they are carried here. Three were found while
fixing `host-lint#26` and none was on the census when it was taken.

- **The LEXICON remedy publishes.** The identifier tier's sanctioned fix mints a cross-reference on
  an upstream thread. Settled by [call/0057](../../call/0057-a-remedy-must-know-whether-its-artefact-publishes.md).
- **A released version shipped a red test suite.** `allcaps_designator_before_decimal_does_not_warn`
  fails at the v0.18.1 pin with no local change, confirmed by stashing. The generator draws
  `[A-Z]{2,5}` but assumes out only `WARN_NOUNS`, while `FLAG_TERMS` holds `BOX`, `LEG`, `LAP`,
  `WAVE` and `WARN_ORDINAL_TERMS` holds `ERA`, `EPOCH`, `BATCH`. Proptest drew `ERA`. The property
  asserted that real vocabulary is silent; the tool was right and the test was wrong. A failure
  that only appears on the draw is a failure that ships.
- **A worktree hook lost its ignore list.** `software --materialize` writes the
  `gitdir` link relatively, so a bare store stays portable. `repo_root()` took that target's parent
  and resolved it against the process working directory. That path lands outside the tree, so
  `.host-lintignore` and the LEXICON went missing without a word. Only git sets `GIT_DIR`, so the fault
  was reachable only from inside a hook, and only after the worktree hooks were installed at all.
  The fix for `host-lint#25` had assumed an absolute gitdir.
- **A failed release poisons the next attempt.** Staging the deps-bundle appends the vendor source
  block to the tracked `.cargo/config.toml` and never removes it, so a second run duplicates
  `[source.crates-io]` and cargo refuses the manifest. The first release attempt here timed out
  mid-build and the second failed on the residue rather than on anything it did.

The last of these is a `host-lifecycle` defect rather than a `host-lint` one, and it is recorded
without a remedy task: this milestone works around it by restoring the file, and the fix belongs to
whoever next opens the release path.

### The two that are already fixed

`host-lifecycle#24` asked for two things: a queryable version, and the generator recorded as a
proven component symmetrically with the checker. Both are present. `host-lifecycle --version`
returns `host-lifecycle 0.50.0`, and `.host-software` carries a `host-lifecycle` stanza with a
pinned toolchain, a canonical artifact hash and a deps-bundle, which is the same shape
`host-lint` has. The issue predates both.

`host-lint#27` reported the `harness` ai-diction trope firing twice on the verbatim template
spine and re-opening the verify receipt. It does not reproduce: `host-lifecycle prose host-template`
returns `prose: clean … [host-lint 0.18.1]` at exit 0. One of the two cited lines is gone from
the spine entirely; `kani:<harness>` remains at `CLAUDE.md:476` and no longer fires. The fault
was never in host-lint's rule set but in the template pinning a host-lint too old to accept its
own spine, which is the skew [call/0056](../../call/0056-a-tool-dependency-is-a-floor-checked-in-the-lane.md)
addresses at the root.

Neither may be closed on this reading alone. Each closing task below re-runs the repro from the
issue body and quotes the output, because an issue closed against a claim rather than a
transcript is how a fixed-looking defect returns.

## What is not in scope

`host#18` is a complete design handover for a fourth methodology tool, and
[plan/0075](../0075-host-reconcile/README.md) already holds it as a cut, design-only milestone.
`host-lifecycle#23` is the owed mechanical half of the room-touching detector, recorded so that
"labelled" could not quietly become the fix; it is enhancement work with its own recorded
stakes. Neither is a bug, and closing them here would be a category error. Both are deferred by
name, with the deferral written into the issue so the tracker states the reason rather than
going quiet.

Zero open bugs is the goal. Zero open issues is not, and a milestone that conflates the two
buys a clean tracker by discarding the record of what is owed.

## Closing is the last act

Operator ruling, 2026-08-10: **no issue is closed until the session's final push has landed.**
Verification and the drafting of each closing comment happen whenever the work is done, but the
`gh issue close` calls are held to the end and run only after every repository the work touched
is pushed.

The reason is the failure this milestone exists to prevent, applied to itself. An issue closed
against a working tree is closed against something no one else can see, and if the push then
fails on auth or the session ends first, the tracker says fixed while the fix exists on one
machine. Closure is a claim made to everyone with access to the repository, and it must not
outrun the evidence for it. The same rule already governs pushes here: never push a host commit
whose software pin is unpushed.

This inverts the natural order of the sequence below. `close-resolved` is written first because
it is the smallest task, but it *executes* last, after `sweep-and-confirm` and after the final
push.

## Build sequence

### close-resolved {#close-resolved}

Re-run each issue's own repro under the current toolchain and close the two that pass. Quote the
transcript in the closing comment. Held to the end of the session by the ruling above: the
verification may run at any point, the close may not. Verify by: `host-lifecycle --version` and
the `.host-software` stanza answer `host-lifecycle#24`; `host-lifecycle prose host-template` at
exit 0 answers `host-lint#27`; both issues are closed with the output pasted, not paraphrased,
and both closes happen after the final push.

### adopter-citation {#adopter-citation}

Fix `connollydavid/host#19`. `host-template/STRUCTURE.md` cites `call/0039`, a record that lives
in agentic-host and that no adopter ever receives, so `refs --check` gates every fresh host on
its first sweep with nothing the adopter did wrong to point at. The citation has to stop being a
register reference in the copied file. Verify by: a clone of the template at the fixed revision
passes `host-lifecycle refs --check` with zero dead pointers.

### lexicon-line-masking {#lexicon-line-masking}

Fix `connollydavid/host-lint#26`. **Landed 2026-09-05 and verified closed 2026-09-06 (plan/0086)**: the grammar decides block structure before the mask (`e5ac04cb`), shipped in v0.19.0 with two regression tests citing the issue; the repro transcript is plan/0086's. `mask_allowed` blanks a declared phrase with spaces, and on
the markdown path a phrase declared at column one leaves four or more leading spaces, which
`scan_prose_markdown` reads as an indented code block and skips the whole line. Every tell on
that line clears silently. Mask with a filler that is neither alphanumeric nor whitespace so the
blast radius is the phrase rather than the line. Verify by: the issue's own reproduction, where
a declared `apache tapestry` at column one still leaves the standalone `tapestry` flagging, and
a test asserts the surviving match.

### lexicon-remedy-publishes {#lexicon-remedy-publishes}

The identifier tier's remedy asks for a tracker reference declared with a backing URL. In a
commit message on a public repository both `owner/repo#N` and the URL mint a cross-reference on
the target, so the hygiene lane's sanctioned fix is what pulls the governance repository into an
upstream thread. host-lint has no notion that a commit message publishes in a way a file does
not. Decide the remedy split before writing code, because this is a design gap rather than a
coding error, and record it. Verify by: a `call/` records the decision, and the remedy text no
longer directs an author toward a form that publishes when the artefact is a commit message.

### defer-with-reason {#defer-with-reason}

Write the deferral into `host#18` and `host-lifecycle#23` naming the milestone that holds each
and why it is not a bug. These are comments rather than closes, but they are outward-facing
writes on a public tracker and are held to the end under the same ruling. Verify by: both issues
carry a comment naming plan/0075 and the owed cross-check respectively, and the suite's open-bug
count is zero while the open-issue count is two by intent.

### sweep-and-confirm {#sweep-and-confirm}

Re-take the census across all nine repositories and confirm it against this document. Verify by:
every open issue is one of the two deferred, and `host-lifecycle software --check .` and
`--verify-setup .` are both green.
