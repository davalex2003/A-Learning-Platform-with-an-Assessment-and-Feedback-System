from fastapi import HTTPException
import json
from os import remove
from typing import Optional, List

from repositories.task import TaskRepository
from repositories.user import UserRepository
from schemas.task import TaskModel, QuestionType, AnswerType, Task
from utils.hash import get_hash_string
from utils.jwt import decode_data

STUDENT = 'student'
TEACHER = 'teacher'
FILE = 'file'

class TaskService():
    def __init__(self):
        self.task_repository = TaskRepository()
        self.user_repository = UserRepository()

    def create_task(self, task: TaskModel, token: str, assignment_id: str) -> Optional[str]:
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if data[0][0] != TEACHER or not data[0][5]:
            return None
        if task.question_type == QuestionType.text and not task.question_text:
            raise HTTPException(status_code=400, detail="question_text is required for 'text' question_type")
        if task.answer_type == AnswerType.variants and not task.answer_variants:
            raise HTTPException(status_code=400, detail="answer_variants is required for 'variants' answer_type")
        return self.task_repository.create_task(task, assignment_id)

    async def add_question_file(self, token: str, task_id: str, file) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != TEACHER or not data[0][5]:
            return False
        self.task_repository.add_question_file(file.filename, task_id)
        with open(file.filename, "wb") as f:
            content = await file.read()
            f.write(content)
        return True

    def delete_task(self, token: str, task_id: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != TEACHER or not data[0][5]:
            return False
        task_data = self.task_repository.get_question_info(task_id)
        if not task_data:
            raise HTTPException(status_code=400, detail="Task not found")
        if task_data[0] == FILE:
            if task_data[1]:
                remove(task_data[1])
        self.task_repository.delete_task(task_id)
        return True

    def get_tasks(self, token: str, assignment_id: str) -> Optional[List[Task]]:
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if data[0][0] not in [STUDENT, TEACHER] or not data[0][5]:
            return None
        response: List[Task] = []
        for i in self.task_repository.get_tasks(assignment_id):
            response.append(Task(id=str(i[0]), question_type=i[1], question_text=i[2], question_file=i[3], answer_type=i[4],
                                 answer_variants=i[5]))
        return response

    def get_question_file(self, token: str, task_id: str):
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] not in [STUDENT, TEACHER] or not data[0][5]:
            return False
        return self.task_repository.get_question_file(task_id)
        