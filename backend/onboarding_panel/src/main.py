from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse, HTMLResponse
from starlette.middleware import Middleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware
from redis.asyncio import Redis
from jwt.exceptions import PyJWTError
from elasticsearch import AsyncElasticsearch

from .core.config import CONFIG, REDIS_CONFIG, POSTGRES, ELASTIC_CONFIG
from .containers.messages import ServiceContainer as MessagesServiceContainer
from .containers.onboarding import ServiceContainer as ChatServiceContainer
from .containers.jwt import ServiceContainer as JWTServiceContainer
from .containers.cache import CacheResource, RedisCacheResource
from .containers.search import ElasticSearchResource, SearchResource
from .api.v1.chat import router as chat_router
from .instances import redis, elastic


def register_di_containers():
    redis_resource = CacheResource(RedisCacheResource)
    elasticsearch_resource = SearchResource(ElasticSearchResource)

    MessagesServiceContainer(cache_svc=redis_resource, search_svc=elasticsearch_resource)
    chat_container = ChatServiceContainer(cache_svc=redis_resource, search_svc=elasticsearch_resource)
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

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
        var ws2 = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost/onboarding/api/v1/chat/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/onboarding")
async def get():
    return HTMLResponse(html)


#TODO
@app.on_event('startup')
async def startup():
    redis.redis = Redis(host=REDIS_CONFIG.HOST, port=REDIS_CONFIG.PORT, password=REDIS_CONFIG.PASSWORD)
    elastic.es = AsyncElasticsearch(hosts=[
        (
            f'{ELASTIC_CONFIG.PROTOCOL}://{ELASTIC_CONFIG.USER}:{ELASTIC_CONFIG.PASSWORD}'
            f'@{ELASTIC_CONFIG.HOST}:{ELASTIC_CONFIG.PORT}'
        )
    ])

#TODO
@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


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
