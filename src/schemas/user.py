from pydantic import BaseModel, Field
from typing import Optional

class FullName(BaseModel):
    first_name: str = Field(min_length=1)
    second_name: str = Field(min_length=1)
    middle_name: Optional[str] = Field(None, min_length=1)

class UserRegisterRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=8)
    full_name: FullName

class UserRegisterResponse201(BaseModel):
    token: str = Field(min_length=1)

class UserAuthorizeRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=8)

class UserAuthorizeResponse200:
    token: str = Field(min_length=1)