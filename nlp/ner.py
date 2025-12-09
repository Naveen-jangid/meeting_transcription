"""Minimal entity extraction placeholder."""
from typing import List, Dict


def extract_entities(text: str) -> List[Dict[str, str]]:
    tokens = text.split()
    return [{"word": t, "category": "Token"} for t in tokens[:3]]
