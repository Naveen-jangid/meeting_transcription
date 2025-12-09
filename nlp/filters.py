"""Rule-based filter assignment for transcript sentences."""


def assign_filter(s: str) -> str:
    s_lower = s.lower()
    if any(k in s_lower for k in ("action", "todo", "we will", "assign")):
        return "taskNoteFilter"
    if s.endswith("?"):
        return "questionFilter"
    if any(k in s_lower for k in ("first", "second", "third")):
        return "noteFilter"
    return "none"
