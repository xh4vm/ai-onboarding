from dependency_injector import containers, providers

from ..services.cache.base import BaseCache
from ..services.search.base import BaseSearch


class BaseContainer(containers.DeclarativeContainer):
    cache_svc = providers.Dependency(instance_of=BaseCache)
    search_svc = providers.Dependency(instance_of=BaseSearch)
