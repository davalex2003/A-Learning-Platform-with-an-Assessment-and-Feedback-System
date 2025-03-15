from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse

from schemas.user import UserRegisterRequest, UserRegisterResponse201
from schemas.common import Response400

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/register')
async def register_user(organization_id: str, request: UserRegisterRequest):
    return UserRegisterResponse201(token='token')