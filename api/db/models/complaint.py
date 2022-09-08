import enum

from api.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship


class Abuse(enum.Enum):
    misleading_spam = "Misleading or spam"
    infringes = "Infringes on my rights"
    abusive_hateful = "Abusive or hateful"
    inappropriate = "Inappropriate images"
    harmful = "Harmful to children"
    violence_suicide = "Violence, suicide, or self harm"
    impersonation = "Impersonation"
    other = "Other"


class Status(enum.Enum):
    accepted = "accepted"
    rejected = "rejected"
    pending = "pending"


class Complaint(Base):
    __tablename__ = "complaint"

    id = Column(Integer, primary_key=True, index=True)
    abuse = Column(
        ENUM(
            Abuse,
            values_callable=lambda obj: [e.value for e in obj],
            name="complaint_abuse",
        ),
        nullable=False,
    )
    description = Column(String)
    status = Column(
        ENUM(Status, name="complaint_status"),
        default=Status.pending.value,
    )
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="complaints")
    petition_id = Column(
        Integer, ForeignKey("petition.id"), nullable=False
    )
    petition = relationship("Petition", back_populates="complaints")
