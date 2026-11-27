I'll follow the web-search-deep protocol. Starting with **Phase 1: Planning**.

## Phase 1: Planning

**Topic:** Compare ripgrep (rg) vs ast-grep (sg) for repository-wide prose scans — implementation language, license, query language, and which can express syntax-tree queries.

**Query set (must-have):**
1. ripgrep official repo — implementation language, license
2. ripgrep regex/syntax docs — query language
3. ast-grep official repo — implementation language, license
4. ast-grep docs — pattern/structural syntax, tree-sitter query language

**Nice-to-have:** license files verbatim, prose-scan relevance (multi-line matching, .txt files).

**Source types:** official GitHub repos, official docs sites, man pages. **Deliverable:** comparison table + cited report, sources.json, fetch-log.jsonl, snapshots.

**Success criteria:** verbatim quotes from fetched pages covering language + license + query language for both tools, and syntax-tree capability.

## Phase 2: Parallel Search

Launching workers in parallel now.
The scaffold is ready and both search workers (`ripgrep` facts and `ast-grep` facts) are running in parallel. I'll continue to **Phase 3 (synthesis)** and my own verbatim fetches for the snapshots once the workers report back — ending this turn to wait for their results.
