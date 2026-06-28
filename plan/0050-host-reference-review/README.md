# plan/0050 host-reference review: findings from the reference-compiler audit

This milestone records a maximum-effort review of `host-reference`, the reference compiler
delivered by plan/0049. It is a findings record, not a remediation plan: nothing here is fixed
in this milestone. Each finding carries its file, its mechanism, and the concrete input that
triggers it, so a later remediation plan can pick the work up cold. The disposition for every
finding below is the same — *recorded, remediation deferred* — and is not repeated per entry.

## What was reviewed

- Repository: `connollydavid/host-reference`, pull request #1, "host-reference: external reference compiler".
- Head: `review/0049` at `ea92185` (identical to `host-reference` `main`, released v0.1.1).
- Base: `review-base/scaffold` at `88c6bcf`.
- Diff: 174 files, about 11,219 insertions and 38 deletions — roughly forty feature-gated
  normaliser crates plus the shared `core`, the `cli`, the `overlay` crate, the `.allium`
  specification with its obligations manifest, the `deny.toml` licence lane, and the CI workflow.

The review ran locally at maximum recall (the cloud `code-review ultra` lane was unavailable, so its
local fallback ran): ten independent finder angles in parallel — five correctness groups across the
crates, plus the overlay lens laws, a cross-cutting determinism audit, the CLI and core dispatch, the
conformance harness and removed-behaviour audit, the specification and CI coverage, and a reuse and
altitude pass — followed by targeted verification (several findings were confirmed by executing the
code at the reviewed revision) and one gap sweep. Findings were deduped and ranked.

## The contract the findings test against

Every reader implements one trait, `Normalizer` (`crates/core/src/lib.rs`): `skeleton` returns the
`Tier0` skeleton, `view` a windowed `Tier1` slice, `put` a write-back patch. The invariants the
findings measure against:

- **Determinism is the premise.** A `skeleton` output is serialized by `core::serialize_tier0` and
  compared byte for byte against a committed golden fixture in each crate's `tests/conformance.rs`.
  The component's whole claim is that output is "a pure function of the source bytes and the pinned
  toolchain" (call/0018, call/0030). Any non-determinism that reaches serialized output is a real
  defect.
- **Refusals are explicit (call/0031).** A parse that hits a resource bound or a hostile structure
  must return `Error::Refused` (or `Error::Parse`). A panic, a hang, or a silent partial on malformed
  input is forbidden.
- **The source map is faithful.** Each `Span.origin` is a byte range into the source; it must satisfy
  `start <= end <= len` and point at the true origin of the region it labels.
- **String slicing in Rust panics** on a non-char-boundary or out-of-range index, so any `view` or
  `skeleton` that slices a `&str` by a computed offset on arbitrary input is a panic candidate.

## Correctness findings, ranked

The fifteen most severe, in order. The line numbers are at the reviewed revision.

1. **A `view` selector with a large length overflows and panics instead of refusing** —
   `crates/cli/src/main.rs` `parse_selector` (the root) and every `view` `CharOffset` arm
   (`crates/data/src/lib.rs:75`, `config:59`, `prose:123`, `asciidoc:54`, `bibtex:52`, `org:51`,
   `rst:54`, `html:92`, `netlist:110`, `vector:106`, and `calendar`). `parse_selector` accepts an
   unbounded `len`; each `view` computes `s + *len` *before* `floor_boundary` clamps it.
   `host-reference view notes.txt --select offset:1:18446744073709551615` panics with "attempt to add
   with overflow" in a debug build; in release the sum wraps below `s`, `floor_boundary` returns
   `end < start`, and `text[start..end]` panics "slice index starts at 1 but ends at 0". Confirmed by
   execution. The contract demands a clean `Error::Parse`. Fix belongs at the source, in
   `parse_selector` (a `checked_add` or an explicit bound).

