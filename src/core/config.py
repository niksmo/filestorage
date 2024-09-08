from logging.config import dictConfig as logging_config
from pathlib import Path
from typing import Optional

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import logger_config


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8')
    app_title: str = 'FileStorage'
    pguser: str = 'stub'
    postgres_password: str = 'stub'
    postgres_db: str = 'stub'
    db_host: str = 'stub'
    db_port: int = 8001
    db_dsn: Optional[PostgresDsn] = None
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    secret_key: str = 'stub'
    jwt_algorithm: str = 'stub'
    jwt_expires: int = 1000
    media_root: Path = Path(__file__).parents[2] / 'media'


logging_config(logger_config)

app_settings = AppSettings()
app_settings.media_root
