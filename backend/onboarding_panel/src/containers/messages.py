from dependency_injector import containers, providers
from typing import Type, Optional

from ..services.messages.chat import ChatMessageService, BaseService
from .base import BaseContainer


class ServiceFactory(providers.Factory):
    provided_type: Optional[Type] = BaseService


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..api.v1.chat'])

    chat_service = ServiceFactory(
        ChatMessageService,
        cache_svc=BaseContainer.cache_svc,
        search_svc=BaseContainer.search_svc
    )
