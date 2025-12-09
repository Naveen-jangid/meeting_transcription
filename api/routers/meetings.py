from fastapi import APIRouter
from api.schemas import MeetingCreate, MeetingUpload
from storage.s3 import get_presigned_put_url
from db.mongo import Meetings
from workers.tasks.persist import mark_meeting_status
from workers.tasks.ingest import pipeline_entry

router = APIRouter()


@router.post("/create")
async def create_meeting(file_name: str, org_id: str):
    mid = Meetings.create_pending(file_name, org_id)
    url = get_presigned_put_url(file_name)
    return {"meeting_id": mid, "upload_url": url}


@router.post("/{meeting_id}/uploaded")
async def uploaded(meeting_id: str, payload: MeetingUpload):
    Meetings.update_status(meeting_id, "uploaded", s3_key=payload.s3_key)
    mark_meeting_status.delay(meeting_id, "uploaded")
    pipeline_entry.delay(meeting_id)
    return {"ok": True}
