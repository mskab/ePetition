from typing import Optional

from pydantic import BaseModel, EmailStr


class DecisionMakerUpdate(BaseModel):
    naming: Optional[str]
    affiliation: Optional[str]
    email: Optional[EmailStr]


class DecisionMakerCreate(BaseModel):
    naming: str
    affiliation: Optional[str]
    email: EmailStr


class DecisionMakerInfo(DecisionMakerCreate):
    id: int
    is_verified: Optional[bool]

    class Config:
        orm_mode = True
