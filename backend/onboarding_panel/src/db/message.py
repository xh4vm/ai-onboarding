from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseModel


class Question(BaseModel):

    user_id: UUID = Column(UUID(as_uuid=True), nullable=False, unique=True, primary_key=True)
    message: str = Column(String(65536), nullable=False)


class Answer(BaseModel):

    question_id: UUID = Column(ForeignKey('questions.id'), nullable=False)
    message: str = Column(String(65536), nullable=False)


class ViewedAnswer(BaseModel):

    answer_id: UUID = Column(ForeignKey('answers.id'), nullable=False)
