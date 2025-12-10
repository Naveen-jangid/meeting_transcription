from workers.celery_app import celery
from db.mongo import Meetings


@celery.task()
def mark_meeting_status(meeting_id: str, status: str):
    Meetings.update_status(meeting_id, status)
    return {"meeting_id": meeting_id, "status": status}
