from workers.celery_app import celery
from db.mongo import Captions, Meetings
from nlp.ner import extract_entities
from nlp.sentiment import classify_sentiment
from nlp.filters import assign_filter


@celery.task()
def enrich_transcript(meeting_id: str):
    caps = Captions.find(meeting_id)
    for c in caps:
        c["metrics"] = extract_entities(c.get("sentence", ""))
        c["sentimentType"] = classify_sentiment(c.get("sentence", ""))
        c["filterType"] = assign_filter(c.get("sentence", ""))
    if caps:
        Captions.replace_many(meeting_id, caps)
    Meetings.update_status(meeting_id, "enrich_done")
    from workers.tasks.summarize import summarize_meeting
    summarize_meeting.delay(meeting_id)
