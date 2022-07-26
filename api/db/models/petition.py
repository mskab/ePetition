from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..base_class import Base
from .supporter_petitions import supporter_petitions
import enum


class Status(enum.Enum):
    active = "active"
    victory = "victory"
    closed = "closed"


class Petition(Base):
    __tablename__ = "petition"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String)
    decision_maker = Column(String, nullable=False)
    location = Column(String, nullable=False)
    creation_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(Enum(Status), default=Status.active)
    supporters = relationship("User",
                              secondary=supporter_petitions,
                              back_populates="supported_petitions")
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="created_petitions")
    complains = relationship("Complain", back_populates="petition")
