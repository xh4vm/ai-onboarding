from .base import BaseRepository
from ..db.message import Question
from src.models.message import Question as QuestionModel


class QuestionRepository(BaseRepository):
    model = Question
    schema = QuestionModel
