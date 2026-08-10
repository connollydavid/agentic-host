# call/0057: a remedy must know whether its artefact publishes

- Status: accepted
- Scope: host-lint's identifier-tier remedy; where a tracker reference's backing URL is allowed to live; what the tool must know about the artefact it is correcting before it names a fix
- Date: 2026-08-10

## Context and problem

The identifier tier refuses an un-cited tracker reference and tells the author to declare it with a
backing URL, through `host-lint lexicon add "<phrase>" --url <url>`. The guard is sound: a bare
`#7` names no repository, and a citation that cannot be resolved is not a citation.

The remedy is not. On a public repository, GitHub mints a cross-reference on the target whenever a
commit naming it is pushed, and it does so for both spellings the guard accepts, `owner/repo#N` and
the URL. That was measured rather than assumed: one commit through each form, each producing an
entry on the target thread. So the sanctioned fix for a hygiene finding is the thing that posts
into someone else's issue, and a branch amended and force-pushed during review posts once per
rewrite.

The governance repository is the one that suffers. `agentic-host` cites other projects' trackers
constantly, because that is what a methodology repository does, and every such citation carried in
a commit message pulls this repository into an upstream thread that never asked for it.

Underneath sits the actual defect: **host-lint has no notion that a commit message publishes in a
way a file does not.** It lints a message and a markdown file through the same tiers and offers the
same remedy, because from inside the linter both are text. They are not. A file changes a working
tree; a pushed commit message is delivered to every watcher of every repository it names. A tool
that recommends an edit is responsible for where that edit ends up, and this one cannot currently
tell.

## The distinction that settles it

The guard and the remedy were fused, and they separate cleanly.

- The **guard** is about resolvability: does this reference name a repository? That is a property
  of the reference and is right to enforce everywhere, unchanged.
- The **remedy** is about where the resolving evidence is written. That is a property of the
  artefact under correction, and it is the half that has to become artefact-aware.

The LEXICON file is the answer already sitting in the tool. It is a file. A file mints no
cross-reference, it is reviewed with the change, and it is exactly the declared-vocabulary store
this project already trusts. The URL belongs there. It never belonged in the commit message.

## Decision

1. **The backing URL lives in the LEXICON, never in an artefact that publishes.** For a commit
   message, the remedy is `host-lint lexicon add`, and the message itself keeps the bare token. The
   declaration resolves the reference for a reader without posting anything to the target.
2. **host-lint learns the publishing surface of what it is linting.** A commit message is a
   publishing artefact. A tracked file is not. The `commit` verb and the commit-msg hook lint a
   publishing artefact by construction, which is enough to decide the tier without inspecting
   remotes.
3. **A remedy naming a form that publishes is never emitted for a publishing artefact.** The
   remedy text is selected by surface, not by tier alone. This is a floor, matching the ones in
   [call/0054](0054-one-commit-message-fault-earns-a-detector.md),
   [call/0055](0055-upstream-artefacts-are-referenced-not-embedded.md) and
   [call/0056](0056-a-tool-dependency-is-a-floor-checked-in-the-lane.md): the tool states what it
   could not do rather than doing the harmful thing quietly.
4. **The guard is unchanged.** A bare numeral naming no repository still fails. Nothing here
   loosens what counts as a citation; it moves where the citation is recorded.

## Consequences

An author correcting a commit message now edits two things, the message and the LEXICON, where
before they edited one. That is the cost, and it buys back a side effect the author could not see
and did not choose. The LEXICON edit is also the durable one: the next occurrence of the same
reference is already declared.

This is the first rule in host-lint keyed to *where output goes* rather than to what the text says,
so it opens a question this decision does not answer: whether other remedies carry the same
hazard. A pull request title becomes a squash-merge subject and so becomes a commit message, which
suggests they do. That sweep is not in scope here and is recorded as owed rather than assumed
clean, because the failure this decision fixes was invisible for as long as it was: the tool was
confidently right about the tell and confidently wrong about the fix, and nothing in the verdict
could have shown the difference.
