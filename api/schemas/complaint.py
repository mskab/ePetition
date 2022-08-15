from typing import Optional

from db.models.complaint import Abuse, Status
from pydantic import BaseModel


class ComplaintUpdate(BaseModel):
    status: Status

    class Config:
        use_enum_values = True


class ComplaintCreate(BaseModel):
    abuse: Abuse
    description: Optional[str]
    owner_id: int
    petition_id: int

    class Config:
        use_enum_values = True


class ComplaintInfo(ComplaintCreate):
    id: int
    status: Status

    class Config:
        orm_mode = True
