from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class QuestionType(str, Enum):
    text = 'text'
    file = 'file'

class AnswerType(str, Enum):
    text = 'text'
    file = 'file'
    variants = 'variants'

class TaskModel(BaseModel):
    question_type: QuestionType
    question_text: Optional[str] = Field(None)
    answer_type: AnswerType
    answer_variants: Optional[List[str]] = Field(None)

class TaskCreateResponse201(BaseModel):
    task_id: int

class Task(BaseModel):
    id: str
    question_type: QuestionType
    question_text: Optional[str] = Field(None)
    question_file: Optional[str] = Field(None)
    answer_type: AnswerType
    answer_variants: Optional[List[str]] = Field(None)