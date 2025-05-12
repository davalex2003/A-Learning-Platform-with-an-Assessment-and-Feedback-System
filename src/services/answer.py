from typing import List

from repositories.answer import AnswerRepository
from repositories.task import TaskRepository
from repositories.user import UserRepository
from schemas.answer import TaskInfo
from utils.hash import get_hash_string
from utils.jwt import decode_data

STUDENT = 'student'
TEACHER = 'teacher'

class AnswerService():
    def __init__(self):
        self.answer_repository = AnswerRepository()
        self.task_repository = TaskRepository()
        self.user_repository = UserRepository()

    def insert_answer_text(self, token: str, assignment_id: str, task_id: str, text: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != STUDENT or not data[0][5]:
            return False
        user_id = data[0][6]
        self.answer_repository.insert_answer_text(task_id, user_id, assignment_id, text)
        return True

    async def insert_answer_file(self, token: str, assignment_id: str, task_id: str, file) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != STUDENT or not data[0][5]:
            return False
        with open(file.filename, "wb") as f:
            content = await file.read()
            f.write(content)
        self.answer_repository.insert_answer_file(task_id, data[0][6], assignment_id, file.filename)
        return True

    def get_answer_file(self, token: str, assignment_id: str, task_id: str, user_id: str):
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] not in [STUDENT, TEACHER] or not data[0][5]:
            return False
        return self.answer_repository.get_answer_file(task_id, user_id, assignment_id)

    def insert_answer_assessment(self, token: str, assignment_id: str, task_id: str, user_id: str, assessment: int):
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != TEACHER or not data[0][5]:
            return False
        self.answer_repository.insert_answer_assessment(task_id, user_id, assignment_id, assessment)
        return True

    def insert_answer_feedback(self, token: str, assignment_id: str, task_id: str, user_id: str, feedback: str):
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != TEACHER or not data[0][5]:
            return False
        self.answer_repository.insert_answer_feedback(task_id, user_id, assignment_id, feedback)
        return True

    def get_answers_for_student(self, token: str, assignment_id: str):
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if data[0][0] != STUDENT or not data[0][5]:
            return None
        tasks = self.task_repository.get_tasks(assignment_id)
        tasks_info: List[TaskInfo] = []
        if tasks:
            for task in tasks:
                answer = self.answer_repository.get_answer(data[0][6], task[0])
                if answer:
                    tasks_info.append(TaskInfo(id=str(task[0]), question_type=task[1], question_text=task[2], question_file=task[3],
                                            answer_type=task[4], answer_variants=task[5], answer_text=answer[0],
                                            answer_file=answer[1], assessment=answer[2], feedback=answer[3]))
                else:
                    tasks_info.append(TaskInfo(id=str(task[0]), question_type=task[1], question_text=task[2], question_file=task[3],
                                            answer_type=task[4], answer_variants=task[5]))
        return tasks_info