from typing import Protocol
from collections.abc import Iterable

from application.DTOs import ToDoInsertDTO, ToDoDeleteDTO, ToDoFindDTO, ToDoUpdateDTO
from domain import ToDoItem

class ToDoServiceProtocol(Protocol):
    async def insert(self, dto: ToDoInsertDTO) -> ToDoItem:
        ...
    async def delete(self, dto: ToDoDeleteDTO) -> None:
            ...
    async def find(self, dto: ToDoFindDTO) -> Iterable[ToDoItem]:
            ...
    async def update(self, dto: ToDoUpdateDTO) -> ToDoItem:
            ...