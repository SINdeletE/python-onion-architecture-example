from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class ToDoUpdateDTO:
    id: UUID
    name: str
    description: str