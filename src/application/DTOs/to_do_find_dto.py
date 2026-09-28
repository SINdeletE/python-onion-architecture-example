from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class ToDoFindDTO:
    id: UUID | None
    name: str | None
    description: str | None
    created_at: datetime | None