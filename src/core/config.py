from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import getLogger
from logging.config import dictConfig as logging_config
from pathlib import Path

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio import from_url as aioredis_from_url

from utils.constants import COMMON_LOGGER, MEDIA_ROOT_NAME
from .logger import logger_config

logger = getLogger(COMMON_LOGGER)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      extra='ignore')
    app_title: str = 'FileStorage'
    secret_key: str = 'stub'
    jwt_algorithm: str = 'stub'
    jwt_expires: int = 1000
    media_root: Path = Path(__file__).parents[2] / MEDIA_ROOT_NAME
    db_dsn: str = 'stub'
    cache_dsn: str = 'stub'
    media_url: str = 'http://127.0.0.1:3000/media/'

    @asynccontextmanager
    async def app_lifespan(self, _: FastAPI) -> AsyncGenerator:
        redis_conn = aioredis_from_url(self.cache_dsn)
        FastAPICache.init(RedisBackend(redis_conn))
        yield
        await redis_conn.close()


logging_config(logger_config)

app_settings = AppSettings()

if not app_settings.media_root.exists():
    app_settings.media_root.mkdir()
    logger.info(f'Create media path: {app_settings.media_root}')
