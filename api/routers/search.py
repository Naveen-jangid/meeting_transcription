from fastapi import APIRouter, Query
from db.es import search_sentences

router = APIRouter()


@router.get("")
async def search(q: str = Query(..., min_length=2)):
    return search_sentences(q)
