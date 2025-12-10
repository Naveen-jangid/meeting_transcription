from workers.celery_app import celery
from nlp.prompts import SYSTEM, USER_FMT
from nlp.llm_client import generate_json
from db.mongo import Meetings, Captions, Summaries
from workers.tasks.analytics import compute_analytics
from workers.tasks.webhooks import notify_ready


@celery.task(bind=True, max_retries=2)
def summarize_meeting(self, meeting_id: str):
    meta = Meetings.get(meeting_id)
    caps = Captions.find(meeting_id)
    mini = [
        {"i": c.get("index"), "t": c.get("time"), "s": c.get("speaker_id", 0), "x": c.get("sentence")}
        for c in caps[:5000]
    ]

    user = USER_FMT.format(
        title=meta.get("file_name"),
        duration=meta.get("duration"),
        date=meta.get("createdAt"),
        org_id=meta.get("org_id"),
        captions=mini,
    )
    result = generate_json(SYSTEM, user)
    Summaries.upsert(meeting_id, result)
    Meetings.update_status(meeting_id, "summary_done")

    compute_analytics.delay(meeting_id)
    notify_ready.delay(meeting_id)
