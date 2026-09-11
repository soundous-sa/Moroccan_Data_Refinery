from dotenv import load_dotenv
import os

load_dotenv()

class Settings:

    APP_NAME = os.getenv("APP_NAME")

    APP_VERSION = os.getenv("APP_VERSION")

    ENVIRONMENT = os.getenv("ENVIRONMENT")

    DB_HOST = os.getenv("DB_HOST")

    DB_PORT = os.getenv("DB_PORT")

    DB_NAME = os.getenv("DB_NAME")

    DB_USER = os.getenv("DB_USER")

    DB_PASSWORD = os.getenv("DB_PASSWORD")

    LOG_LEVEL = os.getenv("LOG_LEVEL")


settings = Settings()