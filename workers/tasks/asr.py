import json
import os
import subprocess
from pathlib import Path
from workers.celery_app import celery
from db.mongo import Captions, Meetings
from workers.tasks.diarize import diarize_audio
from workers.tasks.enrich import enrich_transcript


@celery.task(bind=True, max_retries=2)
def transcribe(self, meeting_id: str):
    meta = Meetings.get(meeting_id)
    wav = _resolve_local_audio(meeting_id, meta)

    out_json = wav + ".json"
    cmd = [
        "whisper",
        wav,
        "--model",
        "medium",
        "--temperature",
        "0",
        "--task",
        "transcribe",
        "--json",
        "--output_format",
        "json",
        "--output_dir",
        os.path.dirname(wav),
    ]
    try:
        subprocess.run(cmd, check=True)
        with open(out_json) as f:
            data = json.load(f)
    except Exception:
        data = {"segments": []}

    captions = []
    for idx, seg in enumerate(data.get("segments", [])):
        captions.append(
            {
                "index": idx,
                "sentence": seg.get("text", "").strip(),
                "time": float(seg.get("start", 0.0)),
                "endTime": float(seg.get("end", 0.0)),
                "speaker_id": None,
            }
        )

    if captions:
        Captions.insert_many(meeting_id, captions)
    Meetings.update_status(meeting_id, "asr_done")

    diarize_audio.delay(meeting_id)
    return {"segments": len(captions)}


@celery.task()
def pipeline_entry(meeting_id: str):
    transcribe.delay(meeting_id)


def _resolve_local_audio(meeting_id: str, meta: dict) -> str:
    candidate = meta.get("local_path")
    if candidate and Path(candidate).exists():
        return str(candidate)

    file_name = meta.get("file_name") or f"{meeting_id}.wav"
    fallback = Path("data/uploads") / file_name
    fallback.parent.mkdir(parents=True, exist_ok=True)
    fallback.touch(exist_ok=True)
    return str(fallback)
