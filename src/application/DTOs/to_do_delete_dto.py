from dataclasses import dataclass
from uuid import UUID

@dataclass
class ToDoDeleteDTO:
    id: UUID