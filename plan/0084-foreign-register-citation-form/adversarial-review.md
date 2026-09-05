# adversarial-review: five lenses on the built diff (2026-09-05)

The diff under review: host-lifecycle `85578b7` against `66c24d6` (spec, scan, verdict, disclosure, tests). The dedicated lens the cut named — a dead local record laundered through a foreign-looking URL — ran first and got the longest hearing.

## Lens 1: the escape-hazard (the dedicated lens)

Attack: the acceptance reads foreign by slug comparison, so a LOCAL dead record is laundered the moment an author writes a foreign-looking URL beside it — `[call/0039](https://github.com/connollydavid/agentic-host/blob/main/call/0039-….md)` in a repository whose own `call/0039` does not exist stops being dead, whether or not the foreign target exists.

Finding, and its disposition: the escape is real and it is the design's stated limit, not a defect in it. The sweep cannot read another repository offline; the citation line discloses "were not read" on every exit; and the URL the launderer must write names a real file in a real foreign register, which is a different claim than the bare dead pointer it replaces. What the attack DID change: the wrong-file case had to gate (it does — the label claiming one record over a URL naming another stays dead, proven by `a_url_naming_another_file_stays_dead`), and the local-slug case had to stay dead (proven by the second half of `a_foreign_citation_in_a_link_is_accepted_and_counted`). Carried as the limit, with the wording carrying it.

## Lens 2: origin spoofing and alternate hosts

Attack: same repository name, different owner (`slartibardfast/agentic-host`) — slug comparison catches it, because the comparison is the full slug. Alternate host spelling of the LOCAL repository (`raw.githubusercontent.com/connollydavid/agentic-host/main/plan/…`): the slug parses to the local one, so it is judged as today, dead when dead — correct, and it fell out of the segment walk rather than being designed in. A URL whose slug will not parse (`https://github.com/plan/0097-x/README.md`, no owner): fail closed, stay dead, proven by `an_unparseable_url_is_never_a_citation`.

Finding: none blocking. The segment walk accepts any forge host by design (gather-data rule six); a malicious well-formed URL pointing at a fork is form-true and existence-false — lens 1's limit again, not a new one.

## Lens 3: regression over the pre-existing verdicts

Attack: zero drift is the requirement — every shape v0.50.0 judged must be judged identically. The early-continue for citations sits BEFORE the dead check, so any reference wrongly marked `foreign_citation` silently loses its dead verdict.

Finding: the risk is real and it is where the mutation budget went. `enclosing_link_target` had to agree with `enclosing_link` on what is a link, and its in-target reconstruction initially omitted the token's own span — a URL token reconstructed as a broken URL, foreignness unestablishable, and the four-form test caught it as cited=0 where the design says 1. Fixed before the round closed; the full suite (306 unit, 34 exit-path) runs byte-identical verdicts on this tree through the gate.

## Lens 4: cost

Attack: the citation facts run per register reference, and plan/0078's defect class was per-reference work that reads state.

Finding: the facts are string work over the line's characters; the only state read per run is `origin_slug`, read once beside the room index. Measured on this tree at the built release binary: 2511 ms gate, same verdict text, against the 2134 ms recorded baseline on the same mount — inside mount variance, no budget breach. No finding.

## Lens 5: spec-code divergence

Attack: the spec models `foreign_citation` as a creation fact, `AcceptForeignCitation` with a corpus condition, and `RecordUncheckedRegister` sparing citations — three claims the code could drift from.

Finding: each is wired and each has a named, mutation-killed test (`scan_document_with` computes the fact at scan; the gate counts only what its corpus lists, the same condition the issue half carries; `count_unowned_registers` skips citations, so a software repository citing its host by link neither gates nor counts as unchecked). The obligations manifest discharges all 93 with `--strict-discharge` clean. One divergence noted and accepted: the spec's `saw_citation`/`disclosed_citations` latch is implemented as a counted line printed when the count exceeds zero — the count is the richer fact, and the spec's booleans model its existence.

## Disposition

Every blocking finding was fixed inside the round (lens 3's reconstruction). Two carries ride forward from the cast round (the `resolve` emission candidate; the doctrine wording), and lens 1's limit is carried into the doctrine node's required content.
