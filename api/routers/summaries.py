from fastapi import APIRouter
from db.mongo import Summaries

router = APIRouter()


@router.get("/{meeting_id}")
async def get_summary(meeting_id: str):
    return Summaries.get(meeting_id)
