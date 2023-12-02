from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from starlette.middleware import Middleware
from starlette_context import plugins
from dependency_injector import providers
from starlette_context.middleware import RawContextMiddleware
from redis.asyncio import Redis
from jwt.exceptions import PyJWTError

from .core.config import CONFIG, REDIS_CONFIG, POSTGRES
from .containers.onboarding import ServiceContainer as ChatServiceContainer
from .containers.jwt import ServiceContainer as JWTServiceContainer
from .containers.cache import CacheResource, RedisCacheResource
from .api.v1.chat import router as chat_router
from .instances import redis


def register_di_containers():
    redis_resource = CacheResource(RedisCacheResource)

    chat_container = ChatServiceContainer(cache_svc=redis_resource)
    chat_container.config.from_dict({
        "db": {"url": POSTGRES.URL}
    })

    JWTServiceContainer(cache_svc=redis_resource)


def register_routers(app: FastAPI):
    API_PATH = f"{CONFIG.APP.API_PATH}/{CONFIG.APP.API_VERSION}"
    app.include_router(router=chat_router, prefix=API_PATH)


def create_app():
    middleware = [
        Middleware(
            RawContextMiddleware,
            plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin()),
        )
    ]

    app = FastAPI(
        title=CONFIG.APP.PROJECT_NAME,
        # docs_url=f'{CONFIG.APP.API_PATH}{CONFIG.APP.SWAGGER_PATH}',
        redoc_url=f"{CONFIG.APP.API_PATH}/redoc",
        openapi_url=f"{CONFIG.APP.API_PATH}{CONFIG.APP.JSON_SWAGGER_PATH}",
        default_response_class=ORJSONResponse,
        middleware=middleware,
    )

    register_routers(app=app)
    register_di_containers()

    return app


app = create_app()


#TODO
@app.on_event('startup')
async def startup():
    redis.redis = Redis(host=REDIS_CONFIG.HOST, port=REDIS_CONFIG.PORT, password=REDIS_CONFIG.PASSWORD)


#TODO
@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return ORJSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


@app.exception_handler(PyJWTError)
async def value_error_exception_handler(request: Request, exc: PyJWTError):
    return ORJSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
