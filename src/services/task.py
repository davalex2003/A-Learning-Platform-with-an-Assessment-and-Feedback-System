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

    async def create_task(self, task: TaskModel, token: str, assignment_id: str, question_file):
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != TEACHER or not data[0][5]:
            return False
        if task.question_type == QuestionType.file and not question_file:
            raise HTTPException(status_code=400, detail="File is required for 'file' question_type")
        if task.question_type == QuestionType.text and not task.question_text:
            raise HTTPException(status_code=400, detail="question_text is required for 'text' question_type")
        if task.answer_type == AnswerType.variants and not task.answer_variants:
            raise HTTPException(status_code=400, detail="answer_variants is required for 'variants' answer_type")
        self.task_repository.create_task(task, None if question_file else question_file.filename, assignment_id)
        if question_file:
            with open(question_file.filename, "wb") as f:
                content = await question_file.read()
                f.write(content)
        return True