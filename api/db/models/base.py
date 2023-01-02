import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from api.utils import camel_to_snake


@as_declarative()
class Base:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    __name__: str
    __table_args__ = {"extend_existing": True}

    @declared_attr
    def __tablename__(self):  # noqa
        return camel_to_snake(self.__name__)
