from typing import Iterator

from ..repositories.base import BaseRepository
from ..db.user import User


class UserService:

    def __init__(self, user_repository: BaseRepository) -> None:
        self._repository: BaseRepository = user_repository

    async def all(self) -> Iterator[User]:
        return await self._repository.all()

    async def get(self, **kwargs) -> User:
        return await self._repository.get(**kwargs)
    
    async def one(self, **kwargs) -> User:
        return await self._repository.one(**kwargs)

    async def create(self, email: str, password: str, **kwargs) -> User:
        return await self._repository.add(email=email, password=password, **kwargs)

    async def delete(self, **kwargs) -> None:
        return await self._repository.delete(**kwargs)
