import typing as tp
from json import JSONEncoder

import jwt
import orjson

from api.services.jwt.exc import TokenDecodeError


class OrjsonEncoder(JSONEncoder):
    def encode(self, o: tp.Any) -> str:
        return orjson.dumps(o).decode()  # pylint: disable=no-member


class JwtTokenEncoderMixin:
    def encode_token(self, payload: dict[str, tp.Any], key: str | bytes) -> str:
        return jwt.encode(payload, key, json_encoder=OrjsonEncoder)


class JwtTokenDecoderMixin:
    def decode_token(self, token: str, key: str | bytes, algorithms: list[str] | None = None) -> dict[str, tp.Any]:
        try:
            return jwt.decode(token, key, algorithms=algorithms)
        except jwt.exceptions.PyJWTError as e:
            raise TokenDecodeError(str(e)) from e
