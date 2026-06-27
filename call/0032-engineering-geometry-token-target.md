# The engineering-geometry token target is a deterministic structure-and-metadata summary

- Status: accepted
- Date: 2026-06-27
- Scope: the token target for the engineering-geometry modality of `host-reference` (`plan/0049`,
  `call/0030`). Instance software, binds no adopter, no spine change. Carved out of `call/0030`,
  which named this the one open design judgement.
- Relates: `call/0030` (the component and the immutable-against-overlay split); `call/0018`
  (re-derivation and attestation); `plan/0049/gather-data.md` (probe five part one, the
  deterministic boundary, passed; probe five part two, the weak agent's field elicitation, recorded
  as input here); `cast/` (Mara, Wren, Bly, Orin, the lenses this judgement was taken to).

## Context and Problem Statement

Geometry is the one modality with no document-like text to normalise. A STEP assembly, a mesh, a
toolpath, or a parametric script is structure and numbers, so the question is what a deterministic,
token-lean representation of it should hold, such that an agent can interpret the part or the
assembly in context without the whole model.

`call/0030` settled two constraints that bound the answer. The target must be deterministic, since
the immutable layer is re-derived and attested (`call/0018`); probe five part one confirmed at the
weak-agent bar that a model-inferred description of a render is not deterministic and belongs in the
overlay. And the target must be token-lean, since inlining a full boundary representation or a mesh
is the token blow-up normalisation exists to avoid.

There is adjacent 2026 work, but it solves the opposite problem: it tokenises a boundary
representation to generate or round-trip CAD, which is large and lossless by design. Our target
reads, it does not generate, so it summarises rather than tokenises the geometry. The technique
worth borrowing from that work is the depth-first linearisation of a cross-referenced graph, which
gives a deterministic, locality-preserving serialisation. The summary target itself has no settled
answer, so `call/0030` routed it to the cast.

## The cast judgement

The weak agent's elicitation (probe five part two) proposed an assembly hierarchy, a
critical-component list, interface topology, an assembly sequence, and constraint boundaries. The
cast took that as input and tempered it.

- Mara asked what an agent actually needs from a twelve-hundred-part assembly: the structure to
  navigate by, the metadata that identifies a part, and the scale, so it can decide where to look
  closer, rather than the geometry itself. That argues for a lean summary keyed on the tree, with
  detail fetched on demand.
- Wren reads the tree as the index and each node's lean facts as the entry: the skeleton stays
  resident and the source map pulls a node's full detail when a task needs it. Inlining the geometry
  would break the context budget it must hold the whole problem in.
- Bly drew the reproducibility line. A fact parsed straight from the source (a name, the hierarchy,
  a unit, an instance count, a declared material, a tolerance annotation) is exactly reproducible. A
  fact a kernel computes (a bounding box, a volume, a surface area, a watertight flag) is
  reproducible only with a pinned kernel and a canonicalised fixed-precision value. So the parsed
  facts are safe in the attested layer; a computed fact enters it only when the pinned kernel yields
  a canonical value, and otherwise it is omitted, never left silently non-deterministic.
- Orin refused a frozen universal field list. Geometry has no settled answer and the useful fields
  vary by domain, so writing one list overfits the author's domain. The decision states the
  extraction principle and a sensible per-format default that a project extends. Orin also split the
  weak agent's list: the assembly hierarchy and any declared constraints are facts in the source,
  while a critical-component judgement, an inferred interface, and an assembly sequence are
  interpretations the source rarely declares, so they belong in the overlay rather than the attested
  layer.

## Decision

The engineering-geometry token target is a deterministic structure-and-metadata summary, keyed on
the model tree.

- The tree is the spine. Parse the product or model hierarchy (the STEP product structure, the 3MF
  or AMF model tree, the OBJ groups, the OpenSCAD module tree, the DXF block and layer structure)
  into the navigable skeleton, serialised by depth-first linearisation so a cross-referenced graph
  becomes a deterministic, locality-preserving sequence. Each node carries its facts.
- Per-node facts split by reproducibility. Parsed facts (names, units, instance and topology counts,
  declared materials, the product-manufacturing and tolerance annotations, the DXF text and
  dimensions, the G-code header summary) are exactly reproducible and enter the attested layer.
  Kernel-computed facts (bounding box, volume, surface area, watertightness) enter it only as a
  canonical fixed-precision value from the pinned kernel, and are omitted when no such value can be
  produced.
