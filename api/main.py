from fastapi import FastAPI
from dotenv import load_dotenv

from api.routers import meetings, transcripts, summaries, search
from api.deps import get_settings

app = FastAPI(title="Fire Meeting Engine")
app.include_router(meetings.router, prefix="/meetings", tags=["meetings"])
app.include_router(transcripts.router, prefix="/transcripts", tags=["transcripts"])
app.include_router(summaries.router, prefix="/summaries", tags=["summaries"])
app.include_router(search.router, prefix="/search", tags=["search"])


def _create_app() -> FastAPI:
    """Ensure environment variables are loaded before the app is used."""
    load_dotenv()
    return app


# Trigger loading of the .env file when the module is imported
_create_app()


if __name__ == "__main__":
    settings = get_settings()
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
