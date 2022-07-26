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


class Complain(Base):
    __tablename__ = "complain"

    id = Column(Integer, primary_key=True, index=True)
    abuse = Column(Enum(Abuse), nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="complains")
    petition_id = Column(Integer, ForeignKey("petition.id"), nullable=False)
    petition = relationship("Petition", back_populates="complains")