- Interpretation goes to the overlay. A model-inferred label for an unnamed body, a criticality
  judgement, an inferred mating interface, or a reconstructed assembly sequence is recorded in the
  overlay with its provenance, never in the attested layer.
- The full geometry is tier one. The boundary representation, the mesh, or a rendered view is
  fetched on demand through the source map, so the summary never carries the whole model.
- The per-format field set is a default that a project declares and extends, rather than a frozen
  list.

The defaults, each becoming a normaliser's conformance fixture:

- STEP: the assembly tree, part names, units, instance and topology counts, declared materials, the
  product-manufacturing annotations, and a canonical per-part bounding box.
- DXF: layers, block definitions, entity counts by kind, every text and dimension value, and units.
- STL and OBJ: object and group names, triangle and vertex counts, declared units, and the canonical
  bounding box, volume, surface area, and watertight flag.
- 3MF and AMF: the model tree, object names, materials, build items, metadata, and units.
- G-code: the layer count, canonical print dimensions, the estimated time and filament and
  temperatures from the header, the slicer identity and settings, and the object count.
- OpenSCAD: the module and function tree, parameters with their defaults, and the include and use
  dependencies.

## Considered Options

1. **A deterministic structure-and-metadata summary keyed on the tree, with a parsed-against-computed
   reproducibility split and extensible defaults (chosen).** It is deterministic, token-lean,
   navigable, and honest about the domain variance.
2. **A frozen universal field list.** Rejected (Orin): geometry has no settled answer and the useful
   fields vary by domain, so a frozen list overfits one domain and underserves the rest.
3. **A model render-and-describe as the primary target.** Rejected (probe five part one,
   `call/0030`): a model reading is not deterministic, so it cannot be attested and belongs in the
   overlay; it also loses the structure an agent navigates by.
4. **Tokenise the full boundary representation, after the 2026 generative work.** Rejected: that
   target is built for generation and round-trip, so it is large and lossless, the token blow-up the
   summary avoids. The full model stays tier one, fetched on demand.

## Consequences

- Good: the summary is deterministic and attestable; it is token-lean, since it carries the tree and
  facts rather than the geometry; it is navigable, since the tree is the skeleton and detail is
  fetched on demand; and it is honest about the unsettled domain through the extensible default. The
  parsed-against-computed split keeps the attested layer reproducible.
- Costs: the computed facts need a pinned geometry kernel and canonicalisation, a real engineering
  burden and a dependency-licence concern (`call/0030`); the extensible default means a domain may
  need to declare its own fields; and the geometry semantics an agent often wants, what a part is
  for, are available only through the overlay's model-inferred layer, which is not attested.

## Confirmation

This is a cast judgement, so the cast is its confirming body: the four lenses above shaped the
decision, with the weak agent's elicitation (probe five part two) as input that was tempered rather
than adopted whole. The deterministic boundary the decision rests on passed the weak-agent bar as
probe five part one (`plan/0049/gather-data.md`). The per-format defaults become the geometry
normalisers' conformance fixtures, each re-deriving byte for byte. The decision is revisited if a
real adopter domain shows the default underserves it, the path the extensible field set leaves open.

## Lineage and sources

The adjacent 2026 work tokenises a boundary representation for generation and round-trip, a
different goal from this reading summary: [STEP-LLM](https://arxiv.org/abs/2601.12641), whose
depth-first reserialisation of the cross-referenced STEP graph this decision borrows for
deterministic serialisation, and the
[holistic boundary-representation tokenisation](https://arxiv.org/pdf/2601.16771) whose split into
geometry, position, and topology mirrors the structure, bounding-box, and counts decomposition here.
The formats parsed are the published standards: STEP is
[ISO 10303-21:2016](https://www.loc.gov/preservation/digital/formats/fdd/fdd000448.shtml), 3MF is
the [3MF Consortium specification](https://3mf.io/spec/) (now ISO/IEC 25422:2025), and the toolpath
is the [RepRap G-code reference](https://reprap.org/wiki/G-code) over the NIST RS274NGC base; DXF,
STL, OBJ, AMF, and OpenSCAD follow their published format references.
