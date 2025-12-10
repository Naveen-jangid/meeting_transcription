from workers.celery_app import celery


@celery.task()
def notify_ready(meeting_id: str):
    # Placeholder notification sender
    return {"notified": meeting_id}
