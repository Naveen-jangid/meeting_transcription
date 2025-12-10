from pydantic import BaseModel
from typing import List, Optional


class MeetingCreate(BaseModel):
    file_name: str
    org_id: str


class MeetingUpload(BaseModel):
    s3_key: str


class Caption(BaseModel):
    index: int
    sentence: str
    time: float
    endTime: float
    speaker_id: Optional[str] = None
    sentimentType: Optional[str] = None
    filterType: Optional[str] = None


class Summary(BaseModel):
    gist: Optional[str] = None
    shortSummary: List[str] = []
    decisions: List[str] = []
    actionItems: List[str] = []
    risks: List[str] = []
    nextSteps: List[str] = []
