from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
