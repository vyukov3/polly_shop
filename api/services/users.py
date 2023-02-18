from fastapi import Depends

from api.repositories.users import UsersRepository, get_users_repository
from api.schemas import users as schemas


class UsersService:
    def __init__(self, users_repository: UsersRepository) -> None:
        self._users_repository = users_repository

    async def register(self, registration_model: schemas.RegistrationModel) -> tuple[bool, str]:
        return await self._users_repository.add_user(**registration_model.dict())

    async def edit_user(self, edit_model: schemas.EditModel) -> tuple[bool, str]:
        fields = edit_model.dict(exclude_none=True)
        user_id = fields.pop("user_id")
        return await self._users_repository.edit_user(user_id, fields)


async def get_users_service(
    users_repository: UsersRepository = Depends(get_users_repository),
) -> UsersService:
    return UsersService(users_repository)
