
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.settings import DbSettings
from application.interfaces import ToDoRepositoryProtocol
from infrastructure.db import ToDoRepository
from infrastructure.db.mappers import ToDoItemMapper

def get_to_do_repository(session: AsyncSession, mapper: ToDoItemMapper) -> ToDoRepositoryProtocol:
    return ToDoRepository(session=session, mapper=mapper)

@lru_cache(maxsize=1)
def get_db_settings() -> DbSettings:
    return DbSettings() # type: ignore
