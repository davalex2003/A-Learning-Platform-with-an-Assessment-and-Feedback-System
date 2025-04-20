from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class CourseModel(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)

class CourseCreateResponse201(BaseModel):
    course_id: int

class CourseAdditionsLinkRequest(BaseModel):
    link: str = Field(min_length=1)

class Addition(BaseModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)

class CourseAdditionsResponse200(BaseModel):
    materials: list[Addition]
    links: list[Addition]

class AdditionType(str, Enum):
    link = 'link'
    material = 'material'

class FullName(BaseModel):
    first_name: str = Field(min_length=1)
    second_name: str = Field(min_length=1)
    middle_name: Optional[str] = Field(None, min_length=1)

class User(BaseModel):
    id: str = Field(min_length=1)
    full_name: FullName
    email: str = Field(min_length=1)