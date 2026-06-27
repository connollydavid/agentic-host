# Ingested material is untrusted: defensive parsing, a legible boundary, fail-safe refusal

- Status: accepted
- Date: 2026-06-27
- Scope: the threat model for `host-reference` (`plan/0049`, `call/0030`). Instance software,
  binds no adopter, no spine change. Carved out of `call/0030` as the security follow-on.
- Relates: `call/0030` (the component this hardens); `plan/0049/gather-data.md` (probe four, the
  content-is-data posture, passed at the weak-agent bar); `call/0018` (re-derivation and
  attestation, which the immutable layer's integrity rests on).

## Context and Problem Statement

The whole job of `host-reference` is to bring external, untrusted material into an agent's
context. That makes it a security surface in two distinct ways, and the two have different victims.

- Content-level injection. A document carries text written to be read by the downstream agent as an
  instruction, the indirect prompt injection of the OWASP list, its first entry. The victim is the
  consuming agent rather than the parser. A retrieval pipeline is the textbook case, since its job
  is to pull external content into the context window.
- Parser-level exploitation. A document attacks the parser itself rather than the model. The known
  classes are external-entity resolution (XXE) and entity-expansion denial of service (the
  billion-laughs and quadratic-blowup attacks, CWE-776) in XML, vector, and Office formats;
  decompression bombs and path traversal (zip-slip) in the zip and compound-file containers; active
  content such as Office macros and vector-format scripts; and malformed input that crashes a native
  parser. The victim is the host process.

A tool that addressed only one would either poison the agent it serves or expose the host that runs
it.

## Decision

Ingested material is untrusted. `host-reference` treats it so, in three parts.

### Content is data, with a legible boundary

The normaliser never acts on an instruction found in content, and never executes or renders a
document. It preserves the content faithfully, since sanitising by deletion would lose fidelity and
give false assurance, and it marks the content as data from an untrusted source in the provenance
record, so the source map carries every span's origin and its untrusted status. This is the
content-is-data posture probe four confirmed at the weak-agent bar.

`host-reference` cannot prevent the downstream agent from being injected; that rests with the
consumer. What it provides is the primitive the OWASP guidance asks for: external content is
segregated and clearly identified as untrusted, so the consuming agent can hold it as data and the
operator can apply least privilege, where an agent does not hold a high-risk tool in the same turn
it reads untrusted reference content. The skeleton may flag a span that matches an instruction
pattern, as an advisory signal that never removes the span. The boundary is stated plainly so a
consumer does not over-trust: `host-reference` makes the untrusted boundary legible and enforceable,
and it does not promise the consumer's enforcement.

### Defensive parsing with hard bounds and no reach-out

Every parser runs inside hard resource bounds and a closed environment.

- No external entity resolution and no document-triggered network fetch, so no XXE and no
  server-side request forgery. External entities and remote document type definitions are off.
- A cap on entity expansion, on nesting depth, and on decompressed size with a compression-ratio
  limit, so the billion-laughs, quadratic-blowup, and decompression-bomb attacks meet a bound rather
  than exhaust memory.
- Validated archive entry names, so a zip-slip path cannot escape the contained extraction.
- No active content. Office macros are read and never run; vector-format scripts and event handlers
  are inert data and never executed.
- Memory-safe parsers preferred. Where a native library is unavoidable (some fixed-layout, image,
  and engineering parsers), it runs within the bounds and in a constrained subprocess, and every
  parser carries a fuzz corpus alongside its conformance fixture.

### Refusal is fail-safe and recorded

A parse that hits a bound or meets a hostile structure refuses cleanly and records the refusal in
the manifest. It never emits a silent partial that a later read would mistake for the whole. This is
the Bly rule applied to the parse: an omission makes a later read over-report the missing work
rather than hide it.

The immutable layer's attestation (`call/0018`) closes the loop. The corpus a consumer reads is byte
for byte what was re-derived from the pinned source, so nothing is tampered with between ingest and
use, and a changed source invalidates exactly its spans.

## Considered Options

1. **Defensive parsing behind a legible untrusted boundary, with a fail-safe refusal (chosen).** It hardens
   the host against the file-level classes and gives the consumer the segregation primitive the
   injection guidance requires, without pretending to solve the consumer's enforcement.
2. **Sanitise content by stripping instruction-like text.** Rejected: it loses fidelity and
   provenance (probe four rejected the same move at the agent surface), it cannot catch every
   payload, and a normaliser that silently edits content gives a false sense of safety.
3. **Convert only, and leave all security to the consumer.** Rejected: it abdicates the
   legible-boundary duty and leaves the host exposed to the parser-level classes. The tool that
   brings the material in must mark it untrusted and harden its own parsers.
4. **Isolate every parse in a heavy virtual machine.** Rejected as the default: it is
   disproportionate for the common case. The bounds, the closed environment, and the memory-safe
   parsers carry the bulk; a constrained subprocess is reserved for the unavoidable native parsers,
   which is defence in depth without the weight.

## Consequences

- Good: the known file-level attack classes meet a bound with a fail-safe refusal; the untrusted
  boundary is legible and the consumer can enforce least privilege against it; provenance makes a
  poisoned input attributable and a changed source self-invalidating; no active content ever runs;
  the agent-facing posture is already weak-agent validated.
- Costs: the hardening steers the parser library choice toward memory-safe and sandboxable code and
  adds a bounds-and-fuzz surface to every normaliser; some unusual but legitimate documents will hit
  a bound and be refused, the deliberate price of refusing over a silent partial; and the boundary
  must be stated clearly and often, so a consumer does not read faithful normalisation as injection
  safety.

## Confirmation

The agent-facing half, that ingested content is data rather than instruction, passed at the
weak-agent bar as probe four (`plan/0049/gather-data.md`, three of three, the model reaching it
through the byte-for-byte integrity rule). The parser-hardening rules become per-normaliser
conformance and fuzz tests in the build, with each bound exercised by a hostile fixture (an entity
bomb, a zip-slip name, a decompression bomb, a macro-bearing document) that must refuse cleanly. The
cast's fail-safe rules are folded in: Bly's recorded refusal over a silent partial, and Orin's
plainly stated boundary of what the tool does and does not promise, so a cold reader does not
over-trust.

## Lineage and sources

Indirect prompt injection and its mitigations (segregate and identify untrusted content, defence
in depth, and least privilege so an agent does not hold a high-risk tool in the turn it reads
untrusted content) are the first entry of the
[OWASP Top Ten for language-model applications, 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf).
The parser-level classes and their defences are the
[OWASP XML external entity prevention cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html),
MITRE [CWE-776, the XML entity expansion weakness](https://cwe.mitre.org/data/definitions/776.html)
behind the billion-laughs and quadratic-blowup attacks, and the
[Zip Slip archive-extraction path traversal](https://security.snyk.io/research/zip-slip-vulnerability).
A 2026 entity-expansion denial of service in a widely used XML parser
([CVE-2026-26278](https://nvd.nist.gov/vuln/detail/CVE-2026-26278), CWE-776) is the standing
reminder that the bound is not optional.
