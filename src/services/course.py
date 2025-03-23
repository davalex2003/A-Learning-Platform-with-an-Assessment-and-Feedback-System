from typing import Optional

from repositories.course import CourseRepository
from repositories.user import UserRepository
from schemas.course import CourseModel
from utils.hash import get_hash_string
from utils.jwt import decode_data

ADMIN = 'admin'
TEACHER = 'teacher'

class CourseService():
    def __init__(self):
        self.course_repository = CourseRepository()
        self.user_repository = UserRepository()

    def create_course(self, course: CourseModel, token: str) -> Optional[str]:
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if data[0][0] != TEACHER or not data[0][5]:
            return None
        id = self.course_repository.create_course(course, data[0][6])
        return id
    
    def update_course(self, course: CourseModel, token: str, course_id: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] not in [TEACHER, ADMIN] or not data[0][5]:
            return False
        self.course_repository.update_course(course, course_id)
        return True