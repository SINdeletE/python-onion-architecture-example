from fastapi import Depends, Request, FastAPI
from typing import Annotated, AsyncIterator, cast
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from infrastructure.db.settings import DbSettings
from infrastructure.db.session import get_session_factory, create_engine
from infrastructure.db.di import get_db_settings, get_to_do_repository

from application.interfaces import ToDoRepositoryProtocol, ToDoServiceProtocol
from application.di import get_to_do_service

# Infrastructure
DbSettingsDep = Annotated[DbSettings, Depends(get_db_settings)]
ToDoRepositoryDep = Annotated[ToDoRepositoryProtocol, Depends(get_to_do_repository)]

# Application
ToDoServiceDep = Annotated[ToDoServiceProtocol, Depends(get_to_do_service)]

# Engine / Session

@asynccontextmanager
async def database_lifespan(app: FastAPI) -> AsyncIterator[None]:
    engine = create_engine(get_db_settings())
    app.state.db_engine = engine
    app.state.db_session_factory = get_session_factory(engine)

    try:
        yield
    finally:
        await engine.dispose()

async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    try:
        session_factory = cast(
            async_sessionmaker[AsyncSession],
            request.app.state.db_session_factory,
        )
    except AttributeError as error:
        raise RuntimeError(
            "database_lifespan must be configured on the FastAPI application"
        ) from error

    async with session_factory() as session:
        yield session

AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]
