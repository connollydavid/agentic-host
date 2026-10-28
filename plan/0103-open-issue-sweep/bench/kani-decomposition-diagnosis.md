# plan/0102 diagnose: why the lem harnesses hung, found by bisection (2026-10-28)

The controlled experiments, each a minimal harness on the same stack (Kani
0.67.0 / CBMC 6.8.0, this machine):

| Harness | Input | Result |
|---|---|---|
| `verify_review_code_accepts_hash_digit` (calibration) | 1 symbolic byte | SUCCESS in 21 s |
| `vec_alloc_smoke` | 1 symbolic byte through `Vec::push` | SUCCESS in 13 s |
| `str_eq_smoke` | 1 symbolic byte through `str` equality | SUCCESS in 19 s |
| `classify_concrete_smoke` (unwind 4) | fully concrete content | FAILED in 22 s: unwinding assertion (the table loop needs more than 4) |
| `classify_concrete_smoke` (unwind 16) | fully concrete content | NO CONCLUSION in 5 minutes |
| `exact_word_..._n1` | 1 symbolic byte through the classifier | NO CONCLUSION in 10 minutes |

The classifier on fully concrete input hanging the solver isolated the cost to
the code shape, and the construct was `word[..3].eq_ignore_ascii_case("lem")`:
a str range slice reaches the panicking-slice machinery, and that is what the
solver drowns in. Replaced with explicit ASCII byte comparisons, the concrete
control passes at once. With the slice gone, the remaining failures became
legible unwinding assertions (a 13-entry table walk needs more than
`unwind(12)`), fixed by `unwind(24)` everywhere. `exact_word_..._n6` then
concluded: SUCCESS in 9 m 19 s.

What did not help, recorded so nobody re-tries it: `from_utf8_unchecked` (no
change; the validation was not the cost), the heap-free classifier shape
(correct to keep anyway, but not the cause), `--no-slice-formula` (not a CBMC
6.8 flag; the kani flag hung), and concrete-vs-symbolic length (necessary for
legibility, not sufficient without the slice fix).

The landed shape: one harness per concrete length (a symbolic length across
monomorphized copies is one enormous VC), `unwind(24)` on every harness, the
classifier filling a fixed `[LemKind; 5]`, and the byte-level prefix. The
lem-table and line-framing worst cases did not conclude inside 20-minute
local caps; the tag run over the 22-row matrix is the acceptance.
