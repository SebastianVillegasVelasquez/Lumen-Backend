from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    This class is used to store the application settings.
    Settings are loaded from the .env file.
    If another file is needed, it can be added here.
    To add a new setting, add it to the .env file, and it will be automatically loaded
    declaring it here.
    """

    DATABASE_URL: str

    # configuration for pydantic_settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # This will ignore any extra variables in the .env file
        # are not declared in the class attributes
    )


settings = Settings()
