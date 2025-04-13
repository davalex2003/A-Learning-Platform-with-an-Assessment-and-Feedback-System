from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class AssignmentModel(BaseModel):
    name: str = Field(min_length=1)
    started_at: datetime
    ended_at: Optional[datetime] = Field(None)

class AssignmentCreateResponse201(BaseModel):
    assignment_id: int