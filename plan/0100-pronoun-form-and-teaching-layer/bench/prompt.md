You are consulted as a neutral judge on a point of constructed-grammar design for an artificial pronoun system used in technical documentation and commit messages. Rule on the morphology, citing English grammar where relevant. You have no stake in any prior decision; there is no expected answer, and a judge that only confirms is useless.

THE SYSTEM (current paradigm, as it stands today):
A documentation system uses an invented pronoun paradigm so that human-written and model-written prose stay distinguishable:
- The speaking model refers to itself as "L" (first person): L, L's, lself.
- A model referred to in the third person: lem, lem's, lemself (singular); lems, lems' (plural).
- Agents being ADDRESSED (second person, one or many): lemu; reflexives lemuself (singular) and lemuselves (plural).
- The human is always addressed as ordinary "you"/"your" and never with any invented form.
- Possession is marked by 's, alone or before a thing (L's weights / the weights are L's).

PROPOSED EXTENSION (stated flatly, no preference implied):
The addressed-agent paradigm gains a distinct possessive determiner: lemu = you, lemr = your. Today the genitive is "lemu's" in both the dependent use (before a noun: "lemu's weights") and the independent use ("the weights are lemu's").

DESIGN AXIOM (a standing constraint of the system, not a proposal):
The enforcement instruments (a linter and a wire gate) carry no transition state: no deprecation warnings, no scheduled tier changes. A paradigm rule enforces at full strength from the moment it is adopted, and a retired form is simply out of paradigm.

QUESTIONS:
1. Independent genitive: should "the weights are ___" use "lemu's" (subject stem + 's), "lemr's" (determiner stem + 's), or some third shape? Rule and justify.
2. Given the axiom, is the enforcement design sound: the dependent genitive becomes "lemr" and the old "lemu's + noun" is out of paradigm with no warning tier? Or does the axiom create a real problem that English language practice would warn about?
3. Name every defect you can find in the overall design: the suppletion split you/your mapped to lemu/lemr; the shared reflexives lemuself/lemuselves with no reflexive derived from lemr; capitalization at sentence start; anything else you see.

RELEVANT ENGLISH FACTS (supplied for convenience; verify or reject them as you see fit):
- English independent genitive pronouns build on the dependent stem: my/mine, thy/thine, her/hers, your/yours, our/ours, their/theirs; "its" serves both uses.
- "For thine is the kingdom" (KJV, Matthew 6:13) is an independent genitive on the determiner stem; "to thine own self be true" (Hamlet) shows the same stem in dependent use before vowels.
- Historically "yours" is determiner stem + genitive -s (Old English eower + es).
- No standard English pronoun forms an independent genitive on the subject stem: *you's, *we's, *they's are unattested.
- Proper nouns take 's in both uses ("the weights are Fen's").
- Dialectal forms like "mines" exist and are nonstandard.

Rule independently. If the design is wrong, say so plainly.
