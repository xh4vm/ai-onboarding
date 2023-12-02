from typing import Any

import backoff
from pydantic import Field
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str
    SCHEMA: str

    class Config:
        env_prefix = "DB_"

    def dsn(self) -> dict[str, Any]:
        return {
            "dbname": self.NAME,
            "user": self.USER,
            "password": self.PASSWORD,
            "host": self.HOST,
            "port": self.PORT,
        }


class RedisSettings(BaseSettings):
    PASSWORD: str
    HOST: str
    PORT: int
    CACHE_EXPIRE: int

    class Config:
        env_prefix = "REDIS_"


class ElasticsearchSettings(BaseSettings):
    PROTOCOL: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int

    class Config:
        env_prefix = "ES_"


class ElasticsearchIndices(BaseSettings):
    ONBOARDING_PANEL: str

    class Config:
        env_prefix = "INDEX_"


REDIS_CONFIG = RedisSettings()
POSTGRES_CONFIG = PostgresSettings()
ELASTIC_CONFIG: ElasticsearchSettings = ElasticsearchSettings()
ELASTIC_INDICES: ElasticsearchIndices = ElasticsearchIndices()

BACKOFF_CONFIG: dict[str, Any] = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "max_value": 8,
}
