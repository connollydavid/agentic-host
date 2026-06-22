# Flag decoration tells on the commit subject line

## Why

Prose tells are advisory (warn, exit 3): any one rhetorical device is legitimate,
so only *density* escalates. But the commit subject (the first line of a message,
and a gh issue/PR title piped the same way) is special: it becomes the
squash-merge subject and the project's front-door text. A single em-dash there is
not rhetoric, it is the tell, and it should be held to the same no-decoration bar
as the front-door docs. Until now host-lint only warned on it (the release-rule
commit subject drew exactly this advisory warn).

## What ships (host-lint v0.4.0)

On a `--stdin` scan, a `decoration` tell (em/en-dash, smart quote, arrow) on the
**first line** escalates from `warn` to blocking `flag` (exit 1). Body prose and
`--prose` documents are untouched; their decoration stays advisory.

- `escalate_subject_decoration(subject, matches)` (lib.rs), flips `decoration`
  matches whose excerpt occurs in the subject to `Flag`; called in main.rs's
  `--stdin` path after the prose scan.
- Spec: `FlagSubjectDecoration` rule + `Line.is_subject` / `Line.has_decoration`
  (host-lint.allium); `allium check` + `analyse` clean.
- Obligations: the three new `FlagSubjectDecoration` obligations dispositioned to
  `subject_decoration_escalates_to_flag` / `body_decoration_stays_advisory`
  (47 total, all dispositioned).
- VOCABULARY §6 records the subject-line exception to "never blocking".

## Verification

- Tests `subject_decoration_escalates_to_flag` + `body_decoration_stays_advisory`;
  52 tests + clippy green.
- CLI: em-dash subject leads to flag (exit 1); em-dash in body only leads to warn (exit 3);
  clean leads to exit 0.
- `allium check`/`analyse` (3.4.2) clean; `host-lifecycle obligations` reports all 47
  dispositioned; `software --check` clean.
- Reproducible: clean-room `rust:1.95.0` container build of `1d0010c` yields
  `9594271d…`, matching the recorded `.host-software` artifact hash.
