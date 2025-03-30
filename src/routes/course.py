from fastapi import APIRouter, File, UploadFile
from starlette.responses import JSONResponse
from typing import Optional

from schemas.course import CourseModel, CourseCreateResponse201, CourseAdditionsLinkRequest
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

@router.get('/teacher/list')
async def get_course_list(organization_id: str, token: str, search_query: Optional[str] = None):
    service = CourseService()
    courses = service.get_courses_list(token, search_query)
    if not courses:
        return JSONResponse(content=None, status_code=401)
    return courses

@router.post('/teacher/additions/link')
async def insert_link(organization_id: str, token: str, course_id: str, request: CourseAdditionsLinkRequest):
    service = CourseService()
    if service.insert_course_link(token, course_id, request.link):
        return JSONResponse(content=None, status_code=201)
    return JSONResponse(content=None, status_code=401)

@router.post('/additions/material')
async def add_material(organization_id: str, token: str, course_id: str, file: UploadFile = File(...)):
    service = CourseService()
    if await service.insert_course_material(token, course_id, file):
        return JSONResponse(content=None, status_code=201)
    return JSONResponse(content=None, status_code=401)

@router.get('/additions')
async def get_additions(organization_id: str, token: str, course_id: str):
    service = CourseService()
    additions = service.get_links_and_materials(token, course_id)
    if not additions:
        return JSONResponse(content=None, status_code=401)
    return additions