from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse

from schemas.user import UserRegisterRequest, UserRegisterResponse201, UserAuthorizeRequest, UserAuthorizeResponse200
from schemas.common import Response400
from services.user import UserService

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/register')
async def register_user(organization_id: str, request: UserRegisterRequest):
    service = UserService()
    if service.check_by_email(request.email):
        return Response400(code='user_already_exists')
    token = service.create_student(request)
    return UserRegisterResponse201(token=token)

@router.post('/authorize')
async def authorize_user(organization_id: str, request: UserAuthorizeRequest):
    service = UserService()
    if not service.check_by_email(request.email):
        return JSONResponse(content=None, status_code=404)
    token = service.check_user_exits(request)
    if not token:
        return Response400(code='wrong_password')
    return UserRegisterResponse201(token=token)