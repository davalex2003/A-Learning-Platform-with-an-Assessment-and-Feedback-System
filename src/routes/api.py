from fastapi import APIRouter, File, UploadFile
from starlette.responses import JSONResponse, FileResponse
from typing import Optional

from schemas.admin import AdminCreateRequest, PutUserRoleRequest
from schemas.common import Response400
from schemas.course import CourseModel, CourseCreateResponse201, CourseAdditionsLinkRequest, AdditionType
from schemas.user import UserRegisterRequest, UserRegisterResponse201, UserAuthorizeRequest, UserAuthorizeResponse200, UserEmailVerifyRequest
from services.admin import AdminService
from services.course import CourseService
from services.user import UserService

router = APIRouter(prefix='/api', tags=['api'])


@router.post('/admin/create')
async def create_admin(organization_id: str, request: AdminCreateRequest):
    service = AdminService()
    service.create_admin(request)
    return JSONResponse(content=None, status_code=200)

@router.get('/admin/user/list')
async def get_user_list(organization_id: str, token: str, search_query: Optional[str] = None):
    service = AdminService()
    if not service.check_is_admin(token):
        return JSONResponse(content=None, status_code=401)
    return service.get_users_list(search_query)

@router.delete('/admin/user')
async def delete_user(organization_id: str, token: str, user_id: str):
    service = AdminService()
    if not service.check_is_admin(token):
        return JSONResponse(content=None, status_code=401)
    service.delete_user(user_id)
    return JSONResponse(content=None, status_code=200)

@router.put('/admin/user/role')
async def update_role(organization_id: str, token: str, request: PutUserRoleRequest):
    service = AdminService()
    if not service.check_is_admin(token):
        return JSONResponse(content=None, status_code=401)
    service.update_role(request.id, request.role)
    return JSONResponse(content=None, status_code=200)

@router.put('/admin/course')
async def update_course(organization_id: str, token: str, course_id: str, course: CourseModel):
    service = CourseService()
    if service.update_course(course, token, course_id):
        return JSONResponse(content=None, status_code=200)
    return JSONResponse(content=None, status_code=401)

@router.delete('/admin/course')
async def delete_course(organization_id: str, token: str, course_id: str):
    service = CourseService()
    if service.delete_course(token, course_id):
        return JSONResponse(content=None, status_code=200)
    return JSONResponse(content=None, status_code=401)

@router.get('/admin/course/list')
async def get_course_list(organization_id: str, token: str, search_query: Optional[str] = None):
    service = AdminService()
    if not service.check_is_admin(token):
        return JSONResponse(content=None, status_code=401)
    return service.get_courses_list(search_query)

@router.post('/course/teacher')
async def create_course(organization_id: str, token: str, course: CourseModel):
    service = CourseService()
    course_id = service.create_course(course, token)
    if not course_id:
        return JSONResponse(content=None, status_code=401)
    return CourseCreateResponse201(course_id=course_id)

@router.put('/course/teacher')
async def update_course(organization_id: str, token: str, course_id: str, course: CourseModel):
    service = CourseService()
    if service.update_course(course, token, course_id):
        return JSONResponse(content=None, status_code=200)
    return JSONResponse(content=None, status_code=401)

@router.delete('/course/teacher')
async def delete_course(organization_id: str, token: str, course_id: str):
    service = CourseService()
    if service.delete_course(token, course_id):
        return JSONResponse(content=None, status_code=200)
    return JSONResponse(content=None, status_code=401)

@router.get('/course/teacher/list')
async def get_course_list(organization_id: str, token: str, search_query: Optional[str] = None):
    service = CourseService()
    courses = service.get_courses_list(token, search_query)
    if courses is None:
        return JSONResponse(content=None, status_code=401)
    return courses

@router.post('/course/teacher/additions/link')
async def insert_link(organization_id: str, token: str, course_id: str, request: CourseAdditionsLinkRequest):
    service = CourseService()
    if service.insert_course_link(token, course_id, request.link):
        return JSONResponse(content=None, status_code=201)
    return JSONResponse(content=None, status_code=401)

@router.post('/course/additions/material')
async def add_material(organization_id: str, token: str, course_id: str, file: UploadFile = File(...)):
    service = CourseService()
    if await service.insert_course_material(token, course_id, file):
        return JSONResponse(content=None, status_code=201)
    return JSONResponse(content=None, status_code=401)

@router.get('/course/additions')
async def get_additions(organization_id: str, token: str, course_id: str):
    service = CourseService()
    additions = service.get_links_and_materials(token, course_id)
    if not additions:
        return JSONResponse(content=None, status_code=401)
    return additions

@router.get('/course/additions/material')
async def get_material(organization_id: str, token: str, course_id: str, addition_id: str):
    service = CourseService()
    material = service.get_course_material(token, course_id, addition_id)
    if material is None:
        return JSONResponse(content=None, status_code=401)
    return FileResponse(path=material, media_type='application/octet-stream', filename=material)

@router.delete('/course/additions')
async def delete_addition(organization_id: str, token: str, course_id: str, addition_id: str, addition_type: AdditionType):
    service = CourseService()
    if service.delete_course_addition(token, course_id, addition_id, addition_type):
        return JSONResponse(content=None, status_code=200)
    return JSONResponse(content=None, status_code=401)

@router.post('/course/student/add')
async def add_student_to_course(organization_id: str, token: str, course_id: str):
    service = CourseService()
    if service.add_user_course_link(token, course_id):
        return JSONResponse(content=None, status_code=201)
    return JSONResponse(content=None, status_code=401)

@router.get('/course/student/list')
async def get_student_courses_list(organization_id: str, token: str, search_query: Optional[str] = None):
    service = CourseService()
    courses = service.get_courses_student_list(token, search_query)
    if courses is None:
        return JSONResponse(content=None, status_code=401)
    return courses

@router.post('/user/register')
async def register_user(organization_id: str, request: UserRegisterRequest):
    service = UserService()
    if service.check_by_email(request.email):
        return Response400(code='user_already_exists')
    token = service.create_student(request)
    return UserRegisterResponse201(token=token)

@router.post('/user/authorize')
async def authorize_user(organization_id: str, request: UserAuthorizeRequest):
    service = UserService()
    if not service.check_by_email(request.email):
        return JSONResponse(content=None, status_code=404)
    token = service.check_user_exits(request)
    if not token:
        return Response400(code='wrong_password')
    return UserAuthorizeResponse200(token=token)

@router.get('/user/info')
async def get_user_info(organization_id: str, token: str):
    service = UserService()
    return service.get_user_info(token) or JSONResponse(content=None, status_code=404)

@router.post('/user/email/send_verification_code')
async def send_verification_code(organization_id: str, token: str):
    service = UserService()
    if service.send_verification_code(token):
        return JSONResponse(content=None, status_code=200)
    return Response400(code='invalid_email')

@router.post('/user/email/verify')
async def verify_email(organization_id: str, request: UserEmailVerifyRequest):
    service = UserService()
    if not service.verify_email(request.token, request.code):
        return Response400(code='invalid_code')
    service.confirm_email(request)
    return JSONResponse(content=None, status_code=200)