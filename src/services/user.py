from typing import Optional

from repositories.user import UserRepository
from schemas.user import UserRegisterRequest, UserAuthorizeRequest, UserInfoResponse200, FullName
from utils.hash import get_hash_string
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

    def get_user_info(self, token: str) -> Optional[UserInfoResponse200]:
        user_data = decode_data(token)
        if not user_data:
            return None
        data = self.repository.get_user_info(user_data['email'], get_hash_string(user_data['password']))
        if not data:
            return None
        response = UserInfoResponse200(role=data[0][0], full_name=FullName(first_name=data[0][1], second_name=data[0][2], middle_name=data[0][3]), email=data[0][4])
        return response