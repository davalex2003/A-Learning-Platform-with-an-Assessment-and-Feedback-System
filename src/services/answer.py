from repositories.answer import AnswerRepository
from repositories.user import UserRepository
from utils.hash import get_hash_string
from utils.jwt import decode_data

STUDENT = 'student'
TEACHER = 'teacher'

class AnswerService():
    def __init__(self):
        self.answer_repository = AnswerRepository()
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