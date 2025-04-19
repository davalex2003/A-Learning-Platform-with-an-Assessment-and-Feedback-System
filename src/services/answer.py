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

    def insert_answer(self, token: str, assignment_id: str, task_id: str, text: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != STUDENT or not data[0][5]:
            return False
        user_id = data[0][6]
        self.answer_repository.insert_answer(task_id, user_id, assignment_id, text)
        return True