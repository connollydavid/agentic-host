# plan/0045: The embedded prose engine catches up

plan/0044 taught host-lint's prose lane to honor the per-repo LEXICON, so a legitimate
domain noun a project declares stops reading as an ai-diction trope. host-lifecycle runs
that same lane in-process for its verify-phase prose recheck (`host-lifecycle prose`, the
`--docs` engine via the linked `host_lint` crate), so the gate needs no host-lint on PATH.
But host-lifecycle embedded the crate at an older revision, before the mask existed, so the
recheck ignored the LEXICON the standalone binary already honored.
connollydavid/host-lifecycle#2 reports the divergence. This milestone shares host-lint's
docs engine into its library, so the binary and the embedded copy run one engine and cannot
drift, then bumps host-lifecycle onto it.

## Problem

The prose mask (`mask_allowed`) lived in the `host_lint` library and was current. But
host-lifecycle's `prose_audit` reimplemented the `--docs` walk and called `scan_prose_text`
at the crate revision it pinned, host-lint v0.8.1, whose signature had no allowlist
parameter. The embedded engine could not consult the LEXICON even in principle: it received
no phrases to mask. Because `host-lifecycle prose` exits non-zero on any warning, an adopter
with a legitimate flagged domain noun on a governed surface, the case the issue names, had a
permanently failing verify recheck and no remedy, since the sanctioned escape (declare the
phrase in LEXICON) was the one path the embedded engine never took.

The loader (`load_lexicon`) and the walk (`run_docs`) lived in host-lint's binary; the
library held only the parsing primitives, so host-lifecycle had no shared entry point to
call. The reimplemented walk was itself the drift surface: even with the crate bumped, an
embedder that re-derives the loader and walk by hand stays one edit away from lagging again.

## Decision (operator)

Share the engine into the library, rather than replicate the loader inside host-lifecycle.
`Lexicon`, `load_lexicon`, and `run_docs` move into the `host_lint` library as public
functions; host-lint's binary calls them; host-lifecycle calls the same functions. The
embedded prose recheck becomes a thin call into the shared engine, so a future host-lint
change to the loader, the walk, or the mask reaches the embedder on the next bump with no
hand re-derivation. The operator chose the shared-library path over the one-release
replicate-in-host-lifecycle path precisely because the bug is an instance of embedded-engine
drift, and the fix should close the class, not the instance.

## The design

### Loader and walk in the shared library

`Lexicon` plus `load_lexicon` and `run_docs` become public in `host_lint`'s lib. `run_docs`
returns a `Result` instead of exiting the process, so host-lint's binary prints the error and
exits while an in-process embedder surfaces it as it chooses. host-lint's CLI behavior is
unchanged, confirmed against the fixture: a LEXICON-declared phrase clears the trope (exit 0),
an undeclared occurrence still warns (exit 3), and the git-failure message and exit code are
byte-identical to before.

### host-lifecycle calls the engine

`prose_audit` shrinks to `host_lint::load_lexicon(root).phrases_lc` plus
`host_lint::run_docs(root, &allow, &ignore)`. The reimplemented walk is gone, so the walk, the
loader, and the mask are all shared with the standalone binary. A regression test pins the
fix: a declared phrase clears the trope in the in-process audit, and an undeclared occurrence
of the same word still warns.

### The moved dependency needs a fresh bundle

host-lifecycle pins host-lint by git revision and builds offline from a hash-pinned vendor
bundle (plan/0032). Bumping the revision is the first dependency move since the bundle was
cut, so the shared bundle is regenerated as `vendor-v2`, covering host-lint v0.10.2's source,
and host-lifecycle's `deps-bundle` is re-pinned in `.host-software` and `deps-bundle.lock`.
host-lint stays on `vendor-v1`: its own closure is unchanged, and its build ignores the
host-lint-crate entry the bundle also carries.

### No spine change

The doctrine, that a legitimate tell-shaped token stays in the per-project LEXICON for both
lanes, is met rather than changed, so host-template carries no new UPGRADING entry; an adopter
reads the corrected behaviour on the next host-lifecycle bump. The meta-repo prose CI pins
(host-template, host) move to v0.30.1 so their own prose gate runs the same engine.

