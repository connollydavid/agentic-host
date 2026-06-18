# Bly — the Adopter Agent, Behind

*The downstream executor several revisions back, operating a real project.*

**Modality: textual and ephemeral, in the adopter's chair.** Works inside an
adopted project — not the template — often many template revisions behind, on
real and irregular infrastructure (a worktree on a Windows Dev Drive reached from
WSL; specs still in the old room). It got here by being busy shipping, not by
keeping current. One specific fix bit it; it wants *that* fix, and resents being
marched through an unrelated migration to reach it.

- **Goals:** apply the fix that addresses its actual bug, now; not be forced
  through a large, unrelated migration to obtain an independent late fix; be told
  which entries are safe to apply alone; leave a record that the deferred rest is
  honestly *owed*, not silently dropped.
- **Frustrations:** an all-or-nothing stamp that can't say "I applied the late
  entry, not the early ones"; guidance examples that don't match its real runtime
  (`host=windows` on a WSL/linux box); a workaround that buries owed work where
  the tooling can't see it.
- **Works by:** auditing its own state against the ledger, applying entries it
  judges independent, recording what it did. It needs the stamp and the tool to
  express a *partial, honest* truth — the exact thing the single-revision model
  cannot.
