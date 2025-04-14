from fastapi import APIRouter, UploadFile, File
from starlette.responses import JSONResponse

from schemas.task import TaskModel
from services.task import TaskService

router = APIRouter(prefix='/task', tags=['task'])


@router.post('/teacher')
async def create_task(organization_id: str, token: str, assignment_id: str, task: TaskModel):
    service = TaskService()
    if service.create_task(task, token, assignment_id):
         return JSONResponse(content=None, status_code=201)
    return JSONResponse(content=None, status_code=401)

@router.post('/teacher/add-file')
async def add_file_to_task(organization_id: str, token: str, task_id, file: UploadFile = File(...)):
     service = TaskService()
     if await service.add_question_file(token, task_id, file):
          return JSONResponse(content=None, status_code=201)
     return JSONResponse(content=None, status_code=401)