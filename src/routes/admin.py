from fastapi import APIRouter
from starlette.responses import JSONResponse
from typing import Optional

from schemas.admin import PutUserRoleRequest
from schemas.course import CourseModel
from services.admin import AdminService
from services.course import CourseService

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

@router.put('/user/role')
async def update_role(organization_id: str, token: str, request: PutUserRoleRequest):
    service = AdminService()
    if not service.check_is_admin(token):
        return JSONResponse(content=None, status_code=401)
    service.update_role(request.id, request.role)
    return JSONResponse(content=None, status_code=200)

@router.put('/course')
async def update_course(organization_id: str, token: str, course_id: str, course: CourseModel):
    service = CourseService()
    if service.update_course(course, token, course_id):
        return JSONResponse(content=None, status_code=200)
    return JSONResponse(content=None, status_code=401)

@router.delete('/course')
async def delete_course(organization_id: str, token: str, course_id: str):
    service = CourseService()
    if service.delete_course(token, course_id):
        return JSONResponse(content=None, status_code=200)
    return JSONResponse(content=None, status_code=401)

@router.get('/course/list')
async def get_course_list(organization_id: str, token: str, search_query: Optional[str] = None):
    service = AdminService()
    if not service.check_is_admin(token):
        return JSONResponse(content=None, status_code=401)
    return service.get_courses_list(search_query)