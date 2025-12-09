"""Local filesystem storage fallback."""
from pathlib import Path


def save_bytes(path: str, content: bytes) -> str:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    return str(target)
