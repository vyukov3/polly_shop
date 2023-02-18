import uuid

from fastapi import Depends

from api import dto
from api.db.models import User
from api.repositories.users import UsersRepository, get_users_repository
from api.services.auth.authorization import AuthorizationService, get_authorization_service
from api.services.auth.base import BaseAuthenticationService, BaseAuthorizationService
from api.services.auth.exc import BadCredentialsError
from api.services.jwt.service import JwtService, get_jwt_service
from api.utils import verify_password


# pylint: disable=arguments-differ
class JwtAuthenticationService(BaseAuthenticationService):
    def __init__(
        self,
        *,
        users_repository: UsersRepository,
        jwt: JwtService,
        authorization: BaseAuthorizationService,
    ):
        self._users_repository = users_repository
        self._jwt = jwt
        self._authorization = authorization

        self._context = dto.AuthContext()

    async def authenticate(self, username: str, password: str) -> dto.TokenPair:
        user = await self.verify_credentials(username=username, password=password)
        self._context.user = user
        tokens = await self.create_tokens(str(user.id))
        return tokens

    async def create_tokens(self, user_id: str):
        _, access_token = await self.create_access_token(user_id)
        _, refresh_token = await self._jwt.create_refresh_token(user_id)

        return dto.TokenPair(access_token=access_token, refresh_token=refresh_token)

    async def verify_authentication(self, token: str, token_type: str = "access"):
        assert token_type in ("access", "refresh")

        token_payload = (
            await self._jwt.verify_access_token(token)
            if token_type == "access"
            else await self._jwt.verify_refresh_token(token)
        )
        self._context.payload = token_payload

    async def verify_credentials(self, username: str, password: str) -> User:
        user = await self._users_repository.find(username=username)
        if not user:
            raise BadCredentialsError("User with specified username was not found")

        hashed_password = user.password
        password_ok = verify_password(password, hashed_password)
        if not password_ok:
            raise BadCredentialsError("Wrong password")

        return user

    async def get_current_user(self) -> User | None:
        user = self._context.user
        if user is not None:
            return user

        if self._context.payload is None:
            return None

        user_id = self._context.payload.get("sub")
        user = await self._users_repository.get_by_id(user_id)
        return user

    def get_auth_context(self) -> dto.AuthContext:
        return self._context

    async def refresh_token(self) -> str:
        refresh_payload = self._context.payload
        sub = refresh_payload.get("sub")
        _, access_token = await self.create_access_token(sub)
        return access_token

    async def revoke_tokens(self):
        access_payload = self._context.payload
        await self._jwt.revoke_tokens(access_payload)

    async def revoke_all_tokens(self):
        access_payload = self._context.payload
        await self._jwt.revoke_all_tokens_except_current(access_payload)

    async def create_access_token(self, user_id: uuid.UUID):
        perms = await self._authorization.get_user_permissions(user_id)
        token = await self._jwt.create_access_token(
            str(user_id),
            perms_in_workspaces={str(perm.workspace_id): perm.permissions for perm in perms},
        )
        return token


async def get_authentication_service(
    users_repository: UsersRepository = Depends(get_users_repository),
    authorization_service: AuthorizationService = Depends(get_authorization_service),
    jwt_service: JwtService = Depends(get_jwt_service),
) -> JwtAuthenticationService:
    return JwtAuthenticationService(
        users_repository=users_repository, jwt=jwt_service, authorization=authorization_service
    )
