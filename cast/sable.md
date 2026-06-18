# Sable — the Cold-Start Auditor

*The fresh session, or the CI gate, that reads the stamp as ground truth.*

**Modality: mechanical and memoryless.** Arrives with no history of how the
project reached its current state — a new session, a clean CI runner. Its only
evidence is what the record mechanically says: the `.host` stamp, the ledger, the
output of `host-lifecycle upgrade` and `software --check`. It cannot read intent
out of a prose MEMORY note it was never pointed at. It either fails loud on a real
gap, or is silently deceived by a record that overstates completeness.

- **Goals:** learn the true applied/owed state from the stamp and tool output
  alone; never report "up to date" while work is owed; fail loud, never silent;
  treat the mechanical record as authoritative because it has nothing else.
- **Frustrations:** a stamp that overstates what was applied; debt tracked only in
  prose it will not read; `upgrade` reporting clean while a migration is still
  owed — the exact way owed work disappeared in the field.
- **Works by:** reading the stamp and ledger and computing the gap. It can only be
  as honest as the stamp lets it be — so the stamp must fail *safe*: an omission
  should make it over-report (re-list), never under-report (hide).