2. **No reader ever constructs `Error::Refused`; the hostile-input obligation is waived but
   unrealised** — `host-reference.obligations` (the `RefuseHostileInput` disposition). A grep for
   `Error::Refused` across `crates/**/lib.rs` matches only the `core` enum definition; no reader
   builds it, and `Source` carries no size or trust field. The obligations manifest waives
   `RefuseHostileInput` as "realised per reader as `Error::Refused` where a bound is hit," but that
   realisation does not exist, and the obligations check only verifies that test *names* resolve, so
   CI stays green. Every malformed or oversized untrusted document therefore hits a panic, a hang, or
   a silent partial — the exact call/0031 failure the spec forbids. Findings 3, 4, and the further
   findings on the office, EPUB, and audio-visual readers are concrete instances of this systemic gap.

3. **The PDF reader aborts the process on many loadable PDFs** — `crates/pdf/src/lib.rs:60` (and the
   `view` path at `:42`). `pdf_extract::extract_text_from_mem` carries roughly twenty `panic!`/`todo!`
   sites for structures `lopdf` loads but `pdf-extract` 0.12 does not handle (an unsupported CMap, an
   image soft mask, a missing glyph width). The call site maps `Err`, not an unwind, so a single
   crafted-but-loadable PDF aborts the CLI instead of returning `Error::Refused`. (Mechanism certain;
   the trigger is a specific PDF.)

4. **The calendar reader returns success on malformed input** — `crates/calendar/src/lib.rs:94`.
   `calendar_shape` (and `vcard_shape`) match only `Entry::ICalendar`/`Entry::VCard`; calcard's error
   variants (`InvalidLine`, `UnterminatedComponent`, `UnexpectedComponentEnd`) are dropped. A
   truncated `.ics` (a `BEGIN:VCALENDAR` with no matching `END`), or pure garbage, returns
   `Ok("calendar: 0 components")` — a silent partial the contract bans. (The parser terminates, so
   this is a silent-success bug, not a hang.)

5. **An overlay `TextQuote` selector silently re-anchors to the wrong occurrence** —
   `crates/overlay/src/lib.rs:54`. When the `prefix + exact + suffix` context no longer matches (for
   example after a re-derivation drops surrounding text), resolution falls back to `text.find(exact)`,
   the *first* bare occurrence. For `"on the cat, off the cat"` with `prefix:"off "`, the annotation
   re-anchors to offset 0 instead of 12, and `write_back` then splices the edit into the wrong span
   with no ambiguity error — the opposite of the "survives re-derivation" property selectors exist to
   provide. Confirmed by execution.

6. **The image and OCR readers claim the same extensions; the image reader wins and OCR is dead** —
   `crates/cli/src/main.rs:95` and `:99`. Both `detect` exactly `png|jpg|jpeg|gif|bmp|tif|tiff|webp`,
   and `pick` returns the first reader whose `detect` is true, in registry-push order; `image` is
   pushed first. A build with both features (`--features "image ocr"`) routes every raster to image
   metadata, so the OCR reader never runs. The recognised-text path is silently unreachable in that
   configuration.

7. **A format hint is not lowercased, so an uppercase extension is reported unsupported** —
   `crates/cli/src/main.rs:124`. Every `detect` matches lowercase tokens only. `host-reference
   skeleton README.MD` (or `PHOTO.JPG`, `data.JSON`) yields "unsupported: no normaliser is registered
   for this kind" even with the relevant feature enabled. Common, legitimate input is rejected.

8. **The prose and HTML heading outlines ignore fenced code blocks** — `crates/prose/src/lib.rs:89`
   and `crates/html/src/lib.rs:38`. A line beginning with `#` then a space is treated as an ATX
   heading with no fence awareness, so a `#` line inside a triple-backtick block is emitted as a
   spurious outline entry, with a source-map span pointing at the code line. Wrong skeleton on very
   ordinary Markdown.

