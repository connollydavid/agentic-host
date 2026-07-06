# plan/0066 task-band-and-ordinal-detection: a sanctioned task group, and the gate that catches its ordinal workaround

This milestone answers host-lifecycle#4 in two halves. A plan author who wants to group tasks has no
sanctioned construct, so an author reaches for an ordinal band name, the position-naming the
milestone-naming rule forbids. The fix is a content-named band over the anchored tasks (the construct),
and a detection rule so the gate catches the ordinal workaround the band replaces (the enforcement).

## The detection half (shipped as host-lint v0.14.0)

host-lint already blocks a phase-synonym noun followed by an arabic numeral. The gap was the spelled
form: a phase-synonym noun followed by a spelled-out ordinal read clean, which is exactly how the band
workaround in plan/0049 slipped every gate. host-lint now recognises a closed spelled set (the cardinals
and ordinals no higher than twenty) after a phase-synonym noun and blocks it the same way the arabic
form blocks, and the gather lane surfaces a novel such noun as an emergent-tell candidate.

The disposition is corpus-grounded, not asserted, per the plan/0055 doctrine. Spelled blocking applies
to the phase-synonym work-unit nouns only. It is excluded from the checklist nouns and from the
domain-heavy warn nouns, because their spelled forms are ordinary descriptive prose. The repo's own
`cast/applying-personas.md` carries the deciding data point, a legitimate spelled use of a checklist
noun that a blanket rule would have flagged and broken the zero-warning doc gate on.

Released as host-lint v0.14.0 (change class adds-flag, the tool flags a superset), reproducibly built,
re-pinned in `.host-software`, receipt recorded, and the host-template `tools/host-lint` pin bumped
(call/0038). The whole-suite `software --check` is green. VOCABULARY.md carries the new shape, and the
lib source stays flag-free so a real tell in it is still caught.

## The construct half (pending, ships with the host-lifecycle release)

The band is a content-named grouping over the anchored tasks, with execution order still carried by the
`depends` edges rather than by the band's name or position. The authoring surface is settled on data:
the real `qwen3.5-4b` authored both a heading-marked band and a per-task-field band correctly, and it
read group membership correctly in both, so the choice rests on the engineering factors. The heading
form wins on backward-compatibility (an existing plan with no marker parses unchanged), on rendering (a
visible divider in the book), and on referenceability (the band carries its own anchor). One
implementation note the Fen scoring surfaced: the parser must attribute a band marker only to its own
immediately-preceding heading, with no look-ahead, or it mis-reads a task as a band.

The construct is doctrine that ships in the template task-graph section (a spine change owing a ledger
entry) plus a `parse_tasks` recognition in host-lifecycle (tool-local). It ships with the host-lifecycle
release that also carries the coded remap and materialise fixes, plan/0062, and the book-mount tool
side, and re-vendors the host-lint above.

## Verification

Detection: host-lint unit and integration tests cover the block on a phase-synonym plus spelled ordinal,
the clean pass on a checklist or warn noun plus spelled ordinal, and the gather surfacing; the released
binary reproduces its recorded hash. Construct: a band-bearing plan fixture validates, a unit test
asserts the linear `depends` default still chains across a band heading, and the weak-agent authoring
run passes at the plan/0042 bar. Both halves land with the whole-suite verify gate green.
