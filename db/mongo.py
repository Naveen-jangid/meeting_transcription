"""Lightweight Mongo client stubs for the reference architecture."""
import uuid
from datetime import datetime
from typing import Dict, List, Any


class _Meetings:
    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def create_pending(self, file_name: str, org_id: str) -> str:
        meeting_id = str(uuid.uuid4())
        self._store[meeting_id] = {
            "_id": meeting_id,
            "org_id": org_id,
            "file_name": file_name,
            "status": "pending",
            "createdAt": datetime.utcnow().isoformat(),
        }
        return meeting_id

    def update_status(self, meeting_id: str, status: str, **kwargs: Any) -> None:
        if meeting_id in self._store:
            self._store[meeting_id].update({"status": status, **kwargs})

    def get(self, meeting_id: str) -> Dict[str, Any]:
        return self._store.get(meeting_id, {})


class _Captions:
    def __init__(self) -> None:
        self._store: Dict[str, List[Dict[str, Any]]] = {}

    def insert_many(self, meeting_id: str, captions: List[Dict[str, Any]]) -> None:
        self._store.setdefault(meeting_id, []).extend(captions)

    def replace_many(self, meeting_id: str, captions: List[Dict[str, Any]]) -> None:
        self._store[meeting_id] = captions

    def find(self, meeting_id: str) -> List[Dict[str, Any]]:
        return self._store.get(meeting_id, [])


class _Summaries:
    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def upsert(self, meeting_id: str, payload: Dict[str, Any]) -> None:
        self._store[meeting_id] = payload

    def get(self, meeting_id: str) -> Dict[str, Any]:
        return self._store.get(meeting_id, {})


class _Analytics:
    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def upsert(self, meeting_id: str, payload: Dict[str, Any]) -> None:
        self._store[meeting_id] = payload

    def get(self, meeting_id: str) -> Dict[str, Any]:
        return self._store.get(meeting_id, {})


Meetings = _Meetings()
Captions = _Captions()
Summaries = _Summaries()
Analytics = _Analytics()
