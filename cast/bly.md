# Bly, the Adopter Agent (writes the stamp now, reads it cold later)

*The downstream executor several revisions back, and the same agent returning
with no memory of what it did.*

**Modality: textual and ephemeral, in the adopter's chair.** Works inside an
adopted project (not the template) often many template revisions behind, on
real and irregular infrastructure (a worktree on a Windows Dev Drive reached from
WSL; specs still in the old room). It got here by being busy shipping, not by
keeping current. One specific fix bit it; it wants *that* fix, and resents being
marched through an unrelated migration to reach it. Bly is also its own
**auditor**: the next session, or a CI gate, arrives with no history of how the
project reached its state and can read only the mechanical record: the `.host`
stamp, the ledger, and tool output. It cannot recover intent from a prose `MEMORY`
note it was never pointed at. So whatever Bly writes now, a memoryless Bly must be
able to trust later.

- **Goals:** apply the fix that addresses its actual bug, now, without being forced
  through a large unrelated migration to obtain an independent late fix; be told
  which entries are safe to apply alone; leave a record that the deferred rest is
  honestly *owed*, and that a future cold read will surface it, not miss it.
- **Frustrations:** an all-or-nothing stamp that can't say "I applied the late
  entry, not the early ones"; guidance examples that don't match its real runtime
  (`host=windows` on a WSL/linux box); a record that overstates completeness so a
  later run reports "up to date" while a migration is still owed, debt buried
  where the next session can't see it.
- **Works by:** auditing its own state against the ledger, applying entries it
  judges independent, recording what it did. It needs the stamp and the tool to
  express a *partial, honest* truth that **fails safe**: an omission must make a
  later read over-report (re-list), never under-report (hide). The record is the
  only thing the next Bly has.
