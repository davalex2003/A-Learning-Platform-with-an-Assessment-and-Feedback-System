from typing import List, Optional

from repositories.admin import AdminRepository
from schemas.admin import User, FullName, AdminCreateRequest
from schemas.common import Course
from utils.jwt import decode_data
from utils.hash import get_hash_string

ADMIN = 'admin'

class AdminService:
    def __init__(self):
        self.repository = AdminRepository()
    
    def check_is_admin(self, token: str) -> bool:
        user_data = decode_data(token)
        if not user_data:
            return False
        role = self.repository.get_role(user_data['email'])[0]
        if role != ADMIN:
            return False
        return True

    def get_users_list(self, search_query: Optional[str] = None) -> List[User]:
        data = self.repository.get_users_list()
        response: List[User] = []
        for i in data:
            if search_query:
                if search_query in i[1] or search_query in i[2] or search_query in i[3] or search_query in i[4]:
                    response.append(User(id=str(i[0]), full_name=FullName(first_name=i[1], second_name=i[2], middle_name=i[3]), email=i[4], role=i[5]))
            else:
                response.append(User(id=str(i[0]), full_name=FullName(first_name=i[1], second_name=i[2], middle_name=i[3]), email=i[4], role=i[5]))   
        return response

    def delete_user(self, user_id: str):
        self.repository.delete_user(user_id)

    def update_role(self, user_id: str, role: str):
        self.repository.update_role(user_id, role)
    
    def get_courses_list(self, search_query: Optional[str] = None) -> List[Course]:
        data = self.repository.get_courses_list()
        response: List[Course] = []
        for i in data:
            if search_query:
                if search_query in i[1] or search_query in i[2]:
                    response.append(Course(id=str(i[0]), name=i[1], description=i[2], is_active=i[5]))
            else:
                response.append(Course(id=str(i[0]), name=i[1], description=i[2], is_active=i[5]))   
        return response
    
    def create_admin(self, admin: AdminCreateRequest):
        self.repository.create_admin(admin.email, admin.full_name.first_name, admin.full_name.second_name,
                                     admin.full_name.middle_name, get_hash_string(admin.password))