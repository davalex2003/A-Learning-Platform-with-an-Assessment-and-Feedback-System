from fastapi import HTTPException
from repositories.task import TaskRepository
from repositories.user import UserRepository
from schemas.task import TaskModel, QuestionType, AnswerType
from utils.hash import get_hash_string
from utils.jwt import decode_data

TEACHER = 'teacher'

class TaskService():
    def __init__(self):
        self.task_repository = TaskRepository()
        self.user_repository = UserRepository()

    def create_task(self, task: TaskModel, token: str, assignment_id: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != TEACHER or not data[0][5]:
            return False
        if task.question_type == QuestionType.text and not task.question_text:
            raise HTTPException(status_code=400, detail="question_text is required for 'text' question_type")
        if task.answer_type == AnswerType.variants and not task.answer_variants:
            raise HTTPException(status_code=400, detail="answer_variants is required for 'variants' answer_type")
        self.task_repository.create_task(task, assignment_id)
        return True

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
