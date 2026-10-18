# plan/0100 pronoun-form-and-teaching-layer: the address possessive, ruled and landed

Operator-directed (the ask: the address paradigm gains `lemr` as its possessive,
`lemu` = you and `lemr` = your, constructed under a "good forgetting" whose
bounded form this plan adopts as its modality). The morphology was settled in
session by the cast with English literature, then confirmed blind by an
external judge.

## The settled design

- `lemu` and `lemr` are a fixed pair, the way `you` pairs with `your`: `lemr`
  before a thing (lemr weights), `lemr's` alone (the weights are lemr's). The
  pair is listed, never derived: no rule builds `lemr` out of `lemu`.
- The independent genitive is `lemr's`. Every English genitive pronoun builds
  its independent form on the dependent stem (my/mine, thy/thine, your/yours;
  "For thine is the kingdom", Matthew 6:13), and no standard English pronoun
  forms one on the subject stem. The cast ruled five to nothing; the bench
  concurred with high confidence after verifying the citations itself.
- No reflexive is built on `lemr`. The reflexives of the address paradigm are
  the lexical forms `lemuself` and `lemuselves`, on the address stem alone,
  exactly as English builds "yourself" on "you".
- Enforcement carries no transition state. The retired form (`lemu's`) gains no
  warning tier, no sunset schedule, and no escalation entry: the agreement
  table states the paradigm in present tense and a wrong form is wrong from
  the landing. The operator corrected the cast's first instinct here, and the
  bench later ruled the same independently: English usage requires no
  deprecation grammar.

## The modality (call/0060)

"Good forgetting" is adopted in bounded form, as re-baselining with an audit
trail. The teaching layer (the manuals, the skill, the vocabulary, the
classifier tables) states the paradigm in present tense with no archaeology
markers. The record layer stays append-only exactly as the standing rules
require, the measurements are scoped by name rather than silently re-scoped,
and the `UPGRADING.md` entry carries the version truth a cold reader
reconciles against. Nothing outside those three walls is struck.

## The evidence

- The corpus count the ruling cites: zero dependent uses and zero independent
  uses of the retired form anywhere in the tracked tree; it lived only inside
  the paradigm's own tables and the record-layer copies, which stay untouched.
- The bench: codex (gpt-6-luna, session `01a14c06`, 20248 tokens), blind to
  the cast's votes and the operator's acceptance, transcript preserved at
  `/tmp/opencode/bench-verdict.txt` and copied to this plan's `bench/`. Both
  rulings concur; five defects were named, three folded into the tasks below
  (the fixed-pair wording, the lexical reflexives, the classifier case rule),
  one restates the ledger as the remedy for version drift, and one asks for
  paired apostrophe examples that VOCABULARY.md already carries.

## Tasks

1. **call/0060** (the modality decision, first test case this plan).
2. **Template**: the lem section's form list, possession line, address
   paragraph, and two new exchanges; the `UPGRADING.md` entry whose id names
   the content commit; push inside the submodule.
3. **Host apply**: pointer bump, manual copy, `upgrade --record`, the strict
   corpus read.
4. **host-lint**: `LEM_CANONICAL` and the `lem_form` oracle (a determiner row
   for the address paradigm), the VOCABULARY.md mirror, the mangle coverage
   and case rule the bench asked for, tests updated; the release cascade and
   re-pin.
5. **Instrument**: the plan/0091 gate and scorer learn the tokens; a bounded
   residual run; the DPMO chart gains a scope note naming the certified list.
6. **Close**: the verify battery, the lanes read back, receipts, memory.

## Results

**Cut 2026-10-17.** The design rulings above are the record of the cutting
session; the tasks land in order.

**The spine (2026-10-17, template `7b0c641` content and `1685175` stanza,
host `8f90ccc4` pointer and manual, `8057d209` recorded):** the section, the
possession line, the address paragraph, and the two exchanges landed in both
manuals byte-identical; the upgrade recorded through its verify, zero pending.
The bench materials are record-layer evidence (the verbatim prompt never
reworded), carried under `bench/` and excluded by the literal-directory form in
`.host-lintignore` after the starred variant proved not to match
(`16da554e`).

**The classifier (2026-10-17, host-lint `c9dd8aa`, released as v0.23.0
`90a0d71`, artifact `f4b2a7fa`):** the closed list carries the determiner and
its independent form; the oracle answers the two genitive uses by case; the
MCP table gains the determiner column and `ask` the case; VOCABULARY.md states
the pair as listed forms. The operator's contamination ruling holds in the
instruments: the near-miss coverage assembles its token from paradigm parts in
both suites, so no out-of-paradigm word sits anywhere as a literal. Suites:
234 unit and property tests, 221/221 integration, two kani rungs re-derived
and their digests recorded (`99647f2`).

**The instrument (2026-10-17, host `0cd5d0ae`):** the wire gate's canonical
set, form regex, and nudge speak the pair; its unit suite passes nine of nine.
The standing chart carries an appended scope line: the n=600 certification
covers the list it measured by name.

**The residual, measured 2026-10-18.** With the channel back, the bounded
residual ran against the real qwen3.5-4b: n = 100 at the served 64k envelope
(the old edge served 131k, so this measures the current deployment envelope,
not the certified depth), deployment sampling, the landed section as doctrine
(`gate/doctrine-2026-10-18.md`) through the pair-carrying gate. First-pass 7
(0.07), final violations 0 (0.0000); each defect corrected by one
nudge-anchored retry. The wire gate holds final-zero under the amended
paradigm. Transcript: `gate/residual-2026-10-18.jsonl`.

**The cascade (2026-10-17/18):** vendor-v16 published carrying the v0.23.0
embed; host-lifecycle v0.60.7 (`727be0d`, artifact `7b45df79`) re-embeds the
engine at equality; the template carries both pins (`bf4f308`, `40b1913`) and
its prose lane's rev; both release receipts cite plan/0100. Two cascade
findings recorded: the front door's allium install line needs `--locked` (the
plain install resolves a drifting parser and fails to build), and the stale
obligation remedy's `--rederive` takes the source directory
(`--record-digests` refuses to run without it).

