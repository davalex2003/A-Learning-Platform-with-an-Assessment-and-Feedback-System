from repositories.user import UserRepository

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def validate_email(self, e_mail: str) -> bool:
        return self.repository.validate_email(e_mail)