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

class UserAuthorizeResponse200(BaseModel):
    token: str = Field(min_length=1)

class UserInfoResponse200(BaseModel):
    role: str = Field(min_length=1)
    full_name: FullName
    email: str = Field(min_length=1)

class UserEmailVerifyRequest(BaseModel):
    token: str = Field(min_length=1)
    code: str = Field(min_length=6, max_length=6)

class UserInfoPutRequest(BaseModel):
    full_name: Optional[FullName] = Field(None)
    password: Optional[str] = Field(None, min_length=8)