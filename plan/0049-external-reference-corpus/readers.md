# plan/0049: reader and dependency pins

This records the pinned reader for each content kind of `host-reference`, under the `call/0033`
policy. Each reader is a pure-Rust plugin behind a Cargo feature and the best maintained library for
its format. Its licence is clear of AGPL, and any GPL dependency is flagged. The versions below are
current as of the 2026-06-27 research pass, and the exact Cargo pins land when each reader is built.
A few kinds have no pure-Rust library, so they take a scoped in-house parser, listed at the end.

## Prose

| Kind | Reader | Licence | Notes |
|---|---|---|---|
| Markdown, plain text | in-house | n/a | landed in the text-cheap kinds |
| HTML | `htmd` 0.5.4 | Apache-2.0 | landed; html5ever-based, lossy to markdown |
| reStructuredText | `rst_parser` 0.4.2 | MIT OR Apache-2.0 | parses a README-level subset, short of full Docutils |
| AsciiDoc | `asciidork-parser` 0.38.1 | MIT OR Apache-2.0 | near-complete and very active |
| Org-mode | `orgize` 0.10.0-alpha.10 | MIT | alpha API, the clear best of field |
| RTF | `rtf-parser` 0.4.3 | MIT | the outline is inferred from style runs |
| EPUB | `rbook` 0.7.9 with `htmd` | Apache-2.0 | `rbook` for the spine and the nav, `htmd` for the chapter text |
| Manual page, troff | deferred | n/a | only generator crates exist |
| TeX, LaTeX | deferred | n/a | only `pulldown-latex` exists, and it covers math alone |
| BibTeX | `biblatex` 0.12.0 | MIT OR Apache-2.0 | the outline is the entry set, the text is the field values |

## Structured data

| Kind | Reader | Licence | Notes |
|---|---|---|---|
| JSON, CSV, YAML, XML | in-house | n/a | landed in the text-cheap kinds |
| TOML | `toml` 1.1.2 | MIT OR Apache-2.0 | |
| INI | `rust-ini` 0.21.3 | MIT | |
| Java properties | `java-properties` 2.0.0 | MIT | |
| dotenv | `dotenvy` 0.15.7 | MIT | the maintained fork of `dotenv` |
| NDJSON, JSON Lines | `serde_json` 1.0 | MIT OR Apache-2.0 | the streaming deserializer, with no dedicated crate |
| TSV, delimited | `csv` 1.4.0 | Unlicense OR MIT | the delimiter is configured on the reader |
| iCalendar | `icalendar` 0.17.12 | MIT OR Apache-2.0 | the `parser` feature reads `.ics` |
| vCard | `vcard4` 0.7.3 | MIT OR Apache-2.0 | `calcard` 0.3.5 reads both `.ics` and `.vcf` if one crate is preferred |
| Jupyter notebook | `serde_json` 1.0, or `nbformat` 3.0.0 | MIT OR Apache-2.0, or BSD-3-Clause | it is JSON; `nbformat` adds typed cells |
| Parquet | `parquet` 59.0.0 | Apache-2.0 | see the feature note below |
| Arrow, Feather | `arrow` 59.0.0 | Apache-2.0 | see the feature note below |

## Office, mail, and fixed-layout

| Kind | Reader | Licence | Notes |
|---|---|---|---|
| DOCX, PPTX, XLSX | `undoc` 0.5.2 | MIT | one pure-Rust crate reading text, structure, embedded images, and metadata; `calamine` stays an option for an XLSX tabular schema |
| EML | `mail-parser` 0.11.4 | Apache-2.0 OR MIT | the parser crate rather than the AGPL Stalwart server |
| MSG | skipped | n/a | Outlook .msg is a binary OLE2 file whose conformance fixture would be disproportionate to build for a niche format; EML covers internet mail |
| Born-digital PDF | `pdf-extract` 0.12.0 over `lopdf` 0.42.0 | MIT | keep the default `flate2` backend for the pure-Rust path |

