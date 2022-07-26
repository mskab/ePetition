from sqlalchemy import Table, Column, ForeignKey
from ..base_class import Base


supporter_petitions = Table("supporter_petitions", Base.metadata,
                            Column("user_id", ForeignKey(
                                "user.id"), primary_key=True),
                            Column("petition_id", ForeignKey("petition.id"), primary_key=True))
