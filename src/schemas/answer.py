from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List

class AnswerTextPostRequest(BaseModel):
    text: str = Field(min_length=1)

class TaskEvaluateRequest(BaseModel):
    assessment: int

class TaskFeedbackRequest(BaseModel):
    feedback: str

class QuestionType(str, Enum):
    text = 'text'
    file = 'file'

class AnswerType(str, Enum):
    text = 'text'
    file = 'file'
    variants = 'variants'

class TaskInfo(BaseModel):
    id: str
    question_type: QuestionType
    question_text: Optional[str] = Field(None)
    question_file: Optional[str] = Field(None)
    answer_type: AnswerType
    answer_variants: Optional[List[str]] = Field(None)
    answer_text: Optional[str] = Field(None)
    answer_file: Optional[str] = Field(None)
    assessment: Optional[int] = Field(None)
    feedback: Optional[str] = Field(None)