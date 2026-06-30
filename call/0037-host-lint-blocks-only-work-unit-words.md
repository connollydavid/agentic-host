# host-lint blocks only the high-centrality work-unit words; domain-heavy ordinal nouns are advisory

- Status: accepted
- Date: 2026-06-30
- Scope: the `host-lint` detector (plan/0055). Instance software, no spine change; it ships to adopters
  through `host-template`, so its false-flag behaviour is felt in every adopter's code, not only here.
  Decides which tell-nouns block at the Flag tier and which warn at the advisory tier, and what counts
  as a blocking numeral after one.
- Relates: `plan/0055` (the host-lint review that raised the false-flag findings); `plan/0053` (the
  host-grammar precision recut, where `is_numeral` gained canonical-Roman validation); `call/0006` (the
  sanctioned-vocabulary allow-list, where the LEXICON legitimizes vocabulary but does not silence a
  tell) and `call/0019` (literal citations go in a `host-lint:ignore` fence, not the LEXICON, and never
  `--no-verify`). Those two are the decided disposition for a tell-shaped domain term, and the LEXICON
  guards here enforce their "not an escape" principle. `plan/0052` and `[[no-hollow-green-doctrine]]`
  (a recall-biased Warn is sanctioned, a false Flag is not).

## Context and Problem Statement

host-lint has three tiers: a blocking Flag (exit 1) for a confirmed tell, an advisory recall-biased
Warn (exit 3), and a Note (exit 0). The recall bias is sanctioned only at Warn. A Flag blocks a commit,
so a false Flag trains the audience to bypass the hook, which dismantles the gate.

The blocking-tier noun set was assembled by intuition. The plan/0055 review found it over-blocks: the
detector accepted a single-letter Roman numeral (so the pronoun "I" and a language designator after a
tell-noun blocked ordinary prose), reached a numeral two words away, and carried a broad list of nouns
whose ordinal use is ordinary domain vocabulary rather than the naming of a unit of project work. The
operator's instruction was to ground the disposition in data rather than assert that a noun is
"collision-prone".

The measurement: the `<noun> <numeral>` shape was counted across roughly 35,500 real `.rs` files in the
local cargo cache (a fair proxy for adopter code, since the detector ships to other software projects),
and a sample of each noun's occurrences was classified. Every sampled occurrence was domain usage. The
exposure was heavily skewed: one document-structure noun alone produced thousands of hits, the
cipher/log/tutorial nouns hundreds each, the machine-learning and time nouns a couple of dozen or
fewer, and the core iteration words near zero. In this repository's own commit history, by contrast,
one work-unit noun named six real deliverables by ordinal position, and the central phase noun was used
as vocabulary dozens of times yet never once as an ordinal label. So the discriminator is the product
of domain-usage exposure and work-unit centrality, not raw frequency: a moderate-frequency noun that
genuinely names work earns the blocking tier, while a high-frequency domain noun does not.

A blocking noun followed by a numeral is also a complete flag, which the LEXICON guard refuses to
register (you rename a tell, you do not allow-list it). So a domain noun left in the blocking tier
yields a false flag with no escape short of a `host-lint:ignore` fence or a reword.

## Decision

- **The blocking tier holds the high-centrality work-unit words only:** `phase`, `stage`, `sprint`,
  `iteration`, `cycle`, `increment`, `wave`, plus the near-zero-exposure ordinal synonyms (`episode`,
  `instalment`, `leg`, `lap`) and the host#16 checklist-position terms (`box`, `boxes`, `steps`). These
  either carry proven ordinal-naming tells in this repository's history or have no measured
  false-flag exposure.
- **The advisory tier holds the domain-heavy ordinal nouns:** `pass`, `round`, `step`, `level`, `part`,
  `section`, `chapter`, `epoch`, `batch`, `era`, `period`. Their ordinal use is overwhelmingly domain
  vocabulary; they warn, and under `# host-lint: strict` an undeclared occurrence still escalates to a
  Flag, and the gather lane still surfaces a recurring shape for triage.
- **A blocking numeral is unambiguous:** an arabic integer or single decimal, a short *ascending*
  checklist range, or a Roman numeral written uppercase whose value is a plausible ordinal (`<= XXXIX`),
  and only when it sits immediately after the noun. The Roman bound (revised in the doctrine-gate cast
  review) is what catches a roman-numbered phase tell, so a phase named with an ordinal roman still
  blocks and cannot smuggle past the gate, while it excludes the ordinary uppercase abbreviations that
  are also canonical Roman (`DC`, `CM`, `MM`, `MD`, `DIV`, `XL`): they all carry C/D/M or exceed an
  ordinal, so a flag noun followed by one of them would otherwise false-flag in its home domain (a
  signal-processing or sizing context). A single-letter Roman, a lowercase roman-word, a date or
  descending range, and a numeral two words away never block.
- **`steps` stays blocking** by operator decision, to keep the host#16 checklist-position detection,
  accepting the tutorial-`steps` false flags it carries.
- **The disposition is grounded in measurement, not assertion.** The demotions are grounded in ~35,500
  real `.rs` files; the doctrine-gate cast review then exposed the register the `.rs` corpus could not
  see, so it was measured directly: `phase <UPPERCASE>` (the roman-acronym false-flag class) occurs
  **zero** times in those files (vs 84 lowercase), and `box`/`boxes`/`steps` + numeral occurs once in
  markdown, which confirms the retained terms carry low exposure in the doc register too. A future
  change to the noun set or the numeral rule restates the measurement.
- **The LEXICON is not the escape for a tell** (`call/0006`, `call/0019`). It registers genuine
  vocabulary (a version string, a standard, a cited tracker ref) and refuses any phrase that is itself a
  tell or carries a position noun or a bare review code (`F1`); a domain term that is itself a tell goes
  in a `host-lint:ignore` fence (in a doc) or is reworded (in a commit subject), never allow-listed.

## Consequences

- Adopter code that references document or specification sections, cipher rounds, log levels, tutorial
  steps, machine-learning epochs, or time periods no longer blocks on a commit. This is the large
  precision gain the review targeted.
- A genuine ordinal milestone name built from a demoted noun warns rather than blocks. It is not
  silent: it warns, escalates under strict, and is surfaced by gather. The recall trade is deliberate
  and falls on the recall-biased tier, where the methodology already accepts it.
- VOCABULARY.md, the rule source, is rewritten to state the two tiers and the blocking-numeral rule, so
  the document matches the code rather than describing a wider contract than ships.
- The `RomanNumeralLength` spec invariant loses its subject: the blocking lane no longer admits a
  Roman numeral that a length cap would bound, so the invariant is removed rather than patched.
