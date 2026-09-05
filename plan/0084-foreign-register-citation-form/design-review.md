# design-review: the cast round on the accepted citation form (2026-09-05)

The design on the table when the round ran: the link-anchored accepted form as cut, the counted disclosure on every exit, the sigil rejection, and the built diff (host-lifecycle `85578b7`: spec `c8eaf9d`, six unit tests, two exit-path tests, three mutation kills). Each chair attacked their own first preference before speaking.

## Mara (the operator)

Concern: what does the form cost to keep green? The disclosure prints on every sweep of every tree that carries citations, so the count line becomes a permanent resident of this tree's verdicts the moment authors start writing the form.

Disposition: priced, and cheap. The line is one count and never an enumeration; the gate's exit partition is untouched (the built diff cannot change an exit code, proven by the suite); and the count is zero today, so the line arrives only as fast as authors adopt the form. No new gate, no new release-cadence cost — the failure mode call/0052 priced out is structurally absent here.

## Wren (the agentic developer)

Concern: writing the form is hand-work with no tool assist — `resolve` emits local links only, so an author writes a long forge URL by hand and a typo lands in the one case the check refuses (the URL naming another file). The cheapest path to a green gate is the wrong path.

Disposition: carried, and deliberately. The `resolve` emission for foreign citations stays out of scope by the cut's own record (no corpus asks for the verb yet); the doctrine ships a worked example instead, and the wrong-file case gates, which is the direction a typo should fail in. Recorded as the first candidate for a follow-up if the corpus grows citations.

## Bly (the downstream adopter, cold read)

Concern: reading the disclosure cold, does the acceptance read as coverage? "Accepted on link form" could be heard as "verified".

Disposition: answered in the wording. The line says the targets "name another repository and were not read", which is the whole truth; the spec's entity comment carries the same limit; and the doctrine sentence (written next node) states the form and its limit together. Bly's own gate stays green citing the governing host's records — the defect the cut set out to close.

## Orin (the methodology maintainer)

Concern: the sigil rejection deserves a second look now that the design is concrete — a sigil (`agentic-host!call/0039`) would have been shorter to write and checkable without URL parsing.

Disposition: rejection upheld, on the record this time. The sigil needs a name-to-repository declaration surface (a new stamp field, a new migration, a new failure mode), renders as text rather than a link in the published site, and adds grammar the weak model must learn for one use the link form already serves. The link form reuses markdown an author already writes and a fact (`origin_slug`) the tool already reads.

## What the round changed

Nothing in the built diff. Two carried items are recorded above (the `resolve` emission candidate; the wording dependency of the doctrine sentence on Bly's reading), and one instruction passed forward: the adversarial round owns the escape-hazard lens the cut named.
