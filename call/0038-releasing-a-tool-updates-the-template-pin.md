# Releasing a tool updates the template's pins of that tool

- Status: superseded by the spine
- Date: 2026-07-04
- Scope: the release process for any `host-*` tool that `host-template` carries. The template
  pins each such tool in more than one place, and a release is complete only when every one of
  those pins equals the released commit. Surfaced as connollydavid/host-lifecycle#9 and folded
  into `plan/0056`. This binds how a release propagates, next to the existing propagate rule.
- Relates: `plan/0056` (the robustness superset that surfaced it); `call/0021` and `plan/0032`
  (re-vendor and propagate to consumers on a tool release); `call/0010` (software as a bare
  store pinned in `.host-software`); the dual-release-authority rule (the producer tag is the
  release, and `.host-software` pins it).

## Supersession

The anti-ouroboros validate gate (`host-template/CLAUDE.md`) retires an `accepted` `call/`
decision whose `Scope:` names `host-template`: such a rule is spine-resident, owned by the
methodology. The cast deliberated whether to author the rule into the spine or keep it
agentic-host-specific, and the operator ruled to author it. The rule now lives in the
host-template spine as the release-side complement of the reference-don't-vendor rule, that a
release reconciles every carried-template pin, phrased so a generic adopter reads the first
clause and skips it, and validated Fen-safe by probing the real weak agent before it was
authored. This record is kept for its history, and the rule stays enforced by `software
--check`'s template-pin gate.

## Context and Problem Statement

`host-template` is the scaffold for new agentic projects and the source of the methodology
spine. It carries the `host-*` tools it depends on and pins each in more than one place:

- host-lifecycle: the `prose.yml` CI install (`cargo install … --rev <sha>`) and the
  `tools/host-lifecycle` submodule gitlink, which `reproducible-build.yml` and `site.yml` build.
- host-lint: the `tools/host-lint` submodule gitlink.

Each of these drifted while `.host-software` moved forward. At discovery the
`tools/host-lifecycle` submodule sat at v0.15.1, `prose.yml` at v0.30.1, and `tools/host-lint`
at v0.2.0, against a host gating on host-lifecycle v0.35.1 and host-lint v0.12.1. So the template
handed new adopters tools twenty releases old, and the pin comment's claim to track "the same
host-lifecycle the host gates on" was false. The `prose.yml` pin is the visible one; the two
submodule gitlinks are easy to overlook, and they were the most stale.

The release sequence re-pins `.host-software` and propagates to the consumer components
(`call/0021`), but the template sits outside that consumer set, so its pins drift on every
release with nothing to catch them.

## Decision

Every release of a `host-*` tool bumps every host-template pin of that tool to the released
commit:

- host-lifecycle: the `prose.yml` `--rev` and the `tools/host-lifecycle` submodule gitlink.
- host-lint: the `tools/host-lint` submodule gitlink.

`host-lifecycle release` prints these as explicit outward steps next to the `.host-software`
re-pin. `software --check` gates the invariant: `template_pin_problems` reads each template pin
site and HAZARDs any that does not match the recorded `.host-software` pin of that tool, so a
release that leaves a pin behind fails the whole-suite check. The invariant: every host-template
pin of a tool equals the commit `.host-software` records for it.

## Consequences

- New projects scaffold with current tools, and the template's own CI matches what it publishes.
- The template joins the surfaces a release reconciles, next to `.host-software` and the
  vendored-dependency bundle, and the gate covers every pin site.
- Each drifted pin is one HAZARD line that carries the site and both commits.
