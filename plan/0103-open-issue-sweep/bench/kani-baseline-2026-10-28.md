# plan/0102 diagnose: the three stuck harnesses, timed locally (2026-10-28)

Kani 0.67.0 (the CI-pinned version), one harness per run, `--output-format terse`,
a 600-second cap, on this machine (WSL, the crate at its pin 90a0d71):

| Harness | Result |
|---|---|
| `scan_line_never_panics` | no conclusion; killed at the 600 s cap |
| `hits_are_word_bounded` | no conclusion; killed at the 600 s cap |
| `form_and_mangle_hits_are_classified_by_the_table` | no conclusion; killed at the cap (run stopped early, the first two establish the shape) |

None of the three concludes in ten minutes locally, consistent with the CI record
(each dies at GitHub's six-hour ceiling) and with stage zero's diagnosis: the
verification condition spans the whole matcher, and the harnesses build a
symbolic-length `Vec<u8>` byte by byte, heap `String`s per word and per hit, and
run the thirteen-entry table over symbolically derived words, with no unwind
bounds declared anywhere.

The decomposition follows plan/0102 as cut: pure per-word classifier and word-run
extraction, word-level proofs at n at most 10 (full table coverage including
`lemuselves`), framing properties split per-property at reduced length, an
explicit `#[kani::unwind(K)]` on every harness, one matrix row each.

Operational note: `timeout 600 cargo kani ... | tail` does not return at the cap:
the solver children survive the SIGTERM and hold the pipe, so `rc` read tail's
and `elapsed` printed only after the children drained. Time the kani process
directly next round.
