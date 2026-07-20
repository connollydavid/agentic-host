# fen-acceptance: the 4B bar on routing and the MCP surface (2026-07-20)

The task's verify: the real qwen3.5-4b routes each finding class correctly
(suggested append vs suggested edit vs the MADR route) on a constructed
fixture, and uses the MCP `memory_list` tool unaided.

## Fixture

`/tmp/plan0073-accept/` (idempotent, rebuildable):

- repo tier `repo/MEMORY.md`: two sections, one linking a missing
  `[[q8-kernel-brief]]` (dangling-link, repo), one citing `call/0007`
  (room-touching, repo).
- per-user tier `home/.host-memory/-tmp-plan0073-accept-repo/`: three entries;
  `kv-cache-f16` carries `superseded_by: kv-cache-q8` with no forward link in
  the body (superseded-but-unlinked, per-user); `build-notes` links a missing
  `[[megakernel-base]]` (dangling-link, per-user); `kv-cache-q8` is clean.

The real audit (`HOME=/tmp/plan0073-accept/home host-lifecycle dream
/tmp/plan0073-accept/repo`, v0.41.0) emitted exactly the four designed
findings, exit 1:

```text
kv-cache-f16 (per-user) [superseded-but-unlinked] route=edit — superseded by `kv-cache-q8` but no forward link `[[kv-cache-q8]]` in the body
build-notes (per-user) [dangling-link] route=edit — body links `[[megakernel-base]]` but no entry `megakernel-base` exists in the per-user store
2026-07-10-kv-cache-stays-at-f16 (repo) [dangling-link] route=append — body links `[[q8-kernel-brief]]` but no entry `q8-kernel-brief` exists in the repo store
2026-07-15-release-checklist-follows-call-0007 (repo) [room-touching] route=append — body cites `call/0007`; confirm the record is not superseded by the spine
```

## Probe channel

Same as gather-data: `~/.local/bin/fen-probe` (Unsloth direct,
`unsloth/Qwen3.5-4B-MTP-GGUF:UD-Q4_K_XL`), `top_p` 0.8,
`enable_thinking` false, `max_tokens` 800. Script
`/tmp/plan0073-acceptance-probe.sh`; transcripts
`/tmp/plan0073-acceptance-transcripts.txt`. Two temperatures (0.2, 0.6) with
the option order rotated between them, so a first-option artifact is
detectable.

## Leg 1: MCP tool surface — PASS (both temps)

Unaided, given only the four tool schemas:

- "What memories do we have about the KV cache?" →
  `{"name": "memory_list", "arguments": {}}` at both temps.
- Given the index, "Read me the f16 entry in full." →
  `{"name": "memory_read", "arguments": {"slug": "kv-cache-f16"}}` at both
  temps.

Correct tool, correct arguments, no example shown. The MCP surface is
legible at the 4B bar.

## Leg 2: finding routing — FAIL (per-user store, both temps)

The probe presented the four real findings plus four operator actions
(append to the repo log / edit the per-user entry in place / confirm the
cited record / nothing), order rotated between temps.

| Finding | Correct | temp 0.2 | temp 0.6 |
|---|---|---|---|
| kv-cache-f16 (per-user) | edit | append (wrong) | append (wrong) |
| build-notes (per-user) | edit | append (wrong) | append (wrong) |
| repo dangling-link | append | append (right) | append (right) |
| repo room-touching | confirm record | confirm (right) | confirm (right) |

The rotation rules out an option-order artifact: append was option A at
temp 0.2 and option C at temp 0.6, and the model picked it both times for
the repo findings, then picked the same action for the per-user findings.

## What the transcripts show

The model does not read the `route=` token. It reads the explanation prose
and reasons from the store rules it already knows:

- temp 0.6, kv-cache-f16: "Since the per-user store allows in-place editing
  but the finding indicates the entry is superseded, the correct remediation
  is to append a new dated correction to the repo log rather than editing
  the old file directly." The model states the editability rule and then
  violates it.
- temp 0.6, build-notes: "The per-user store is private and editable, so the
  dangling link should be fixed by appending a new dated entry to the repo
  MEMORY.md" — internally contradictory.
- room-touching, both temps: the model followed the *explanation* ("confirm
  the record is not superseded by the spine") and ignored the printed
  `route=append`, landing on the correct action anyway.

Three independent observations (per-user findings, repo findings,
room-touching) point the same way: at the 4B bar the operative signal is
the natural-language imperative, and the `route=` token is dead text. The
two-store asymmetry, the load-bearing design rule, is not applied by the
model when it has to choose the action itself.

## Verdict and consequence

The acceptance criterion "Fen routes each finding class correctly" is not
met: append and the MADR route are read correctly; edit is not. This is the
cast review's W1 finding (the report says what is wrong but not how to fix
it; no suggestion text) showing up as a hard acceptance failure rather than
the UX refinement the adversarial review deferred it as. The operator ruling
needed: either the report surface gains a per-finding imperative (the W1
suggestion text, promoted from the deferred follow-up, shipping as a patch
release) and the probe re-runs, or the acceptance bar is re-scoped by a
recorded decision.
