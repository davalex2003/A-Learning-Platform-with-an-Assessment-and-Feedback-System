from fastapi import FastAPI, UploadFile, File, Request, WebSocket
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return JSONResponse(status_code=200, content={"message": "pong"})


@app.get("/")
async def root():
    return "Бэкенд для выпускной квалификационной работы. Для документации вызовите /docs"
