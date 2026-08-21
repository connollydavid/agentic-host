# calx-knap

A controlled register for prompt and memory files. *Knap*: to shape flint by striking flakes off to leave the working edge. *Calx*: the counting pebble that gave us *calculus*; in the alchemists' books, the residue that survives calcination. The register removes mass and keeps the edge.

Scope boundary: the register binds artifacts, never the harness that measures them. Probes, rewrite prompts, and grader instructions stay in full longhand English, exempt from the K-rules, so every model under test reads the same instrument and the document is the only compressed variable. The boundary is audience: register text is written for machine decoders, and prose rulers built for human-audience documents measure a different genre. An adopting repo that runs an outer prose linter scopes it with that tool's own exclusion mechanism; nothing in the register names or configures the tool.

## Premise

Three design sources, one conflict, one delivery form.

ASD-STE100 was built for a stressed human decoder on a hangar floor. Caveman mode was built for a metered machine decoder. Classical Chinese (文言, wenyan) is the field test showing a register can stay terse and precise for two millennia, provided the grammar changes shape to pay for the missing words.

The conflict: STE forbids telegraphic omission. It mandates articles and full clauses because omission is where human misreadings start ("close the valve": command, or the valve that is near?). Caveman's savings come almost entirely from telegraphic omission. A naive merge is incoherent.

Wenyan supplies the resolution. It has no articles, no inflection, and drops recoverable subjects and objects freely, yet it is not ambiguous soup: rigid slot order carries reference, and a small closed set of particles carries logic. In classical corpora the particles sit at the top of the frequency tables (之 ranks first; the register is nicknamed by its emblem set 之乎者也) precisely because everything else is droppable and they are not. calx-knap imports that division of labour: position does the work of ballast function words, a fixed operator lexicon does the work of logic, and nothing else is grammar.

The RFC series supplies the delivery form: a closed capitalized keyword set with normative force, a robustness asymmetry between writer and reader, and the editorial habit of numbered single-claim rules that survive being quoted out of context.

## What each source contributes

**ASD-STE100** (Issue 9, 2025-01-15): 53 writing rules in 9 sections plus a controlled dictionary of roughly 900 approved words, each with one meaning and one part of speech, and roughly 1,200 banned words with substitutes. *Fall* means to move down by gravity, never to decrease; *start* is approved, *begin/commence/initiate* are not. Procedural sentences cap at 20 words, descriptive at 25, paragraphs at 6 sentences, one instruction per sentence, active voice, no synonym variation. calx-knap takes the lexical discipline and the instruction grain. It rejects mandatory articles and full clauses: correct for a fatigued human reading torque values at 3 a.m., wasted tokens for a model. The dictionary itself is ASD's copyright; build a project word list from corpus frequency instead. Prior art for pointing STE at agent-facing English exists (danyuchn's asd-ste100-skill); calx-knap differs in taking a token budget as a co-equal goal.

**Caveman**: the mass target (~46% on memory files via `caveman-compress`), byte-exact protection of code, commands, and error strings, graded intensity levels, and a culture of honest measurement. calx-knap takes the target, the span protection, and the levels. It rejects unregulated omission: nothing in caveman stops "never X unless Y" degrading to "no X", and that is the failure mode that costs behaviour on small models.

**Wenyan**: four structural precedents.

