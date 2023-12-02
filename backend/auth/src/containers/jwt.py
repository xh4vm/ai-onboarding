from dependency_injector import containers, providers

from ..services.jwt import JWTService
from .base import BaseContainer


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..api.v1.auth', '..api.v1.token'])
    
    config = providers.Configuration()

    jwt_service = providers.Factory(
        JWTService,
        cache_svc=BaseContainer.cache_svc
    )
