from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect

from src.containers.messages import ServiceContainer as MessagesServiceContainer
from src.containers.onboarding import ServiceContainer
from src.containers.jwt import ServiceContainer as JWTServiceContainer
from src.services.messages.chat import ChatMessageService
from module.services.jwt import JWTService
from src.services.question import QuestionService
from src.models.message import MessageData
from src.models.base import PageModel


router = APIRouter(prefix='/chat', tags=['Onboarding panel'])


@router.websocket("/ws")
@inject
async def create_question(
    websocket: WebSocket,
    token: str | None,
    question_service: QuestionService = Depends(Provide[ServiceContainer.question_service]),
    jwt_service: JWTService = Depends(Provide[JWTServiceContainer.jwt_service]),
) -> None:
    claims = await jwt_service.required(request=websocket, token=token)
    user_id = claims.get('sub')

    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message_data = MessageData(message=data)

            await websocket.send_text(message_data.message)

            await question_service.create(user_id=user_id, message=message_data.message)
    except WebSocketDisconnect:
            return

@router.get(path='', name='Get chat messages', response_model=PageModel)
@inject
async def get_chat_messages(
    request: Request,
    page: int | None = 1,
    page_size: int | None = 100,
    search: str | None = None,
    chat_service: ChatMessageService = Depends(Provide[MessagesServiceContainer.chat_service]),
    jwt_service: JWTService = Depends(Provide[JWTServiceContainer.jwt_service])
) -> PageModel:  
    claims = await jwt_service.required(request=request)
    user_id = claims.get('sub')

    return await chat_service.search(
        page=page,
        page_size=page_size,
        search_value=search,
        sort_fields='question.created_at:desc,answer.created_at:desc',
        filters=f'question.user_id:{user_id}'
    )
