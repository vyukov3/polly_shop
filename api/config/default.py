from os import environ

from pydantic import BaseSettings


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    """

    ENV: str = environ.get("ENV", "local")
    PATH_PREFIX: str = environ.get("PATH_PREFIX", "/api/v1")
    APP_HOST: str = environ.get("APP_HOST", "http://127.0.0.1")
    APP_PORT: int = int(environ.get("APP_PORT", 8000))

    POSTGRES_DB: str = environ.get("POSTGRES_DB", "polly_shop_db")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = environ.get("POSTGRES_USER", "user")
    POSTGRES_PORT: int = int(environ.get("POSTGRES_PORT", "5432")[-4:])
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "hackme")
    DB_CONNECT_RETRY: int = environ.get("DB_CONNECT_RETRY", 20)
    DB_POOL_SIZE: int = environ.get("DB_POOL_SIZE", 15)

    MAIL_USERNAME: str = environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD: str = environ.get("MAIL_PASSWORD", "")
    MAIL_FROM: str = environ.get("MAIL_FROM", "")
    MAIL_PORT: int = int(environ.get("MAIL_PORT", "465"))
    MAIL_SERVER: str = environ.get("MAIL_SERVER", "smtp.yandex.ru")
    MAIL_STARTTLS: bool = environ.get("MAIL_STARTTLS", False)
    MAIL_SSL_TLS: bool = environ.get("MAIL_SSL_TLS", True)
    USE_CREDENTIALS: bool = environ.get("USE_CREDENTIALS", True)

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def email_config(self) -> dict:
        """
        Get all settings for connect to Email server
        """
        return {
            "MAIL_USERNAME": self.MAIL_USERNAME,
            "MAIL_PASSWORD": self.MAIL_PASSWORD,
            "MAIL_FROM": self.MAIL_FROM,
            "MAIL_PORT": self.MAIL_PORT,
            "MAIL_SERVER": self.MAIL_SERVER,
            "MAIL_STARTTLS": self.MAIL_STARTTLS,
            "MAIL_SSL_TLS": self.MAIL_SSL_TLS,
            "USE_CREDENTIALS": self.USE_CREDENTIALS,
        }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
