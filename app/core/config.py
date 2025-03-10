import os
from dotenv import load_dotenv
from pydantic import SecretStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings
from pydantic.networks import AnyHttpUrl

load_dotenv()

class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION")

    # API
    API_PREFIX: str = os.getenv("API_PREFIX")

    # Secrets
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")

    # Server
    SERVER_HOST: str = os.getenv("SERVER_HOST")
    SERVER_PORT: int = os.getenv("SERVER_PORT")
    DEBUG: bool = os.getenv("DEBUG")

    # CORS
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = os.getenv("PROJECT_NAME")

    # Email
    SMTP_TLS: bool = os.getenv("SMTP_TLS")
    SMTP_PORT: int = os.getenv("SMTP_PORT")
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASSWORD: SecretStr = os.getenv("SMTP_PASSWORD")
    EMAILS_FROM_EMAIL: str = os.getenv("EMAILS_FROM_EMAIL")
    EMAILS_FROM_NAME: str = os.getenv("EMAILS_FROM_NAME")

    # Database
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: SecretStr = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")

    # Database async connection string
    DATABASE_URL: str = None

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v, info: FieldValidationInfo) -> str:
        if isinstance(v, str):
            return v
        user = info.data.get("DB_USER")
        password = info.data.get("DB_PASSWORD")
        if isinstance(password, SecretStr):
            password = password.get_secret_value()
        host = info.data.get("DB_HOST")
        port = info.data.get("DB_PORT")
        db_name = info.data.get("DB_NAME")
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"

settings = Settings()
