from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse

from schemas.user import UserRegisterRequest, UserRegisterResponse201
from schemas.common import Response400
from services.user import UserService

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/register')
async def register_user(organization_id: str, request: UserRegisterRequest):
    service = UserService()
    if service.validate_email(request.email):
        return Response400(code='user_already_exists')
    token = service.create_student(request)
    return UserRegisterResponse201(token=token)