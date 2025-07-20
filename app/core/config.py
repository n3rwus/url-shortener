from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field
from dotenv import load_dotenv
import os

# Determine which env file to load
env_file = ".env.test" if Path(".env.test").is_file() else ".env"
load_dotenv(dotenv_path=env_file)


def _load_secret(secret_name: str, env_var: str = None) -> str:
    secret_file = Path(f"/app/secrets/{secret_name}")
    if secret_file.is_file():
        return secret_file.read_text().strip()
    if env_var:
        return os.getenv(env_var, "")
    return ""


class Settings(BaseSettings):
    USER: str = Field(default_factory=lambda: _load_secret("db_user", "USER"))
    PASSWORD: SecretStr = Field(default_factory=lambda: _load_secret("db_password", "PASSWORD"))
    HOST: str = Field(default_factory=lambda: _load_secret("db_host", "HOST"))
    PORT: int = Field(default_factory=lambda: int(_load_secret("db_port", "PORT") or 6543))
    DBNAME: str = Field(default_factory=lambda: _load_secret("db_name", "DBNAME"))
    ENV: bool = Field(default_factory=lambda: os.getenv("ENV", "development") != "production")
    BASE_URL: str = Field(default_factory=lambda: _load_secret("base_url", "BASE_URL") or "http://localhost:8000")
    REDIS_URL: str = Field(default_factory=lambda: _load_secret("redis_url", "REDIS_URL") or "redis://localhost:6379")

    model_config = SettingsConfigDict(env_file=env_file)

@lru_cache()
def get_settings():
    return Settings()
