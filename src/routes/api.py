from fastapi import APIRouter
from starlette.responses import JSONResponse

from schemas.admin import AdminCreateRequest
from services.admin import AdminService

router = APIRouter(prefix='/api', tags=['api'])


@router.post('/admin/create')
async def create_admin(organization_id: str, request: AdminCreateRequest):
    service = AdminService()
    service.create_admin(request)
    return JSONResponse(content=None, status_code=200)