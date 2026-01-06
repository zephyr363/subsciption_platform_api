from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
ENV_DIR = BASE_DIR / "env"


class DBSettings(BaseSettings):
    host: str = "localhost"
    password: str = "admin"
    driver: str = "postgresql+asyncpg"
    port: int = 5432
    user: str = "postgres"
    name: str = "subscription_platform"
    model_config = SettingsConfigDict(env_prefix="DB_")

    @property
    def db_url(
        self,
    ) -> URL:
        return URL.create(
            drivername=self.driver,
            password=self.password,
            port=self.port,
            username=self.user,
            host=self.host,
            database=self.name,
        )


class AuthSettings(BaseSettings):
    cookie_name: str = "sessionid"
    device_id_cookie_name: str = "deviceid"
    secret_key: str = "super-secret-key"
    httponly: bool = True
    cookie_max_age: int = 60 * 60 * 24 * 7

    model_config = SettingsConfigDict(env_prefix="SESSION_")


class Settings(BaseSettings):
    debug: bool = True
    app_env: Literal["dev", "prod", "stage"] = "dev"
    db: DBSettings = DBSettings()
    auth: AuthSettings = AuthSettings()
