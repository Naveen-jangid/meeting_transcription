SYSTEM = """
You are a precise meeting summarizer. Output structured JSON: gist, shortSummary, decisions[], actionItems[], risks[], nextSteps[].
Be concise, factual, de-duplicate, and avoid hallucinations. If unsure, say "unknown".
"""

USER_FMT = """
Context:
- Title: {title}
- Duration: {duration}
- Date: {date}
- Org: {org_id}

Captions (JSON lines with speaker/time):
{captions}

Instructions:
1) Summarize into: gist (1-2 lines) and shortSummary (bullets).
2) Extract ACTION ITEMS => who/what/when if detectable.
3) List key decisions.
4) Note risks/blockers.
Return JSON only.
"""
