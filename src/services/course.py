from typing import Optional, List

from repositories.course import CourseRepository
from repositories.user import UserRepository
from schemas.common import Course
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
    
    def delete_course(self, token: str, course_id: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return False
        if data[0][0] not in [TEACHER, ADMIN] or not data[0][5]:
            return False
        self.course_repository.delete_course(course_id)
        return True

    def get_courses_list(self, token: str, search_query: Optional[str] = None) -> Optional[List[Course]]:
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.user_repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if len(data) != 1:
            return None
        if data[0][0] != TEACHER or not data[0][5]:
            return None
        user_id = data[0][6]
        data = self.course_repository.get_courses_list(user_id)
        response: List[Course] = []
        for i in data:
            if search_query:
                if search_query in i[1] or search_query in i[2]:
                    response.append(Course(id=str(i[0]), name=i[1], description=i[2], is_active=i[5]))
            else:
                response.append(Course(id=str(i[0]), name=i[1], description=i[2], is_active=i[5]))   
        return response