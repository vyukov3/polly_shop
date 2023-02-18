import typing as tp
from abc import abstractmethod
from datetime import datetime, timedelta, timezone

import orjson
from fastapi import Depends
from redis.asyncio import Redis

from api.db.connection import get_redis


def utcnow() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp())


class BaseKeyValueStorage(tp.Protocol):
    @abstractmethod
    async def set(self, key: str, value: tp.Any, ex: int | timedelta | None = None):
        pass

    @abstractmethod
    async def get(self, key: str) -> tp.Any | None:
        pass

    @abstractmethod
    async def delete(self, key: str):
        pass


# pylint: disable=no-member
class RedisStorage(BaseKeyValueStorage):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def set(self, key: str, value: tp.Any, ex: int | timedelta | None = None):
        encoded = orjson.dumps(value)
        await self._redis.set(key, encoded, ex=ex)

    async def get(self, key: str) -> tp.Any | None:
        value = await self._redis.get(key)

        if value is not None:
            value = orjson.loads(value)

        return value

    async def delete(self, key: str):
        await self._redis.delete(key)


class RefreshTokensRepository:
    def __init__(self, storage: BaseKeyValueStorage, *, expire_time: int | timedelta = timedelta(weeks=2)):
        self._storage = storage
        self._expire_time = expire_time

    async def set_refresh_token(self, payload: dict[str, tp.Any]):
        sub = payload.get("sub")
        refresh_key = self.generate_refresh_key(sub)
        await self._storage.set(refresh_key, payload, ex=self._expire_time)

    async def unset_refresh_token(self, sub: str):
        refresh_key = self.generate_refresh_key(sub)
        await self._storage.delete(refresh_key)

    async def get_refresh_token_from_storage(self, sub: str) -> dict[str, tp.Any] | None:
        refresh_key = self.generate_refresh_key(sub)
        return await self._storage.get(refresh_key)

    def generate_refresh_key(self, sub: str) -> str:
        return f"{sub}:refresh"


class BlocklistRepository:
    def __init__(self, storage: BaseKeyValueStorage, *, expire_time: int | timedelta = timedelta(hours=1)):
        self._storage = storage
        self._expire_time = expire_time

    async def in_blocklist(self, token_payload: dict[str, tp.Any]) -> bool:
        key = self.generate_blocklist_key(token_payload)
        return await self._storage.get(key) is not None

    async def add_to_blocklist(self, token_payload: dict[str, tp.Any]):
        key = self.generate_blocklist_key(token_payload)
        await self._storage.set(key, token_payload, ex=self._expire_time)

    async def blocked_by_allblock(self, token_payload: dict[str, tp.Any]) -> bool:
        jti = token_payload.get("jti")
        iat = token_payload.get("iat")

        key = self.generate_allblock_key(token_payload.get("sub"))
        allblock = await self._storage.get(key)
        if allblock is None:
            return False

        exclude_jti = allblock.get("exclude")
        blocked_at = allblock.get("blocked_at")
        return (jti != exclude_jti) and (iat <= blocked_at)

    async def block_all_except_current(self, token_payload: dict):
        jti = token_payload.get("jti")
        key = self.generate_allblock_key(token_payload.get("sub"))
        now = utcnow()
        await self._storage.set(key, {"blocked_at": now, "exclude": jti})

    async def block_all(self, user_id: str):
        key = self.generate_allblock_key(user_id)
        now = utcnow()
        await self._storage.set(key, {"blocked_at": now, "exclude": None})

    def generate_allblock_key(self, sub: str) -> str:
        return f"{sub}:allblock"

    def generate_blocklist_key(self, token_payload: dict[str, tp.Any]) -> str:
        return token_payload.get("jti")


async def get_key_value_storage(redis: Redis = Depends(get_redis)) -> RedisStorage:
    return RedisStorage(redis=redis)


async def get_refresh_tokens_repository(
    storage: RedisStorage = Depends(get_key_value_storage),
) -> RefreshTokensRepository:
    return RefreshTokensRepository(storage)


async def get_blocklist_repository(
    storage: RedisStorage = Depends(get_key_value_storage),
) -> BlocklistRepository:
    return BlocklistRepository(storage)
