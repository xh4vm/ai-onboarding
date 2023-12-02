from typing import Type, Optional

from dependency_injector import containers, providers

from ..services.token.access import AccessTokenService
from ..services.token.base import BaseTokenService
from ..services.token.refresh import RefreshTokenService
from ..db.base import Database
from ..repositories.user import UserRepository
from ..services.user import UserService
from .base import BaseContainer


class TokenFactory(providers.Factory):
    provided_type: Optional[Type] = BaseTokenService


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..api.v1.auth', '..api.v1.token'])
    
    config = providers.Configuration()

    db = providers.Singleton(Database, db_url=config.db.url)

    access_token_service = TokenFactory(
        AccessTokenService,
        cache_svc=BaseContainer.cache_svc,
        ttl=config.token.ttl_access,
    )
    
    refresh_token_service = TokenFactory(
        RefreshTokenService,
        cache_svc=BaseContainer.cache_svc,
        ttl=config.token.ttl_refresh,
    )
    
    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
