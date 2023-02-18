from typing import Any

from api.services.jwt.exc import InvalidTokenTypeError, TokenRevokedError, WrongRefreshTokenError


class JwtTokenVerifierMixin:
    _secret_key: str | bytes = None

    async def verify_access_token(self, token: str) -> dict[str, Any]:
        token_payload = self.decode_token(token, self._secret_key, algorithms=["HS256"])

        token_type = token_payload.get("type")
        if token_type != "access":
            raise InvalidTokenTypeError(token_type, expected_type="access")

        if await self._blocklist_repository.in_blocklist(
            token_payload
        ) or await self._blocklist_repository.blocked_by_allblock(token_payload):
            raise TokenRevokedError

        return token_payload

    async def verify_refresh_token(self, token: str) -> dict[str, Any]:
        token_payload = self.decode_token(token, self._secret_key, algorithms=["HS256"])

        token_type = token_payload.get("type")
        if token_type != "refresh":
            raise InvalidTokenTypeError(token_type, expected_type="refresh")

        jti = token_payload.get("jti")
        sub = token_payload.get("sub")

        stored_refresh = await self._refresh_tokens_repository.get_refresh_token_from_storage(sub)
        if not stored_refresh:
            raise TokenRevokedError

        if jti != stored_refresh.get("jti"):
            raise WrongRefreshTokenError

        return token_payload
