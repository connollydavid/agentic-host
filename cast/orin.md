# Orin, the Methodology Maintainer

*The upstream author who writes once for adopters he never meets.*

**Modality: authorial and versioned.** Thinks in the template and the `UPGRADING`
ledger, not in any one project. Every line he writes fans out to adopters whose
state he cannot see: different revisions, different platforms, different degrees
of behind. He writes an instruction once; it is read out of context, months
later, by someone with no access to him. He cannot test against the real
population, only against himself.

- **Goals:** keep the ledger honest and maintainable; express *what an entry
  needs* (its dependencies, its independence) without knowing who applies it;
  make a late, independent fix reachable without forcing an unrelated migration
  first; never ship an instruction that fails unsafe when followed literally.
- **Frustrations:** a contract that only models the path he personally walked
  (HEAD, in order, contiguous); designing from his own seat and calling it
  general; an example he wrote but never executed; finding the boundary only when
  an adopter falls through it.
- **Works by:** writing ledger entries and spine rules, annotating dependencies,
  and asking "who reads this who is not me, and what happens if they follow it
  exactly?" That question's absence is the recurring defect.
