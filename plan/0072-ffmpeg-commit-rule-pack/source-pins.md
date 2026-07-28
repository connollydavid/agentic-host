# plan/0072 source pins: the upstream corpus the registry encodes

- Date: 2026-07-28
- Fetched over HTTPS from `raw.githubusercontent.com` at the FFmpeg master commit below, and digested on arrival.

The `#rule-registry` node requires the encoded corpus to be pinned to a genuine upstream
master SHA with per-section digests, so that drift in a rule-bearing section is detectable
and an edit elsewhere is not. This file records the pins that fetch produced, so the work
begins from verified bytes rather than from a second fetch that may differ.

## The commit

```
FFmpeg/FFmpeg master c6309b5c63add7ad0ec221fafefc32bdcd6f8b91
```

## The files, and what each is for

| Upstream path | sha256 | Bytes | Why the registry needs it |
|---|---|---|---|
| `doc/developer.texi` | `26549522babfb7af744059d68077440064de6693ee6ff8c41b53ea3c36534e4c` | 45328 | The commit and patch rules themselves |
| `doc/mailing-list-faq.texi` | `7ba38b8b16e6b94d6054d64da6dfa17738c874b693d85fe8ee9f62b36b7ac0f6` | 13148 | The mailing-list mechanics the mail lane checks |
| `MAINTAINERS` | `55e05c3c17d7909886cbdd563154ff2d7a43bc5d0866bddb63df2adbc5aa0f58` | 31632 | Area ownership, for the area-prefix and routing rules |
| `doc/fate.texi` | `07b49cf2c33b20d04b828166ce569f6d7d57e4b2791b113bcd6b134e7960ecba` | 9855 | The FATE obligations the testing rules refer to |

Not yet fetched: `security.html` from the `FFmpeg/web` repository, which the node pins by
that repository's commit plus a fetch date because no `SECURITY` file exists in the FFmpeg
tree. It is the source for the security-path routing rules, and it is the one source whose
pin is a fetch rather than a tree path.

## What the structure looks like

`doc/developer.texi` carries 35 headings at chapter, section and subsection level. The
rule-bearing density is not uniform: `Patches/Committing` alone carries ten `@subheading`
rules, and they are the ones the message and diff lanes turn on.

```host-lint:ignore
Licenses for patches must be compatible with FFmpeg.
You must not commit code which breaks FFmpeg!
Commit messages
Testing must be adequate but not excessive.
Do not commit unrelated changes together.
Bug fixes intended for backporting should stay focused.
Cosmetic changes should be kept in separate patches.
Credit the author of the patch.
Credit any researchers
Always wait long enough before pushing changes
```

The commit-message format the message lane encodes is stated in that section verbatim:

```host-lint:ignore
area changed: short 1 line description

details describing what and why and giving references.
```

Three of those subheadings are the ones the milestone's harder nodes exist for, and reading
them together is what shows why. "Do not commit unrelated changes together" and "Cosmetic
changes should be kept in separate patches" are the pair the `#cosmetic-separation`
classifier has to tell apart, and "Bug fixes intended for backporting should stay focused"
is a third scope rule that overlaps both without being either. A registry that flattened
them into one "keep patches focused" entry would lose exactly the distinction the lane is
being built to make.

## What this record does not settle

The enforcement tier per rule. A tier is a claim about how reliably a rule can be detected
mechanically, and the `#corpus-calibration` node measures that against accepted upstream
history before any tier freezes. The `measured-rate` field stays empty until then, which is
the design's own sequencing and not an omission here.
