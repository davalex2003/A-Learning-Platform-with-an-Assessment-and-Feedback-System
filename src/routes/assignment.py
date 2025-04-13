from fastapi import APIRouter
from starlette.responses import JSONResponse

from schemas.assignment import AssignmentModel, AssignmentCreateResponse201
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