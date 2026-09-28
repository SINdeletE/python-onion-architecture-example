from dataclasses import dataclass

@dataclass
class ToDoInsertDTO:
    name: str
    description: str