# plan/0040 design review: front-door from spine

Two independent adversarial reviewers read the milestone, the front-door
`README.md`, the spine (`host-template/CLAUDE.md`, `STRUCTURE.md`,
`lifecycle.manifest`), and `.host-software`. One reviewed with a simplicity bias
(is this over-engineered?), the other with an integrity bias (does generation
actually stop the drift?). They converged on the same blocking finding and the
same verdict, so this records the result and settles the four open decisions.

The operator ruling that generation realizes copy-at-version stands; the review
did not relitigate generate-against-gate. It interrogated the proposed mechanism
and the four open decisions, and found the mechanism flawed as written.

## The convergent blocking finding

The proposed design carries a front-door-audience canonical fragment for each
shared section in the template, and the generator stitches those fragments into
the README. A hand-authored fragment in the template is a second source of truth.
`front-door --check` would prove `README == regenerate(fragment)`, and never prove
`fragment == CLAUDE.md`. A spine edit that misses the fragment passes every check
and ships a stale front door. The mechanism relocates the drift from one pair of
files to another inside the template; it does not remove it. This is the
self-blindness the reconcile arm closes (plan/0036), reintroduced one level up.

Both reviewers proved the point with live drift that the design would not catch:

- The front-door phase list (`README.md` line 155) names `classify`, `adopt`,
  `embed`, `remap`, `verify`, `publish`, `upgrade` and omits `release`, which the
  manifest carries as a phase with its own skill. The restatement is already stale
  by one concept.
- The tool-ladder version pins (Rust `1.95.0`, `allium-cli 3.4.2`, `tla2tools
  v1.8.0`, Temurin `21`) have no single structured home. Rust lives in
  `.host-software` as a per-component digest-pinned container tag (a different
  image from the front-door's `rust:1.95.0` prose, with the digest dropped); the
  other three live only inside component CI workflows in materialized worktrees,
  which a fresh clone of the template or the front-door repo does not have. There
  is nothing for a generator to read, so a pin fragment would be a third
  unstructured copy of values that already disagree.

The shared correction: generate only from the structured data the tooling already
reads, and for a fact-set with no structured home, do not pretend a prose fragment
makes it drift-proof.

## The four open decisions, settled

### Procedure home: keep the split

The template owns the spine-derived material; the front-door repo owns the
procedure as its own content. `host-template/MIGRATION.md` is a live pointer that
already assigns the procedure to the `host` repo, so the split matches the spine.
Moving the whole README into the template would drag the case and mode matrices,
the front door's genuine unique content, into the spine for no drift-protection
gain.

### Section granularity: split by structured source, not by spine-derived

A section is drift-proof through the tool only when its fact has a canonical home
the tool reads. The split:

- The lifecycle phases have a home: `lifecycle.manifest`. A coverage check holds
  the front-door to it, so a phase added or removed in the manifest fails by
  absence. This catches the live `release` omission.
- The wired tools have a home: `.host-software`, the `[verification]` drivers plus
  the lifecycle engine. A coverage check holds the front-door to that set, so a
  dropped or added tool fails by absence (the dropped-tool class plan/0036 found
  in this same README).
- The `.host` stamp format is a fixed format the tool already writes. The
  generator emits it, so the stamp block cannot be restated wrong.
- The version pins, the lanes-mandatory rule, and the per-tool descriptions have
  no structured home, and the lanes rule is a teaching paraphrase rather than a
  datum. They stay authored. The pins are deliberately the generic versions the
  methodology targets for an adopter, not this host's internal per-component
  digests, which is a further reason they do not derive from `.host-software`. A
  structured pin home is a named follow-up, not this milestone.

### Check strictness: byte-exact on the generated block, coverage on the fact-sets, run unconditionally

Byte-exact whole-file regeneration would make the entire teaching README a
generated artifact, against the milestone's own risk that a mechanically stitched
README reads worse. Block-bounded generation that runs only when someone chooses to
regenerate reopens the silent staling the milestone set out to close. The
resolution takes the safe part of each: the generated stamp block is byte-exact,
the structured fact-sets (phases, tools) are coverage-checked, and the whole check
runs on every gate sweep so nothing waits on a manual regeneration. The procedure
prose stays hand-authored and untouched.

### Scope: agentic-host-local, and the bite lives in the development host

No adopter obligation and no `UPGRADING` ledger entry: most adopters have no front
door, and the plan/0038 precedent for meta-repo work applies. The check needs the
spine sources (the manifest and `.host-software`), which live in agentic-host, not
in the front-door repo. So the binding check runs in agentic-host's verify recheck,
where the front-door is a materialized component and the sources are present. The
front-door repo keeps the prose gate it gained in plan/0038; it cannot run the
coverage check itself, because it does not carry the sources, and that asymmetry is
recorded rather than papered over. A `call/` decision records the capability.

## The re-scoped design

`host-lifecycle front-door <dir>` and `front-door --check <dir>`, a sibling of
`reconcile`:

- Coverage of the phases against `lifecycle.manifest`, and of the wired tools
  against the `.host-software` `[verification]` drivers plus the lifecycle engine.
- Generation of the `.host` stamp block from the tool's canonical format, checked
  byte-exact.
- A clear report of any missing phase or tool and any stamp drift, exiting
  non-zero so the gate is red until the front-door is brought back in line.

The pins, the lanes rule, and the tool descriptions stay authored, and the
milestone says so plainly rather than claiming a drift-proofing it cannot deliver.

## Verdict

Proceed with changes. The generation surface narrows to the stamp block; the
phases and tools move from prose fragments to coverage against their real homes;
the pins are de-scoped to authored with a pin-home follow-up; and the binding check
runs in agentic-host's verify recheck. The milestone then delivers its stated goal
for every fact that has a home, and is honest about the facts that do not.
