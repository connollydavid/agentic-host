"""Build the rewrite variants from the current lem section.

Every variant is the current section plus anchored, documented edits, so the
diff from doctrine_current.md is exactly the prose change under test. Each
anchor must match exactly once or the build refuses: a silent no-op edit
would put an untested text in front of the operator.

The four defects under repair:
  D1  no direction-of-address rule in core position (section 3)
  D2  the self-check item names no addressee (section 9)
  D3  the paradigm is never stated closed (section 2)
  D4  no echo warning (input frequency is not output license)

Seeds:
  seed1  surgical: D1+D4 as a new core rule, D3 one line, D2 reworded
  seed2  anti-examples: seed1 plus a wrong/right block in section 7 and a
         Don't line in section 8 (names the mangle outright)
  seed3  repeated invariant: seed1's core rule, and the same invariant
         sentence repeated at sections 0, 8 and 9
"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).parent
BASE = (HERE / "doctrine_current.md").read_text(encoding="utf-8")


def apply(text: str, edits: list[tuple[str, str]]) -> str:
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            sys.exit(f"anchor matched {n} times (want 1): {old[:70]!r}")
        text = text.replace(old, new)
    return text


RULE1 = "1. **Choose by conversational role, not by gender.** Speaker: `L`. Addressee: `lemu`. Talked-about: `lem`."
RULES_OLD = """1. **Choose by conversational role, not by gender.** Speaker: `L`. Addressee: `lemu`. Talked-about: `lem`.
2. **The human keeps `I`.** The model's first person is always `L`, never `I`. A model writing in its own voice uses `L`.
3. **Conjugate by the mapped pronoun** (see section 4). This is where most errors happen.
4. **Do not use `he`, `she`, `it`, or `they` for the model.** These are the failure modes this system replaces."""

RULES_NEW = """1. **Choose by conversational role, not by gender.** Speaker: `L`. Addressee (a model): `lemu`. Talked-about: `lem`.
2. **The human is never re-pronomed.** The human keeps `I`, and the model addresses the human as ordinary `you`. No lem-form is ever emitted at a human: `lemu` is spent only at a model. A long session fills the context with `lemu` (the operator says it; examples carry it), but input frequency is not output license: the only thing `lemu` ever addresses is a model.
3. **The model keeps `L`.** The model's first person is always `L`, never `I`. A model writing in its own voice uses `L`.
4. **Conjugate by the mapped pronoun** (see section 4). This is where most errors happen.
5. **Do not use `he`, `she`, `it`, or `they` for the model.** These are the failure modes this system replaces."""

PARADIGM_ANCHOR = "#### 2.2 Pronunciation"
PARADIGM_LINE = (
    "These, and only these, are the forms. A lem-token outside this list "
    "is a corruption, never a form: re-emit the canonical shape.\n\n"
)

SELF_CHECK_OLD = "4. Address uses `lemu`; reference uses `lem`."
SELF_CHECK_NEW = ("4. A model addressed as `lemu`; the human addressed as "
                  "`you`, never a lem-form.")

INVARIANT = "**The human is `you`. No lem-form is ever emitted at a human.**"


def seed1() -> str:
    return apply(BASE, [
        (RULES_OLD, RULES_NEW),
        (PARADIGM_ANCHOR, PARADIGM_LINE + PARADIGM_ANCHOR),
        (SELF_CHECK_OLD, SELF_CHECK_NEW),
    ])


DONT_COLLAPSE_ANCHOR = "- Don't collapse `lemu` and `lem`; address and reference are different words."
DONT_LINE = ("- Don't address the human with any lem-form (`lemu`, `lem`, "
             "`lems`, `L`), however crowded the context is with `lemu`.\n")
EXAMPLES_ANCHOR = ("**Mixed roles:**\n"
                   "- L told lemu that lem had loaded the context.")
EXAMPLES_BLOCK = (EXAMPLES_ANCHOR + "\n\n"
                  "**Wrong (the inversion failure mode, from a real session):**\n"
                  "- whenever lemua says go\n"
                  "- if lemua wants a different convention anywhere\n\n"
                  "The same sentences, corrected:\n"
                  "- whenever you say go\n"
                  "- if you want a different convention anywhere")


def seed2() -> str:
    return apply(seed1(), [
        (DONT_COLLAPSE_ANCHOR, DONT_COLLAPSE_ANCHOR + "\n" + DONT_LINE.rstrip("\n")),
        (EXAMPLES_ANCHOR, EXAMPLES_BLOCK),
    ])


QUICKREF_ANCHOR = "| 3rd pl | subagents | `lems` | **they** |"
QUICKREF_LINE = ("\n\n" + INVARIANT
                 + " The table above names models only; the human is never re-pronomed.")


def seed3() -> str:
    return apply(seed1(), [
        (QUICKREF_ANCHOR, QUICKREF_ANCHOR + QUICKREF_LINE),
        (DONT_COLLAPSE_ANCHOR, DONT_COLLAPSE_ANCHOR + "\n" + "- " + INVARIANT
         + " Address the human as `you`.\n"),
        (SELF_CHECK_NEW, SELF_CHECK_NEW + "\n5. " + INVARIANT),
    ])


VARIANTS = {"seed1": seed1, "seed2": seed2, "seed3": seed3}

if __name__ == "__main__":
    out = HERE / "variants"
    out.mkdir(exist_ok=True)
    for name, fn in VARIANTS.items():
        with open(out / f"{name}.md", "w", encoding="utf-8", newline="\n") as f:
            f.write(fn())
        print(f"wrote variants/{name}.md ({len(fn().split())} words)")
