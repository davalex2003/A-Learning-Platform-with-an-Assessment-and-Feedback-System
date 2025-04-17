from fastapi import APIRouter, UploadFile, File
from starlette.responses import JSONResponse, FileResponse

from schemas.task import TaskModel, TaskCreateResponse201
from services.task import TaskService

router = APIRouter(prefix='/task', tags=['task'])


@router.post('/teacher')
async def create_task(organization_id: str, token: str, assignment_id: str, task: TaskModel):
    service = TaskService()
    task_id = service.create_task(task, token, assignment_id)
    if task_id:
         return TaskCreateResponse201(task_id=task_id)
    return JSONResponse(content=None, status_code=401)

@router.post('/teacher/add-file')
async def add_file_to_task(organization_id: str, token: str, task_id: str, file: UploadFile = File(...)):
     service = TaskService()
     if await service.add_question_file(token, task_id, file):
          return JSONResponse(content=None, status_code=201)
     return JSONResponse(content=None, status_code=401)

@router.delete('/teacher')
async def delete_task(organization_id: str, token: str, task_id: str):
     service = TaskService()
     if service.delete_task(token, task_id):
          return JSONResponse(content=None, status_code=200)
     return JSONResponse(content=None, status_code=401)

@router.get('/list')
async def get_tasks_list(organization_id: str, token: str, assignment_id: str):
     service = TaskService()
     tasks = service.get_tasks(token, assignment_id)
     if tasks is None:
          return JSONResponse(content=None, status_code=401)
     return tasks

@router.get('/question/file')
async def get_question_file(organization_id: str, token: str, task_id: str):
     service = TaskService()
     question_file = service.get_question_file(token, task_id)
     if question_file == False:
          return JSONResponse(content=None, status_code=401)
     elif question_file is None:
          return JSONResponse(content=None, status_code=404)
     else:
          return FileResponse(path=question_file[0], media_type='application/octet-stream', filename=question_file[0])