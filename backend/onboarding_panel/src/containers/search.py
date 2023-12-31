from typing import Optional, Type

from dependency_injector import providers, resources

from ..instances.elastic import get_elasticsearch
from ..services.search.base import BaseSearch
from ..services.search.elastic import ElasticSearch


class SearchResource(providers.Resource):
    provided_type: Optional[Type] = BaseSearch


class ElasticSearchResource(resources.AsyncResource):
    async def init(self, *args, **kwargs) -> BaseSearch:
        elasticsearch = await get_elasticsearch()
        return ElasticSearch(elastic=elasticsearch)
