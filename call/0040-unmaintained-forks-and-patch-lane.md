# call/0040: retire unmaintained-crate advisories with maintained forks and a patch lane

- Status: accepted
- Scope: host-reference
- Date: 2026-07-07

## Context and problem

host-reference pulls four crates that RustSec flags as unmaintained, each through an opt-in reader:
paste (RUSTSEC-2024-0436), atomic-polyfill (RUSTSEC-2023-0089), proc-macro-error (RUSTSEC-2024-0370),
and ttf-parser (RUSTSEC-2026-0192). None is a vulnerability; each is an author-declared unmaintained
label. The operator's standing rule is zero-unmaintained, met by genuine fixes rather than blanket
ignores.

## Decision

Redirect each dead crate to a maintained slartibardfast fork through `[patch.crates-io]`. cargo-deny
does not advisory-check a git source, and no same-name registry successor exists, so a fork under our
control is the only route to a zero-ignore lane. The forks are not `.host-software` members: they are
vendored third-party dependencies, not software developed here, governed by this decision.

Three crates have a maintained successor, so the fork routes to real maintained code:

- paste re-exports pastey's `paste!` macro.
- atomic-polyfill re-exports portable-atomic (the crate's own README already points there).
- proc-macro-error is a two-crate rename of proc-macro-error2 and its attribute crate, with the one
  codegen path edited, because a re-export cannot satisfy the attribute macro's hardcoded crate path.

ttf-parser has no drop-in successor (skrifa is a different API, and lopdf pins ttf-parser
at version 0.25), so we ADOPT it as a maintained lane. Our fork declares maintenance in a MAINTENANCE.md,
and the unmaintained label is resolved by our maintaining it rather than by a frozen dodge. The lane's
standing obligation is the untrusted-input contract of the glyph and metrics reads the pdf reader
drives; a fuzzing pass is its first real maintenance task. ttf-parser forbids unsafe code, so its
worst case is a panic, never memory corruption.

## Consequences

Good: zero-unmaintained with no accepted risk, and the deployed default `text` binary is unchanged,
since the patched crates reach only opt-in readers. Bad: we carry five fork repositories to maintain,
and the ttf-parser lane takes on a real maintenance obligation we must honour. Sunset: retire each
fork when a maintained upstream or a drop-in successor lands.

## Relates

connollydavid/host-reference#3 (the quick-xml DoS advisories, fixed by upgrade in the same release);
the reproducible re-vendor recipe (plan/0032, call/0021).
