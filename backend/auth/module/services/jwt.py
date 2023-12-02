from fastapi import Request
from typing import Any
from pydantic import ValidationError
from jwt.exceptions import ExpiredSignatureError, DecodeError

from .cache.base import BaseCache
from ..models.token import TokenHeader

import jwt
import uuid
from string import Template
from datetime import datetime, timedelta

from module.core.config import CONFIG


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


class JWTService:

    def __init__(self, cache_svc: BaseCache):
        self.cache_svc = cache_svc

    async def required(self, request: Request, refresh: bool = False) -> dict[str, Any]:

        try:
            token_header = TokenHeader(token=request.headers.get('Authorization'))
            token = token_header.get_payload()
        except ValidationError:
            raise DecodeError("Bad token format")

        payload = decode_token(token)

        key = revoke_key.substitute(jti=payload.get('jti'))

        if await self.cache_svc.get(key) is not None: 
            raise ExpiredSignatureError("Token has expired")

        if refresh:
            refresh_key = user_refresh_key.substitute(jti=payload.get('jti'))

            if await self.cache_svc.get(refresh_key) is None:
                raise ExpiredSignatureError("Token has expired")
            
        return payload

    async def optional(self, request: Request, refresh: bool = False) -> dict[str, Any] | None:
        try:
            return await self.required(request=request, refresh=refresh)
        except:
            return None
