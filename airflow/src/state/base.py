from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseState(ABC):
    @abstractmethod
    def get(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        """Получение данных из кеша"""

    @abstractmethod
    def set(self, key: str, data: Any) -> None:
        """Установка данных в кеш"""
