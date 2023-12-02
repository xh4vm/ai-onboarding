from fastapi import Request
from typing import Any
from pydantic import ValidationError
from jwt.exceptions import ExpiredSignatureError, DecodeError

from .cache.base import BaseCache
from ..models.token import TokenHeader
from .token.base import decode_token, revoke_key, user_refresh_key


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