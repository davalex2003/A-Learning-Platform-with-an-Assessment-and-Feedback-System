from fastapi import APIRouter
from starlette.responses import JSONResponse

from schemas.assignment import AssignmentModel, AssignmentCreateResponse201
from services.answer import AnswerService
from services.assignment import AssignmentService

router = APIRouter(prefix='/assignment', tags=['assignment'])


@router.post('/teacher')
async def create_assignment(organization_id: str, token: str, course_id: str, assignment: AssignmentModel):
    service = AssignmentService()
    assignment_id = service.create_assignment(assignment, course_id, token)
    if not assignment_id:
        return JSONResponse(content=None, status_code=401)
    return AssignmentCreateResponse201(assignment_id=assignment_id)

@router.put('/teacher')
async def update_assignment(organization_id: str, token: str, assignment_id: str, assignment: AssignmentModel):
    service = AssignmentService()
    if service.update_assignment(assignment, assignment_id, token):
        return JSONResponse(content=None, status_code=200)
    return JSONResponse(content=None, status_code=401)

@router.delete('/teacher')
async def delete_assignment(organization_id: str, token: str, assignment_id: str):
    service = AssignmentService()
    if service.delete_assignment(assignment_id, token):
        return JSONResponse(content=None, status_code=200)
    return JSONResponse(content=None, status_code=401)

@router.get('/list')
async def get_assignment_list(organization_id: str, token: str, course_id: str):
    service = AssignmentService()
    assignments = service.get_assignments(course_id, token)
    if assignments is None:
        return JSONResponse(content=None, status_code=401)
    return assignments

@router.get('/courses')
async def get_assignment_courses(organization_id: str, token: str):
    service = AssignmentService()
    assignments = service.get_homeworks(token)
    if assignments is None:
        return JSONResponse(content=None, status_code=401)
    return assignments

@router.get('/student/info')
async def get_student_info(organization_id: str, token: str, assignment_id: str):
    service = AnswerService()
    tasks_info = service.get_answers_for_student(token, assignment_id)
    if tasks_info is None:
        return JSONResponse(content=None, status_code=401)
    return tasks_info

@router.get('/teacher/info')
async def get_teacher_info(organization_id: str, token: str, assignment_id: str, user_id: str):
    service = AnswerService()
    tasks_info = service.get_answers_for_teacher(token, assignment_id, user_id)
    if tasks_info is None:
        return JSONResponse(content=None, status_code=401)
    return tasks_info