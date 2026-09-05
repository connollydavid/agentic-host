# adversarial-review: five lenses on the built diff (2026-09-05)

The diff under review: host-lifecycle `36c1703` against `f5d69f7` (the declaration reader, the strict tier, the census, the rename surfaces), plus the host and template content migrations. The cut named three dedicated lenses; they ran first.

## Lens 1: the declaration becoming a second ignore list

Attack: `.host-lintignore` and `.host-corpus` are both dot-files read by sweeps, and a reader meeting both asks why one hides files and the other hunts them. Worse: a project could declare a file IN the corpus while ignoring it in the list, and the two lists would fight.

Finding: the fight case is real but its resolution is already ordered. The ignore list excludes a file from the engine's walk, so a declared-and-ignored file yields no engine verdict, while the declaration still checks presence (the file exists), and any warns inside it are invisible because the engine never read it. That is a silent hole: a declared file that is also ignored gets corpus membership without strict-tier coverage. The walk's ignore behavior is load-bearing for the record layer (MEMORY.md by construction), so the remedy names the interaction instead of bypassing ignores; the doctrine node's ledger entry carries it as a stated rule (a file in the declared corpus must not be in the ignore list), recorded as a candidate check for the obligations if it ever bites in practice. Not blocking today; no declared file here is ignored.

## Lens 2: the census growing into a gate by drift

Attack: today the census discloses; tomorrow someone adds `exit 1` under the census print "just for non-ASCII tropes", and the operator's exemption ruling is quietly dead.

Finding: the spec is the guard. `CensusIsNeverAViolation` was modeled as `CensusNamesPresentFiles` plus the structural fact that no rule creates a Violation from a CensusRow; the disclosure text itself says "never on script". The invariant that would make drift visible is the obligations' mutation discipline: any future rule creating a Violation from a Census must disposition against `the_census_discloses_non_ascii_without_flagging_it`, which asserts exit 0 with bytes present. Carried as the standing test, not a new mechanism.

## Lens 3: the doctrine fragmenting between the manual and the future zh translation

Attack: removing the zh partials and deferring the translation means the deferred work arrives into a corpus whose gate knows nothing about zh; the translation lands, the census counts it, and nothing guarantees the translation tracks the English doctrine as it evolves.

Finding: real, and already on the record twice: the follow-up table row and the census's stated expected populations. The additional guarantee this round adds: the doctrine node's ledger entry supersedes the lem entry's sync instruction with the English-only manual, so the future translation is cut as its own milestone with its own sync instruction, never as an edit that drifts. Carried.

## Lens 4: the rename's silent surfaces

Attack: a rename driven by grep misses the surface that greps miss: the classify heuristic, the book placement, and any adopter tooling keyed to the old name.

Finding: the surface list in gather-data was built from the grep plus a read of every hit, and the classify and placement changes carry tests (the suite runs green with both names accepted). The pointer file is the escape hatch for unknown surfaces: anything keyed to `CLAUDE.md` finds a file that names the manual. One real gap found and accepted: the ledger's three old `verify` greps name `host-template/CLAUDE.md` and would fail for an adopter applying those entries after this rename; the ledger is append-only, so the fix is the doctrine node's rename entry instructing mid-flight adopters. Blocking on the doctrine node, not on this diff.

## Lens 5: zero drift for undeclared trees

Attack: every project without an `active-corpus` key must behave byte-identically to v0.51.0, or the release is a behavior change smuggled to every adopter.

Finding: the implementation's own structure makes the claim checkable: an absent key returns an empty declaration, which escalates nothing, censuses nothing, and misses nothing: and the undeclared-advisory test pins it end to end. The suite runs green. No finding.

## Disposition

No blocking findings in the diff. Three carries: the declared-and-ignored interaction (doctrine node names it; candidate check), the census's standing mutation test (already in the obligations), and the mid-flight ledger greps (doctrine node's rename entry). The plan/0079 dependency from the cast round rides with Orin's carry.
