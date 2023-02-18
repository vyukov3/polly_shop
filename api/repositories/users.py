from uuid import UUID

from fastapi import Depends
from sqlalchemy import exc, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.connection import get_session
from api.db.models import Role, User


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User:
        query = select(User).where(User.id == user_id)
        user = await self._session.scalar(query)
        return user

    async def find(self, **kwargs) -> User:
        query = select(User)
        for field, value in kwargs.items():
            query = query.where(getattr(User, field) == value)

        users = await self._session.scalars(query)
        return users.first()

    async def add_user(self, email: str, password: str) -> tuple[bool, str]:
        try:
            query = select(Role).where(code="user")
            role = await self._session.scalars(query)
            role = role.first()

            query = insert(User).values(email=email, password=password, role_id=role.id)
            await self._session.execute(query)
            await self._session.commit()
        except exc.IntegrityError:
            return False, "User with that email already exists."
        return True, "Successful registration!"

    async def edit_user(self, user_id: UUID, fields: dict) -> tuple[bool, str]:
        try:

            query = update(User).where(id=user_id).values(**fields)
            await self._session.execute(query)
            await self._session.commit()
        except exc.IntegrityError:
            return False, "User with that email already exists."
        return True, "Successful registration!"


async def get_users_repository(session: AsyncSession = Depends(get_session)) -> UsersRepository:
    return UsersRepository(session=session)