## Recognition and audio-visual

The deterministic parses stay in the attested layer; the machine-learning output goes to the overlay.

| Task | Reader | Licence | Layer | Notes |
|---|---|---|---|---|
| Image decode and metadata | `image` 0.25 with `kamadak-exif` 0.6 | MIT OR Apache-2.0, and BSD-2-Clause | attested | format, dimensions, EXIF |
| OCR | `ocrs` over `rten` | MIT OR Apache-2.0 | overlay | carries ML weights, and inference is not bit-deterministic; lands in #overlay |
| Audio metadata | `symphonia` 0.5 | MPL-2.0 | attested | codec, sample rate, channels, duration; symphonia alone carried these, so `lofty` was not needed |
| Video metadata | `mp4` 0.14 | MIT | attested | per-track type, dimensions, duration; Matroska deferred until a fixture and a need arise |
| Transcription | `candle` with Whisper | MIT OR Apache-2.0 | overlay | Whisper weights are MIT, and inference is not bit-deterministic; lands in #overlay |

## Electronic design

| Kind | Reader | Licence | Notes |
|---|---|---|---|
| SPICE netlist | in-house | n/a | landed in the text-cheap kinds |
| KiCad schematic, PCB | `lexpr` 0.2 | MIT OR Apache-2.0 | the generic fallback was taken: a tally of the top-level S-expression forms. `kiutils_kicad` reads from a path, not the bytes a `Source` carries, so it did not fit the reader contract |
| Gerber | `gerber_parser` 0.5.0 with `gerber-types` 0.7.0 | MIT OR Apache-2.0 | pin at or above 0.2.0, below which it was AGPL |
| Eagle | `roxmltree` 0.21.1 | MIT OR Apache-2.0 | a generic XML read, since Eagle 6 and later is XML; no dedicated crate |

## Engineering geometry

| Kind | Reader | Licence | Notes |
|---|---|---|---|
| STEP | `ruststep` 0.4.0 | Apache-2.0 | pure-Rust but immature; deferred rather than hand-rolled if it proves unworkable |
| IGES | deferred | n/a | no pure-Rust reader exists, every working reader is C++ |
| DXF | `dxf` 0.6.1 | MIT | ASCII, binary, and the legacy DXB |
| STL | `stl_io` 0.11.0 | MIT | binary and ASCII, with zero runtime dependencies |
| OBJ | `tobj` 4.0.4 | MIT | a Rust port rather than a tinyobjloader binding |
| 3MF | `threemf` 0.8.0 | 0BSD | pure-Rust only on the deflate path, so the C zip codecs stay off |
| AMF | `quick-xml` 0.40.1 with `zip` | MIT | a generic XML read, with deflate for the compressed variant; no dedicated crate |
| G-code | `gcode` 0.7.0 | MIT OR Apache-2.0 | a tokenizer that does not interpret machine state |
| OpenSCAD | `openscad-rs` 0.1.0, run out-of-process | GPL-3.0, flagged | a separate GPL helper binary behind an arms-length boundary, per `call/0033`; the plugin is opt-in |
| glTF, GLB | `gltf` 1.4.1 | MIT OR Apache-2.0 | both the JSON and the binary container |
| PLY | `ply-rs-bw` 4.0.0 | MIT | the maintained fork; the original carries a security advisory |

## Recognition-and-engineering: what landed

The `#recognition-and-engineering` wave landed the attested, deterministic readers of the recognition
split. Each is a feature-gated `Normalizer` with byte-for-byte conformance fixtures, built and pinned
on its own lifecycle pass.

- Image (`image` feature): format, pixel dimensions, and EXIF.
- Audio-visual (`av` feature, the new `AudioVisual` modality): audio codec, sample rate, channels,
  and duration through symphonia; video per-track type, dimensions, and duration through `mp4`.
- Electronic design (`eda` feature): KiCad form tally, Eagle element tally, Gerber command count.
- Engineering geometry (`geometry` feature): STL, glTF, DXF, OBJ, PLY, and G-code.

