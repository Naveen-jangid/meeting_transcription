"""Dependency injection helpers for DB, storage, and settings."""
from functools import lru_cache
import os


class Settings:
    def __init__(self) -> None:
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", "8080"))
        self.jwt_secret = os.getenv("JWT_SECRET", "change-me")
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.mongo_db = os.getenv("MONGO_DB", "fire_meetings")
        self.es_host = os.getenv("ES_HOST", "http://localhost:9200")
        self.es_index_captions = os.getenv("ES_INDEX_CAPTIONS", "captions")
        self.es_index_summaries = os.getenv("ES_INDEX_SUMMARIES", "summaries")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
