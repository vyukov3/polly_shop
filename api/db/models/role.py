from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT

from api.db.models.base import Base


class Role(Base):
    """
    Model class for table role
    """

    name = Column(TEXT, unique=True, index=True)
    code = Column(TEXT, unique=True)
