from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, UUID
from sqlalchemy.orm import relationship

from api.db.models.base import Base
from api.db.models.role import Role


class User(Base):
    """
    Model class for table user
    """

    username = Column(TEXT, unique=True, index=True)
    password = Column(TEXT)
    bonus_account = Column(INTEGER)

    role_id = Column(UUID(as_uuid=True), ForeignKey("role.id"))

    role = relationship(Role)
