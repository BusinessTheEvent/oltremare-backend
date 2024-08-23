import os
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from .default_logger import get_custom_logger
from dotenv import dotenv_values

logger = get_custom_logger(__name__)

working_directory = os.getcwd()

config = {
    **dotenv_values(os.path.join(working_directory, ".env")),  # load shared development variables
    # **dotenv_values(".env.secret"),  # load sensitive variables
    # **os.environ,  # override loaded values with environment variables
}


logger.info("Loading environment variables from .env file.")

# Pydantic settings for environmental variables
class Settings(BaseSettings):

    # Databases
    SQLALCHEMY_DATABASE_HOST: str = ""
    SQLALCHEMY_DATABASE_USER: str = ""
    SQLALCHEMY_DATABASE_PASSWORD: str = ""
    SQLALCHEMY_DATABASE_DRIVER: str = ""
    SQLALCHEMY_DATABASE_NAME: str = ""
    SQLALCHEMY_DATABASE_PORT: str = ""

    # Auth db start options
    AUTH_DATABASE_CHECK: bool = False
    AUTH_DATABASE_PURGE: bool = False
    AUTH_DATABASE_INIT_TABLES: bool = True

    # Other options
    USE_COOKIES_AUTH: bool = False

    # Files
    FILEPATH_ROOT: str = "default"

    # Services
    PIPELINES_URL: str = "http://localhost:8001"

    # Security
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = '9173012271586b4215e17fa9b9ded4d1eec420e4207e95adbc46e0c652c8377e'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 720 # 12 hours
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 30 ## for testing purposes only
    ACCESS_TOKEN_EXPIRE_NOW: int = 5 # (seconds)

    # SMTP
    SMTP_HOST: str = ""
    SMTP_PORT: int = None
    SMTP_SENDER_EMAIL: str = ""
    SMTP_PASSWORD: str = ""


    # Licenses
    USE_LICENSES: bool = False
    USE_VALIDATION_SCHEMA: bool = True
    LICENSE_HASH_ALGORITHM: str = "sha256"

    # MISC
    DEBUG: bool = False
    TESTING: bool = False
    APP_VERSION: str = None

    # allow_origins cannot be set to ['*'] for credentials to be allowed, origins must be specified.
    ORIGINS: List[str] = [
        "http://localhost:4321",
        "http://127.0.0.1:8000"
    ]
    METHODS: List[str] = [
        "GET",
        "POST",
        "DELETE",
        "OPTIONS"
    ]
    HEADERS: List[str] = [
        "Access-Control-Allow-Headers",
        'Content-Type',
        'Authorization',
        'Access-Control-Allow-Origin'
    ]

    model_config = SettingsConfigDict()


settings = Settings(**config)
logger.info("Succesfully loaded environment variables from .env file.")
