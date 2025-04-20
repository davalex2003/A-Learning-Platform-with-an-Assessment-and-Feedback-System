from pydantic import BaseModel, Field

class AnswerTextPostRequest(BaseModel):
    text: str = Field(min_length=1)

class TaskEvaluateRequest(BaseModel):
    assessment: int