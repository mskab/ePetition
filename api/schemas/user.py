from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str


class UserInfo(UserBase):
    is_active: Optional[bool]
    is_admin: Optional[bool]

    class Config():
        orm_mode = True
