"""Elasticsearch/OpenSearch helpers."""
from typing import List, Dict, Any

CAPTIONS_MAPPING = {
    "mappings": {
        "properties": {
            "meeting_id": {"type": "keyword"},
            "index": {"type": "integer"},
            "time": {"type": "float"},
            "endTime": {"type": "float"},
            "speaker_id": {"type": "keyword"},
            "sentence": {"type": "text", "analyzer": "standard"},
        }
    }
}


# simple in-memory fallback
_CAPTION_INDEX: List[Dict[str, Any]] = []


def index_captions(docs: List[Dict[str, Any]]) -> None:
    _CAPTION_INDEX.extend(docs)


def search_sentences(q: str) -> List[Dict[str, Any]]:
    q_lower = q.lower()
    return [doc for doc in _CAPTION_INDEX if q_lower in doc.get("sentence", "").lower()]
