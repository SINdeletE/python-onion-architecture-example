from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from infrastructure.db.settings import DbSettings

def create_engine(settings: DbSettings) -> AsyncEngine:
    return create_async_engine(
        url=settings.asyncpg_database_url,
        echo=settings.db_echo,
        pool_size = settings.db_pool_size,
        max_overflow = settings.db_max_overflow,
        pool_timeout = settings.db_pool_timeout,
        pool_pre_ping=settings.db_pool_pre_ping,
        pool_recycle=settings.db_pool_recycle,
        connect_args={})

def get_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False
    )
