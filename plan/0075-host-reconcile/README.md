# plan/0075 host-reconcile: the merge-driver framework design

**Status: cut, design-only, not started** (operator ruling 2026-07-22, recorded in the closure queue in PLAN.md's Open work). Queued last, behind plan/0072.

## Why

`host-reconcile` is a proposed new `host-*` methodology tool: a framework for domain-aware git merge drivers that reconcile typed files (version metadata, changelogs, manifests) across a moving base, the friction at the heart of an out-of-tree patch set carried atop a fast-moving upstream. The core is methodology-general; per-domain articulations (such as `host-reconcile-ffmpeg`) encode project-specific resolution rules. The full proposal is recorded in [connollydavid/host#18](https://github.com/connollydavid/host/issues/18); that issue is the design record this milestone starts from.

## Scope

Design only. The milestone produces the reviewed design: the tool boundary against the existing `host-*` family, the articulation model, and a go or no-go recommendation for a build. The build is not gated here; a build milestone is cut only if the design survives adversarial review. plan/0072's FFmpeg pack supplies the nearest concrete articulation candidate, which is why this milestone sits behind it in the queue.
