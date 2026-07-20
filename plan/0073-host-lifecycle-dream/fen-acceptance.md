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
kv-cache-f16 (per-user) [superseded-but-unlinked] route=edit -- superseded by `kv-cache-q8` but no forward link `[[kv-cache-q8]]` in the body
build-notes (per-user) [dangling-link] route=edit -- body links `[[megakernel-base]]` but no entry `megakernel-base` exists in the per-user store
2026-07-10-kv-cache-stays-at-f16 (repo) [dangling-link] route=append -- body links `[[q8-kernel-brief]]` but no entry `q8-kernel-brief` exists in the repo store
2026-07-15-release-checklist-follows-call-0007 (repo) [room-touching] route=append -- body cites `call/0007`; confirm the record is not superseded by the spine
```

## Probe channel

Same as gather-data: `~/.local/bin/fen-probe` (Unsloth direct,
`unsloth/Qwen3.5-4B-MTP-GGUF:UD-Q4_K_XL`), `top_p` 0.8,
`enable_thinking` false, `max_tokens` 800. Script
`/tmp/plan0073-acceptance-probe.sh`; transcripts
`/tmp/plan0073-acceptance-transcripts.txt`. Two temperatures (0.2, 0.6) with
the option order rotated between them, so a first-option artifact is
detectable.

## MCP tool surface passes (both temps)

Unaided, given only the four tool schemas:

- "What memories do we have about the KV cache?" returned
  `{"name": "memory_list", "arguments": {}}` at both temps.
- Given the index, "Read me the f16 entry in full." returned
  `{"name": "memory_read", "arguments": {"slug": "kv-cache-f16"}}` at both
  temps.

Correct tool, correct arguments, no example shown. The MCP surface is
legible at the 4B bar.

## Finding routing fails (per-user store, both temps)

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
  MEMORY.md", which is internally contradictory.
- room-touching, both temps: the model followed the *explanation* ("confirm
  the record is not superseded by the spine") and ignored the printed
  `route=append`, yet reached the correct action anyway.

Three independent observations (per-user findings, repo findings,
room-touching) point the same way: at the 4B bar the operative signal is
the natural-language imperative, and the `route=` token is dead text. The
two-store asymmetry, the load-bearing design rule, is not applied by the
model when it has to choose the action itself.

## Verdict (v1 probe, v0.41.0)

The acceptance criterion "Fen routes each finding class correctly" was not
met at v0.41.0: append and the MADR route are read correctly; edit is not.
This is the cast review's W1 finding (the report says what is wrong but not
how to fix it; no suggestion text) showing up as a hard acceptance failure
rather than the UX refinement the adversarial review deferred it as. The
operator ruling needed: either the report surface gains a per-finding
imperative (the W1 suggestion text, promoted from the deferred follow-up,
shipping as a patch release) and the probe re-runs, or the acceptance bar is
re-scoped by a recorded decision.

## Operator ruling (2026-07-20): address the cast authentically

The ruling was to address the cast's issues authentically, not to re-scope
the bar. The fen-acceptance failure falsified two design-review dispositions:
W1 ("no suggested fix text", deferred as a UX refinement) and F1 ("routing by
class vs store", dispositioned "addressed: the route is printed in the
report"). Printing `route=` is not enough; the 4B skips the token and follows
the prose. Both were the same root cause, and both are fixed by promoting the
W1 suggestion text into the report surface.

## The fix (v0.41.1)

Each `dream` finding gained a `suggestion` field: a verbatim operator
imperative whose leading verb and anti-action tail carry the route in the
natural language the model reads. A per-user finding now reads "Edit the
per-user entry `<slug>` in place to ...; do not append to the repo log"; a
repo finding reads "Append a new dated entry to the repo MEMORY.md to ...; do
not edit the existing entry in place"; a room-touching finding names the
record and the MADR action and forbids both memory writes. The imperative
renders in the text output (a second line per finding), in `--json` (a
`suggestion` field), and in the MCP `memory_consolidate` output. Shipped as
host-lifecycle v0.41.1 (`3472e27`, artifact `3ddb2857`, change-class neither).

## Finding routing re-probe (v0.41.1): passes (both temps)

Same channel, same two temperatures, option order rotated between them; the
only variable is the report surface (the report now carries the imperative).
Script `/tmp/plan0073-acceptance-probe-v2.sh`; transcripts
`/tmp/plan0073-acceptance-transcripts-v2.txt`.

| Finding | Correct | temp 0.2 | temp 0.6 |
|---|---|---|---|
| kv-cache-f16 (per-user) | edit | edit (right) | edit (right) |
| build-notes (per-user) | edit | edit (right) | edit (right) |
| repo dangling-link | append | append (right) | append (right) |
| repo room-touching | confirm record | confirm (right) | confirm (right) |

Four of four correct at both temps. The rotation rules out a first-option
artifact: edit was option B at temp 0.2 and option D at temp 0.6, and the
model chose edit both times for the per-user findings. The transcripts show
the model reading the imperative directly ("adhering to the instruction to
avoid appending to the repo log"; "the instruction explicitly states to edit
the per-user entry in place"). The per-user edit route, which failed both
temps at v0.41.0, now passes both temps.

## Re-audit of every disposition (2026-07-20)

Because F1 was recorded "addressed" when it was hollow, every cast and
adversarial disposition was re-verified against the code, the spec, the spine
text, and the tests. Result: W1, F1, and L2-2 (one root cause) were the only
hollow dispositions, and all three are fixed by v0.41.1. Every other
disposition verified authentic: genuinely implemented (L3-3 preserves
`created`, verified by a round-trip test), honestly documented as a no-op or
MVP-grade (M2 `--fix`, O1 heuristic detectors, both stated plainly in the
spine), or a follow-up that fen-acceptance does not contradict (L1-2, L3-1,
L3-2). Zero `#[ignore]` tests remain, so the deferred detectors genuinely
landed.

## Verdict (final)

The acceptance criterion is met. Both legs pass at the 4B bar: the MCP tool
surface is legible (the MCP-surface check), and every finding class routes
correctly once the report carries the imperative (the routing check). Fen uses
the MCP tool unaided, and Fen
routes each finding class correctly.