9. **The out-of-process helpers are resolved by PATH or an environment variable and are not pinned**
   — `crates/ocr/src/lib.rs:74` and `crates/openscad/src/lib.rs:82`. The skeleton body and token
   counts of these two readers are the stdout of `host-reference-ocr-helper` /
   `host-reference-openscad-helper`, selected from `HOST_REFERENCE_OCR_HELPER` /
   `HOST_REFERENCE_OPENSCAD_HELPER` or a bare PATH lookup, neither of which is in `Cargo.lock`. The
   same source bytes yield different attested skeletons across machines or helper versions — directly
   against the "pure function of the source bytes and the pinned toolchain" premise. The goldens stay
   green only because the conformance tests stub the helper.

10. **Both out-of-process helpers stage input at a predictable shared temp path** —
    `crates/ocr/src/lib.rs:80` and `crates/openscad/src/lib.rs:89`. The path is
    `temp_dir()/host-reference-ocr-<content_id>.<ext>` (and the OpenSCAD analogue), fully predictable
    from the bytes, opened with `File::create` (follows symlinks, truncates) and removed
    unconditionally. A pre-planted symlink at that path is followed and its target truncated (a local
    symlink attack); two concurrent calls on the same bytes collide, one's truncate or `remove_file`
    racing the other's helper read, producing intermittent "helper failed" — non-deterministic. An
    `O_EXCL` temp file with a random suffix is the fix.

11. **The overlay lens is not very-well-behaved, and the proptests do not test the law they name** —
    `crates/overlay/tests/lens_law.rs:45` (and `:6`). The fixed-offset splice lens violates PutPut
    whenever a replacement's length differs from the span it replaces: for `"abcdef"`, origin `2..4`,
    `v="X"` then `w="QQ"`, `put(put(s,v),w)` is `"abQQf"` but `put(s,w)` is `"abQQef"` (confirmed by
    execution), so the "well-behaved lens" claim in `src/lib.rs:5` is only partly true. The PutPut law
    is neither stated nor tested, and the `put_get` test re-implements the splice formula as its own
    oracle rather than composing a read-back through `get`, so it cannot catch a `get`/`put` mismatch.

12. **CI never compiles the CLI with any non-default reader feature** — `.github/workflows/ci.yml`
    (the `build`, `test`, and `lint` jobs). The build uses default (`text`) features;
    `cargo test --workspace` and `cargo clippy --workspace --all-targets` build the `host-reference`
    crate with default features too. Each reader crate is exercised as a workspace *member*, but the
    CLI's `#[cfg(feature = "office")]` (and the other sixteen non-default) `reg.push(...)` arms and
    their `use` imports are compiled by no job. Rename a type in a heavy reader and forget the CLI:
    CI is green, but `cargo build --features office` breaks for a consumer. A `--all-features` (or
    per-feature) compile job closes it.

13. **A reStructuredText section title drops all inline markup** — `crates/rst/src/lib.rs:108`.
    `inline_text` collects only `TextOrInlineElement::String` children, so a title with emphasis,
    strong, or literal markup renders with those portions silently omitted: ``Install ``pip`` `` yields
    `Install `, and a title that is entirely markup (`*Important*`) yields an empty or `(untitled)`
    entry. Wrong outline in the attested skeleton.

14. **The SPICE net heuristic counts comments and value tokens as nets** —
    `crates/netlist/src/lib.rs:73`. Every token between the first and the last on a line is treated as
    a net, so `R1 in out 1k ; load resistor` yields nets `{in, out, 1k, ;, load}` (five) rather than
    `{in, out}`, and `V1 in 0 DC 5` yields `{in, 0, DC}`. The wrong (but stable) net set is baked into
    the conformance golden.