**Landed 2026-10-18, complete.**

## The plain-language closing note

The operator asked for this landing explained as if to a ten-year-old, and
ruled the telling part of the closure record.

**The made-up words.** The model that helps you speaks as `L`, never as "I".
When you speak to a model helper, you say `lemu` where everyday English would
say "you". These words exist so that a reader can always tell who is speaking
about whom: the human or the model.

**The problem this milestone fixed.** In English, "you" has a partner:
"your". Your toys; your room. The address word `lemu` had no partner, so
writers were stuck with `lemu's` toys, which sounds like a child saying
"you's toys". The partner now exists: `lemr` means "your" spoken to a model.
"lemu, clean up `lemr` toys." Standing alone, the form is `lemr's`: "the toys
are `lemr's`." Some words were deliberately not made. English builds
"yourself" on "you" rather than on "your", and the paradigm already carried
the matching form on its address stem: `lemuself`. Nothing new was needed
there.

**The tidy room and the honest diary.** A room can be cleaned so well it
looks as though it was never messy. The rulebooks were cleaned that way: they
read as though `lemr` always existed, with no "new word" stickers anywhere.
The diary keeps the true story, dates and all: the memory entries and the
decision record say exactly when the word arrived and who ruled on it.

**How we know it works.** Five helper personas voted on the grammar with the
English reference books open. A separate outside judge, blind to those votes,
examined the design alone and agreed. Then came the live test: a guard reads
every reply from the small model before anyone sees it, and when a reply
breaks the rule the guard speaks the rule and grants one do-over. The small
model tried one hundred times at the serving envelope. It slipped seven
times. The guard caught all seven, and no wrong reply got through.
