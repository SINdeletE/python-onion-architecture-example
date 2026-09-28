from typing import Protocol
from uuid import UUID
from datetime import datetime
from collections.abc import Iterable

from domain import ToDoItem

class ToDoRepositoryProtocol(Protocol):
    async def insert(self, entity: ToDoItem) -> ToDoItem:
        ...
    async def delete(self, id: UUID):
        ...
    async def find(self, id: UUID | None, 
                        name: str | None, 
                        description: str | None, 
                        created_at: datetime | None) -> Iterable[ToDoItem]:
        ...
    async def get_by_id(self, id: UUID) -> ToDoItem:
        ...
    async def update(self, entity: ToDoItem) -> ToDoItem:
        ...