from workers.celery_app import celery
from workers.tasks.asr import pipeline_entry


@celery.task()
def normalize_and_probe(meeting_id: str):
    # placeholder for audio normalization/media probe
    pipeline_entry.delay(meeting_id)
