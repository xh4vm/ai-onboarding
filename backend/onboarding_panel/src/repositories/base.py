from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session


class BaseRepository(ABC):

    @property
    @abstractmethod
    def model(self):
        """Модель БД"""

    @property
    @abstractmethod
    def schema(self):
        """Pydantic model"""

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory
    
    async def add(self, **kwargs):
        data_entity = self.schema(**kwargs)

        async with self.session_factory() as session:
            entity = self.model(**data_entity.model_dump())

            session.add(entity)
            await session.commit()
            await session.refresh(entity)

            return entity
