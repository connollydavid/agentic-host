I'll follow the web-search-deep protocol. Starting with **Phase 1: Planning**, and checking the bundled worker definition.
**Phase 1 — Planning.**

- **Topic:** `bstr` vs `os_str_bytes` for classifying non-UTF-8 file paths in a Rust CLI; must nail each crate's byte-path type name and license.
- **Must-have queries:** (1) bstr docs/type/license, (2) os_str_bytes docs/type/license, (3) non-UTF-8 path handling in Rust community experience, (4) bstr GitHub/license/maintenance, (5) os_str_bytes GitHub/license/maintenance/downstream users.
- **Source tiers:** official (docs.rs, crates.io API, GitHub raw) > community (users.rust-lang.org, Reddit) > blog.
- **Deliverable:** comparison matrix + house recommendation.
- **Success criteria:** verbatim, located quotes for: byte-path type of each crate, license of each crate, maintenance status, feature fit for path classification.

**Phase 2 — Parallel search.** Launching 5 `web-search-worker` subagents in one batch (using the skill's preconfigured worker model, unchanged):
Both official sources for `os_str_bytes` fetched (v7.2.1, docs.rs + crates.io JSON). Now I'll save snapshots. The harness saved large outputs to tool-output files; let me check and copy them into `snapshots/`:
