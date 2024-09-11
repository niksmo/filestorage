from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core import app_settings


async_engine = create_async_engine(app_settings.db_dsn, echo=True)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
