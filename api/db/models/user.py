import os
print("2---------------------",os.getcwd())
from api.db.base_class import Base
from api.db.models.supporter_petitions import supporter_petitions
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    supported_petitions = relationship(
        "Petition",
        secondary=supporter_petitions,
        back_populates="supporters",
    )
    created_petitions = relationship("Petition", back_populates="owner")
    complaints = relationship("Complaint", back_populates="owner")
