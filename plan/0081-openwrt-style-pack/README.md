# plan/0081 openwrt-style-pack: the OpenWrt package style rules as a second external pack

This milestone delivers `host-lint-openwrt`, the second external pack in the host-lint
workspace, built to the shape [plan/0072](../0072-ffmpeg-commit-rule-pack/README.md)
established for `host-lint-ffmpeg`. Where the FFmpeg pack encodes one upstream project's
commit and patch rules, this one encodes the four style manuals that govern a package
contributed to `openwrt/packages`, and it checks all four of them.

The rules are not upstream policy. `.github/llm-review-rules.md:100` states that the
description block is free-form prose with no enforced convention, so there is no document
to cite in review. The three manuals are **measured practice**: each rule rests on a
counted share of the live tree, and each carries that share into the registry as its
measured rate. This is a stronger footing than the FFmpeg pack started from, where every
`measured_rate` was `None` until the calibration node ran, and the pack should not throw
that away by re-deriving the rates from scratch.

## Scope

Delivered by this milestone, all in the host-lint repository except the final re-pin:

- `host-lint-openwrt`, a workspace member beside `host-lint-ffmpeg`, sharing the lockfile
  and the vendored bundle, listed in `default-members` so a bare `cargo build` produces it.
- The three vendored style manuals, pinned by whole-file digest, as the pack's sources.
- A rule registry carrying the same `Source` / `Section` / `Rule` / `Tier` structs the
  FFmpeg pack uses, with completeness-as-a-test over the vendored manuals.
- Four lanes, one per manual, each with its own checker and its own fixtures.
- `RULES.md` generated from the registry, and `CALIBRATION.md` recording where each
  measured rate comes from.

Not delivered here, and deliberately:

- The mail, series, maintainers, forge and cosmetic lanes the FFmpeg pack carries. Those
  encode a mailing-list submission workflow that `openwrt/packages` does not have; it
  takes pull requests. Cloning a lane nothing reads would put dead code behind a tier.
- Any check that needs a build. The OpenWrt manuals state no build-time rule, so there is
  no `build` lane and no attested tier drawn from one.

## The four lanes

Each lane is one manual, and the manual's own Checklist section is the lane's rule list.

| Lane | Reads | Manual |
|---|---|---|
| `meta` | `TITLE:=` and `define Package/<name>/description` in a package Makefile | Writing TITLE and description for an OpenWrt package |
| `comment` | comments in the files OpenWrt writes, never a patch body | Writing comments in an OpenWrt package |
| `msg` | one commit message | Writing a commit for an OpenWrt package |
| `pr` | the body of a pull request, handed in | Writing a pull request for openwrt/packages |

The `pr` lane differs from the other three in where its subject lives. A Makefile, a comment and
a commit message are all in the clone; a pull request body is on GitHub and nothing in a clone
records it. That lane therefore reads an argument or standard input and can never run as a
repository sweep, which is a shape the pack has to carry deliberately rather than discover when
someone points it at a directory and gets silence.

It is also the one lane with a real upstream artefact behind it.
`.github/pull_request_template.md` is a file the project ships and GitHub prefills, so the rules
keyed to its headings cite something rather than measure it. That artefact is **referenced and
resolved at check time, never embedded**, by [call/0055](../../call/0055-upstream-artefacts-are-referenced-not-embedded.md):
a vendored copy would be wrong the moment upstream edited it, and wrong silently. A short-lived
gitignored cache is permitted so a sweep does not refetch, but it may only hold what the canonical
location returned and may never change a verdict. When the template cannot be resolved, the rules
keyed to it do not run and say so; they never fall back to the copy quoted inside
`openwrt-pr-style.md`, which is illustration and not the artefact.

The rules about *filling* those headings stay measured and stay offline, and that is where the
finding is: a template body keeps the testing lines about 95% of the time and gives them a value
only about two thirds of the time.

The `comment` lane carries a provenance guard the other two do not need. A package
directory mixes OpenWrt's own files with upstream's source, and every line a patch adds is
upstream's in upstream's style. The lane must read a patch header before it treats a patch
as carrying local prose: a file opening `From <40-hex-sha>`, or carrying `From:` and
`Subject:`, is a cherry-picked upstream commit and is exempt. Two thirds of the tree's
patches were written locally and one third were not, so directory alone cannot decide it.
Getting this wrong restyles an upstream author's words, which is the one failure in these
three manuals that damages something outside the repository.

## Sources and pinning

The manuals are Claude artifacts, not files in a tree the pack can fetch, so the pack
vendors them under `fixtures/manuals/` and pins the vendored copies by digest. A
`PROVENANCE.md` beside them records, for each: the artifact identifier, the date read, and
the upstream state the figures were measured against. The four rest on three different bases,
which the provenance file keeps apart because their shares are not interchangeable: the
description and comment manuals were measured at `1d40ad929a` on `master` dated 2026-06-07;
the commit manual against the full history, 27197 non-merge commits; and the pull request
manual against 5039 merged pull requests read from the GitHub API, with a targeted sample of
683 behind its new-package figures.

