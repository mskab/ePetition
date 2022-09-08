from api.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Table

petition_decision_maker = Table(
    "petition_decision_maker",
    Base.metadata,
    Column("decision_maker_id", ForeignKey("decision_maker.id")),
    Column("petition_id", ForeignKey("petition.id")),
)
