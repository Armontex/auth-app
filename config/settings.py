from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    secret_key: SecretStr
    
    redis_url: str
    postgres_url: str
    
    debug: bool


settings = Settings()  # type: ignore