The commit manual's Exemplars are fenced `host-lint:ignore`. Vendor them intact: they quote
real commit subjects, and the prose audit would otherwise fire on the quoted text.

## Tiers

The tier says how much a finding is worth, and it is a claim about detectability, not about
importance. The same three the FFmpeg pack uses:

- **mechanical**, decidable from the artefact with no judgement. A trailing full stop, a
  tab indent, a missing sign-off, a line past 80 columns.
- **heuristic**, decidable with a false-positive rate. Whether a description lists features,
  whether a comment says what rather than why.
- **attested**, not mechanically decidable. Whether the comment explains something the line
  could not show; whether the commit holds one concern.

A rule whose manual reports a share becomes that rule's `measured_rate`, and the recent
column is the honest one where a convention has moved: two-space indent is 52.5% across the
tree and 87.8% among 2025-2026 additions, and the rule follows the newer figure.

## Build sequence

### vendor-manuals {#vendor-manuals}

Create the crate, add it to `members` and `default-members`, and vendor the three manuals
under `fixtures/manuals/` with `PROVENANCE.md`. Verify by: `cargo build` from the workspace
root produces `host-lint-openwrt`, and a test asserts each vendored manual matches its
recorded digest.

### rule-registry {#rule-registry}

Encode the corpus: `Source` per manual, `Section` per manual heading, `Rule` per checklist
line, each naming its section and carrying its tier, lane and measured rate. Carry the
completeness test across, so a manual heading that states rules and has no rule encoded
against it reddens. Verify by: the completeness test passes, and deleting a rule fails it.

### meta-lane {#meta-lane}

Check `TITLE:=` and the description block: noun phrase, capitalised, no full stop, three to
seven words, does not name OpenWrt; description two-space indent, one or two lines, under 80
columns, present tense, ends with a full stop, and none of the five prohibitions. Verify by:
the seven Exemplars pass clean and each cited counter-example flags its own rule.

### comment-lane {#comment-lane}

Implement the provenance guard first, then the form rules: own line, column 0, lowercase
opening, no closing full stop, one line, no trailing inline comment, no commented-out code.
Exempt the licence header. Verify by: the six Exemplars pass, a patch body carrying an
upstream comment is skipped, and a locally-written patch is read.

### msg-lane {#msg-lane}

Check subject shape `<package>: <what you did>`, lowercase after the colon, no full stop,
under 72 columns, bare package name rather than a path; body present and wrapped; sign-off
present and matching the author. Verify by: the four Exemplars pass and each "Do not" case
flags.

### pr-template-resolver {#pr-template-resolver}

Implement [call/0055](../../call/0055-upstream-artefacts-are-referenced-not-embedded.md) before
the lane that depends on it: resolve `.github/pull_request_template.md` from a given
`openwrt/packages` checkout or from the published raw file, cache it briefly under a gitignored
path, and record the last-seen digest so a moved template reports as drift. Verify by: a resolved
template yields its headings, a second run inside the lifetime does not refetch, an expired or
absent cache with no reachable source returns unresolved rather than a stale hit, and no code path
reads the fence inside `openwrt-pr-style.md`.

### pr-lane {#pr-lane}

Check a pull request body handed in on standard input or as a file argument: template headings
kept, maintainer a GitHub handle, description one or two lines, version and target and device
each named rather than left blank behind a kept label, the CONTRIBUTING box ticked, and the
patch section either deleted or ticked truthfully. Refuse a directory argument rather than
sweeping, because the subject is not in the clone. Split the rules by what they need: the
heading-matching rules consume the resolver and do not run without it, while the filling rules
are measured and stay offline. Verify by: the quoted exemplar passes clean, a body with
kept-but-empty testing labels flags, a directory argument exits with the refusal rather than
silence, and an unresolved template leaves the heading rules unrun and named in the output while
the filling rules still report.

### docs-and-calibration {#docs-and-calibration}

Generate `RULES.md` from the registry with a `make-rules-doc.sh`, and write `CALIBRATION.md`
recording each measured rate and the table it came from. Verify by: a drift test regenerates
the doc and fails if it differs from the committed one.

### release-and-repin {#release-and-repin}

Run the tool-carried release for host-lint, push the worktree, tag, then re-pin
`.host-software` and record the receipt. Verify by: `host-lifecycle software --check .`
returns to green with every component at its pin.

## The delivery boundary

Committing in the worktree moves its HEAD past the recorded pin, so
`host-lifecycle software --check .` goes red from the first commit until the re-pin in the
final task. That red is expected and is not drift. A session that stops before the release
cascade must say so, because a clean `--check` is the signal the rest of the tooling trusts.
