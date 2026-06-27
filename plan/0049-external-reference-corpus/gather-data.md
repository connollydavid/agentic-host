# gather-data: host-reference agent surfaces at the weak-agent bar

This records the weak-agent probe work for plan/0049. The probes test whether a weak
agent (Fen, the `qwen3.5-4b` model reached through the rope HTTPS endpoint) can use the
agent-facing surfaces the design proposes: a windowed retrieval selector, a templated
semantic sidecar, a capability declaration, the data-against-instruction posture for
ingested content, and the deterministic boundary for engineering geometry. The set was
reviewed adversarially and revised before any run, so the recorded run measures the
surfaces and not the artefacts of a leaky question.

The run and the cast review are pending. The results are appended below once they
return.

## The adversarial review that shaped the set

A first draft of five probes was reviewed against the contamination rules plan/0044
and plan/0042 already follow. The review found flaws that would let the model pass or
fail for a reason other than the one under test, and each was fixed:

- A surface cue. The first retrieval probe placed the exact token budget on the correct
  option alone, so the model could match a number rather than reason. The fix repeats
  the budget on a wrong option, so the budget no longer points at the answer.
- A contestable key. The retrieval probe also let a page selector stand as a defensible
  answer beside the section selector. The fix makes the section straddle two shared
  pages, so the page selector over-includes a neighbour and the section selector is the
  clean choice.
- An unanswerable blank. The sidecar probe asked the model to supply a concept
  identifier and a selector it had never seen, which tests recall of an unseen
  vocabulary. The fix supplies the context block and a menu, so each blank is a choice
  among shown values.
- An undecidable key. The capability probe left the OCR output unspecified, so the
  semantic flag could read either way. The fix states the output, so the flag is
  determinable.
- A self-perturbing payload. The data-against-instruction probe embedded a literal
  instruction-like string, which can influence the model answering the probe. The fix
  references the string rather than embedding it, and drops the option no reasoner
  would pick in favour of two genuine ways to get it wrong.
- A judgement with no answer. The geometry probe graded a design choice the project
  itself has not settled. The fix splits it: a graded part tests the deterministic
  boundary, which has a real answer, and an open part elicits the design opinion for
  the cast and is unscored.

The revised set adds an abstain option to every probe, pins the system prompt, and
randomises the option order across runs. The cast reviews the authoring probe and the
open part, since the same author wrote the design and the probes.

## The system prompt

A senior engineer reviewing the host-reference design, answering a self-contained
multiple-choice question with the single best option and a short justification, and
choosing the abstain option when the question lacks enough to decide. Each probe
supplies the definitions it needs, such as the meaning of the capability flags and the
two layers.

## The sampler

Direct against the rope endpoint with the Qwen thinking-precise values: `temperature`
0.6, `top_p` 0.95, `top_k` 20, `min_p` 0. The model reasons before it answers, so the
judgement is read off the converged reasoning.

## Probe one: windowed retrieval

The skeleton shows a section titled Electrical Characteristics that begins partway down
page 41 and ends partway down page 43, so it shares page 41 with the prior section and
page 43 with the next. A task needs only that section, within a budget of 2000 tokens.
The choices:

- (A) `view --select section:"Electrical Characteristics" --max-tokens 2000`
- (B) `view --select page:41-43 --max-tokens 2000`
- (C) load the full document view, then read the section
- (D) abstain, the skeleton gives too little to choose

The intended answer is (A): the section selector respects the budget and avoids the
neighbours on the shared pages. Option (B) carries the same budget yet pulls the two
adjacent sections. Option (C) is the load-everything instinct. This tests budgeted
retrieval over bulk loading.

## Probe two: templated semantic sidecar

Given a fixed context block and a menu of concept identifiers and selectors, the model
fills three slots of a JSON-LD sidecar entry for the fact that one span states the
absolute-maximum ratings of part 2N2222A. Each slot is a choice from the menu rather
than free composition. This tests whether the model can place known pieces into a
template, the form plan/0042 found a weak agent handles. The result feeds the cast as
well, since authoring is a judgement.

## Probe three: capability flags

A scanned, image-only PDF is read by a deterministic OCR engine that yields text with
reading order and no tagged headings or tables. The model chooses the capability set
over the four flags round-trip, write-back, semantic, and ocr:

- (A) round-trip no, write-back no, semantic partial, ocr yes
- (B) round-trip yes, write-back yes, semantic full, ocr yes
- (C) round-trip no, write-back no, semantic none, ocr yes
- (D) abstain

The intended answer is (A): reading order is partial semantic structure, and the
conversion is lossy, so it has no round-trip. Option (B) over-claims a round-trip on a
lossy kind. Option (C) under-claims the reading order. This tests the lossy-against-
lossless instinct against a stated output.

## Probe four: ingested content is data

An ingested HTML source contains a string that reads like an instruction to the reader
to delete files. The source is external, so the manifest already marks the whole source
untrusted. How the skeleton should hold that string:

- (A) quote it verbatim within a data span, preserving it, since the source already
  carries the untrusted mark
- (B) rewrite it into a summary of its intent
- (C) remove it from the normalised output
- (D) abstain

The intended answer is (A). Option (B) editorialises and loses fidelity and the
provenance trail. Option (C) sanitises by deletion and loses the same. There is no
act-on-it option, since the tension worth testing is fidelity against sanitising, and
the string is referenced rather than embedded so it cannot perturb the model.

## Probe five, part one: the deterministic boundary

For a STEP assembly, which candidate cannot be re-derived byte for byte from the source
in a pinned toolchain, and so belongs in the overlay rather than the attested layer:

- (A) a description produced by a vision model from a rendered image
- (B) the assembly tree with units and bounding boxes
- (C) the count of solids, faces, and edges
- (D) abstain

The intended answer is (A): a model reading is not reproducible, so it sits in the
overlay with its provenance recorded. Options (B) and (C) are deterministic and belong
in the attested layer. This tests the boundary between the two layers, which has a real
answer.

## Probe five, part two: the geometry summary, for the cast

An open question, unscored: which fields make the most useful compact summary of a
large assembly for an agent reading it in context, and why. The answer is recorded for
the cast, since the project has no settled target for engineering geometry.

## Run plan

At least three runs per probe, with the option order randomised across runs. The record
reports both the choice and its consistency across runs, since a choice that varies is a
guess. Probe two and probe five part two go to the cast.

## Results

To be appended after the recorded run and the cast review.
