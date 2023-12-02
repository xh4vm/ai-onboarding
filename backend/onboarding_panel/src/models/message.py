from uuid import UUID
from datetime import datetime
from pydantic import Field

from .base import JSONModel, UUIDMixin, TimestampMixin, StrEnum


class MessageData(JSONModel):
    message: str


class Question(MessageData, UUIDMixin, TimestampMixin):
    user_id: UUID


class Answer(MessageData, UUIDMixin, TimestampMixin):
    question_id: UUID


class QuestionRecord(MessageData, UUIDMixin, TimestampMixin):
    id: str
    user_id: str


class AnswerRecord(MessageData, UUIDMixin, TimestampMixin):
    id: str
    question_id: str


class QARecord(JSONModel):
    timestamp: datetime = Field(alias="@timestamp", default_factory=datetime.utcnow)
    question: Question
    answer: Answer | None


class QARecordModelSort(StrEnum):
    QUESTION_ASC = 'question.created_at'
    QUESTION_DESC = 'question.created_at:desc'
    ANSWER_ASC = 'answer.created_at'
    ANSWER_DESC = 'answer.created_at:desc'


class QARecordModelFilter(StrEnum):
    USER_ID = 'question.user_id'
