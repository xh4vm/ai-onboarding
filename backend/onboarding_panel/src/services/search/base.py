from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from src.core.config import CONFIG

SFTYPE = TypeVar('SFTYPE')


class SearchParams(BaseModel, Generic[SFTYPE]):
    page: int = 1
    page_size: int = CONFIG.APP.PAGE_SIZE
    search_fields: list[str] | None = None
    search_value: str | None = None
    sort_fields: list[SFTYPE] | None = None
    filters: list[tuple[str, str]] | None = None

    def __str__(self) -> str:
        return (
            f'page={self.page},search_fields={self.search_fields},search_value={self.search_value},'
            f'sort_field={self.sort_fields},filters={self.filters},page_size={self.page_size}'
        )


class SearchResult(BaseModel):
    items: list[dict[str, Any]]
    total: int = 0


class BaseSearch(ABC):
    @abstractmethod
    def get_by_id(self, index: str, id: str) -> type | None:
        """Получить результат по ид"""

    @abstractmethod
    def search(self, index: str, params: SearchParams) -> SearchResult:
        """Поиск по search_filds внутри индекса"""
