from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from domain import ToDoItem

@dataclass
class ToDoAPIItem:
    id: UUID
    name: str
    description: str
    created_at: datetime

    @classmethod
    def create(cls, entity: ToDoItem) -> ToDoAPIItem:
        return cls(id=entity.id, name=entity.name, description=entity.description, created_at=entity.created_at)