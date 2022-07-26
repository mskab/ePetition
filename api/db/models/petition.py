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
    title = Column(String)
    description = Column(String)
    image = Column(String)
    decision_maker = Column(String)
    location = Column(String)
    creation_time = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(Status))
    supporters = relationship("User",
                              secondary=supporter_petitions,
                              back_populates="petitions")
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="own_petitions")
    complains = relationship("Complain", back_populates="petition")
