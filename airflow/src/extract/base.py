from abc import ABC, abstractmethod
from typing import Any


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self) -> Any:
        """Метод извлечения данных"""
