from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from routes.admin import router as admin_router
from routes.api import router as api_router
from routes.assignment import router as assignment_router
from routes.course import router as course_router
from routes.task import router as task_router
from routes.user import router as user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router)
app.include_router(api_router)
app.include_router(assignment_router)
app.include_router(course_router)
app.include_router(task_router)
app.include_router(user_router)

@app.get("/ping")
async def ping():
    return JSONResponse(status_code=200, content={"message": "pong"})


@app.get("/")
async def root():
    return "Бэкенд для выпускной квалификационной работы. Для документации вызовите /docs"
