import enum
from datetime import datetime

from db.base_class import Base
from db.models.petition_decision_maker import petition_decision_maker
from db.models.supporter_petitions import supporter_petitions
from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship


class Status(str, enum.Enum):
    active = "active"
    closed = "closed"
    pending = "pending"
    victory = "victory"


class Petition(Base):
    __tablename__ = "petition"
    __table_args__ = (CheckConstraint("signed_goal >= 0"), {})

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String)
    country = Column(String)
    creation_date = Column(Date, default=datetime.now().date())
    due_date = Column(Date)
    signed_goal = Column(Integer, nullable=False)
    status = Column(
        ENUM(Status, name="petition_status"),
        default=Status.pending.value,
    )
    supporters = relationship(
        "User",
        secondary=supporter_petitions,
        back_populates="supported_petitions",
    )
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="created_petitions")
    complaints = relationship("Complaint", back_populates="petition")
    decision_makers = relationship(
        "DecisionMaker",
        secondary=petition_decision_maker,
        back_populates="petitions",
    )
