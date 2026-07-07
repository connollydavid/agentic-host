# plan/0065 code-review: adversarial review of the onboarding surface before release

Before releasing the onboarding surface (the init/adopt/scaffold verbs, the host-init/host-adopt shims,
the MCP stdio server, and the oneshot git and GitHub finalize), a multi-agent adversarial review swept the
new code across five dimensions (correctness, the MCP protocol, the gh oneshot, security and invariants,
and reproducibility), and each raised finding was independently verified against the real code. Twelve
findings survived verification as confirmed defects; three were rejected. All twelve are fixed here, per
the doctrine that a review finding is a requirement, not a descope.

## Confirmed findings, all fixed

- **High, the deprecate shim mutated the source.** `adopt` treated any two positional arguments as the
  retired `adopt <dir> <revision>` primitive and forwarded to `scaffold`, so a mistaken
  `host-adopt <source> <name>` wrote the rooms and stamp into the source folder and broke the flagship
  source-read-only invariant. Fixed: the two-positional form is now a hard error that names `scaffold`,
  never a silent forward (call/0041 corrected).
- **High, the MCP elicitation assumed the next line was the response.** An interleaved notification between
  `elicitation/create` and the answer was mistaken for the answer. Fixed: read until the response whose
  JSON-RPC id matches, and skip any interleaved message.
- **High, a clean commit read as a fatal error.** `git_init_commit` checked stderr for "nothing to
  commit", but git writes that to stdout. Fixed: check both streams.
- **High, MCP argument injection through the adopt source.** The `source` argument was emitted as a bare
  positional, so a value beginning with a dash was read as a flag by the subprocess. Fixed: the source
  follows an end-of-options `--`, and the adopt parser honours it.
- **Medium, the software-repo refusal returned the wrong exit code.** Route one exited 2 (a usage error)
  rather than the ruled contract's 4 for a refuse. Fixed: route one exits 4.
- **Medium, the in-place emptiness test counted `.git`.** A freshly `git init`ed or cloned empty
  `agentic-<name>` folder failed the route-two carve-out and could dead-end. Fixed: emptiness ignores the
  artifacts a fresh repo carries (`.git`, `.gitignore`, a README, a LICENSE).
- **Medium, one bad line killed the MCP server.** `read_message` returned the same sentinel for a parse
  failure and a closed pipe. Fixed: a non-JSON line is skipped, not treated as end-of-input.
- **Medium, the conflicting-flags check ran after scaffolding.** The `--no-git` with `--github` conflict
  was caught inside the finalize, after the directory was already created. Fixed: it is preflighted before
  any write.
- **Medium, in-place adopt ignored the git and GitHub flags.** Route two never committed or wired a
  remote. Fixed: route two runs the same finalize as the create-elsewhere route and init.
- **Medium, `--force` on a populated repo committed unrelated files.** `git add -A` swept the whole working
  tree. Fixed: only the scaffold artifacts are staged.
- **Medium, route three could target inside the source.** An `--at` pointing into the source would create
  the host within it, breaking source-read-only. Fixed: the resolved target is checked to lie outside the
  source, else refused.
- **Medium, the release must re-vendor.** Adding tokio and serde_json grew the lockfile past the vendored
  deps-bundle, so the offline locked musl reproducible build fails until re-vendored. Resolved as the
  release step: a fresh deps-bundle is vendored and pinned with the release.

## Verification

The verbs' unit tests cover the routing, the name backstop, `dir_effectively_empty`, and `git_init_commit`;
the MCP tests cover the elicitation round trip, the interleaved-notification skip, and the `--`-guarded
argv. The behavioural fixes were smoke-verified on the built binary: the two-positional form errors without
touching the source, a software repo refuses with exit 4, a `.git`-only `agentic-<name>` adopts in place,
and an `--at` inside the source is refused. The whole suite is green and clippy is clean.
