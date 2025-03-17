from fastapi import APIRouter
from starlette.responses import JSONResponse
from typing import Optional

from schemas.admin import User
from schemas.common import Response400
from services.admin import AdminService

router = APIRouter(prefix='/admin', tags=['admin'])


@router.get('/user/list')
async def get_user_list(organization_id: str, token: str, search_query: Optional[str] = None):
    service = AdminService()
    if not service.check_is_admin(token):
        return JSONResponse(content=None, status_code=401)
    return service.get_users_list(search_query)

@router.delete('/user')
async def delete_user(organization_id: str, token: str, user_id: str):
    service = AdminService()
    if not service.check_is_admin(token):
        return JSONResponse(content=None, status_code=401)
    service.delete_user(user_id)
    return JSONResponse(content=None, status_code=200)