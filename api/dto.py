import typing as tp
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from api.db.models.user import User


@dataclass(kw_only=True, slots=True)
class AuthContext:
    user: User | None = None
    payload: dict[str, tp.Any] | None = None
    token_type: str | None = None


@dataclass(kw_only=True, slots=True)
class AccessTokenPayload:
    jti: UUID = field(default_factory=uuid4)
    type: str = "access"
    exp: int
    iat: int
    sub: UUID


@dataclass(kw_only=True, slots=True)
class RefreshTokenPayload:
    jti: UUID = field(default_factory=uuid4)
    type: str = "refresh"
    exp: int
    iat: int
    sub: UUID


@dataclass(kw_only=True, slots=True)
class TokenPair:
    access_token: str
    refresh_token: str
