from workers.celery_app import celery
from db.mongo import Captions, Meetings
from workers.tasks.enrich import enrich_transcript


@celery.task(max_retries=1)
def diarize_audio(meeting_id: str):
    # lookup wav, run pyannote pipeline -> map speakers to nearest caption windows
    captions = Captions.find(meeting_id)
    for idx, cap in enumerate(captions):
        cap["speaker_id"] = cap.get("speaker_id") or f"S{idx % 2}"
    if captions:
        Captions.replace_many(meeting_id, captions)
    Meetings.update_status(meeting_id, "diarize_done")
    enrich_transcript.delay(meeting_id)
