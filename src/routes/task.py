from fastapi import APIRouter, UploadFile, File
from starlette.responses import JSONResponse

from schemas.task import TaskModel
from services.task import TaskService

router = APIRouter(prefix='/task', tags=['task'])


@router.post('/teacher')
async def create_task(organization_id: str, token: str, assignment_id: str, task: TaskModel, question_file: UploadFile = File(None)):
    service = TaskService()
    if not await service.create_task(task, token, assignment_id, question_file):
         return JSONResponse(content=None, status_code=201)
    return JSONResponse(content=None, status_code=401)