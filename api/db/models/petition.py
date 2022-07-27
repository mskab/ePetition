from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..base_class import Base
from .supporter_petitions import supporter_petitions
from .petition_decision_maker import petition_decision_maker
import enum


class Status(enum.Enum):
    active = "active"
    closed = "closed"
    pending = "pending"
    victory = "victory"


class Petition(Base):
    __tablename__ = "petition"
    __table_args__ = (
        CheckConstraint('signed_goal >= 0'),
        {})

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String)
    country = Column(String)
    creation_time = Column(DateTime(timezone=True),
                           server_default=func.now(), nullable=False)
    due_date = Column(DateTime(timezone=True),
                      server_default=func.now())
    signed_goal = Column(Integer, nullable=False)
    status = Column(Enum(Status), default=Status.pending)
    supporters = relationship("User",
                              secondary=supporter_petitions,
                              back_populates="supported_petitions")
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="created_petitions")
    complaints = relationship("Complaint", back_populates="petition")
    decision_makers = relationship("DecisionMaker",
                             secondary=petition_decision_maker,
                             back_populates="petitions")
