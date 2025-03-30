from pydantic import BaseModel, Field

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