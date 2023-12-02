from elasticsearch import AsyncElasticsearch


es: AsyncElasticsearch | None = None


async def get_elasticsearch() -> AsyncElasticsearch:
    return es
