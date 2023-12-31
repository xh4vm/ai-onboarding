from datetime import datetime
from typing import Any, Iterator
from loguru import logger

import backoff
import psycopg2
from core.config import BACKOFF_CONFIG, PostgresSettings
from core.schema import Schema
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor
from state.base import BaseState


class PostgreSQLExtractor:
    """Класс для извлечения сырых данных из постгрес"""

    def __init__(
        self, settings: PostgresSettings,
        state: BaseState,
        pg_conn: connection | None = None,
        chunk_size: int = 1000
    ):
        self._pg_conn = pg_conn
        self._settings = settings
        self._state = state
        self.chunk_size = chunk_size

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def _reconnection(self) -> connection:
        """Метод подключения/переподключения к бд"""

        if self._pg_conn is not None:
            self._pg_conn.close()

        return psycopg2.connect(**self._settings.dsn(), cursor_factory=DictCursor)

    @property
    def pg_conn(self) -> connection:
        if self._pg_conn is None or self._pg_conn.closed:
            self._pg_conn = self._reconnection()

        return self._pg_conn

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def extract(self) -> Iterator[tuple[Any]]:
        """Метод получения сырых данных из бд.
        В результате возвращаю генератор, которых позволяет брать
        данные из бд сразу пачкой по chunk_size штук"""

        down_limit = self._state.get(f'down_limit_chats', default_value=str(datetime.min))
        logger.debug(r'state setted in ' + down_limit)

        cursor = self.pg_conn.cursor()
        cursor.itersize = self.chunk_size

        # query = (
        #     f'SELECT fw.id, fw.title, fw.description, fw.rating, fw.creation_date, fw.type, '
        #     f'fw.created_at, GREATEST(fw.updated_at, MAX(p.updated_at), MAX(g.updated_at)) as updated_at, '
        #     f"COALESCE(ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) "
        #     f"FILTER (WHERE pfw.role = '{PersonFilmWorkRoleEnum.DIRECTOR}')," + " '{}') AS directors, "
        #     f"COALESCE(ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) "
        #     f"FILTER (WHERE pfw.role = '{PersonFilmWorkRoleEnum.ACTOR}')," + " '{}') AS actors, "
        #     f"COALESCE(ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) "
        #     f"FILTER (WHERE pfw.role = '{PersonFilmWorkRoleEnum.WRITER}')," + " '{}') AS writers, "
        #     f'ARRAY_AGG(DISTINCT g.name) as genres FROM {SCHEMA}.{Schema.film_work} fw '
        #     f'LEFT JOIN {self._settings.SCHEMA}.{Schema.person_film_work} AS pfw ON pfw.film_work_id = fw.id '
        #     f'LEFT JOIN {self._settings.SCHEMA}.{Schema.person} AS p ON p.id = pfw.person_id '
        #     f'LEFT JOIN {self._settings.SCHEMA}.{Schema.genre_film_work} AS gfw ON gfw.film_work_id = fw.id '
        #     f'LEFT JOIN {self._settings.SCHEMA}.{Schema.genre} AS g ON g.id = gfw.genre_id '
        #     f"WHERE GREATEST(fw.updated_at, p.updated_at, g.updated_at) > '{down_limit}' "
        #     f'GROUP BY fw.id '
        #     f'ORDER BY GREATEST(fw.updated_at, MAX(p.updated_at), MAX(g.updated_at));'
        # )
        query = (
            f'SELECT q.id question_id, q.user_id question_user_id, q.message question_message, q.created_at question_created_at, q.updated_at question_updated_at, '
            f'a.id answer_id, a.question_id answer_question_id, a.message answer_message, a.created_at answer_created_at, a.updated_at answer_updated_at '
            f'FROM {self._settings.SCHEMA}.{Schema.questions} q '
            f'LEFT JOIN {self._settings.SCHEMA}.{Schema.answers} AS a ON a.question_id = q.id '
            f"WHERE GREATEST(q.updated_at, a.updated_at) > '{down_limit}' "
            f'ORDER BY GREATEST(q.updated_at, a.updated_at);'
        )
        cursor.execute(query)

        for row in cursor:
            yield row

        cursor.close()
