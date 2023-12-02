from uuid import UUID

from .base import JSONModel, UUIDMixin, TimestampMixin


class MessageData(JSONModel):
    message: str


class Question(MessageData, UUIDMixin, TimestampMixin):
    user_id: UUID


class Answer(MessageData, UUIDMixin, TimestampMixin):
    question_id: UUID
