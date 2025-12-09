from workers.celery_app import celery


@celery.task()
def align_audio(meeting_id: str):
    # Placeholder for WhisperX alignment
    return {"meeting_id": meeting_id, "aligned": True}
