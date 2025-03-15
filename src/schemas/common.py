from pydantic import BaseModel

class Response400(BaseModel):
    code: str