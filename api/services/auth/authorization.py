from fastapi import Depends

from api.repositories.users import UsersRepository, get_users_repository
from api.services.auth.base import BaseAuthorizationService


class AuthorizationService(BaseAuthorizationService):
    def __init__(self, *, users_repository: UsersRepository):
        self._users_repository = users_repository


async def get_authorization_service(
    users_repository: UsersRepository = Depends(get_users_repository),
) -> AuthorizationService:
    return AuthorizationService(users_repository=users_repository)
