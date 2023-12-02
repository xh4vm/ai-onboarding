import backoff
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings
from typing import Any


class JWTSettings(BaseSettings):
    SECRET: str
    ALGORITHM: str
    DECODE_ALGORITHMS: list[str]
    TTL_ACCESS_TOKEN: int
    TTL_REFRESH_TOKEN: int

    class Config:
        env_prefix = "AUTH_JWT_"


class AppSettings(BaseSettings):
    HOST: str = Field("localhost")
    PORT: int
    PROJECT_NAME: str
    API_PATH: str
    API_URL: str
    SCHEMA_REGISTRY_URL: str = Field("http://localhost:8081")
    API_VERSION: str
    SWAGGER_PATH: str
    JSON_SWAGGER_PATH: str
    JWT: JWTSettings = JWTSettings()

    class Config:
        env_prefix = "AUTH_"


class PostgresSettings(BaseSettings):
    SCHEMA: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str

    class Config:
        env_prefix = "DB_"

    def dsl(self) -> dict[str, Any]:
        return {
            "dbname": self.NAME,
            "user": self.USER,
            "password": self.PASSWORD,
            "host": self.HOST,
            "port": self.PORT,
        }
    
    @property
    def URL(self):
        return f'postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}'


class RedisSettings(BaseSettings):
    PASSWORD: str
    HOST: str
    PORT: int
    CACHE_EXPIRE: int

    class Config:
        env_prefix = "REDIS_"


POSTGRES: PostgresSettings = PostgresSettings()


class Config(BaseSettings):
    APP: AppSettings = AppSettings()


CONFIG = Config()
REDIS_CONFIG = RedisSettings()
BACKOFF_CONFIG: dict[str, Any] = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "max_value": 8,
}
