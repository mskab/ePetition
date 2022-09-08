from api.db.base_class import Base
from api.db.models.petition_decision_maker import petition_decision_maker
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship


class DecisionMaker(Base):
    __tablename__ = "decision_maker"

    id = Column(Integer, primary_key=True, index=True)
    naming = Column(String, nullable=False)
    affiliation = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    petitions = relationship(
        "Petition",
        secondary=petition_decision_maker,
        back_populates="decision_makers",
    )
