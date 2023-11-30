from typing import Any

import backoff
from pydantic import Field
from pydantic_settings import BaseSettings


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


class BaseSecuritySettings(BaseSettings):
    USER: str
    PASSWORD: str


class SecurityDefaultElasticsearchSettings(BaseSecuritySettings):
    class Config:
        env_prefix = "SECURITY_DEFAULT_ES_"


class SecurityElasticsearchSettings(BaseSecuritySettings):
    class Config:
        env_prefix = "ES_"


class SecurityKibanaSettings(BaseSecuritySettings):
    class Config:
        env_prefix = "KIBANA_"


ELASTIC_CONFIG: ElasticsearchSettings = ElasticsearchSettings()

SECURITY_DEFAULT_ELASTIC_CONFIG: SecurityDefaultElasticsearchSettings = (
    SecurityDefaultElasticsearchSettings()
)

SECURITY_ELASTIC_CONFIG: SecurityElasticsearchSettings = SecurityElasticsearchSettings()
SECURITY_KIBANA_CONFIG: SecurityKibanaSettings = SecurityKibanaSettings()

SECURITY_CONFIG: list[BaseSecuritySettings] = [
    SECURITY_ELASTIC_CONFIG,
    # SECURITY_KIBANA_CONFIG,
]

ELASTIC_CONFIG: ElasticsearchSettings = ElasticsearchSettings()
ELASTIC_INDICES: ElasticsearchIndices = ElasticsearchIndices()
BACKOFF_CONFIG: dict[str, Any] = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "max_value": 8,
}