The machine-learning half of recognition stays out of this wave by design. OCR over an image and the
transcript of audio-visual media are non-deterministic inference, so they ride the provider-agnostic
overlay adapter of `call/0030` and land in `#overlay`, the next node. The image and audio-visual
readers here declare `ocr: false`, the attested reader's honest capability.

Four geometry kinds wait. STEP joins the deferred set under the maturity rule, since `ruststep` is the
only pure-Rust reader and it is immature. 3MF and AMF are zip-and-XML containers whose fixture
overhead is not yet earned by a corpus need. OpenSCAD is the GPL out-of-process helper, an opt-in
plugin and its own task as described below.

## Licence watch-list

- AGPL is banned, and the pinned set carries none. The one risk was `gerber_parser`, which was AGPL
  through its 0.1 line and relicensed to MIT or Apache at 0.2, so the pin sits at or above 0.2.
- GPL is avoided and flagged. The `epub` crate is GPL and a permissive equal exists, so EPUB reads
  through the Apache-licensed `rbook` and the GPL crate never enters the build. `openscad-rs` is GPL
  and has no permissive equal, so OpenSCAD takes the out-of-process route of `call/0033`, described
  below. These are the only two GPL crates in view.
- Weak copyleft is allowed and noted. The `symphonia` and `mp4parse` media readers are MPL-2.0, a
  file-level copyleft that binds only their own files. The dormant `tex-parser` is LGPL, and it is
  passed over for the in-house tokenizer on maturity grounds rather than licence.
- A `cargo-deny` lane denies AGPL and surfaces GPL, so the line holds as readers are added.

## The OpenSCAD out-of-process boundary

OpenSCAD is the one kind that takes a GPL reader. `openscad-rs` is a real tested `.scad` parser and
the strongest reader for the kind, so the build uses it through the out-of-process rule of
`call/0033`. A separate helper binary depends on `openscad-rs` and carries the
GPL licence the crate requires. It reads a `.scad` file into a structure summary and prints it as
JSON. The host-reference OpenSCAD plugin stays permissive: it runs the helper at arm's length over
the command line and reads the JSON back, so the two are aggregated rather than linked. The plugin is
feature-gated and opt-in, and it depends on the helper binary being installed, which is the cost the
`call/0033` consequence names. The `cargo-deny` lane treats this one helper as the expressly-flagged
GPL exception rather than a violation. This is the first use of the out-of-process rule, and a useful
test of the plugin API: the OpenSCAD plugin implements the same `Normalizer` interface as every
in-process reader, so the interface proves general enough to drive an out-of-process helper with no
special case.

## Pure-Rust feature discipline

Some readers are pure-Rust only with the right features. The `parquet` reader builds with default
features off and the pure-Rust codecs on, which drops the C `zstd` codec and with it the ability to
read zstd-compressed Parquet. The `arrow` reader keeps `ipc_compression` off for the same reason. The
`lopdf` reader keeps its default `flate2` backend, the pure-Rust `miniz_oxide` rather than C zlib.
The `threemf` reader and the other zip-backed readers stay on the pure-Rust deflate path. The
`cargo-deny` lane and the pure-Rust build both run in the verification lanes.

## Deferred kinds

Three kinds have no maintained pure-Rust library and no composition over the existing pure-Rust
readers, so normalising one would mean a substantial from-scratch parser. Rather than hand-roll a
parser or reach for a C library, the build defers them until a pure-Rust library appears.

- Manual page and troff: only generator crates exist, with no parser.
- TeX and LaTeX: no maintained permissive pure-Rust document parser exists, and `pulldown-latex`
  covers the math alone.
- IGES: every working reader is C++.

This keeps the pure-Rust line and the scope discipline together. A kind earns a reader when a
pure-Rust library can carry it, and it waits otherwise. STEP sits just inside the line on `ruststep`,
and it joins the deferred set rather than a hand-rolled parser if that crate proves unworkable.
