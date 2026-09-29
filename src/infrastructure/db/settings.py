from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

class DbSettings(BaseSettings):
    db_user: str = Field(min_length=1)
    db_password: SecretStr = Field(min_length=8)
    db_name: str = Field(min_length=1)
    db_host: str = Field(default="localhost", min_length=1)
    db_port: int = Field(ge=1, le=65535)
    db_echo: bool = False
    db_pool_size: int = 5
    db_max_overflow: int = 5
    db_pool_timeout: float = 30.0
    db_pool_pre_ping: bool = True
    db_pool_recycle: int = 3600

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def asyncpg_database_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_password.get_secret_value(),
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )
