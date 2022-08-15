from db.base_class import Base
from sqlalchemy import Column, ForeignKey, Table

supporter_petitions = Table(
    "supporter_petitions",
    Base.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("petition_id", ForeignKey("petition.id")),
)