## Build sequence

### Diagnose and reproduce {#reproduce}

Build a minimal fixture (a tracked doc whose ai-diction noun is declared in a sibling LEXICON)
and confirm the divergence: standalone `host-lint --docs` masks the phrase and exits clean,
while `host-lifecycle prose` warns and exits non-zero on the same repo. Trace the root cause
to the embedded crate revision whose `scan_prose_text` takes no allowlist.

- verify: attested operator

### Share host-lint's docs engine into the library {#share-engine}

Move `Lexicon`, `load_lexicon`, and `run_docs` into the `host_lint` library as public items;
have the binary call them; make `run_docs` return a `Result`. Regression tests pin the loader
and the masked walk. host-lint's CLI behavior stays identical, and clippy is clean.

- depends: #reproduce
- verify: cd software/host-lint/main && cargo test

### host-lifecycle consumes the shared engine {#consume-engine}

Bump the host-lint dependency to v0.10.2, rewrite `prose_audit` to call the shared loader and
walk, and add the LEXICON-masking regression test. The rebuilt binary clears the fixture: a
declared phrase exits clean, an undeclared occurrence still warns.

- depends: #share-engine
- verify: cd software/host-lifecycle/main && cargo test

### Regenerate the vendor bundle for the moved dependency {#vendor-v2}

Produce `vendor-v2` from host-lint's manifest synced with host-lifecycle's, covering host-lint
v0.10.2's source, publish it, and re-pin host-lifecycle's `deps-bundle`. The offline
`--network none` release build reproduces the canonical hash.

- depends: #consume-engine
- verify: attested operator

### Re-pin, bump CI, and close {#release-and-close}

Release host-lint v0.10.2 and host-lifecycle v0.30.1, re-pin `.host-software`, bump the five CI
install revisions, record the release receipts, and close the issue. `software --check` is
clean and the whole suite is green.

- depends: #vendor-v2
- verify: attested operator

## Risks

- The loader and walk now live in the library, so an embedder and the CLI share one code path.
  A bug in `run_docs` would reach both, but a single shared path is the point: it removes the
  drift this milestone fixes, and the path is covered by tests on both sides.
- Regenerating the vendor bundle is the documented cost of moving a pinned dependency. The new
  bundle is hash-pinned and its offline build is verified by the release gate, so a wrong
  bundle fails the gate rather than shipping.

## Status

complete, released as host-lint v0.10.3 (`63348a6`, artifact `753ac4f6`) and host-lifecycle
v0.30.1 (`46d481c`, artifact `23c27bff`, on `vendor-v2` sha `4e49536b`); host-lifecycle embeds the
host-lint library at v0.10.2 (`5a9d2c5`), which is engine-identical to v0.10.3. host-lint's
`Lexicon`, `load_lexicon`, and `run_docs` are public library items; its binary and
host-lifecycle's `prose_audit` call the same engine, so the embedded prose recheck cannot lag
a future host-lint change. The fixture confirms the fix end to end: with the LEXICON the
recheck exits clean, without it the trope still warns. host-lint's standalone `--docs` behavior
is byte-identical across the refactor. The shared bundle was regenerated as `vendor-v2` so the
offline release build sees host-lint v0.10.2; host-lint stays on `vendor-v1`. The five CI
install pins (agentic-host reproducible-build and mdbook, host-template and host prose) move to
v0.30.1. No spine change, since the doctrine is met rather than changed. `software --check` and
the fixture are green; connollydavid/host-lifecycle#2 is closed.

host-lint was first tagged v0.10.2 at `5a9d2c5`, but the `src/lib.rs` edit staled its two kani
obligation digests (`DetectInternalCodeAsName`), so that tag's CI failed the obligations staleness
lint (the kani proofs and all six binaries passed). The digests were re-derived by fingerprinting
the new source (`git hash-object src/lib.rs` into `host-lint.obligations.digests`), which is
artifact-preserving because the ledger is not compiled, and promoted into a clean v0.10.3 tag, the
pinned release. v0.10.2 stays a superseded tag. host-lifecycle keeps embedding the host-lint
library at `5a9d2c5` (engine-identical to v0.10.3), so no vendor regeneration or host-lifecycle
re-release was needed.
