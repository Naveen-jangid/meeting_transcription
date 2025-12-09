from fastapi import FastAPI
from api.routers import meetings, transcripts, summaries, search

app = FastAPI(title="Fire Meeting Engine")
app.include_router(meetings.router, prefix="/meetings", tags=["meetings"])
app.include_router(transcripts.router, prefix="/transcripts", tags=["transcripts"])
app.include_router(summaries.router, prefix="/summaries", tags=["summaries"])
app.include_router(search.router, prefix="/search", tags=["search"])
