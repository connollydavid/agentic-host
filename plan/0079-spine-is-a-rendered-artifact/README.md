# plan/0079 the spine is a rendered artifact, guarded where it is authored

- Status: cut 2026-08-02, not started
- Decides: [call/0053](../../call/0053-the-spine-copy-is-re-derived-not-asserted.md)

## Why

[call/0004](../../call/0004-template-is-versioned-source.md) chose copy-at-version
on 2026-06-14 and this repository never made the copy. Measured on 2026-08-02
against the canonical `host-lint` artifact: no non-trivial line of the root
`CLAUDE.md` or `STRUCTURE.md` is byte-identical to the template's, and
`git log --follow` puts the manual at fewer than one hundred and forty lines
continuously since adoption, against the template's thousand. The rule was
ratified, promoted into the spine itself, and was not true for a single commit.

Nothing detected it because nothing re-derives it. An artifact reproduces from
its pin or the build lane fails; a rung re-runs in its recorded toolchain; a
task's inputs are fingerprinted; every phase carries a closed recheck. The
methodology re-derives everything except itself, and the spine arrives instead by
an instruction to an agent: "Re-apply the spine doc changes across the span."

[plan/0078](../0078-sweep-in-the-verify-gate/README.md) recorded the downstream
symptom and deferred it: twenty-six of the ledger's thirty-two `verify`
conditions grep a template that `upgrade` requires present before it will run, so
they can neither refuse a false record nor detect a revert. Those conditions are
an author reaching for something checkable on the adopter's side and finding
nothing there. This milestone builds the thing that was missing.

## What the measurement showed

| | this repo | template | byte-identical |
|---|---|---|---|
| `CLAUDE.md`, non-trivial lines | 77 | 814 | 0 |
| `STRUCTURE.md`, non-trivial lines | 15 | 84 | 0 |

Three further readings, each taken rather than assumed:

- The spine as adopter root content already measures clean: naming and prose both
  exit zero, references exit zero. The bar this milestone must hold is met by the
  text as it stands.
- This repository's own manual exits three, on a paragraph the render deletes as
  subsumed doctrine. The single failing text is duplicated doctrine.
- The template's hooks directory is empty, so its commits pass ungated. Every
  line it holds ships verbatim to every adopter. `--install-hooks` covers the
  host and its materialized worktrees; a template held as a submodule falls
  outside that set.

## Build sequence

### Guard the source {#guard-the-source}

- band

### The template is guarded at its own commits {#template-hooks}

- verify: the template repository carries the same commit hooks every other repository under this methodology carries; a commit staging spine text that flags is refused there rather than reported later; the installer reaches a template held as a submodule rather than only the host and its materialized worktrees
- depends: none

### The naming lane runs in the template's continuous integration {#template-naming-ci}

- verify: the template's own workflow runs the naming audit beside the prose audit over its tracked files, and a planted spine tell reddens it; the second line holds when the first is bypassed
- depends: #template-hooks

### Address the reader {#address-the-reader}

- band

### The spine addresses the project that holds it {#spine-addresses-adopter}

- verify: every sentence in the spine addresses the project holding it, so the text reads correctly once rendered into an adopter; the orientation a template reader needs moves to a file outside the render
- depends: #template-hooks

### The mechanism {#the-mechanism}

- band

### A project's manual is rendered {#spine-render}

- verify: `spine --render` writes the root manual and structure map from the template at the stamped revision followed by the project's own fragment; a second run yields identical bytes; a project carrying no fragment renders the spine alone
- depends: #spine-addresses-adopter

### The render is re-derived, not asserted {#spine-check}

- verify: `spine --check` re-renders and compares byte for byte, exits non-zero on any drift, prints the resolved executable path and version so the deriving binary is named rather than inferred, and fails closed when the template is absent or unreadable rather than reporting clean
- depends: #spine-render

### The stamp names bytes {#stamp-spine-hash}

- verify: the stamp carries the rendered file's digest, written by the tool and never by hand, so a cold read establishes what text the project holds; a stamp lacking the field is migrated once rather than refused
- depends: #spine-render

### The check is protected core {#verify-recheck-clause}

- verify: the clause runs in the verify phase's recheck, refuses a skip receipt outright, and carries no waiver key and no advisory tier; a hand-edited manual re-opens the verify receipt and stops a release at its first step, proven on a tree rather than only in a fixture
- depends: #spine-check, #stamp-spine-hash

### The fragment cannot become a second source {#reconcile-fragment}

- verify: reconcile reads the fragment and reports a restatement of any concept that has a spine home, so the paraphrase that produced zero shared lines here is caught rather than silently accepted
- depends: #spine-render

### The loop survives a weak reader {#acceptance}

- verify: the render and check outputs are put in front of a materially weaker model together with the exit code, and one correct next action comes back; where the local model cannot be driven the substitution is recorded and the claim is left unproven rather than asserted
- depends: #spine-check

### The mechanism ships {#release-host-lifecycle}

- verify: released through the tool-carried sequence authorized by call/0053, the artifact re-derived in its recorded toolchain, the pin and the release receipt recorded, and the component pushed before the host commit that pins it
- depends: #verify-recheck-clause, #reconcile-fragment, #template-naming-ci, #acceptance

### The migration {#the-migration}

- band

### This repository holds the spine {#migrate-this-repo}

- verify: the root manual is the render; this project's own text lives in its fragment and restates no spine rule; `spine --check` is clean here; the rendered files carry zero findings at the flagging and the warning tier both
- depends: #release-host-lifecycle

### Adopters are told once, structurally {#ledger-entry}

- verify: one ledger entry whose action is structural rather than prose, whose condition tests the adopter's own tree, and which can actually fail; proven against a binary built before the change
- depends: #migrate-this-repo

## Out of scope, and recorded

- The disposition of the fifty-one existing ledger entries once regeneration
  carries the prose half. They are append-only and stay. Whether a later entry
  supersedes a class of them is a separate decision.
- Whether the structure map takes a fragment slot of its own or stays spine-only.
  It is rendered either way.
- The ledger's own `verify` convention, where a condition resolves its tool from
  the environment rather than from the binary running the gate. Found on
  2026-08-02 beside this work, it belongs to the ledger rather than to the spine,
  and it is left for the decision that settles what a ledger entry claims.
