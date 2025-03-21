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