# plan/0043 gather-data: the declaration form and the exit-code convention (Qwen-3.5-4B)

Two pre-generalization questions put to Fen (Qwen-3.5-4B) through pal, the way the name and
the front-door coverage call were settled. The probes were short, and each is judged on the
converged reasoning.

## The declaration form (finding 1)

How a project declares an entrance and the concepts it must keep complete. Three candidate
`.host-software` styles, put to Fen across three runs:

- Style A, a concept list on the member: `entrance = phases tools` under `[software "host"]`.
- Style B, a boolean with a restates line: `entrance = true` and `restates = phases tools`.
- Style C, a dedicated stanza: `[entrance "host"]` with `restates = phases tools`.

The picks were C, then A, then C (the host with two concepts, the host judged on first-try
authoring, and a skill with one concept).

- **Style B is rejected in every run.** `entrance = true` reads as ambiguous (is an entrance,
  or entrance is enabled), and the boolean with a separate restates line is redundant and
  verbose for the same fact.
- **Style C wins in isolation** (the `[entrance "host"]` header self-documents the purpose),
  **and both the C runs and the A run raised the same caveat unprompted**: when the entrance
  is an existing `[software]` member carrying `url` and `pin`, a member-level form is wanted,
  since a separate `[entrance]` stanza splits the declaration off from the member it
  describes.
- **agentic-host's entrance is the `[software "host"]` member** (it carries `url` and `pin`),
  so the caveat applies and the data resolves to **Style A**: a concept list on the member,
  `entrance = <concepts>`, which both marks the member and names what it keeps complete. So
  `entrance = true` generalizes to `entrance = phases tools`, or an all-concepts value for a
  full front door. One caveat carried forward: a bare single value such as `entrance = phases`
  reads cryptic, so the value wants a clear list shape.

The leaning for the generalization review: the declaration form is a concept-list value on the
member (`entrance = <concepts>`), rather than the boolean-with-restates pair or a separate
stanza. The review confirms it.

## The exit-code convention (finding 3)

The convention set in the plan/0040 and plan/0041 decision review: exit `1` is an unexpected
or internal fault, exit `2` is an expected logic or usage error. Put to Fen as a routing task
over two scenario sets.

- The first set: a missing named `.host-software` exits `2`; a disk-full write exits `1`; a
  directory with no numbered entries exits `2`.
- The second set (the converged reasoning, before a pal format-loop): a named missing config
  stanza exits `2`; a kernel socket drop mid-read exits `1`; a `--check` on a document
  missing a required heading exits `2`.

Every scenario routed correctly, including the no-entries case to `2`, which matches the
fail-closed `next` decision (plan/0041). The convention wording is clear enough for a weak
agent to route a new error, so the one-line comment is safe to write into the generalization
release. The second run hit the documented pal format-loop after it converged, so the
reasoning before the loop is what counts here.
