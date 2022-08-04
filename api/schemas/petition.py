from typing import Optional, List
from pydantic import BaseModel
from datetime import date
from .decision_maker import DecisionMakerInfo
from .user import UserBase
from db.models.petition import Status


class PetitionSign(BaseModel):
    supporter_id: int


class PetitionUpdate(BaseModel):
    due_date: Optional[date]
    signed_goal: Optional[int]
    decision_makers: Optional[List[int]]
    status: Optional[Status]

    class Config:
        use_enum_values = True


class PetitionBase(BaseModel):
    title: str
    description: str
    image: Optional[str]
    country: Optional[str]
    due_date: Optional[date]
    signed_goal: int


class PetitionCreate(PetitionBase):
    owner_id: int
    decision_makers: List[int]


class PetitionInfo(PetitionBase):
    id: int
    status: Status
    creation_date: date
    owner_id: int
    decision_makers: List[DecisionMakerInfo]
    supporters: List[UserBase]

    class Config:
        orm_mode = True
        use_enum_values = True
