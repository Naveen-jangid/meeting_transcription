from fastapi import APIRouter
from db.mongo import Captions

router = APIRouter()


@router.get("/{meeting_id}")
async def get_transcript(meeting_id: str):
    return Captions.find(meeting_id)