1. *Particles as protected logic.* Negation (不), prohibition (勿), necessity (必), restriction (唯), universals (凡, 皆), conditionals (若…則), cause (故) survive every act of compression the tradition performed. The Sunzi opens chapter after chapter with 凡 ("in every case of…") before an imperative: a spec register, 2,300 years old.
2. *The judgment sentence.* "A 者, B 也" asserts A is B with two particles and no copula verb. Definition without ballast.
3. *Canon and explanation.* The Mohist Canons pair an ultra-compressed canonical line (經, jing) with a separate expansion (說, shuo). Canon A1: 故, 所得而後成也, roughly "cause: what a thing must get before it comes about" (Graham's rendering). Compressed text is canonical; the gloss lives out-of-band. Cavemem's round-trip-guaranteed grammar rediscovers this shape.
4. *Deterministic decompression markup.* Kanbun kundoku let Japanese readers expand Chinese text into Japanese syntax using kaeriten reading marks: a fixed annotation scheme that makes the expansion mechanical, not interpretive.

**Internet RFCs**: three practices. BCP 14 keyword discipline (RFC 2119, sharpened by RFC 8174): a closed set of capitalized words carries requirement force, and only the capitalized instances are normative; the same word in lowercase is ordinary prose. calx-knap gives the whole operator class the same capitalized force. The robustness principle (RFC 1122 §1.2.2, after Postel), mapped onto roles: the writer emits the register, the reader accepts anything up to full natural English, so a half-converted file degrades to prose instead of breaking. And the editorial form itself: numbered rules, one claim per sentence, checkable references. Fifty years of memos written for machines and argued over by humans is prior art for the genre.

## The operator class

Shannon put the redundancy of printed English near 75%. That redundancy is the compression budget, and the whole design question is which redundancy to spend. calx-knap splits function words into two classes:

*Ballast*: articles, copula, expletive subjects ("there is", "it is"), hedges, politeness, meta-discourse. Deletable once slot order is fixed, because position recovers their work.

*Operators*: the words whose deletion changes truth conditions. Irreducible. Protected like code fences.

| operator | role | wenyan analogue |
|---|---|---|
| NOT, NEVER | negation, prohibition | 不, 勿 |
| CANNOT | inability | 不能 |
| ONLY | restriction | 唯 |
| UNLESS | exception | 非…不 pattern |
| IF, THEN | condition, consequent | 若…則 |
| ALL, EACH | universal | 凡, 皆 |
| ANY, NONE | existential, empty | 或, 莫 |
| BEFORE, AFTER | sequence | 先, 後 |
| MUST | necessity | 必 |
| SHOULD | recommendation | 宜 |
| MAY | permission | 可 |
| BECAUSE, SO | cause, consequence | 以, 故 |

## Rules

Tags mark lineage: [STE], [CVM] caveman, [文] wenyan. The rules obey themselves. Where rules conflict, meaning rules (K6, K8, K12) outrank surface rules (K16, K17), and surface rules outrank the K5 budget target; the preferred resolution restructures the line so an operator carries the logic. The K-register is append-only: a number, once assigned, is never reused and never reshuffled; a retired rule leaves a gap; a new rule takes the next number. That contract is what lets a bare K-number serve as a durable name.

**Lexicon**

- K1. One term, one meaning, one part of speech, read per slot type: the object slot of BEFORE and AFTER nominalizes, so a verb there names its event (`BEFORE commit`). Keep a project word list; prefer entries that are single tokens on every target tokenizer. [STE, 文]
- K2. One synonym survives. Same referent, same string, every file. Verbatim reuse also feeds prefix caching. [STE]
- K3. Verbs: imperative for procedure, bare present for fact. No modal stacking. [STE]

**Line grammar**

- K4. Slot order fixed: `[condition:] [agent] action object (reason)`. Topic fronting allowed as `topic: comment`. [文]
- K5. One instruction per line. Budget 12 tokens; hard cap 20. Measure on the zone-lifted line: EACH byte zone counts as one placeholder token. [STE, tightened by CVM]
- K6. Delete ballast. Deletion legal only where K4 order recovers reference; if a reading survives that you did not intend, restore the word. [CVM, 文]
- K7. No pronouns across lines. Repeat the noun. Pro-drop applies inside a line only. [STE, 文]

**Operators**

- K8. Operator words: never deleted, never abbreviated, never synonym-swapped. Write NOT, NEVER, CANNOT, ONLY, UNLESS, IF, THEN, ALL, EACH, ANY, NONE, BEFORE, AFTER, MUST, SHOULD, MAY, BECAUSE, SO in full, capitalized. Per BCP 14 practice, only capitalized instances carry force; lowercase occurrences read as ordinary prose. [文, RFC 2119/8174]
- K9. Negation sits directly before its verb. One negation per line, counting operator negation only (NOT, NEVER, CANNOT); morphological negatives (unrelated, impractical) are vocabulary under K1. [STE, 文]
- K10. Exception follows its rule, on the same line or the next, opened by UNLESS. Never mid-clause. [STE]
- K11. Parallel content takes parallel slots: sibling lines share shape. [文, 骈文 parallelism]

**Protection and structure**

- K12. Code, commands, paths, URLs, numbers with units (spelled or numeric), error strings: byte-exact. [CVM]
- K13. Six lines max per block, each block under a topic label; the label takes the artifact format's native heading form (markdown headings in a markdown artifact). [STE]
- K14. Canon and gloss: the compressed file is canonical; expansions live in a companion file keyed by stable IDs; the round trip is checkable. [文 經/說, CVM cavemem]
- K15. Encoder strict, decoder liberal: writers emit the register; readers MUST accept full natural English. Partial conversion degrades to prose, never to breakage. [RFC 1122]

**Surface**

- K16. Emitted register lines use ASCII punctuation. Typographic marks (em and en dashes, curled quotes, arrows, ellipsis) are ballast: replace with a colon, a comma, parentheses, or an operator; write sequence with BEFORE and AFTER, never `from X to Y`; enumerate without a closing conjunction at three items or more; a two-item pair keeps its conjunction. Byte zones (K12), quoted material, and cited foreign-script text are exempt. [RFC]
- K17. Labels name content. Topic labels and headings carry content words, never bare numerals or position codes; a source heading named by numeral or position is renamed to its content at compression. A number is a durable name only inside an append-only register; a position in a re-cuttable sequence takes a content name. [RFC]

## Line grammar sketch

ABNF (RFC 5234). Informative until a bound structural gate enforces it; the K-rules win any conflict.

```abnf
file      = 1*( line LF )
line      = topic-label / rule / byte-zone
rule      = [ condition ":" SP ] clause *1( SP "UNLESS" SP clause )
clause    = [ operator SP ] [ agent SP ] action [ SP object ]
            [ SP "(" reason ")" ]
operator  = "NOT" / "NEVER" / "CANNOT" / "ONLY" / "IF" / "THEN" / "ALL"
          / "EACH" / "ANY" / "NONE" / "BEFORE" / "AFTER"
          / "MUST" / "SHOULD" / "MAY" / "BECAUSE" / "SO"
```

## Worked example

Source, typical memory-file prose (~50 tokens):

> Please make sure that you always run the complete test suite before committing any changes. The only exception is when a change touches documentation files exclusively, in which case tests are not required. You should never force-push to the main branch.

STE register (~35 tokens): articles kept, one instruction per sentence, approved words.

> Always do the full test procedure before you commit a change. If a change is only to the documentation, the tests are not necessary. Do not do a force-push to the main branch.

Caveman register (~13 tokens):

> run tests before commit. docs-only skip. no force-push main.

Two tokens of logic went missing: "docs-only skip" no longer says what is skipped, and the always/exception structure has gone soft.

calx-knap (~17 tokens):

> BEFORE commit: run full test suite. UNLESS docs-only change. NEVER force-push main.

About 66% off the source, three or four tokens over caveman, operators intact. Counts are approximate and tokenizer-dependent.

The same rule in wenyan:

> 凡提交, 必先盡試; 唯改文書者免。主幹勿強推。

Gloss: 凡 fán, in every case of; 提交, commit; 必 bì, must; 先 xiān, first/before; 盡試, run the tests in full; 唯 wéi, only; 改文書者, that which changes documents; 免 miǎn, is exempt; 主幹, the trunk; 勿 wù, do not (prohibitive); 強推, force-push.

At maximal density the surviving grammar is exactly the operator column: 凡, 必, 先, 唯, 者, 勿. ALL, MUST, BEFORE, ONLY, the nominalizer, NEVER. The tradition compressed everything else out and kept these. That convergence is the empirical case for K8.

## Decoder budget and limits

Cross-linguistic speech studies find that languages trade information density per syllable against rate and converge on roughly 39 bits per second of transmitted information (Coupé et al. 2019). Density is never free; it moves work to the decoder. For calx-knap the consequence is procedural: validate compressed files against the weakest model that will read them. A rule that holds on a 4B canary holds upward; the reverse is untrue. For automated passes, the caveman fine-tune supplies measured starting gates: accepted rewrites sat in a 0.91-0.98 semantic-cosine band against source, and fence exactness fell short of 100% without external span handling (Caveman Labs, 2026). SO: lift byte zones before any model touches the text.

Character density and token density are different quantities. Tokenizers price languages unevenly (Petrov et al. 2023), so a wenyan-style CJK register pays off on CJK-efficient tokenizers such as Qwen's and can lose elsewhere. Measure per tokenizer before adopting a level.

Brevity itself can help: across 31 models (0.5B-405B), constraining large models to brief responses raised their accuracy by about 26 points on some benchmarks and reversed size hierarchies on others (Hakim 2026, arXiv:2604.00025; single-author preprint). That supports the length aim; it does not license touching operators.

STE optimizes misreading risk, and some STE rewrites run longer than their source. calx-knap inherits the priority: where token budget and an operator conflict, the operator wins.

## References

- ASD-STE100, Issue 9. ASD Simplified Technical English Maintenance Group, 2025-01-15. 53 rules in 9 sections; ~900 approved words, one meaning and one part of speech each; ~1,200 unapproved words with substitutes. asd-ste100.org.
- Brussee, J. *caveman* and *cavemem*. github.com/JuliusBrussee/caveman; github.com/JuliusBrussee/cavemem, 2025-2026.
- Caveman Labs. "The caveman phenomenon." caveman.so/labs, 2026. CaveGemma cosine and fence-exactness bands.
- danyuchn. *asd-ste100-skill*. github.com/danyuchn/asd-ste100-skill, accessed 2026-08-07.
- Bradner, S. "Key words for use in RFCs to Indicate Requirement Levels." BCP 14, RFC 2119, 1997.
- Leiba, B. "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words." BCP 14, RFC 8174, 2017.
- Braden, R., ed. "Requirements for Internet Hosts: Communication Layers." RFC 1122, §1.2.2, 1989.
- Crocker, D., Overell, P. "Augmented BNF for Syntax Specifications: ABNF." STD 68, RFC 5234, 2008.
- Shannon, C. "Prediction and Entropy of Printed English." *Bell System Technical Journal* 30(1), 1951.
- Coupé, C., Oh, Y.M., Dediu, D., Pellegrino, F. "Different languages, similar encoding efficiency: Comparable information rates across the human communicative niche." *Science Advances* 5(9), 2019.
- Petrov, A., La Malfa, E., Torr, P., Bibi, A. "Language Model Tokenizers Introduce Unfairness Between Languages." NeurIPS 2023.
- Pan, Z. et al. "LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression." arXiv:2403.12968, 2024.
- Kuhn, T. "A Survey and Classification of Controlled Natural Languages." *Computational Linguistics* 40(1), 2014.
- Ogden, C.K. *Basic English*, 1930. Ancestor line: Caterpillar Fundamental English (1970s), AECMA Simplified English (1986), ASD-STE100.
- Pulleyblank, E.G. *Outline of Classical Chinese Grammar.* UBC Press, 1995.
- Graham, A.C. *Later Mohist Logic, Ethics and Science.* Chinese University Press, 1978. Canon A1.
- Harbsmeier, C. *Science and Civilisation in China*, vol. 7 pt. 1: *Language and Logic.* Cambridge, 1998.
- Frellesvig, B. *A History of the Japanese Language.* Cambridge, 2010. Kanbun kundoku and kaeriten.
- 孫子兵法 (Sunzi), 凡-opened imperatives; 墨子·經上 (Mohist Canons), 經/說 structure.
- Hakim, M.A. "Brevity Constraints Reverse Performance Hierarchies in Language Models." arXiv:2604.00025, 2026. Preprint, single author.
