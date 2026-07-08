# plan/0070 benchmark-data-numerals: the bare-numeral lane stops flagging measurement data

Answers [host-lint#21](https://github.com/connollydavid/host-lint/issues/21). The
bare-numeral scanner flags every numeral-shaped token in document content as a potential
naming tell, so a benchmark-heavy engineering record produces thousands of false positives
where the numerals are measurement values, not filing-code labels. The
`host-lifecycle remap --check` gate cannot close with them present, and declaring each
value in the LEXICON does not scale: one such record carries 829 once-only measurement
values. The naming and prose lanes are clean on these records; only the bare-numeral
advisory fires on data.

The fix is precision at the warn tier, not a new escape. The bare-dotted-code rule
(VOCABULARY.md §4) gains the context it was missing: a numeral that sits in a data
position is skipped. The noun-gated flag tier is untouched, so a real tell still flags
wherever it appears.

## The false-positive classes, grounded in a Fen run

A neutral classification probe on the real qwen3.5-4b (see gather-data.md) returned 32 of
32 correct across two temperatures and a shuffled order. The boundary Fen drew is the
boundary the rule will encode. The false-positive classes are a table cell, an
approximation or comparison operator, and a compound or domain unit. The label controls
stayed label, including the load-bearing precision case: a real tell placed inside a table
cell still reads as a label, because the flag tier is location-independent.

## Decided direction

Four additions to the warn rule, each narrowing it only:

- Table cells. A bare numeral whose neighbours are pipe delimiters is a data cell; the
  column header that carries the unit sits on another line the token-local rule cannot
  see.
- Prose operators. A numeral preceded by an approximation or comparison operator, or
  followed by the multiplication sign, is a quantity.
- Compound units. A numeral followed by a slashed unit token is a quantity; the slash is
  a structural signal in the same way the pipe is.
- Domain units, declared. A non-structural domain unit after the numeral is declared in
  the LEXICON and consulted alongside the built-in unit set. An all-caps unit before the
  numeral is already skipped by the all-caps designator rule; the gap is a domain unit
  that follows.

## Open design questions

- The unit-declaration form. Whether the LEXICON carries a dedicated block for units or a
  per-entry marker is an authoring-ergonomics call. A second Fen run settles it the way
  plan/0066 settled the band form, rather than the author guessing.

## Build sequence

### Gather the Fen data {#gather-data}
- verify: the classification table in gather-data.md is 32 of 32 at two temperatures

### Skip table-cell numerals {#skip-table-cells}
- depends: #gather-data
- verify: cd software/host-lint/main && cargo test table_cell
- inputs: software/host-lint/main/src/lib.rs

### Add prose-quantity operators {#prose-quantity-operators}
- depends: #gather-data
- verify: cd software/host-lint/main && cargo test quantity_operators
- inputs: software/host-lint/main/src/lib.rs

### Recognise slashed compound units {#compound-units}
- depends: #gather-data
- verify: cd software/host-lint/main && cargo test compound_units
- inputs: software/host-lint/main/src/lib.rs

### Declare domain units in the LEXICON {#lexicon-domain-units}
- depends: #gather-data
- verify: cd software/host-lint/main && cargo test declared_units
- inputs: software/host-lint/main/src/lib.rs, software/host-lint/main/src/main.rs

### Document the shapes in VOCABULARY.md {#update-vocabulary}
- depends: #skip-table-cells, #prose-quantity-operators, #compound-units, #lexicon-domain-units
- verify: cd software/host-lint/main && cargo test vocabulary
- inputs: software/host-lint/main/VOCABULARY.md

### Update the spec and obligations {#spec-and-obligations}
- depends: #update-vocabulary
- verify: cd software/host-lint/main && host-lifecycle obligations host-lint.allium --tests tests
- inputs: software/host-lint/main/host-lint.allium, software/host-lint/main/host-lint.obligations

### Release and re-pin {#release-and-repin}
- depends: #spec-and-obligations
- verify: attested operator

### Close host-lint#21 {#close-issue}
- depends: #release-and-repin
- verify: attested operator

## Follow-ups (not this plan)

- The density advisory. The issue's third option, a single advisory when a document
  carries very many bare numerals, is out of scope; the precision fix removes the mass of
  false positives directly, so the density signal is no longer needed to close the gate.

## Verification

The released host-lint binary reproduces its recorded hash. The unit and integration
suites cover each new skip and its controls, with a real tell still flagging inside a
table cell. The obligations manifest is fully dispositioned, and the whole-suite verify
gate is green.
