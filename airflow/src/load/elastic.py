import uuid
import backoff
from loguru import logger
from typing import Iterator, Any
from elasticsearch import Elasticsearch, helpers
from datetime import datetime

from src.core.config import BACKOFF_CONFIG, ElasticsearchSettings
from src.state.base import BaseState


def es_conn_is_alive(es_conn: Elasticsearch) -> bool:
    """Функция для проверки работоспособности Elasticsearch"""
    try:
        return es_conn.ping()
    except Exception:
        return False


class ElasticsearchLoader:
    def __init__(
        self,
        settings: ElasticsearchSettings,
        state: BaseState,
        es_conn: Elasticsearch | None = None,
        chunk_size: int = 1000,
    ) -> None:
        self._settings = settings
        self._es_conn = es_conn
        self.chunk_size = chunk_size
        self._state = state

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def _reconnection(self) -> Elasticsearch:
        if self._es_conn is not None:
            self._es_conn.close()

        return Elasticsearch(
            [
                (
                    f"{self._settings.PROTOCOL}://{self._settings.USER}:{self._settings.PASSWORD}"
                    f"@{self._settings.HOST}:{self._settings.PORT}"
                )
            ]
        )

    @property
    def es_conn(self):
        if self._es_conn is None or not es_conn_is_alive(self._es_conn):
            self._es_conn = self._reconnection()
        return self._es_conn

    def _load_wrapper(
        self, data: Iterator[dict[str, Any]], index: str, key: str
    ) -> Iterator[dict[str, Any]]:
        i = 0
        down_limit = datetime.fromisoformat(
            str(self._state.get(key, default_value=datetime(1970, 1, 1, 0, 0)))
        )

        for _data in data:
            i += 1

            dict_data = _data.model_dump(by_alias=True)
            dict_data["_id"] = uuid.uuid4()
            dict_data["_index"] = index
            down_limit = max(
                datetime.fromisoformat(str(_data.question.updated_at)),
                datetime.fromisoformat(str(_data.answer.updated_at)) if _data.answer is not None else datetime(1970, 1, 1, 0, 0),
                down_limit
            )

            yield dict_data

            if i % self.chunk_size == 0:
                logger.debug(f'Sending chunk with "{i}" size')
                self._state.set(key, down_limit)

        self._state.set(key, down_limit)

    def load(self, data: Iterator[dict[str, Any]], index: str, key: str) -> None:
        patched_data: Iterator[dict[str, Any]] = self._load_wrapper(data, index, key)

        lines, _ = helpers.bulk(
            client=self.es_conn, chunk_size=self.chunk_size, actions=patched_data
        )

        if lines == 0:
            logger.info(f"Nothing to update for index {index}")
        else:
            logger.info(f"{lines} lines saved for index {index}")
