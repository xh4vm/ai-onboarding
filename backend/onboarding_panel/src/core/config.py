import backoff
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings
from typing import Any


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

    class Config:
        env_prefix = "ONBOARDING_PANEL_"


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


POSTGRES: PostgresSettings = PostgresSettings()


class Config(BaseSettings):
    APP: AppSettings = AppSettings()


CONFIG = Config()
BACKOFF_CONFIG: dict[str, Any] = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "max_value": 8,
}
