from repositories.user import UserRepository
from schemas.user import UserRegisterRequest
from utils.jwt import decode_data, encode_data

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def validate_email(self, email: str) -> bool:
        return self.repository.validate_email(email)
    
    def create_student(self, user: UserRegisterRequest) -> str:
        self.repository.create_student(user)
        return encode_data({'email': user.email, 'password': user.password})