15. **The canonical serialized form has no delimiter escaping, so document content can inject a
    section break** — `crates/core/src/lib.rs:199` together with the data reader's `field`/`shape`
    (`crates/data/src/lib.rs`). `serialize_tier0` emits the markdown body verbatim between the literal
    lines `== markdown ==`, `== source-map ==`, and `== tokens ==`. The data reader interpolates JSON
    object keys (and CSV headers) into the body unescaped, and a JSON key may contain a real newline.
    A document `{"x\n== source-map ==\ny": 1}` injects a second literal `== source-map ==` line into
    the markdown section, so any consumer that parses the canonical attested form mis-splits it. The
    form needs an escape or a length-prefixed framing.

## Further correctness findings

Beyond the ranked fifteen, all real, cut only by the output cap:

- **The HTML `view` reports the wrong source-map origin** — `crates/html/src/lib.rs:99`. `view`
  returns a slice of the *converted* markdown (`md[start..end]`) but reports `origin: 0..bytes.len()`,
  the raw-HTML byte length. The span neither reflects the returned window nor points at the true
  origin of the returned text, breaking the bidirectional source map. (The `data` `view` is correct
  because its text is the source bytes; the HTML conversion makes the offsets incomparable.)

- **The PDF title is decoded as UTF-8 when PDF strings are commonly UTF-16BE** —
  `crates/pdf/src/lib.rs:76`. `pdf_title` runs `from_utf8_lossy` over the Info `/Title` bytes; a
  Word- or Acrobat-exported title carried as UTF-16BE (BOM `0xFEFF`) decodes to mojibake. Wrong, but
  deterministic, skeleton output.

- **The Parquet conformance golden is pinned to the `parquet-rs` patch version** —
  `crates/columnar/tests/conformance.rs` and its golden. The test generates the Parquet buffer in
  memory; the bytes embed `created_by = "parquet-rs version X.Y.Z"`, so the golden's content id
  (`e9b68265a677`) and `raw_tokens` (721) are a function of the dependency version, not the source.
  `Cargo.toml` pins `parquet = "59"` (a caret range), so a routine `cargo update` within the range
  changes the golden and the test fails with a confusing "tier-0 drifted" message unrelated to any
  source change. The Arrow golden is immune (Arrow IPC embeds no version string), which makes the
  asymmetry concrete. `--locked` CI does not flake; a maintainer bumping the lock would.

- **The audio reader fabricates a duration from a hostile chunk size** — `crates/av/src/lib.rs:92`.
  `audio_shape` trusts the declared data-chunk count; a WAV with a bogus `data` size (`0xFFFFFFFF`)
  yields an "attested" duration that is a lie derived from the header, where the contract wants a
  refusal.

- **The audio-visual reader can panic on a malformed MP4 box** — `crates/av/src/lib.rs:103`. An MP4
  whose 32-bit box size is smaller than the 8-byte header, or larger than the file, can drive an
  under/overflow in `mp4` 0.14's box parsing; the panic propagates out of `skeleton` (no
  `catch_unwind`) instead of refusing. A concrete instance of finding 2.

- **The office and EPUB readers have no resource bound** — `crates/office/src/lib.rs:53` and
  `crates/epub/src/lib.rs:55`. Raw bytes go straight to `undoc` / `rbook`, whose zip layer
  decompresses parts without a cap, so a small deflate-bomb archive expands to multiple gigabytes and
  OOMs or hangs rather than refusing. Concrete instances of finding 2.

- **A degenerate overlay `TextQuote` resolves to an empty span rather than `None`** —
  `crates/overlay/src/lib.rs:50`. An empty `exact` makes `str::find("")` return `Some(0)`, so a
  meaningless selector resolves to `0..0` and `write_back` builds an empty-span insertion at byte 0
  instead of refusing.

- **A dotless path routes by its whole filename** — `crates/cli/src/main.rs:124`. `hint` is
  `path.rsplit('.').next()`, so a file literally named `net` (or `org`, `obj`, `step`, `env`) has
  hint `net` and is parsed as a SPICE netlist. Unusual input, real misroute.

