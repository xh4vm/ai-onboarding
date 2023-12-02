from abc import ABC, abstractmethod
from typing import Iterator, Any


class BaseTransformer(ABC):
    @abstractmethod
    def transform(
        self, raw: Iterator[dict[str, Any]], to_dict: bool = False
    ) -> Iterator[Any]:
        """Метод трансформации данных"""
