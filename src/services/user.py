from typing import Optional

from repositories.user import UserRepository
from schemas.user import UserRegisterRequest, UserAuthorizeRequest
from utils.jwt import decode_data, encode_data

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def check_by_email(self, email: str) -> bool:
        return self.repository.check_by_email(email)
    
    def create_student(self, user: UserRegisterRequest) -> str:
        self.repository.create_student(user)
        return encode_data({'email': user.email, 'password': user.password})
    
    def check_user_exits(self, user: UserAuthorizeRequest) -> Optional[str]:
        if not self.repository.check_by_email_and_password(user):
            return None
        return encode_data({'email': user.email, 'password': user.password})