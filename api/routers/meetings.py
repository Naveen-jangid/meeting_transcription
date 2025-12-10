from fastapi import APIRouter, File, UploadFile
from pathlib import Path
from api.schemas import MeetingCreate, MeetingUpload
from storage.local import save_bytes
from db.mongo import Meetings
from workers.tasks.persist import mark_meeting_status
from workers.tasks.ingest import pipeline_entry

router = APIRouter()


@router.post("/create")
async def create_meeting(file_name: str, org_id: str):
    mid = Meetings.create_pending(file_name, org_id)
    return {"meeting_id": mid, "upload_path": str(Path("data/uploads") / file_name)}


@router.post("/{meeting_id}/upload")
async def upload_media(meeting_id: str, file: UploadFile = File(...)):
    dest = Path("data/uploads") / f"{meeting_id}_{file.filename}"
    content = await file.read()
    save_bytes(str(dest), content)
    Meetings.update_status(
        meeting_id,
        "uploaded",
        local_path=str(dest),
        file_name=file.filename,
    )
    mark_meeting_status.delay(meeting_id, "uploaded")
    pipeline_entry.delay(meeting_id)
    return {"ok": True, "local_path": str(dest)}


@router.post("/{meeting_id}/uploaded")
async def uploaded(meeting_id: str, payload: MeetingUpload):
    Meetings.update_status(meeting_id, "uploaded", local_path=payload.local_path)
    mark_meeting_status.delay(meeting_id, "uploaded")
    pipeline_entry.delay(meeting_id)
    return {"ok": True}
