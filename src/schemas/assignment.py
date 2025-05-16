from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List

class AssignmentModel(BaseModel):
    name: str = Field(min_length=1)
    started_at: datetime
    ended_at: Optional[datetime] = Field(None)

class AssignmentCreateResponse201(BaseModel):
    assignment_id: int

class AssignmentStatus(str, Enum):
    pending = 'pending'
    in_review = 'in_review'
    graded = 'graded'

class Assignment(BaseModel):
    id: str
    name: str
    started_at: datetime
    ended_at: Optional[datetime] = Field(None)
    status: Optional[AssignmentStatus] = Field(None)

class AssignmentCourse(BaseModel):
    course_id: str
    course_name: str
    assignments: List[Assignment]