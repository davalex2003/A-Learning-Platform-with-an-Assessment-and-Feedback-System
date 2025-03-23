from fastapi import APIRouter
from starlette.responses import JSONResponse

from schemas.course import CourseModel, CourseCreateResponse201
from services.course import CourseService

router = APIRouter(prefix='/course', tags=['course'])


@router.post('/teacher')
async def create_course(organization_id: str, token: str, course: CourseModel):
    service = CourseService()
    course_id = service.create_course(course, token)
    if not course_id:
        return JSONResponse(content=None, status_code=401)
    return CourseCreateResponse201(course_id=course_id)

@router.put('/teacher')
async def update_course(organization_id: str, token: str, course_id: str, course: CourseModel):
    service = CourseService()
    if service.update_course(course, token, course_id):
        return JSONResponse(content=None, status_code=200)
    return JSONResponse(content=None, status_code=401)

@router.delete('/teacher')
async def delete_course(organization_id: str, token: str, course_id: str):
    service = CourseService()
    if service.delete_course(token, course_id):
        return JSONResponse(content=None, status_code=200)
    return JSONResponse(content=None, status_code=401)