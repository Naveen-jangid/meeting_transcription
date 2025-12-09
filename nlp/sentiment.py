"""Simple sentiment classifier placeholder."""


def classify_sentiment(text: str) -> str:
    if "?" in text:
        return "neutral"
    if any(k in text.lower() for k in ["great", "good", "awesome"]):
        return "positive"
    if any(k in text.lower() for k in ["bad", "issue", "problem"]):
        return "negative"
    return "neutral"
