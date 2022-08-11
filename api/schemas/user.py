from typing import Optional

from pydantic import BaseModel, EmailStr
from schemas.common import PaginationRequest


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


class UserUpdateAllAllowedFields(UserUpdate):
    is_active: Optional[bool]
    is_admin: Optional[bool]


class UserCreate(UserBase):
    password: str


class UserInfo(UserBase):
    id: int


class UserInfoAllAllowedFields(UserInfo):
    is_active: bool
    is_admin: bool


class UserFilters(BaseModel):
    is_active: Optional[bool]
    is_admin: Optional[bool]


class ResponseModificators(BaseModel):
    pagination: PaginationRequest
    filtering: Optional[UserFilters]
