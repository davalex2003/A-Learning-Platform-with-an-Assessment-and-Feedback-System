from typing import Optional

from repositories.assignment import AssignmentRepository
from repositories.user import UserRepository
from schemas.assignment import AssignmentModel
from utils.hash import get_hash_string
from utils.jwt import decode_data

TEACHER = 'teacher'

class AssignmentService():
    def __init__(self):
        self.assignment_repository = AssignmentRepository()
        self.user_repository = UserRepository()

    def create_assignment(self, assignment: AssignmentModel, course_id: str, token: str):
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if data[0][0] != TEACHER or not data[0][5]:
            return None
        return self.assignment_repository.create_assignment(assignment, course_id)

    def update_assignment(self, assignment: AssignmentModel, assignment_id: str, token: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] != TEACHER or not data[0][5]:
            return False
        self.assignment_repository.update_assignment(assignment, assignment_id)
        return True