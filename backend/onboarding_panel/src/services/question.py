from uuid import UUID

from ..repositories.base import BaseRepository
from ..db.message import Question


class QuestionService:

    def __init__(self, question_repository: BaseRepository) -> None:
        self._repository: BaseRepository = question_repository

    async def create(self, user_id: UUID, message: str, **kwargs) -> Question:
        return await self._repository.add(message=message, user_id=user_id, **kwargs)
