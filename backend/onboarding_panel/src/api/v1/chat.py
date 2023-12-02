from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, Body
from typing import Annotated

from src.containers.messages import ServiceContainer as MessagesServiceContainer
from src.containers.onboarding import ServiceContainer
from src.containers.jwt import ServiceContainer as JWTServiceContainer
from src.containers.gigachat import ServiceContainer as GigachatServiceContainer
from src.services.messages.chat import ChatMessageService
from module.services.jwt import JWTService
from src.services.question import QuestionService
from src.services.answer import AnswerService
from src.services.gigachat import GigachatService
from src.models.message import MessageData, QARecord, Question, Answer
from src.models.base import PageModel


router = APIRouter(prefix='/chat', tags=['Onboarding panel'])


@router.post(path='', name='Create message', response_model=QARecord)
@inject
async def create_question(
    request: Request,
    message: Annotated[str, Body(embed=True)],
    question_service: QuestionService = Depends(Provide[ServiceContainer.question_service]),
    answer_service: AnswerService = Depends(Provide[ServiceContainer.answer_service]),
    gigachat_service: GigachatService = Depends(Provide[GigachatServiceContainer.gigachat_service]),
    jwt_service: JWTService = Depends(Provide[JWTServiceContainer.jwt_service]),
) -> None:
    claims = await jwt_service.required(request=request)
    user_id = claims.get('sub')

    message_data = MessageData(message=message)

    answer_message = gigachat_service.chat(message_data)

    question = await question_service.create(user_id=user_id, message=message_data.message)
    question_record = Question(
        id=question.id,
        user_id=question.user_id,
        message=question.message,
        created_at=question.created_at,
        updated_at=question.updated_at,
    )

    answer = await answer_service.create(question_id=question.id, message=answer_message)
    answer_record = Answer(
        id=answer.id,
        question_id=answer.question_id,
        message=answer.message,
        created_at=answer.created_at,
        updated_at=answer.updated_at,
    )

    record = QARecord(question=question_record, answer=answer_record)

    return record


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
