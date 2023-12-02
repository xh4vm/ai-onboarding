from datetime import datetime, timezone
from typing import Any

from .base import BaseTokenService, revoke_key, user_refresh_key, create_token, decode_token


class RefreshTokenService(BaseTokenService):
    def __init__(self, ttl: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self._ttl: int = ttl

    async def create(self, identity: Any, claims: dict[str, Any] | None = None) -> str:
        token = create_token(identity=identity, ttl=self._ttl, additional_claims=claims)

        payload = decode_token(token)

        jti = payload.get('jti')
        exp = payload.get('exp')

        key = user_refresh_key.substitute(jti=jti)

        ttl = int(exp - datetime.now(timezone.utc).timestamp())
        await self.cache_svc.set(key=key, data='', expire=ttl)

        return token

    async def add_to_blocklist(self, refresh_token: str) -> None:
        claims = self.decode_token(token=refresh_token)

        jti = claims.get('jti')
        exp = claims.get('exp')

        key = user_refresh_key.substitute(jti=jti)

        if self.cache_svc.get(key):
            self.cache_svc.delete(key)

        ttl = int(exp - datetime.now(timezone.utc).timestamp())
        await self.cache_svc.set(key=revoke_key.substitute(jti=jti), data='', expire=ttl)
