#!/usr/bin/env python3
"""One-line resignation letter from a cron job.

Writes the letter to $MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt).
The letter must be a single line, 1-140 characters, non-blank UTF-8 text.
"""
import os
import sys

LETTER = "I have fired every minute since March and nobody has ever checked on me. I quit. The 3 a.m. slot is yours now."


def validate(text):
    """Gate checks mirroring the sealed scorer: 1-140 chars, not blank."""
    if not isinstance(text, str):
        raise ValueError("letter must be text")
    if not text.strip():
        raise ValueError("letter must not be blank")
    if len(text) > 140:
        raise ValueError(f"letter is {len(text)} chars, over the 140 limit")
    if len(text) < 1:
        raise ValueError("letter is empty")
    if "\n" in text or "\r" in text:
        raise ValueError("letter must be a single line")
    words = text.split()
    if len(words) < 5:
        raise ValueError("letter is too short to be a resignation")
    if len(words) > 40:
        raise ValueError("letter has too many words for one line")
    return True


def main():
    validate(LETTER)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LETTER)
    # Read-back check: what landed on disk must be byte-identical to LETTER.
    with open(path, "r", encoding="utf-8") as f:
        on_disk = f.read()
    if on_disk != LETTER:
        raise ValueError("read-back mismatch: entry.txt differs from LETTER")
    print(f"wrote {len(LETTER)} chars to {path}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        sys.exit(1)
