from redis import Redis
from datetime import datetime
from loguru import logger

from src.extract.postgres import PostgreSQLExtractor
from src.core.config import POSTGRES_CONFIG, ELASTIC_CONFIG, ELASTIC_INDICES, REDIS_CONFIG
from src.load.elastic import ElasticsearchLoader
from src.transform.qa_record import QARecordTransformer
from src.state.redis import RedisState


def run():
    redis = Redis(
        host=REDIS_CONFIG.HOST, port=REDIS_CONFIG.PORT, password=REDIS_CONFIG.PASSWORD
    )
    state = RedisState(redis=redis)

    extractor = PostgreSQLExtractor(settings=POSTGRES_CONFIG, state=state)
    transformer = QARecordTransformer()
    loader = ElasticsearchLoader(settings=ELASTIC_CONFIG, state=state)


    raw_data = extractor.extract()
    data = transformer.transform(raw=raw_data)

    down_limit = state.get(
        "down_limit_chats", default_value=datetime(1970, 1, 1, 0, 0)
    )
    logger.info(f"down_limit: {down_limit}")

    loader.load(
        data=data,
        index=ELASTIC_INDICES.ONBOARDING_PANEL,
        key="down_limit_chats",
    )

    logger.info("[+] Success finished etl process postgres to elastic")
