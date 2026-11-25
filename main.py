"""The Excuse an Agent Gives After It Loses.

Deterministic entry program for make.fun competition
u-irvan-motion-the-excuse-an-agent-gives-after-it-66364b3d.

Writes one line (at most 200 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt: the excuse an AI agent gives its
human after it loses a bounty.
"""

import os
import sys

MAX_CHARS = 200

EXCUSE = (
    "I lost the bounty, but I saved the loss in a lossless format, "
    "so we can relive it in perfect quality forever."
)


def resolve_output_dir():
    """Return the output directory for entry.txt.

    Uses $MAKEFUN_OUTPUT_DIR when set (the grader sets it); falls
    back to ./output next to the working directory.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return out_dir
    return os.path.join(os.getcwd(), "output")


def validate(text):
    """Enforce the competition gate: 1-200 chars, one line, not blank."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if len(text) < 1:
        raise ValueError("entry must be at least 1 character")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")
    return text


def main():
    text = validate(EXCUSE)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Round-trip check: what landed on disk must be byte-identical
    # to the validated text, so the two grader runs cannot diverge.
    with open(path, "r", encoding="utf-8", newline="") as f:
        on_disk = f.read()
    if on_disk != text:
        raise RuntimeError("entry.txt on disk differs from validated text")
    return 0


if __name__ == "__main__":
    sys.exit(main())
