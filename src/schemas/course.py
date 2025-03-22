from pydantic import BaseModel, Field

class CourseModel(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)

class CourseCreateResponse201(BaseModel):
    course_id: int