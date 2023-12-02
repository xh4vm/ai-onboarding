from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request

from src.containers.auth import ServiceContainer
from src.services.user import UserService
from src.services.token.access import AccessTokenService
from src.containers.jwt import ServiceContainer as JWTServiceContainer
from src.models.user import User
from src.services.token.refresh import RefreshTokenService
from module.services.jwt import JWTService
from src.models.token import TokenPair


router = APIRouter(prefix='/token', tags=['Auth token'])


@router.post(path='/refresh', name='Refresh token', response_model=TokenPair)
@inject
async def refresh_token(
    request: Request,
    user_service: UserService = Depends(Provide[ServiceContainer.user_service]),
    access_token_service: AccessTokenService = Depends(Provide[ServiceContainer.access_token_service]),
    refresh_token_service: RefreshTokenService = Depends(Provide[ServiceContainer.refresh_token_service]),
    jwt_service: JWTService = Depends(Provide[JWTServiceContainer.jwt_service])
) -> TokenPair:  
    claims = await jwt_service.required(request=request, refresh=True)
    identity = claims.get('sub')
    
    entity = await user_service.get(id=identity)

    if entity is None:
        HTTPException(status_code=400, detail="Bad refresh roken data")
    
    user = User(id=entity.id, email=entity.email, password=entity.password)

    access_token: str = await access_token_service.create(identity=str(user.id), claims=user.get_claims())
    refresh_token: str = await refresh_token_service.create(identity=str(user.id))

    return TokenPair(access=access_token, refresh=refresh_token)
