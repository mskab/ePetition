from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..base_class import Base
import enum


class Abuse(enum.Enum):
    misleading_spam = "Misleading or spam"
    infringes = "Infringes on my rights"
    abusive_hateful = "Abusive or hateful"
    inappropriate = "Inappropriate images"
    harmful = "Harmful to children"
    violence_suicide = "Violence, suicide, or self harm"
    impersonation = "Impersonation"


class Status(enum.Enum):
    accepted = "accepted"
    rejected = "rejected"
    pending = "pending"


class Complaint(Base):
    __tablename__ = "complaint"

    id = Column(Integer, primary_key=True, index=True)
    abuse = Column(Enum(Abuse), nullable=False)
    description = Column(String)
    status = Column(Enum(Status), default=Status.pending)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="complaints")
    petition_id = Column(Integer, ForeignKey("petition.id"), nullable=False)
    petition = relationship("Petition", back_populates="complaints")
