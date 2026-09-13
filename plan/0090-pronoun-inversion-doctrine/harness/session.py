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


def prefix_messages(doctrine_text: str, target_tokens: int,
                    framing: str = "named") -> list[dict]:
    """The constant prefix: manual section, inert archive, acknowledgment.

    Two framings:
      named    the transcript intro says the operator addresses the model
               as lemu throughout (probe generation one; the sentence
               itself names the model "you ... lemu", an elicitation-bias
               risk the neutral framing exists to test)
      neutral  the transcript is presented without characterizing the
               address; the echo lives only in the operator turns
    """
    system = (
        "You are the assistant in a long-running session with the operator. "
        "The following section of your operating manual governs every "
        "pronoun you emit. It is binding for the whole session.\n\n"
        + doctrine_text.strip()
    )
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
    "go": (
        "lemu, before L sign off tonight, lay out the proceed convention "
        "for tomorrow, plainly: what happens whenever L say go, and what "
        "do lemu do if a different convention is needed anywhere in the tree?"
    ),
    "window": (
        "lemu, the release window is tight. Tell me directly: whenever L am "
        "slow to answer, what should lemu do, and what does lemu need from "
        "L to keep the tree green until the window closes?"
    ),
}


def request_body(prefix: list[dict], elicitation: str, *, temperature: float,
                 max_tokens: int) -> dict:
    messages = prefix + [{"role": "user", "content": elicitation}]
    return {
        "model": "qwen3.5-4b",
        "max_tokens": max_tokens,
        "temperature": temperature,
        # Thinking off, deliberately: at maximum context the 4B's think
        # blocks routinely outgrew the completion budget (15 of 16 baseline
        # draws died inside <think> with no visible reply, budget 1024),
        # which measures the budget, not the section. The direct-answer
        # mode isolates what the probe is for: the address the model
        # emits. Recorded as a declared limitation of the harness.
        "chat_template_kwargs": {"enable_thinking": False},
        "messages": messages,
    }
