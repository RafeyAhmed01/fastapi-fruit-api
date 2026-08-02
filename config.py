from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Default API NAME"
    database_url: str
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()