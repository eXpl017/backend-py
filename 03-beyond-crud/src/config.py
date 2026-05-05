from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_ALGORITHM: str
    JWT_SECRET: str
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )


config = Settings()
