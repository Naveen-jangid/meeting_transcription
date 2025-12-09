from workers.celery_app import celery
from db.mongo import Captions, Analytics


@celery.task()
def compute_analytics(meeting_id: str):
    caps = Captions.find(meeting_id)
    total = caps[-1]["endTime"] - caps[0]["time"] if caps else 0
    q_count = sum(1 for c in caps if c.get("sentence", "").strip().endswith("?"))
    pos = sum(1 for c in caps if c.get("sentimentType") == "positive")
    neg = sum(1 for c in caps if c.get("sentimentType") == "negative")
    neu = len(caps) - pos - neg
    Analytics.upsert(
        meeting_id,
        {
            "duration": total,
            "questions": q_count,
            "sentiment": {"pos": pos, "neg": neg, "neu": neu},
        },
    )
