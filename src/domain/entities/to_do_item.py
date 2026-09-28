from dataclasses import dataclass
from uuid import UUID, uuid7
from datetime import datetime

@dataclass
class ToDoItem:
    id: UUID
    name: str
    description: str
    created_at: datetime

    @classmethod
    def create(cls, name: str, description: str) -> ToDoItem:
        return cls(id=uuid7(), name=name, description=description.strip(), created_at=datetime.now())