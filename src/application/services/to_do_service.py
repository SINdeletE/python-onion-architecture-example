from collections.abc import Iterable

from application.interfaces import ToDoRepositoryProtocol
from application.DTOs import ToDoInsertDTO, ToDoDeleteDTO, ToDoFindDTO, ToDoUpdateDTO
from domain import ToDoItem

class ToDoService:
    def __init__(self, repo: ToDoRepositoryProtocol) -> None:
          super().__init__()

          self.repo = repo

    async def insert(self, dto: ToDoInsertDTO) -> ToDoItem:
        return await self.repo.insert(ToDoItem.create(dto.name, dto.description))
    async def delete(self, dto: ToDoDeleteDTO) -> None:
        await self.repo.delete(dto.id)
    async def find(self, dto: ToDoFindDTO) -> Iterable[ToDoItem]:
        return await self.repo.find(dto.id, dto.name, dto.description, dto.created_at)
    async def update(self, dto: ToDoUpdateDTO) -> ToDoItem:
        item = await self.repo.get_by_id(dto.id)

        item.name = dto.name
        item.description = dto.description

        return await self.repo.update(item)