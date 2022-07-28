from sqlalchemy import Table, Column, ForeignKey
from ..base_class import Base


petition_decision_maker = Table("petition_decision_maker", Base.metadata,
                            Column("decision_maker_id", ForeignKey(
                                "decision_maker.id"), primary_key=True),
                            Column("petition_id", ForeignKey("petition.id"), primary_key=True))
