from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import (
    DataError,
    DBAPIError,
    IntegrityError,
    OperationalError,
    SQLAlchemyError,
    TimeoutError as SQLAlchemyTimeoutError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from domain import ToDoItem
from infrastructure.db.mappers import ToDoItemMapper
from infrastructure.db.models import ToDoItemModel
from application.exception import (
    ApplicationError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    ServiceUnavailableError,
    UnprocessableEntityError,
)


def _translate_database_error(exc: SQLAlchemyError | OSError) -> ApplicationError:
    if isinstance(exc, DBAPIError):
        sqlstate = (
            getattr(exc.orig, "sqlstate", None)
            or getattr(exc.orig, "pgcode", None)
            or ""
        )

        if isinstance(exc, IntegrityError):
            if sqlstate == "23505":
                return ConflictError("A task with these unique values already exists.")
            if sqlstate in {"23503", "23P01"}:
                return ConflictError("The operation conflicts with related or existing data.")
            if sqlstate in {"23502", "23514"}:
                return UnprocessableEntityError("Task data violates a required constraint.")

        if isinstance(exc, DataError) or sqlstate.startswith("22"):
            return UnprocessableEntityError("Task data has an invalid value or format.")

        if sqlstate in {"40001", "40P01"}:
            return ConflictError("The operation conflicts with a concurrent transaction.")

        if (
            exc.connection_invalidated
            or sqlstate.startswith("08")
            or sqlstate in {"53300", "57P01", "57P02", "57P03"}
        ):
            return ServiceUnavailableError("The database is temporarily unavailable.")

    if isinstance(exc, (OperationalError, SQLAlchemyTimeoutError, OSError)):
        return ServiceUnavailableError("The database is temporarily unavailable.")

    return InternalServerError("The database operation could not be completed.")


@dataclass(slots=True)
class ToDoRepository:
    session: AsyncSession
    mapper: ToDoItemMapper

    async def insert(self, entity: ToDoItem) -> ToDoItem:
        try:
            self.session.add(self.mapper.to_model(entity))
            await self.session.flush()

            return entity
        except (SQLAlchemyError, OSError) as exc:
            raise _translate_database_error(exc) from exc

    async def delete(self, id: UUID) -> None:
        try:
            item = await self.session.get(ToDoItemModel, id)
            if item is None:
                raise NotFoundError(f"Task {id} was not found.")

            await self.session.delete(item)
            await self.session.flush()
        except (SQLAlchemyError, OSError) as exc:
            raise _translate_database_error(exc) from exc

    async def find(
        self,
        id: UUID | None,
        name: str | None,
        description: str | None,
        created_at: datetime | None,
    ) -> Iterable[ToDoItem]:
        try:
            query = select(ToDoItemModel)
            if id is not None:
                query = query.where(ToDoItemModel.id == id)

            if name is not None:
                query = query.where(ToDoItemModel.name == name)

            if description is not None:
                query = query.where(ToDoItemModel.description == description)

            if created_at is not None:
                query = query.where(ToDoItemModel.created_at == created_at)

            result = await self.session.scalars(query)
            return [self.mapper.to_entity(model) for model in result]
        except (SQLAlchemyError, OSError) as exc:
            raise _translate_database_error(exc) from exc

    async def get_by_id(self, id: UUID) -> ToDoItem:
        try:
            item = await self.session.get(ToDoItemModel, id)
            if item is None:
                raise NotFoundError(f"Task {id} was not found.")

            return self.mapper.to_entity(item)
        except (SQLAlchemyError, OSError) as exc:
            raise _translate_database_error(exc) from exc

    async def update(self, entity: ToDoItem) -> ToDoItem:
        try:
            query = (
                update(ToDoItemModel)
                .where(ToDoItemModel.id == entity.id)
                .values(name=entity.name, description=entity.description)
                .returning(ToDoItemModel)
            )
            item = await self.session.scalar(query)

            if item is None:
                raise NotFoundError(f"Task {entity.id} was not found.")

            return self.mapper.to_entity(item)
        except (SQLAlchemyError, OSError) as exc:
            raise _translate_database_error(exc) from exc
