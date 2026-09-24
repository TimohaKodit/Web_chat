from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str = Field(min_length=3)

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()