from functools import wraps
from typing import AsyncIterable, Callable

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base

from src.core.app_settings import app_settings

# Создаём базовый класс для будущих моделей
Base = declarative_base()

postgres_url = URL.create(
    drivername="postgresql+asyncpg",
    username=app_settings.POSTGRES_USER,
    password=app_settings.POSTGRES_PASS,
    host=app_settings.POSTGRES_HOST,
    port=app_settings.POSTGRES_PORT,
    database=app_settings.POSTGRES_NAME,
)

# Создаём движок
# Настройки подключения к БД передаём из переменных окружения, которые заранее загружены в файл настроек
engine = create_async_engine(postgres_url, echo=False, future=True)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, future=True)


async def get_session() -> AsyncIterable[AsyncSession]:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()


def db_session(func: Callable) -> Callable:
    """Decorator to inject a session into a function."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        async for session in get_session():
            try:
                res = await func(db=session, *args, **kwargs)
                return res
            finally:
                await session.close()

    return wrapper


async def start_engine() -> None:
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("All tables created successfully.")
    except Exception as e:
        print(f"Error during table creation: {e}")
        raise


async def stop_engine() -> None:
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print("Disposing of the database engine...")
        await engine.dispose()
        print("Database engine disposed successfully.")
    except Exception as e:
        print(f"Error during database shutdown: {e}")
        raise
