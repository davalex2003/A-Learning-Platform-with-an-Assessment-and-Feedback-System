from pydantic import BaseModel, Field
from typing import Optional

class FullName(BaseModel):
    first_name: str = Field(min_length=1)
    second_name: str = Field(min_length=1)
    middle_name: Optional[str] = Field(None, min_length=1)

class User(BaseModel):
    id: str = Field(min_length=1)
    full_name: FullName
    email: str = Field(min_length=1)
    role: str