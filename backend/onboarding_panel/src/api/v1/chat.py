from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request

from src.containers.onboarding import ServiceContainer
from src.containers.jwt import ServiceContainer as JWTServiceContainer
from module.services.jwt import JWTService
from src.services.question import QuestionService
from src.models.message import MessageData


router = APIRouter(prefix='/chat', tags=['Onboarding panel'])


@router.post(path='', name='Create question', response_model=None)
@inject
async def create_question(
    request: Request,
    data: MessageData,
    question_service: QuestionService = Depends(Provide[ServiceContainer.question_service]),
    jwt_service: JWTService = Depends(Provide[JWTServiceContainer.jwt_service])
) -> None:  
    claims = await jwt_service.required(request=request)
    user_id = claims.get('sub')

    question = await question_service.create(user_id=user_id, message=data.message)

    return {"question": question.message}
