# SKILL_AUTHORING.md

A conformance standard for writing agent skills that run unmodified across
Claude Code, Codex CLI, Gemini CLI, GitHub Copilot, Cursor, Cline, Windsurf,
and OpenCode. The `SKILL.md` format is the shared substrate; this document
defines the portable subset and the gates a skill must pass before it ships.

Scope: authoring rules plus pass/fail gates. The gates are split into
**mechanical** (a script can verify) and **judgement** (a human or agent reads
and decides). A skill conforms when every mechanical gate passes and no
judgement gate is failing.

---

## 1. Anatomy

```
skill-name/
├── SKILL.md          # required; YAML frontmatter + markdown body
├── reference.md      # optional; loaded on demand
├── examples.md       # optional; loaded on demand
└── scripts/          # optional; executed via bash, never read into context
    └── validate.py
```

Only `SKILL.md` is required. Everything else exists to keep `SKILL.md` short.

## 2. Frontmatter

```yaml
---
name: pdf-processing
description: Extracts text and tables from PDFs, fills forms, merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or extraction.
---
```

`name` and `description` are the only fields guaranteed to be read by every
agent. Anything else (Claude Code's `context`, Codex's `openai.yaml` keys,
`allowed-tools`) is tool-specific and breaks the portability guarantee. Keep it
out of a skill meant to be universal, or fence it so a missing parser degrades
cleanly.

The `description` is the entire discovery mechanism. It is the only text
pre-loaded into the agent's context, so it is the sole basis for deciding
whether the skill fires. Write it third person, as *what it does* plus *when to
use it*, and pack it with the nouns a user would actually type. A vague
description is the most common reason a correct skill never triggers.

## 3. Body

Procedural knowledge: workflows, decision points, gotchas. Three loading tiers
operate here: frontmatter is always resident, the `SKILL.md` body is read once
the skill triggers, and supporting files are read only when the body points to
them. Push depth outward:

```
## Editing documents
For tracked changes see REDLINING.md
For OOXML internals see OOXML.md
```

The linked file costs nothing until the task needs it. Scripts cost only their
output, not their source, because they run under bash rather than being read,
so deterministic logic belongs in a script, not in prose the agent has to
re-derive each time.

State rules with their reason. A naked imperative tells the agent the letter of
a rule but not how to handle the case the rule never anticipated.

```
Use constructor injection. Field injection can't be mocked without a Spring
context, so it breaks unit tests.
```

reads better and generalises further than `NEVER use field injection`. The
reason becomes the rubric for the edge cases.

For multi-step work, give an ordered checklist the agent copies into its
response and ticks off. Where output quality matters, add a validation loop:
run a check, fix what it flags, repeat until clean. The check can be a script
or a reference doc the agent compares against.

## 4. Portability constraints

- The hosted execution environment has no network and no runtime package
  installation. List required packages in the body and confirm they are present
  in the target environment. Stdlib-only scripts avoid the problem entirely and
  are the safest default for a skill distributed across agents.
- Reference every supporting file by relative path. Absolute paths and
  repo-specific layouts do not survive being copied into another agent's skills
  directory.
- When documenting file creation in the body, use a heredoc rather than a
  "create this file:" heading followed by a code block:

  ```
  cat > config/settings.yaml << 'EOF'
  key: value
  EOF
  ```

  The heredoc is unambiguous about target path and exact content; the heading
  form leaves the agent to infer both.

---

## 5. Conformance gates

Each gate carries an ID and an assertion alongside its check and pass condition. Mechanical
gates are phrased so a linter can evaluate them. Run mechanical gates first;
they are cheap and catch the structural failures.

### Mechanical

**G1: Frontmatter present and parseable.**
Check: file begins with a `---` fenced block that parses as YAML.
Pass: parse succeeds and yields a mapping.

**G2: Required keys.**
Check: the mapping contains `name` and `description`, both non-empty strings.
Pass: both present and non-empty.

**G3: Name format.**
Check: `name` is lowercase, hyphen-separated, ≤ 64 chars, and equals the
containing directory name.
Pass: matches `^[a-z0-9]+(-[a-z0-9]+)*$`, length ≤ 64, equals dirname.

**G4: Description length.**
Check: `description` length ≤ 1024 chars.
Pass: within bound. (Empty or one-word descriptions also fail G9.)

**G5: Portable frontmatter only.**
Check: frontmatter keys are a subset of `{name, description}` for a skill
declaring itself universal. Extra keys are reported, not silently accepted.
Pass: no keys outside the allowed set, OR each extra key is documented in a
`# Portability notes` section as a known tool-specific extension.

**G6: Body length.**
Check: line count of the markdown body (everything after the closing `---`).
Limit: ≤ 500 lines. Over it, content belongs in a reference file.

**G7: References resolve.**
Check: every relative path and intra-repo link in the body points to a file
that exists in the skill directory.
Pass: zero dangling references.

**G8: Imperative density.**
Check: count of standalone all-caps directives (`MUST`, `ALWAYS`, `NEVER`) in
the body.
Pass: each occurrence is accompanied within the same paragraph by a reason. A
linter approximates this by flagging any such token whose sentence contains no
"because", "so", "since", or equivalent causal marker, for human review.

### Judgement

**G9: Description triggers.**
Assertion: the description names the artifacts, file types, and verbs a user
would actually say, not an abstract category.
Fail signal: you cannot list three realistic user phrasings the description
would match.

**G10: Reason over rule.**
Assertion: rules in the body explain why, so the agent can generalise.
Fail signal: imperatives that would leave the agent guessing on an unlisted
edge case.

**G11: Disclosure discipline.**
Assertion: detail used in a minority of runs lives in a reference file, not the
body.
Fail signal: the body is near the G6 limit because of content most tasks skip.

**G12: Logic in scripts.**
Assertion: deterministic, repeatable procedures are scripts the agent executes,
not prose it re-derives.
Fail signal: the body walks through a fixed algorithm step by step in English.

**G13: Real invocation.**
Assertion: the skill has been triggered on at least one genuine task end to end,
not only read back.
Fail signal: no record of the skill firing and producing correct output.

**G14: Cross-agent dry run.**
Assertion: the skill has been dropped into at least one second agent's skills
directory and triggered there.
Fail signal: only ever exercised in the agent it was written for.

---

## 6. Ship checklist

A skill ships when G1 through G8 pass mechanically and G9 through G14 have no open fail signal.
A future `lint-skill.sh` reads this file's mechanical section and asserts G1 through G8
directly; the judgement gates stay a human or agent review step.

## 7. Sources

- Anthropic, Skill authoring best practices:
  https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- Agent Skills format reference (portable subset):
  https://www.agensi.io/learn/skill-md-format-reference
- Open standard overview: agentskills.io
