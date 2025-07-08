import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from dotenv import load_dotenv


# Determine which env file to load
env_file = ".env.test" if Path(".env.test").is_file() else ".env"
load_dotenv(dotenv_path=env_file)


class Settings(BaseSettings):
    USER: str
    PASSWORD: SecretStr
    HOST: str
    PORT: int
    DBNAME: str
    ENV: str = "development"
    BASE_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(env_file=env_file)


@lru_cache()
def get_settings():
    return Settings()
