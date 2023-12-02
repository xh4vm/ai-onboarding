from uuid import UUID

from ..repositories.base import BaseRepository
from ..db.message import Answer


class AnswerService:

    def __init__(self, answer_repository: BaseRepository) -> None:
        self._repository: BaseRepository = answer_repository

    async def create(self, question_id: UUID, message: str, **kwargs) -> Answer:
        return await self._repository.add(message=message, question_id=question_id, **kwargs)
