from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Response400(BaseModel):
    code: str = Field(min_length=1)

class Course(BaseModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    is_active: bool