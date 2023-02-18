import re
from urllib.parse import urlparse


def camel_to_snake(name) -> str:
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def get_hostname(url: str) -> str:
    return urlparse(url).netloc
