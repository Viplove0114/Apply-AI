"""
helpers.py — Utility functions for formatting and display.
"""

import re


def format_output(text: str) -> str:
    """
    Clean up LLM response text.

    - Strips leading/trailing whitespace
    - Removes common AI wrapper artifacts (e.g. triple backticks)
    - Normalizes line breaks

    Args:
        text: Raw LLM output.

    Returns:
        Cleaned text ready for display.
    """
    if not text:
        return ""

    # Remove markdown code fences if the LLM wrapped the output
    text = re.sub(r"^```[\w]*\n?", "", text.strip())
    text = re.sub(r"\n?```$", "", text.strip())

    # Remove any "Here is your cover letter:" type prefixes
    prefixes_to_remove = [
        r"^Here(?:'s| is) (?:your |the )?(?:cover letter|cold email|email)[:\.]?\s*\n*",
        r"^Sure[!,.]?\s*(?:Here(?:'s| is)[^:]*:?)?\s*\n*",
    ]
    for pattern in prefixes_to_remove:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    return text.strip()


def count_words(text: str) -> int:
    """
    Count the number of words in a text string.

    Args:
        text: Input text.

    Returns:
        Word count.
    """
    return len(text.split()) if text else 0
