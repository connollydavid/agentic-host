# Markdown-aware prose scanning

Running `host-lint --prose` on the host README surfaced the gap: the prose engine
treated markdown as flat text, so headings were counted as "staccato paragraphs"
(`punchy-fragments`) and — more seriously — **fenced code blocks would be scanned
as prose**, flagging em-dashes, words, and arrows inside code. The engine must be
markdown-aware at the structural level, not via line regexes.

## Approach

Add **pulldown-cmark** to host-grammar (6 small pure-Rust transitive crates; the
same parser mdBook already uses here — reproducible-build anchor holds). A new
`scan_prose_markdown(md)` parses the document into blocks and scans only prose:

- **Code blocks** (fenced and indented) and **inline code** — excluded entirely.
- **Link / image targets** — keep the visible text, drop the URL.
- **Headings** — their text is still scanned for lexical/sentence tells (a heading
  can read "Let's unpack…"), but they are **not** counted as prose paragraphs, so
  `shape()`'s punchy-fragments ratio no longer miscounts them.
- **Paragraphs, list items, block quotes, table cells** — scanned as prose.
- **`shape()`** is computed from block structure: paragraph blocks (not headings,
  not code) for punchy-fragments; list items whose first inline is bold for
  bold-first-bullets (read from the parse, not from `**` markers in flat text).

Plain-text callers are unchanged: titles, commit subjects, and code comments
(`--stdin`) still use `scan_prose`. host-lint routes `.md` sources to
`scan_prose_markdown` and everything else to `scan_prose`.

## Verification (allium lane)

No new concurrency, so this stays in the allium lane (no TLA+). Property tests:

- A fenced code block containing em-dashes / `delve` / arrows yields **no** tells.
- A document of only headings does not trip `punchy-fragments`.
- Link URLs are not scanned (a URL with `delve` in the path is clean; the link
  text still is).
- For markdown with no code/headings/links, `scan_prose_markdown` agrees with
  `scan_prose` on the prose tells.

## Lifecycle / chain (software-first)

1. host-grammar: add pulldown-cmark + `scan_prose_markdown`; PBT; allium update;
   commit/push.
2. host-lint: route `.md` to the markdown-aware scan; tests; commit/push.
3. agentic-host: re-pin, rebuild in the pinned container, record artifact,
   `software --verify-build`; PLAN.md + MEMORY; re-lint the README clean.