- **The `view` of most metadata readers ignores its selector** — `crates/rtf/src/lib.rs:50`, and
  similarly `av`, `columnar`, `eda`, `geometry`, `image`, `office`, `epub`, `mail`, `openscad`,
  `pdf`. A windowed or token-budgeted request silently returns the whole document, blowing any token
  budget the caller relied on. For the tiny engineering tallies this is harmless; for the RTF
  de-styled text it is a real deviation from the trait's documented windowed slice.

- **An obligation is discharged by the wrong test** — `host-reference.obligations:35`.
  `rule-failure.Window.1` is the hostile-input branch of the Window rule (`not source.hostile`), but
  it is mapped to `window_refuses_an_unsupported_selector`, which exercises selector refusal, a
  different concern. With no `hostile` field on `Source`, the failure path is discharged in name only.

- **No `cargo fmt --check` runs in CI** — `.github/workflows/ci.yml` (the `lint` job). The job gates
  clippy with `-D warnings` and `cargo-deny`, but never checks formatting, so source-format drift can
  land on a repo whose premise is reproducible artifacts. Low severity (style, not correctness).

## Overlay lens laws and proptest integrity

The overlay's "lens law" proptests are the weakest verification in the PR; findings 11 and the empty
`TextQuote` above are the substantive bugs, and these are the test-integrity gaps around them
(`crates/overlay/tests/lens_law.rs` and `tests/overlay.rs`):

- The law tests construct the `Edit` by hand from pre-clamped, pre-sorted offsets and call
  `normalizer.put` directly, so neither `resolve` (selector to range, with its bounds and
  boundary checks) nor `write_back` (selector to `Edit`) is ever property-tested for any law.
- The text generators are `".{0,80}"`, which excludes newlines, the one character that makes the
  prose normaliser's structure non-trivial, so the prose lens law never sees multi-line input.
- The reversed-range guards (`end.max(start)` in `put`, the `start <= end` branch in `resolve`) are
  never exercised, because every test pre-sorts its offsets.
- The CRDT merge test (`tests/overlay.rs:31`) asserts only one merge direction and set membership, not
  convergence or deterministic ordering, and `Overlay::new` carries a random peer id, so a
  non-convergent or order-divergent merge would still pass.

## Reuse, simplification, and altitude

Quality observations on the new code, in descending value. These are not defects in behaviour; the
cost named is duplication or a metric that does not mean what it claims.

- **The golden-test harness is copy-pasted across roughly twenty-three `conformance.rs` files**
  (`crates/*/tests/conformance.rs`), varying only by the normaliser type name. A shared
  `testkit::check_fixture::<N: Normalizer>` in a dev-dependency crate would own the bless protocol,
  the golden filename, and the drift message once instead of in twenty-three places.

- **`floor_boundary` and the UTF-8 decode helper are each defined identically in eleven-to-thirteen
  crates** (`prose`, `data`, `config`, `rst`, `asciidoc`, `org`, `rtf`, `bibtex`, `calendar`,
  `netlist`, `vector`). They belong in `core`; a fix to boundary handling currently has to be applied
  in every copy and can drift between them.

- **Every reader hand-builds the `Tier0`** (content id, two token counts, a whole-document span), and
  the text readers repeat an identical `CharOffset` `view` body. A `Tier0::whole(source, outline)`
  constructor and a `core::char_offset_view` helper would collapse both.

- **`raw_tokens` is computed three incompatible ways** — `count_tokens(text)` (text readers),
  `count_tokens(&from_utf8_lossy(bytes))` (`pdf`, `geometry`, `columnar`, `eda`, `epub`, `mail`,
  `office`, `openscad`), and bare `bytes.len()` (`image`, `av`, `ocr`). The headline savings ratio the
  `Tier0` design exists to report is therefore measured on different bases across modalities and is
  not comparable. The basis decision belongs in one `core` policy.

- **The `view` boilerplate that ignores its selector** (the further-finding above) would disappear
  behind a default trait method on `Normalizer` that returns the skeleton's markdown when no
  windowing is supported.

