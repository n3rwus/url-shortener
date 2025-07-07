from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    USER: str
    PASSWORD: SecretStr
    HOST: str              # ✅ should be str, not int
    PORT: int              # ✅ port should be int
    DBNAME: str
    ENV: str = "development"
    BASE_URL: str = "http://localhost:8000"  # Default for local dev

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache()
def get_settings():
    return Settings()

