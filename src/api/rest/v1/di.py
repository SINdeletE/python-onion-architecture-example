from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated, cast

from fastapi import Depends, FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.di import get_to_do_service
from application.interfaces import ToDoRepositoryProtocol, ToDoServiceProtocol
from infrastructure.db.di import get_db_settings, get_to_do_repository
from infrastructure.db.mappers import ToDoItemMapper
from infrastructure.db.session import create_engine, get_session_factory


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

    async with session_factory.begin() as session:
        yield session


AsyncSessionDep = Annotated[
    AsyncSession,
    Depends(get_session, scope="function"),
]


async def provide_to_do_repository(session: AsyncSessionDep) -> ToDoRepositoryProtocol:
    return get_to_do_repository(session=session, mapper=ToDoItemMapper())


ToDoRepositoryDep = Annotated[
    ToDoRepositoryProtocol,
    Depends(provide_to_do_repository),
]


async def provide_to_do_service(repo: ToDoRepositoryDep) -> ToDoServiceProtocol:
    return get_to_do_service(repo=repo)


ToDoServiceDep = Annotated[ToDoServiceProtocol, Depends(provide_to_do_service)]
