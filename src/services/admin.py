from typing import List, Optional

from repositories.admin import AdminRepository
from schemas.admin import User, FullName
from utils.jwt import decode_data

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
        response : List[User] = []
        for i in data:
            if search_query:
                if search_query in i[1] or search_query in i[2] or search_query in i[3] or search_query in i[4]:
                    response.append(User(id=str(i[0]), full_name=FullName(first_name=i[1], second_name=i[2], middle_name=i[3]), email=i[4], role=i[5]))
            else:
                response.append(User(id=str(i[0]), full_name=FullName(first_name=i[1], second_name=i[2], middle_name=i[3]), email=i[4], role=i[5]))   
        return response