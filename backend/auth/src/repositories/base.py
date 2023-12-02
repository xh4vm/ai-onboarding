from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Callable, Iterator

from sqlalchemy.orm import Session


class BaseRepository(ABC):

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    @abstractmethod
    async def all(self) -> Iterator[type]:
        """Получение списка объектов"""
        
    @abstractmethod
    async def get(self, **kwargs) -> type:
        """Получение одного экземпляра"""
        
    @abstractmethod
    async def one(self, **kwargs) -> type:
        """Получение одного экземпляра или исключение"""

    @abstractmethod
    async def add(self, **kwargs) -> type:
        """Добавление элемента в БД""" 

    @abstractmethod
    async def delete(self, **kwargs) -> None:
        """Удаление элемента из БД""" 
