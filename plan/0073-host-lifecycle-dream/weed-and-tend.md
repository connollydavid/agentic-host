# weed-and-tend for plan/0073 (2026-07-19)

The lifecycle gap (operator catch): weed and tend were skipped between
implement-dream and write-tests. Per MEMORY plan/0015, weed is the spec↔code
alignment check that catches hand-authored spec drift the implementation
passes clean on (the host-lint `DetectInternalCodeAsName` flag-vs-warn bug is
the precedent). The fable review caught the spec's INTERNAL inconsistencies
but could not see spec↔code drift.

## weed check: enumerated divergences

Grouped by spec construct. Classifications: **spec-bug** (trim spec),
**code-bug** (code catches up at #implement-remaining), **aspirational**
(spec describes future behaviour; note gap), **intentional** (divergence is
deliberate; the spec models conceptually, the code implements).

### Entities

#### MemoryWrite (and MemoryWriteOp, MemoryWriteOrigin)
- Spec: full entity with `target_store, op, target_entry, origin, suggestion,
  accepted, completed` (host-lifecycle-dream.allium, MemoryWrite block).
- Code: **no Rust type**. The MCP `memory_write` surface lands at
  #extend-mcp; dream itself does not write.
- Classification: **spec-bug for the current scope; aspirational for
  #extend-mcp.** The dream audit does not need MemoryWrite; the entity and
  its flavour belong with the MCP layer, not here. Tend action: remove from
  this spec; restore (with the MemoryWrite* rules and invariants) at
  #extend-mcp.

#### Suggestion
- Spec: entity with `finding, target_store, applies`.
- Code: **no Rust type**. The dream `--fix` path refuses the repo store via
  a direct count + exit 2; no Suggestion entity needed.
- Classification: **spec-bug for the current scope; aspirational.** Same
  reasoning as MemoryWrite. Tend action: remove; restore at #extend-mcp
  when the `--fix` surface grows real Suggestion-shaped fixes (the cast
  review rules on whether Suggestion ever needs to be a Rust type).

#### LinkRef
- Spec: entity with `src, target_slug, resolves`.
- Code: **no Rust type**. The dangling-link detector uses a `known_slugs:
  &BTreeSet<String>` resolver against the store; it does not materialise
  LinkRef entities.
- Classification: **spec-bug.** The entity adds modelling weight without
  easing the analyser; a boolean field `has_dangling_link` on MemoryEntry
  is the same shape as the other detector preconditions. Tend action:
  remove LinkRef; rephrase DetectDanglingLink to key on
  `MemoryEntry.has_dangling_link`.

#### MemoryEntry field set
- Spec: 6 detector-precondition booleans (`has_description_body_drift`,
  `is_superseded_unlinked`, `is_stale_state`, `is_workaround_not_plan`,
  `is_append_only_violation`, `is_room_touching`).
- Code: `MemoryEntry { slug, description, body, entry_type, created,
  last_edited, superseded_by }` (memory.rs). The precondition booleans are
  computed in `DetectorInput`, not stored on the entry.
- Classification: **intentional.** The spec models the precondition as a
  field on the entry (the allium idiom, mirroring host-lint's
  `line.has_phase_synonym_numeral`); the code computes it on demand. Both
  correct; the divergence is the spec/code boundary. Tend action: none.

#### MemoryStore.loc vs MemoryStore.dir
- Spec: `entity MemoryStore { loc: StoreLoc }`.
- Code: `MemoryStore { dir: PathBuf }` (memory.rs).
- Classification: **intentional.** The spec models the store by its
  location kind; the code stores the path. The repo-store handle in dream
  passes `StoreLoc::Repo` directly without a MemoryStore instance. Tend
  action: none.

#### Finding field set
- Spec: `Finding { entry, kind, route, dream }`.
- Code: `Finding { entry_slug, store, kind, route, explanation }`.
- Classification: **spec-bug on the `dream` field** (added for multi-run
  safety per fable F2, but the model is single-shot by ruling; the
  back-reference is unused), **intentional on the rest** (the spec's
  `entry` is the code's `entry_slug`; `store` and `explanation` are code
  extras that do not change the model). Tend action: drop `dream` from the
  spec's Finding.

#### Dream entity and state machine
- Spec: `Dream { status: dreaming | clean | findings | error, saw_finding,
  fix_mode }` with a full transition graph.
- Code: `DreamConfig { fix_mode, json }` + a procedural `dream()` that
  returns exit codes 0/1/2. No explicit state machine.
- Classification: **intentional.** The spec models the verdict lifecycle
  conceptually; the code implements it procedurally. Both correct (fable's
  F2 process-level check confirmed the transition graph is sound and
  reachable). Tend action: none.

### Rules

#### Detect{DescriptionBodyDrift, SupersededButUnlinked, DanglingLink, RoomTouching}
- Spec: present.
- Code: present (dream.rs).
- Classification: **intentional** (aligned, modulo field naming).

#### Detect{StaleStateOverLore, WorkaroundVsPlan, AppendOnlyViolation}
- Spec: present.
- Code: **stubbed / absent** with documented TODOs (stale-state and
  workaround-vs-plan need richer heuristics; append-only-violation needs
  git history).
- Classification: **code-bug.** Spec is authority; code catches up at
  #implement-remaining. Tend action: keep in spec; record in the bucket-(b)
  list.

#### ScopeSuggestion
- Spec: present (creates Suggestion per Finding).
- Code: **absent** (no Suggestion type).
- Classification: **spec-bug for the current scope.** Goes when Suggestion
  goes. Tend action: remove.

#### StartDream / RecordFinding / VerdictFindings / VerdictClean / VerdictError
- Spec: present, with `RecordFinding` dreaming-guarded and `StartDream`
  inits `saw_finding = false`.
- Code: procedural; `dream()` exits 0/1/2 based on `findings.is_empty()`.
- Classification: **intentional.** The state machine is a model of the
  procedural logic. Tend action: none.

#### MemoryWrite{RefusesRepoUpdateDelete, RefusesRepoCreateForAudit, AcceptsPerUser, Completes}
- Spec: present.
- Code: **absent** (no MemoryWrite type).
- Classification: **spec-bug for the current scope; aspirational.** Tend
  action: remove; restore at #extend-mcp.

### Invariants

#### AuditNeverWrites / RepoStoreAppendOnly
- Spec: keys on `MemoryWrite.origin` and `MemoryWrite.op`.
- Code: the dream audit returns findings; it does not mutate. The repo
  store is read-only in dream by construction.
- Classification: **spec-bug for the current scope.** The invariants
  reference the removed MemoryWrite type. Tend action: remove; the
  dream-side property ("dream never mutates") is enforced by inspection
  (detectors return `Option<Finding>`, never `&mut`). Restore at
  #extend-mcp with the full MemoryWrite surface.

#### FixNeverTouchesRepo / SuggestionTargetsItsFinding
- Spec: keys on Suggestion.
- Code: dream `--fix` refuses the repo store by counting repo findings and
  exiting 2.
- Classification: **spec-bug for the current scope.** Tend action: remove
  with Suggestion. The dream-side property is enforced by the `--fix` exit
  code; the MCP/consolidation property lands at #extend-mcp.

#### AcceptanceBiconditional / CompletedImpliesAccepted / IdempotentSuggestionDischarge
- Spec: keys on MemoryWrite.
- Code: **absent.**
- Classification: **spec-bug for the current scope; aspirational.** Tend
  action: remove; restore at #extend-mcp.

#### RepoFindingsNeverEdit
- Spec: `for f in Findings where f.entry.store.loc = repo: f.route != edit`.
- Code: enforced by `DetectorInput::route_for(StoreLoc::Repo) == Route::Append`.
- Classification: **intentional** (aligned; load-bearing, Kani-provable).
  Tend action: keep.

#### VerdictMatchesFindings
- Spec: `for d in Dreams where d.status = clean: not d.saw_finding`.
- Code: enforced procedurally (exit 0 iff `findings.is_empty()`).
- Classification: **intentional.** Tend action: keep.

## tend reconciliation summary

| Bucket | Constructs | Action |
|---|---|---|
| (a) trim spec | MemoryWrite + MemoryWriteOp + MemoryWriteOrigin enums; MemoryWrite, Suggestion, LinkRef entities; ScopeSuggestion rule; MemoryWrite* rules (4); AuditNeverWrites, RepoStoreAppendOnly, FixNeverTouchesRepo, SuggestionTargetsItsFinding, AcceptanceBiconditional, CompletedImpliesAccepted, IdempotentSuggestionDischarge invariants (7); `Finding.dream` field | remove from spec; restore at #extend-mcp with the MCP surface |
| (b) code catches up | DetectStaleStateOverLore, DetectWorkaroundVsPlan, DetectAppendOnlyViolation | keep in spec; record for #implement-remaining |
| (c) intentional gap | Dream entity (conceptual model vs procedural code); MemoryEntry precondition booleans (spec-stored vs code-computed); MemoryStore.loc vs .dir; Finding field naming (modulo the dropped `dream`) | no change |

## Post-tend spec shape

- 2 enums (StoreLoc, Route) — MemoryWriteOp and MemoryWriteOrigin removed.
- 5 entities (MemoryStore, MemoryEntry, Finding, Dream, Project) — LinkRef,
  Suggestion, MemoryWrite removed.
- 7 detector rules — all kept (3 are bucket-b for #implement-remaining).
- DetectDanglingLink rephrased to key on `MemoryEntry.has_dangling_link`
  (the field already exists) instead of LinkRef.
- 5 verdict-lifecycle rules (StartDream, RecordFinding, VerdictFindings,
  VerdictClean, VerdictError) — unchanged.
- 2 invariants (RepoFindingsNeverEdit, VerdictMatchesFindings) — the
  MemoryWrite/Suggestion-flavoured ones removed.

## Post-tend manifest shape

The MemoryWrite/Suggestion-flavoured obligation IDs disappear (those
constructs are gone from the spec). The deferred-detector obligations stay,
dispositioned `waived: pending #implement-remaining` (the tests land with
the implementation, not ahead of it). The remaining structural + detector +
verdict + invariant obligations keep their `test:` / `structural`
dispositions; the `test:` names are still forward refs until #write-tests.

## Verification

- `allium check host-lifecycle-dream.allium` rc=0, zero errors / warnings.
- `allium analyse host-lifecycle-dream.allium` rc=0.
- `host-lifecycle obligations host-lifecycle-dream.allium --tests src` rc=0,
  zero STALE entries (every disposition's obligation ID still exists in the
  trimmed spec).
