from typing import Any

from .base import BaseTokenService, revoke_key, get_jti, create_token


class AccessTokenService(BaseTokenService):
    def __init__(self, ttl: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self._ttl: int = ttl

    async def create(self, identity: Any, claims: dict[str, Any] | None = None) -> str:
        return create_token(identity=identity, ttl=self._ttl, additional_claims=claims)

    async def add_to_blocklist(self, claims: dict[str, Any]) -> None:
        await self.cache_svc.set(key=revoke_key.substitute(jti=claims.get('jti')), data='')
