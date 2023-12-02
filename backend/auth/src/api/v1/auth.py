from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request, Body
from typing import Annotated

from src.containers.auth import ServiceContainer as AuthServiceContainer
from src.containers.jwt import ServiceContainer as JWTServiceContainer
from src.services.user import UserService
from module.services.jwt import JWTService
from src.services.token.access import AccessTokenService
from src.services.token.refresh import RefreshTokenService
from src.models.user import User, UserData
from src.models.token import TokenPair


router = APIRouter(prefix='/action', tags=['Auth action'])


@router.post(path='/sign_in', name='Sign in', response_model=TokenPair)
@inject
async def sign_in_action(
    request: Request,
    sign_in_user_data: UserData,
    user_service: UserService = Depends(Provide[AuthServiceContainer.user_service]),
    access_token_service: AccessTokenService = Depends(Provide[AuthServiceContainer.access_token_service]),
    refresh_token_service: RefreshTokenService = Depends(Provide[AuthServiceContainer.refresh_token_service]),
    jwt_service: JWTService = Depends(Provide[JWTServiceContainer.jwt_service])
) -> TokenPair:  
    claims = await jwt_service.optional(request=request)

    if claims is not None:
        raise HTTPException(
            status_code=200,
            detail=f"Вы уже авторизованы"
        )

    user = await user_service.get(email=sign_in_user_data.email)

    if user is None or not user.verify(password=sign_in_user_data.password):
        raise HTTPException(
            status_code=401,
            detail=f"Неверный логин или пароль"
        )
    
    user = User(id=user.id, email=user.email, password=user.password)
    
    access_token: str = await access_token_service.create(identity=str(user.id), claims=user.get_claims())
    refresh_token: str = await refresh_token_service.create(identity=str(user.id))

    return TokenPair(access=access_token, refresh=refresh_token)


@router.post(path='/sign_up', name='Sign up', response_model=None)
@inject
async def sign_up_action(
    request: Request,
    sign_up_user_data: UserData,
    user_service: UserService = Depends(Provide[AuthServiceContainer.user_service]),
    jwt_service: JWTService = Depends(Provide[JWTServiceContainer.jwt_service])
) -> None:
    
    claims = await jwt_service.optional(request=request)

    if claims is not None:
        raise HTTPException(
            status_code=200,
            detail=f"Вы уже авторизованы"
        )

    entity = await user_service.get(email=sign_up_user_data.email)

    if entity is not None:
        raise HTTPException(
            status_code=400,
            detail=f"Пользователь '{sign_up_user_data.email}' уже существует"
        )

    user_data = User(**sign_up_user_data.model_dump())

    await user_service.create(**user_data.model_dump())

    return None


@router.delete(path='/logout', name='Logout', response_model=None)
@inject
async def logout(
    request: Request,
    refresh_token: Annotated[str, Body(embed=True)],
    access_token_service: AccessTokenService = Depends(Provide[AuthServiceContainer.access_token_service]),
    refresh_token_service: RefreshTokenService = Depends(Provide[AuthServiceContainer.refresh_token_service]),
    jwt_service: JWTService = Depends(Provide[JWTServiceContainer.jwt_service])
) -> None:
    claims = await jwt_service.required(request=request)

    await access_token_service.add_to_blocklist(claims)
    await refresh_token_service.add_to_blocklist(refresh_token)
