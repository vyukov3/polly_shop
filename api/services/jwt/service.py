import typing as tp
import uuid
from datetime import timedelta

from fastapi import Depends

from api.dto import TokenPair
from api.repositories.tokens import (
    BlocklistRepository,
    RefreshTokensRepository,
    get_blocklist_repository,
    get_refresh_tokens_repository,
)
from api.services.jwt.coders import JwtTokenDecoderMixin, JwtTokenEncoderMixin
from api.services.jwt.utils import to_seconds, utcnow
from api.services.jwt.verifier import JwtTokenVerifierMixin


class JwtService(
    JwtTokenEncoderMixin,
    JwtTokenDecoderMixin,
    JwtTokenVerifierMixin,
):
    def __init__(
        self,
        *,
        refresh_tokens_repository: RefreshTokensRepository,
        blocklist_repository: BlocklistRepository,
        secret_key: str = "",
        access_ex_time: int | timedelta = timedelta(hours=1),
        refresh_ex_time: int | timedelta = timedelta(weeks=2),
    ):
        self._refresh_tokens_repository = refresh_tokens_repository
        self._blocklist_repository = blocklist_repository
        self._secret_key = secret_key
        self.access_ex_time = to_seconds(access_ex_time)
        self.refresh_ex_time = to_seconds(refresh_ex_time)

    # pylint: disable=dangerous-default-value
    async def create_tokens(
        self,
        sub: str,
        access_extra_payload: dict[str, tp.Any] = {},
        refresh_extra_payload: dict[str, tp.Any] = {},
    ) -> TokenPair:
        _, access_token = await self.create_access_token(sub, **access_extra_payload)
        _, refresh_token = await self.create_refresh_token(sub, **refresh_extra_payload)

        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    async def create_access_token(self, sub: str, **extra_payload) -> tuple[dict[str, tp.Any], str]:
        iat = utcnow()
        payload = {
            "jti": uuid.uuid4(),
            "type": "access",
            "sub": sub,
            "iat": iat,
            "exp": iat + self.access_ex_time,
        }
        payload |= extra_payload

        return payload, self.encode_token(payload, self._secret_key)

    async def create_refresh_token(self, sub: str, **extra_payload) -> tuple[dict[str, tp.Any], str]:
        iat = utcnow()
        payload = {
            "jti": uuid.uuid4(),
            "type": "refresh",
            "sub": sub,
            "iat": iat,
            "exp": iat + self.refresh_ex_time,
        }
        payload |= extra_payload

        await self._refresh_tokens_repository.set_refresh_token(payload)

        return payload, self.encode_token(payload, self._secret_key)

    async def refresh_token(self, refresh_payload: dict[str, tp.Any]) -> str:
        sub = refresh_payload.get("sub")
        _, token = self.create_access_token(sub)
        return token

    async def revoke_tokens(self, access_payload: dict[str, tp.Any]):
        sub = access_payload.get("sub")
        await self._blocklist_repository.add_to_blocklist(access_payload)
        await self._refresh_tokens_repository.unset_refresh_token(sub)

    async def revoke_all_tokens_except_current(self, access_payload: dict[str, tp.Any]):
        await self._blocklist_repository.block_all_except_current(access_payload)

    async def revoke_all_tokens(self, user_id: uuid.UUID):
        await self._blocklist_repository.block_all(str(user_id))


async def get_jwt_service(
    blocklist_repository: BlocklistRepository = Depends(get_blocklist_repository),
    refresh_tokens_repository: RefreshTokensRepository = Depends(get_refresh_tokens_repository),
) -> JwtService:
    return JwtService(refresh_tokens_repository=refresh_tokens_repository, blocklist_repository=blocklist_repository)
