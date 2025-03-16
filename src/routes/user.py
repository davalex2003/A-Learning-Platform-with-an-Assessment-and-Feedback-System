from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse

from schemas.user import UserRegisterRequest, UserRegisterResponse201
from schemas.common import Response400
from services.user import UserRepository

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/register')
async def register_user(organization_id: str, request: UserRegisterRequest):
    repository = UserRepository()
    if repository.validate_email(request.email):
        return Response400(code='user_already_exists')
    return UserRegisterResponse201(token='token')