from .base import BaseRepository
from ..db.message import Answer
from src.models.message import Answer as AnswerModel


class AnswerRepository(BaseRepository):
    model = Answer
    schema = AnswerModel
