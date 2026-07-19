# plan/0072 ffmpeg-commit-rule-pack: pack dispatch in the core and the first external pack

This milestone delivers the FFmpeg commit-rule checker as host-lint's first external pack:
a reserved `pack` dispatch verb in the core, a new `host-lint-ffmpeg` binary built on the
`host_lint` library, and a rule registry that encodes every FFmpeg commit and patch rule
with an honest enforcement tier. The consuming project is pgs-release (the FFmpeg subtitle
upstreaming programme); the consuming milestone lives there, not here.

The design record is [host-lint#22](https://github.com/connollydavid/host-lint/issues/22)
(the opening design, the pgs9-review addendum, the consolidated revision that supersedes
both, and the public-signals addendum of 2026-07-17), adversarially reviewed in
[host-lint#23](https://github.com/connollydavid/host-lint/issues/23). Every design-level
finding of #23 is folded into #22's consolidated build sequence, task by task, with each
task naming the findings it absorbs; the public-signals addendum then verified the design
against the live upstream state and amended the sequence again (the review below). This
README does not restate the rule tables or the finding bodies; the issues are the record,
and RULES.md (the docs-and-release task) becomes the in-repo human form of the corpus.
What lives here is the milestone: scope, the settled architecture, the open operator
decisions, and the receipted task graph, which merges the consolidated revision and the
public-signals deltas into one final sequence.

## Scope

Delivered by this milestone, all in the host-lint repository except the final re-pin:

- The core fix for the live defect #23 verified: an explicit nonexistent file argument
  exits 0 clean on v0.14.2 where the tool fails closed everywhere else.
- The reserved `pack` dispatch verb (`host-lint pack ffmpeg ...`), sibling to `lexicon` and
  `gather`, with a `packs` listing and a strict core/pack version handshake.
- The `host-lint-ffmpeg` pack: rule registry with completeness-as-a-test, message, diff,
  series, mail, and forge lanes, the cosmetic/functional classifier, receipted expensive
  legs, the checklist reporter, the project-pack config layer, and the hook installer.
- The security-path routing rules (exploitable issues route to ffmpeg-security, never to
  the public patch paths) and the mailing-list mechanics from the FAQ, MAINTAINERS, and
  fate.texi sources the public-signals review surfaced.
- Corpus calibration over accepted upstream history before any severity tier freezes.
- The network-having upstream-drift CI lane against every acknowledged source, ffmpeg.org
  and the FFmpeg/web-carried security page included.
- The pack's spec discipline at the repo bar (`ffmpeg-pack.allium`, obligations, Kani,
  proptest), RULES.md, and the release.

Out of scope, recorded so the boundary is explicit:

- host-adoption: the pgs project pack TOML, `install-hooks` into the pgs FFmpeg worktrees,
  and the acceptance runs (the live pgs9 series, plus the frozen pgs8-wip series as a
  known-findings regression fixture whose recorded mechanical findings the pack must
  reproduce). That is a pgs-release milestone, cut there once the release exists.
- Full patcheck parity (typo lists, micro-optimization hints): deferred, and the registry
  marks those entries deferred rather than silently absent.
- FFmpeg's release-manager process and maintainer push-timing etiquette: excluded, and the
  completeness fixture carries the exclusions as explicit entries.

## The settled architecture

The consolidated revision on #22 settled these after #23's review; they are constraints on
every task below, not open questions:

- Dispatch is a reserved verb, never a bare name. A bare argument stays what it always
  was, a file path; `host-lint pack ffmpeg` dispatches while `host-lint ffmpeg` scans a
  file named `ffmpeg` (or fails closed when it is not scannable).
- The version handshake is strict: the pack refuses to run on a major or minor mismatch
  with the core, exit 2 with both versions named; the installer stamps and re-stamps core
  and pack together.
- Enforcement is three honest tiers: mechanical (the pack asserts it), expensive (a
  receipted re-derivable run; the cheap lane reports receipt presence and staleness, never
  a pass it did not run), attested (listed for the human, never auto-greened). This is the
  no-hollow-green rule (plan/0052) applied to a rule corpus.
- Severity tiers freeze only after calibration against accepted upstream history, and the
  registry records each mechanical rule's measured false-positive rate. Intuition
  proposes; measurement disposes.
- Completeness is a test, not a claim: a fixture enumerates every rule-bearing section of
  the pinned developer.texi (Coding Rules and Code behaviour included) and the test fails
  when any entry lacks a registry mapping. Source digests are scoped per rule-bearing
  section, so unrelated texi edits do not raise drift, and a separate network-having lane
  fails when ffmpeg.org drifts from what the corpus acknowledges.
- Nothing the pack needs is ever committed into the target FFmpeg clone; config resolves
  worktree-first (the worktree's private gitdir, then the git common dir, then defaults),
  so a submission-mode worktree and a wip-mode worktree coexist. Receipts live in the git
  common dir with an export form the consuming host can ledger.
- The project pack is data, not code: a TOML declaring branch grammar, tag grammar, and
  frozen-branch derivation, authored in the consuming host.
- The installed commit-msg hook chains the core `--stdin` naming scan with the pack msg
  lane and aggregates verdicts, so an agentic naming tell in a target-clone commit message
  is still caught.
- The corpus baseline is a genuine upstream master SHA. The revision the opening post
  recorded is a pgs-release fork commit, not an upstream one (the public-signals review's
  finding), so every drift claim keyed to it was unsound; the registry pins upstream and
  carries a corpus-freshness check at encode time.
- Submission is dual-path and the pack checks both: the mail lane covers the ffmpeg-devel
  path and the forge lane covers code.ffmpeg.org, whose landing mechanics (rebase and
  fast-forward only, per-commit messages landing verbatim) make the msg, diff, and series
  lanes apply to a pull request exactly as to a mailed series.
- AI-policy honesty: FFmpeg has no adopted AI/LLM contribution policy, so the pack encodes
  none. What it encodes instead is the operative text that does exist (the security page's
  automated-submissions ban, the optional Forgejo Fairy reviewer) and the community-enforced
  human-review norm as an attested leg grounded in the primary review record, never as an
  invented mechanical rule.

## The public-signals review (2026-07-17)

Before this milestone was cut, a fanned-out research pass (four angles, adversarial
primary-source verification of every load-bearing claim, a completeness critic, and a
targeted second round) verified the design against the live upstream state. The full
findings are the public-signals addendum on
[host-lint#22](https://github.com/connollydavid/host-lint/issues/22); the headlines:

- The corpus baseline was a fork SHA (the provenance defect above), and exactly five
  upstream developer.texi commits post-date the pinned content, three of them substantive
  rules the corpus lacked: narrow variable scope in loops (2026-04-22, advisory), bug
  fixes intended for backporting stay focused (2026-06-24), and the reviews-section
  rewrite adding the official optional Forgejo Fairy LLM reviewer (2026-07-13). The
  SI-units item became written rule text and promotes from attested to advisory. All five
  changes were live in the developer.html fetch the opening post records, so the misses
  were encoding gaps, not staleness: a second, independent argument for the
  completeness-as-a-test discipline.
- FFmpeg's LLM rules as they stand: no adopted policy (the July 2025 RFC remained
  discussion-only), per-maintainer discretion in practice, an official optional LLM
  reviewer on the forge path, a hard "Automated submissions are not accepted" plus
  named-human-reviewer requirement on the security path, and kernel-DCO sign-off
  semantics, so the responsible human signs off and certifies provenance of agent-drafted
  code. The January 2026 review of the AMD HIP-SDK pull request grounds the enforced
  human-review norm in primary quotes and names the concrete reviewer-recognized tells
  (end-user setup instructions in a commit message, a self-describing AVOption constant,
  duplicated documentation, untested configure targets).
- Four operative rule sources were never encoded: ffmpeg.org/security.html (three-way
  submission routing, the 10-item report contents), doc/mailing-list-faq.texi (per-message
  size cap, plain-text MIME, threading and etiquette mechanics, the DMARC bounce trap),
  MAINTAINERS (the CC routing rule and the parser realities), and doc/fate.texi (sample
  sequencing and immutability). The issue tracker also moved (Forgejo primary, Trac
  legacy), which changes the ticket-reference shapes.
- The Forgejo landing mechanics were established empirically from the live repo settings
  and observed merges (the API answers anonymous non-browser reads): no squash, no merge
  commits, verbatim per-commit landings, PR title as the relayed list subject, the PR
  description never entering history, and resubmission as force-push to the same PR.

## Open decisions for the operator

Five, carried from #22's consolidated revision. The build sequence proceeds on the
recommendations until the operator rules otherwise; each ruling lands in the registry or
config as data, not as a redesign.

1. Pack residence. Recommended: the host-lint cargo workspace, extraction reconsidered
   when a second pack appears.
2. The pgs branch grammar versus the live `-wip` branch name. The ruling belongs in a
   pgs-release decision record; the pack encodes whichever grammar is ruled.
3. patcheck depth. Recommended: the correctness-adjacent subset; the rest deferred with
   deferred registry entries.
4. Sign-off default. Recommended: `wip` mode default, `submission` mode set by hook config
   in pgs worktrees and by CI for series checks.
5. The calibration threshold: the agreed false-positive rate above which a mechanical rule
   may not hold flag tier. This one has no recommendation; it is set when the calibration
   report exists.

## Issue disposition

- [host-lint#23](https://github.com/connollydavid/host-lint/issues/23) stays open for the
  one live code defect and closes when the core-fix release ships. The fix travels first
  and does not wait on the pack build.
- [host-lint#22](https://github.com/connollydavid/host-lint/issues/22) is the design
  record and closes when docs-and-release ships the pack.

## Build sequence

The tasks are anchored receipted nodes (plan/0042), transplanted from #22's consolidated
revision, merged with the public-signals deltas, and with the release seams made explicit
for this host. Tasks with no stated dependency follow the previous task; stated
dependencies override. Each pack task names the #23 findings it absorbs in the issue
text; the verify lines here are the receipts' checks.

### core-fail-closed-file-args {#core-fail-closed-file-args}

An explicit file argument that is not a scannable file exits 2 with a diagnostic naming
the path, in line with the tool's fail-closed pattern everywhere else.

- depends: none
- verify by: regression test; `host-lint no-such-file.md` exits 2 and names the path

### core-fix-release {#core-fix-release}

The live-defect fix ships as its own patch release ahead of the pack, so #23 does not
wait on the pack build: `host-lifecycle release host-lint --change-class neither`, re-pin
`.host-software`, record the release receipt, close #23 with the release named.

- depends: #core-fail-closed-file-args
- verify by: `host-lifecycle software --check .` clean at the new pin; #23 closed

### pack-dispatch {#pack-dispatch}

The reserved `pack` verb: resolution beside the binary then on PATH, arg and exit-code
passthrough, `packs` listing, strict version handshake with refusal on skew, exit 2 with
an install hint when the pack is absent.

- depends: #core-fail-closed-file-args
- verify by: stub-pack integration tests covering passthrough of each exit code, the
  collision case (a file named `ffmpeg` in cwd: `pack ffmpeg` dispatches, bare `ffmpeg`
  scans the file), skew refusal, and the missing-pack hint

### engine-surface {#engine-surface}

The reporting surface (`output_text`, `output_json`, `fix_hint`) moves from `main.rs`
into the `host_lint` lib; the stable embedding surface is documented.

- depends: none
- verify by: `cargo build` and `cargo test` green with `main.rs` consuming only the lib
  surface; host-lifecycle's embedding compiles unchanged

### workspace-split {#workspace-split}

The repository becomes a cargo workspace: the existing crate unchanged plus the
`host-lint-ffmpeg` bin crate; release assets per platform; `deps-bundle.lock`
regenerated.

- depends: #engine-surface
- verify by: `cargo build --workspace --release` offline from the vendored bundle; both
  binaries produced on all release targets in CI

### fixture-licensing {#fixture-licensing}

The licensing policy decided before any fixture lands: synthesized fixtures by default; a
real upstream excerpt only where synthesis cannot reproduce the case, isolated with
explicit provenance and licensing notes.

- depends: none
- verify by: the fixtures directory ships its provenance README; a CI check requires it
  wherever real excerpts sit

### rule-registry {#rule-registry}

The encoded corpus, widened per #23 and re-grounded per the public-signals review: the
baseline re-pins to a genuine upstream master SHA with a corpus-freshness check at encode
time; the five-commit developer.texi drift set is absorbed (narrow-scope, backport-minimal,
SI-units promotion, reviews/Fairy, tracker transition); the source set widens to
security.html (pinned by FFmpeg/web commit plus fetch date, since no SECURITY file exists
in the FFmpeg tree), mailing-list-faq.texi, MAINTAINERS (snapshot pinned by SHA plus
content hash), and fate.texi; every rule-bearing chapter sits in the completeness fixture;
a measured-rate field per mechanical rule (empty until calibration); per-section source
digests. `rules`, `rules --json`, and `rules --verify-source <tree>`.

- depends: #workspace-split
- verify by: the completeness test fails when any rule-bearing chapter entry lacks a
  registry mapping; a doctored section raises drift while an edit elsewhere does not; the
  freshness check fails on a pin older than the newest developer.texi commit

### msg-lane {#msg-lane}

The message checks corrected against measured ground truth: the widened area grammar,
the `Revert`/`fixup!`/`squash!` exemptions, the enumerated exact-string vague list,
ascii-clean, mode-aware sign-off, no-end-user-setup-instructions (commit bodies are
why-and-what, never install walkthroughs; grounded in the January 2026 review record),
and ticket-ref accepting Forgejo issue references alongside legacy Trac shapes and CVE
ids now that the primary tracker moved.

- depends: #rule-registry
- verify by: the measured ground-truth subjects from #23 join the fixtures as a must-pass
  corpus; synthetic violations fire each rule exactly once; proptest over the grammar

### diff-lane {#diff-lane}

The added-line checks with scope drawn precisely: the full Makefile-class and golden-output
whitespace exemptions, library-trees-only naming scope, the lexical VLA rule retired in
favour of a `-Wvla` build leg, ascii-comments, the api-misuse patcheck subset, the
narrow-variable-scope advisory heuristic (a loop counter declared immediately before the
for loop that uses it), and the self-describing AVOption constant heuristic (name equals
value, the reviewer-named tell).

- depends: #rule-registry, #fixture-licensing
- verify by: per-rule positive and negative fixtures, with a `*.mak` tab, a `tests/ref`
  golden file, and an fftools identifier all passing; patcheck parity cases

### cosmetic-separation {#cosmetic-separation}

The mixed cosmetic/functional classifier, fully specified: `diff -w -b` per git-howto,
blank-line handling defined, the brace allowance and the 2026-03-25 whitespace-only
relaxation encoded as fixtures.

- depends: #diff-lane
- verify by: six fixture commits (mixed flags; pure re-indent, pure functional, brace
  allowance, whitespace-only relaxation, and blank-line-only all pass)

### corpus-calibration {#corpus-calibration}

The tier freeze: every mechanical rule runs over several thousand recent accepted
upstream commits; a rule flagging above the agreed rate is demoted or refined; the
registry's measured-rate fields are populated. Tiers freeze here and nowhere earlier.

- depends: #msg-lane, #diff-lane
- verify by: the calibration report is committed beside the registry; a gate test asserts
  no flag-tier mechanical rule exceeds the agreed rate on the calibration corpus

### series-lane {#series-lane}

The per-commit walk and series-order checks, corrected and widened: the generated-header
allowlist and dual-root include resolution, provider-before-consumer extended to Makefile
object references, registration triggers over every table (filters and bitstream filters
included), the version-bump check reading the split version headers and Makefile HEADERS
variables, plus alphabetical-order, maintainers-coverage, checkasm-obligation, gpl-gating,
doc-updated, and shared-abi with its false-positive mode documented. The public-signals
additions land here too: the backport-fix focus warn (a ticket- or CVE-referencing fix
carrying hunks the fix does not need warns to split), the fate-sample checks (a FATE test
referencing a sample absent from fate-suite requires a samples-request note, an existing
fate-suite path is never repurposed, sample minimality attested), and the security
three-way routing classifier (exploitable to ffmpeg-security, non-exploitable UB or leak
to a Forgejo PR, everything else the normal path).

- depends: #cosmetic-separation, #corpus-calibration
- verify by: the synthetic-repo suite extends per rule; a series including
  `config_components.h` passes; a Makefile object reference ahead of its source flags; a
  filter registration with no Changelog, doc, or MAINTAINERS hunk fires each obligation;
  an avpriv move without a minor bump flags; a crash-fix commit with a new fate sample
  and no samples-request note fires both the routing note and the sample check

### build-receipts {#build-receipts}

The expensive lane with home and legs settled: per-commit compile, `--enable-shared`,
`-Wvla`, standalone-compile, `--disable-x86asm` when assembly is added, an out-of-tree
configure-and-make leg when the series touches Makefiles or ffbuild (a reviewer-enforced
expectation from the January 2026 record), optional FATE. Receipts in the git common dir
with the export form, carrying base and head SHAs, toolchain identity, config digest, and
the legs run; missing receipt notes, stale receipt warns (exit 3), an unrun leg renders
unrun, never passed.

- depends: #series-lane
- verify by: toy-repo run producing a receipt with legs recorded; a rewritten head reads
  stale (warn); a missing leg renders unrun; the export form round-trips

### mail-lane {#mail-lane}

The format-patch directory checks, widened by the mailing-list-faq and MAINTAINERS
sources: parseability, subject-prefix coherence, cover-letter warn, the per-message
1000 kB flag (oversize mail stalls silently in an unwatched moderation queue), plain-text
MIME, the 70-character prose-wrap advisory (composed prose only, never the diff payload),
the uncompressed-attachment advisory, single-list To/Cc addressing, the thread-targeting
check (an `--in-reply-to` target must belong to the same series' prior-version thread),
maintainer-cc (a CC-marked MAINTAINERS entry matching a touched path must appear in the
Cc list, with the section-scoped glob matcher and all three observed CC syntaxes), the
DMARC pre-send warn (a From: domain publishing reject or quarantine bounces off
ffmpeg-devel), and patchwork post-send verification (the series appears, prior versions
marked superseded). Attested: the subscription precondition and interleaved-reply style.

- depends: #msg-lane
- verify by: fixtures generated by `git format-patch`, with a broken numbering case, a
  missing cover letter case, an oversize-mail case, an HTML-only case, a wrong-list case,
  a hijacked-thread case, and a missing-CC case among them; the MAINTAINERS parser passes
  the live-syntax fixture set (three CC forms, the non-CC parenthesized address, the
  section-scoped duplicate globs)

### forge-lane {#forge-lane}

The code.ffmpeg.org path checks, empirically grounded in the live repo settings and
observed landings and re-checkable via the anonymous API: the PR title satisfies the
area-prefix subject grammar (it becomes the relayed list subject), `WIP:` as the draft
marker, the description-as-cover-letter advisory plus the rationale-lands-in-commits
check (the description never enters git history), and force-push resubmit discipline
(same PR per revision, no [PATCH vN] title, a delta comment on each push). The msg, diff,
and series lanes already apply per commit since landings are rebase or fast-forward with
verbatim messages; this lane adds only the forge-specific surface.

- depends: #msg-lane
- verify by: fixture PR metadata cases (a bare-branch-name title flags, an area-prefixed
  title passes, a WIP title notes, a versioned title flags); the empirical-grounding note
  names the API endpoints a re-check reads

### checklist-reporter {#checklist-reporter}

`checklist` renders the full registry over a series: mechanical results from the lanes,
expensive results from receipts, the widened attested set listed with citations, measured
rates alongside each mechanical result, the tier boundary visible (checked, receipted,
attested). The attested set gains the human-review leg (grounded in the January 2026
primary quotes and enumerating the reviewer-named tells), the post-land fate.ffmpeg.org
monitoring leg, and the security-path attested items (named human reviewer, finder
credit, reproducible-with-existing-applications).

- depends: #series-lane, #build-receipts
- verify by: golden-output test; a grep asserts no attested item ever renders as checked
  and no unrun leg renders as passed

### project-pack-config {#project-pack-config}

The config layer with worktree-first resolution: TOML schema (upstream ref, mode, branch
grammar, tag grammar, frozen derivation from history tags), the loader, a documented
example, and the branch and tag checks.

- depends: #rule-registry
- verify by: precedence tests including a two-worktree clone holding different modes;
  branch, tag, and frozen-branch checks against a synthetic repo with history tags

### hook-installer {#hook-installer}

`install-hooks` lands hooks per worktree with config in the worktree's private gitdir;
the installed commit-msg hook runs the core `--stdin` scan and the pack msg lane with
aggregated verdicts; core and pack versions stamped together, a skewed pair refused;
nothing tracked or untracked lands in the target tree.

- depends: #msg-lane, #diff-lane, #project-pack-config
- verify by: a two-worktree install with differing modes; a phase-tell commit message in
  the target clone is blocked by the chained core scan; a staged tab is blocked; the skew
  case refuses; `git status` in the target shows nothing new

### upstream-drift-lane {#upstream-drift-lane}

The network-having CI lane, watching every acknowledged source: developer.html and
git-howto as designed, plus security.html (keyed to FFmpeg/web commits, since the page
changed five times in 2026 alone), mailing-list-faq.html, the MAINTAINERS snapshot, and
fate.texi. Normalize, compare each rule-bearing section against the digest the corpus
acknowledges, fail on unacknowledged drift; drift audits use a recursive tree diff, never
a flat listing or a capped compare API. Acknowledging drift is a deliberate corpus edit.

- depends: #rule-registry
- verify by: a doctored snapshot of each source fails the lane; acknowledging its digest
  passes it; the offline gates never depend on this lane

### spec-obligations {#spec-obligations}

The pack's spec discipline at the repo bar: `ffmpeg-pack.allium` modelling the verdict
lifecycle and rule tiers, the `.obligations` manifest with `exercises=` links, Kani
harnesses for the byte-level predicates, proptest over open input spaces.

- depends: #series-lane, #checklist-reporter
- verify by: `allium check` + `analyse` + `plan` clean; `host-lifecycle obligations
  ffmpeg-pack.allium --tests tests --prove src --strict-discharge` clean; `cargo kani`
  green

### docs-and-release {#docs-and-release}

RULES.md (the corpus in human form, each rule with its citation, measured rate, and
documented false-positive modes, plus the AI-policy note: no adopted upstream policy, the
two operative texts, the DCO sign-off reading, the dormant RFC thread as the re-check
trigger before each submission campaign, and the recorded license-objection risk), README
and SKILL.md coverage, the id-sync drift-guard test, then the release: `host-lifecycle
release host-lint --change-class adds-flag`, annotated tag, release assets for core and
pack. Close #22.

- depends: #spec-obligations
- verify by: `host-lint --docs` clean; id-sync green; tag and assets present; #22 closed

### re-pin-and-receipt {#re-pin-and-receipt}

Re-pin host-lint in agentic-host's `.host-software` at the pack release, record the
release receipt, and record the named follow-up: the host-adoption milestone in
pgs-release (pin bump, the pgs project pack TOML including the maintainer table the
public-signals review recorded, a code.ffmpeg.org account plus API access for the forge
path, a DMARC-safe sending address for the mailing-list path, `install-hooks` into the
FFmpeg worktrees, the pgs9 acceptance run, and the frozen pgs8-wip known-findings
reproduction).

- depends: #docs-and-release
- verify by: `host-lifecycle software --check .` clean at the new pin; the follow-up named
  in PLAN.md's follow-up table
