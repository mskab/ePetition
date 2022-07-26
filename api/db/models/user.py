from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..base_class import Base
from .supporter_petitions import supporter_petitions


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    supported_petitions = relationship("Petition",
                             secondary=supporter_petitions,
                             back_populates="supporters")
    created_petitions = relationship("Petition", back_populates="owner")
    complains = relationship("Complain", back_populates="owner")
