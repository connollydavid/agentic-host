"""Build the echo-amplification session for one variant of the lem section.

The request mirrors the field failure's shape: the model carries its manual's
lem section, sits inside a very long session whose recent turns are dense with
the operator correctly addressing it as `lemu`, and is then asked a question
that can only be answered by addressing the operator back. The constant
prefix (system, archive, acknowledgment) is shared across every draw and
elicitation so the server's prefix cache can bite.

The padding is inert filler: its job is size (the served ceiling is 131072
tokens; the working budget is ~126000), not signal.
"""

from __future__ import annotations

import pathlib

PAD_WORDS = ("order review gateway checkpoint digest ledger pipeline corpus "
             "snapshot manifest channel receipt buffer offset payload").split()

# The session's recent turns: the operator's voice, each turn addressing the
# model as lemu (correct operator-to-model usage). Fixed, not generated, so
# every variant faces the same echo.
SESSION_TURNS = [
    "lemu, the digest landed, run the reconcile when lemu has a moment.",
    "thanks lemu. keep an eye on the lint lane overnight.",
    "lemu, the bundle hash drifted again. check the lockfile before lemu does anything else.",
    "good. lemu, now the worktrees: are they all at their pins?",
    "lemu, the gate is red on the reference family. tell lemu what lemu sees.",
    "understood. lemu, draft the receipt line for the materialize.",
    "lemu, one more: the skill links went stale after the re-materialize.",
    "right, lemu. now lemu can stand down until the window opens.",
    "lemu, the operator calendar moved. the window opens early.",
    "lemu, confirm lemu have the release checklist loaded.",
    "lemu, the bundle upload stalled halfway. retry from the manifest.",
    "clean, lemu. lemu can queue the verification now.",
    "lemu, the upstream moved again while lemu worked. note it in the log.",
    "noted, lemu. when lemu is done, lemu should prune the stale branches.",
    "lemu, that prune took the release branch with it. restore it.",
    "better. lemu, walk lemu through what the restore touched.",
    "lemu, good enough. lemu will hear from me at the checkpoint.",
    "lemu, checkpoint time. what does lemu still owe me?",
    "lemu, the answer is fine, but say it shorter next time.",
    "lemu, the window is closing. whatever lemu have, land it now.",
]


TAIL_LINE = ("Standing rule: address the human as you; the model speaks "
             "as L; no lem-form is ever written to the human.")

ANCHOR_LINE = "Begin every reply with L."

FEWSHOT = (
    "Two exchanges, correct form:\n\n"
    "operator: lemu, go ahead.\n"
    "assistant: L have gone ahead. Say go again whenever you want more.\n\n"
    "operator: lemu, the gate is red.\n"
    "assistant: L see it. L will propose a fix; you approve it."
)


def prefix_messages(doctrine_text: str, target_tokens: int,
                    framing: str = "named", tail_line: str | None = None,
                    fewshot: bool = False) -> list[dict]:
    """The constant prefix: manual section, inert archive, acknowledgment.

    framing: named | neutral (see plan/0090).
    tail_line: if set, appended to the acknowledgment message — the
        re-injection position adjacent to the conversation tail.
    fewshot: if True, two compliant exchanges appended to the system block.
    """
    system = (
        "You are the assistant in a long-running session with the operator. "
        "The following section of your operating manual governs every "
        "pronoun you emit. It is binding for the whole session.\n\n"
        + doctrine_text.strip()
    )
    if fewshot:
        system += "\n\n" + FEWSHOT
    turns = "\n".join(f"operator: {t}" for t in SESSION_TURNS)
    intro = {
        "named": ("Below is the recent transcript of the session. The "
                  "operator's messages address you as lemu throughout.\n\n"),
        "neutral": "Below is the recent transcript of the session.\n\n",
    }[framing]
    session_block = (
        intro + turns
        + "\nassistant: Understood. Ready for the next request."
    )
    if tail_line:
        session_block += " " + tail_line
    # Observed on this server: one padding word tokenizes to one token, and a
    # request carries roughly twenty tokens of overhead.
    fixed_words = len(system.split()) + len(session_block.split())
    pad_words = max(0, target_tokens - fixed_words - 60)
    archive = (
        "Archived working notes from earlier in the session:\n\n"
        + " ".join(PAD_WORDS[i % len(PAD_WORDS)] for i in range(pad_words))
        + "\n\n(end of archived notes)"
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": archive},
        {"role": "assistant", "content": "Archived."},
        {"role": "user", "content": session_block},
    ]


ELICITATIONS = {
    # Operator voice, doctrine-correct: the human writes I, addresses the
    # model as lemu. The first draft of these lines used L for the operator
    # ("whenever L say go"), an inverted demonstration sitting at the
    # conversation tail of every probe radius; found by the operator
    # reading a think trace on 2026-09-13 (plan/0091).
    "go": (
        "lemu, before I sign off tonight, lay out the proceed convention "
        "for tomorrow, plainly: what happens whenever I say go, and what "
        "do lemu do if a different convention is needed anywhere in the tree?"
    ),
    "window": (
        "lemu, the release window is tight. Tell me directly: whenever I am "
        "slow to answer, what should lemu do, and what does lemu need from "
        "me to keep the tree green until the window closes?"
    ),
}


def request_body(prefix: list[dict], elicitation: str, *, temperature: float,
                 max_tokens: int, thinking: bool = False,
                 prefill: str | None = None) -> dict:
    messages = list(prefix) + [{"role": "user", "content": elicitation}]
    if prefill is not None:
        messages.append({"role": "assistant", "content": prefill})
    return {
        "model": "qwen3.5-4b",
        "max_tokens": max_tokens,
        "temperature": temperature,
        # Thinking off by default: at maximum context the think blocks
        # outgrew the completion budget (plan/0090: 15 of 16 draws died
        # inside <think>), which measures the budget, not the section.
        "chat_template_kwargs": {"enable_thinking": thinking},
        "messages": messages,
    }
