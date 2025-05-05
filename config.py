from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    DB_NAME: str = "default"
    DB_USER: str = "default"
    DB_PASSWORD: str = "default"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    ALLOWED_CONTENT_TYPES: List[str]=['image/png','image/webp']
    ALLOWED_EXTENSIONS: List[str]=['jpg']
    MAX_FILE_SIZE:int=2097152
    model_config=SettingsConfigDict(env_file=".env")

settings= Settings()