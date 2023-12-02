import jwt
import uuid
from abc import ABC, abstractmethod
from string import Template
from typing import Any
from datetime import datetime, timedelta

from ..cache.base import BaseCache
from src.core.config import CONFIG


revoke_key = Template('revoked::token::$jti')
user_refresh_key = Template('refresh_token::$jti')


def get_jwt_claims(token: str) -> dict[str, Any]:
    return jwt.decode(token, key=CONFIG.APP.JWT.SECRET, algorithms=CONFIG.APP.JWT.DECODE_ALGORITHMS)


def get_jwt_identity(token: str) -> Any:
    return get_jwt_claims(token)['sub']


def get_jwt_exp(token: str) -> int:
    return get_jwt_claims(token)['exp']


def get_jti(token: str) -> str:
    return get_jwt_claims(token)['jti']


def verify_exp_jwt(token: str) -> bool:
    exp = get_jwt_exp(token)
    return exp > datetime.utcnow().timestamp()


def decode_token(token: str) -> dict[str, Any]:
    claims = get_jwt_claims(token)
    
    if claims['exp'] < datetime.utcnow().timestamp():
        raise ValueError("Token has expired")

    return claims


def create_token(identity: Any, ttl: int, additional_claims: dict[str, Any] | None = None) -> str:

    payload = {
        'sub': identity,
        'exp': (datetime.utcnow() + timedelta(minutes=ttl)).timestamp(),
        'jti': str(uuid.uuid4())
    }

    if additional_claims is not None:
        payload = {**payload, **additional_claims}

    return jwt.encode(
        payload,
        key=CONFIG.APP.JWT.SECRET,
        algorithm=CONFIG.APP.JWT.ALGORITHM
    )


class BaseTokenService(ABC):
    def __init__(self, cache_svc: BaseCache):
        self.cache_svc = cache_svc

    @abstractmethod
    async def create(self, identity: Any, claims: dict[str, Any] | None = None) -> str:
        """Метод для генерации токена"""

    @abstractmethod
    async def add_to_blocklist(self, **kwargs) -> None:
        """Помечивание токена как протухшего"""

    def decode_token(self, token: str) -> dict[str, Any]:
        return decode_token(token)
