from datetime import datetime, timedelta, timezone


def utcnow() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp())


def to_seconds(dt: int | timedelta) -> int:
    if isinstance(dt, int):
        return dt
    if isinstance(dt, timedelta):
        return int(dt.total_seconds())
    raise TypeError("Supported types for dt are int and timedelta")