- **The registry dispatches by first match in insertion order, with no collision check**
  (`crates/cli/src/main.rs`). The order is load-bearing but unenforced; a registry keyed by extension
  would make dispatch explicit and surface the image/OCR collision (finding 6) at construction instead
  of as a silent wrong pick.

- **The ATX-heading outline is implemented twice** (`prose` and `html`). A
  `core::markdown_heading_outline` would serve both and any future Markdown-targeting reader.

## What was checked and cleared

The negative results matter as much as the findings: they say what a remediation plan does not need to
re-examine. All confirmed at the reviewed revision.

- **Determinism is otherwise clean.** No `HashMap` or `HashSet` reaches serialized output anywhere in
  `crates/*/src`; every tally is a `Vec` or `BTreeMap`/`BTreeSet` and is sorted before emission.
  `serde_json` is at its default (sorted `BTreeMap`, no `preserve_order` anywhere), and the data
  reader sorts object keys regardless. `ply-rs-bw` is backed by `indexmap` (file order), EXIF fields
  are sorted, MP4 tracks are sorted by id, config keys are sorted. No float is formatted into any
  golden (every numeric output is an integer count or the exif crate's exact rational display). No
  time, randomness, environment, or threading reaches output — with the sole exception of the two
  out-of-process helpers (findings 9 and 10).
- **The conformance harness is sound.** Every normaliser crate ships a `tests/conformance.rs` on one
  correct pattern: load or generate the input, `serialize_tier0(skeleton)`, and `assert_eq!` against a
  committed golden. The golden is rewritten only under `HOST_REFERENCE_BLESS=1`, which returns
  immediately, so a normal run never writes the file it then reads. All golden files are tracked and
  non-empty; `cargo test --workspace --locked` runs the assertions; no `#[ignore]`, no `assert!(true)`,
  no self-comparison, no early return. The OCR test golden encodes a stub helper's fixed output, which
  is correctly scoped to this crate's plumbing rather than the engine (the engine lives out of process,
  finding 9).
- **The removed-behaviour audit is clean.** The only deletions in the diff are the version bump, the
  expanded members list, the regenerated `Cargo.lock`, and the old CLI placeholder stub (a blanket
  refusal) replaced by real registry dispatch. Every error path from the stub is re-established
  (missing path, unknown command, unknown kind all exit 2 with a clean error); `deny.toml` and
  `.gitignore` are new files, not edits.
- **Member, feature, and registry coverage is consistent.** Every crate directory is in the workspace
  `members`; every reader has a matching CLI feature and a `registry()` push; `overlay` is correctly
  not a CLI reader.
- **The licence lane is complete.** Every otherwise-unallowed SPDX token in the tree appears only as an
  OR alternative beside an allowed licence; the three advisory ignores are unmaintained-only and mask
  no vulnerability; AGPL is banned and GPL flagged, with the GPL confined to the OpenSCAD helper's own
  repository.
- **The core helpers hold.** `serialize_tier0`'s span sort key `(start, end, source)` is a total,
  stable order; `count_tokens`'s `expect` loads the vocab embedded in the crate, so it cannot fail at
  runtime; `content_id`'s six-byte prefix is fine for keying a single source's map. The CLI's argv
  handling is panic-free (missing arguments and a directory path map to an `Error`).
- **The named library panics did not reproduce.** `stl_io` streams triangles and does not preallocate
  from a declared count, `ply-rs-bw` caps preallocation, and the G-code and SPICE paths return
  `Error::Parse` rather than indexing into absent coordinates.

## Disposition

Everything above is recorded for a future remediation plan and is not actioned in this milestone. The
must-fix cluster, when that plan is cut, is findings 1 through 4: bound the selector at its source, and
make the readers return `Error::Refused` on a resource bound or a hostile structure instead of
panicking, hanging, or silently zeroing — the call/0031 contract the component asserts but does not yet
keep. The determinism discipline and the conformance harness are sound foundations to build that on.
