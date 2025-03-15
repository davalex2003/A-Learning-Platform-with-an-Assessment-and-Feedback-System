from pydantic import BaseModel
from typing import Optional

class FullName(BaseModel):
    first_name: str
    second_name: str
    middle_name: str

class UserRegisterRequest(BaseModel):
    email: str
    password: str
    full_name: FullName

class UserRegisterResponse201(BaseModel):
    token: str