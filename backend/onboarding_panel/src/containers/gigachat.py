from dependency_injector import containers, providers
from typing import Type, Optional

from ..services.gigachat import GigachatService
from .base import BaseContainer


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..api.v1.chat'])

    gigachat_service = providers.Factory(GigachatService)
