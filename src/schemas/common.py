from pydantic import BaseModel, Field

class Response400(BaseModel):
    code: str = Field(min_length=1)