"""PII scrubbing helpers for prompts and logs."""
import re

PII_PATTERNS = [re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), re.compile(r"\+?\d{9,15}")]


def scrub(text: str) -> str:
    cleaned = text
    for pattern in PII_PATTERNS:
        cleaned = pattern.sub("<redacted>", cleaned)
    return cleaned
