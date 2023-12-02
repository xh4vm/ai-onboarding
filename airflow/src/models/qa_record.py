from uuid import UUID
from datetime import datetime
from pydantic import Field

from .base import JSONModel, UUIDMixin, TimestampMixin


class MessageData(JSONModel):
    message: str


class Question(MessageData, UUIDMixin, TimestampMixin):
    id: str
    user_id: str


class Answer(MessageData, UUIDMixin, TimestampMixin):
    id: str
    question_id: str


class QARecord(JSONModel):
    timestamp: datetime = Field(alias="@timestamp", default_factory=datetime.utcnow)
    question: Question
    answer: Answer | None
