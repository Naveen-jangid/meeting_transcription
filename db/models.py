"""Conceptual Mongo document shapes for reference."""

MEETINGS = {
    "_id": "uuid",
    "org_id": "01",
    "file_name": "TSE_3_2025-10-07.mp3",
    "s3_key": "uploads/..",
    "status": "pending|uploaded|asr_done|diarize_done|enrich_done|summary_done",
    "createdAt": "ISO",
    "duration": 675.1,
}

CAPTION = {
    "meeting_id": "uuid",
    "index": 0,
    "sentence": "...",
    "speaker_id": 0,
    "time": 1.2,
    "endTime": 4.0,
    "metrics": [{"word": "data", "category": "Nouns"}],
    "sentimentType": "neutral",
    "filterType": "noteFilter|taskNoteFilter|questionFilter|none",
}

SUMMARY = {
    "meeting_id": "uuid",
    "gist": "...",
    "shortSummary": ["..."],
    "decisions": [],
    "actionItems": [],
    "risks": [],
    "nextSteps": [],
}
