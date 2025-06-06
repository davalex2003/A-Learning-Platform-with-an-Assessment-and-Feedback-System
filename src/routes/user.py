from fastapi import APIRouter
from starlette.responses import JSONResponse

from schemas.user import UserRegisterRequest, UserRegisterResponse201, UserAuthorizeRequest, UserAuthorizeResponse200, UserEmailVerifyRequest, UserInfoPutRequest
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
    return UserAuthorizeResponse200(token=token)

@router.get('/info')
async def get_user_info(organization_id: str, token: str):
    service = UserService()
    return service.get_user_info(token) or JSONResponse(content=None, status_code=404)

@router.post('/email/send_verification_code')
async def send_verification_code(organization_id: str, token: str):
    service = UserService()
    if service.send_verification_code(token):
        return JSONResponse(content=None, status_code=200)
    return Response400(code='invalid_email')

@router.post('/email/verify')
async def verify_email(organization_id: str, request: UserEmailVerifyRequest):
    service = UserService()
    if not service.verify_email(request.token, request.code):
        return Response400(code='invalid_code')
    service.confirm_email(request)
    return JSONResponse(content=None, status_code=200)

@router.put('/info')
async def update_user_info(organization_id: str, token: str, request: UserInfoPutRequest):
    service = UserService()
    if not service.update_user_info(request, token):
        return JSONResponse(content=None, status_code=404)
    return JSONResponse(content=None, status_code=200)