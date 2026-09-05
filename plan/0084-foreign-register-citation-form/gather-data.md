# gather-data: the four-form re-run, the corpus, the URL bar, the protocol (2026-09-05)

This records the #gather-data node. Everything here was measured before the spec was written.

## The binary identity

`host-lifecycle --version` answers `host-lifecycle 0.50.0`; the worktree `software/host-lifecycle/main` sits at `66c24d6` (release v0.50.0) with a clean tree, which is the pin `.host-software` records. The PATH copy is a cargo-installed glibc build of that revision; its hash differs from the recorded canonical artifact because the canonical artifact is the musl target, not because the binary is stale (the identity rule from the 2026-08-02 entry: hash against the record, and the record names the musl target). The probes below measure behavior at the pinned version.

## The four-form re-run

The issue's repro, rebuilt as a scratch repository carrying a `call/` room with one entry and a document citing records that room does not hold, swept with the pinned binary. Every form the issue reported DEAD reproduces; the code span stays clean; exit 1:

| form | line | verdict on v0.50.0 |
|---|---|---|
| bare prose: `per agentic-host call/0039 the layout holds` | DEAD | `call/0039 names no entry in that room` |
| qualified prose: `recorded as agentic-host plan/0077` | DEAD | same class |
| link label matching the URL: `[agentic-host call/0039](…/blob/main/call/0039-….md)` | DEAD | same class |
| link label not matching: `[bare-store decision](…/blob/main/call/0039-….md)` | DEAD | same class |
| code span: `` `call/0039` `` | clean | absent from the verdict, as the issue recorded |

Three boundary shapes the design must judge were added to the same document, and the pinned binary already answers all three the way the cut README settles them:

- a relative target naming an absent record (`[a local record](call/0042-nothing.md)`) is DEAD, the token inside the relative URL being detected like prose;
- a foreign URL naming a different file than the label claims (`[call/0039](…/call/0044-prose-lexicon.md)`) produces two findings today, and under the accepted form the label stays DEAD (the mismatch) while the URL's own token becomes an accepted citation, the URL naming a record that really exists in the foreign register;
- a URL naming a section of an index rather than the record (`[plan/0077](…/PLAN.md#open-work)`) stays DEAD, because the path never contains the `plan/0077` segment.

## The corpus

Counted 2026-09-05 against host-template `933b7f1` and the whole tracked tree:

- the template's upgrade ledger carries **six** prose citations: `call/0046`, `call/0047`, `plan/0077`, `plan/0078`, `call/0051`, `call/0052`, all of the form "Recorded as agentic-host …" inside the excluded record layer;
- **zero** accepted-form (link-shaped) citations exist in any tracked document, which is expected: no such form is accepted, so nobody can write one;
- the count is revision-dependent: the template at the earlier pin carried a seventh citation (`call/0045`), whose entry text the lem-revision bump reworded. The population is whatever the record says at the revision being swept, which is one more reason the form, not the count, is what the tool judges.

The accepted form therefore lands with no remediation wall. The six ledger citations stay as they are: the ledger is append-only, its file is excluded, and the doctrine sentence written later tells new authors the link form.

## The URL bar

The rule this plan implements, grounded in the shapes this tree's own documents actually write:

1. **Segment containment.** An absolute URL names the cited record when its path contains the segment `{room}/{NNNN}` after the repository part. `…/blob/main/plan/0077-reference-resolver/README.md` qualifies; `…/PLAN.md#open-work` does not.
2. **The revision is irrelevant.** The ref between `/blob/` (or `/tree/`) and the path may be a branch (`main`, `proposals`) or a commit; the check judges the file, never the revision, because form is the claim and existence is not checkable offline.
3. **`blob` and `tree` both qualify.** A milestone record is a directory (the `tree` view) and a decision record is a file (the `blob` view); the tree writes both shapes (`/blob/main/host-lint-ffmpeg/RULES.md`, `/tree/main/skills`).
4. **A trailing anchor is ignored.** `…/call/0039-bare-store-is-dot-bare-with-a-git-file.md` anchors nothing; an anchored URL still names the file.
5. **Foreign means the full slug differs.** The comparison is `owner/repo` against the local `origin_slug`, never the repository name alone: this tree cites `slartibardfast/calx-knap`, whose repository name differs from everything local anyway, but the owner half is what makes two same-named repositories distinct.
6. **Any forge host qualifies.** The URL's host is read, not matched against the local forge; `origin_host` is already forge-aware in the tool.
7. **The form mints nothing.** Checked against call/0057: a URL to another repository's file posts no cross-reference on the target, so directing an author to write one never publishes; the doctrine must stay free of `owner/repo#N`-style spellings, which do mint.

Origin-absent repositories: the design reads foreign by default. An absolute URL visibly names another repository, and treating it as dead would gate the rare offline or remote-less clone on a link that is honest on its face; the disclosure names the condition either way.

## The protocol

The weak-agent acceptance runs on the real qwen3.5-4b through the gateway behind TLS at `api.d07yx58.net`, under the plan/0076 corrected protocol exactly as plan/0080's thinking kit records it: thinking enabled through the chat template (`enable_thinking: true`), the model card's thinking-general parameters, the answer read after the closing `</think>`, two draws per probe, results appended after every cell so a mid-run failure preserves the completed ones. The parameters, as the kit carries them:

```
temperature 1.0, top_p 0.95, top_k 20, min_p 0.0,
presence_penalty 1.5, repetition_penalty 1.0, max_tokens 32768
```

The two recorded lessons are binding on the kit this plan builds: check a new kit against the last corrected protocol before running it (the plan/0080 kit had regressed against a correction that lived in a script comment), and record protocol corrections beside the prompts the next kit is built from. plan/0080 preserves the no-think runner and its truncated run beside the corrected one; they are the labeled counterexample.
