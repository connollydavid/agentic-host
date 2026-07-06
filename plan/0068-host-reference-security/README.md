# plan/0068 host-reference-security: fix the DoS advisories and retire every unmaintained-crate advisory

Completing the CI lint lane (plan/0058) un-masked real and informational advisories in host-reference's
dependency tree. This milestone resolves all of them, so the advisory lane is clean with no accepted
risk. Shipped as host-reference v0.1.5.

## The real vulnerabilities, fixed by upgrade

Two denial-of-service advisories are genuine and are fixed by moving to the patched lines:

- quick-xml (RUSTSEC-2026-0194 quadratic start-tag parsing, RUSTSEC-2026-0195 unbounded namespace
  allocation) reached three opt-in readers. The premise had gone stale: undoc 0.5.3 and rbook 0.7.10
  now require quick-xml at the 0.41 line, so a lockfile-only bump cleared the office and epub paths. The
  geometry reader moved from threemf to threemf2 0.4, which drops quick-xml entirely (it reads with
  instant-xml), a ten-line port whose 3mf golden reproduces byte for byte.
- crossbeam-epoch (RUSTSEC-2026-0204, an invalid pointer dereference in the pointer formatter), freshly
  published and reaching the opt-in pdf reader through rayon, is fixed by a bump to 0.9.20.

## The unmaintained advisories, retired by maintained forks

The four unmaintained-crate advisories are retired through `[patch.crates-io]` redirects to maintained
slartibardfast forks, per call/0040: paste to pastey, atomic-polyfill to portable-atomic, proc-macro-error
to a two-crate rename of proc-macro-error2, and ttf-parser adopted as a maintained lane (it has no
successor). cargo-deny does not advisory-check a git source, so each redirect retires the advisory
genuinely rather than by a blanket ignore. ttf-parser forbids unsafe code, so the lane's obligation is a
fuzzing pass over its untrusted-input surface, not a memory-safety audit.

## Release and reproducibility

The patched crates and the migrated readers are all opt-in, absent from the default `text` binary that is
built and deployed, so the release is change-class neither and the default binary reproduces (its hash
moves only with the version string). Re-vendored offline as vendor-v2, re-pinned, receipt recorded, and
the whole-suite `software --check` is green with the deny.toml ignore list empty.

## Verification

`cargo deny check advisories` is clean with an empty ignore list and no accepted risk. The geometry 3mf
golden reproduces under threemf2. `cargo build --all-features` compiles every opt-in reader against the
forks. The default binary re-derives its recorded hash offline against vendor-v2. Closes
connollydavid/host-reference#3.
