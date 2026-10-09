from fastapi import APIRouter, Query, Path, Body

from typing import Annotated
from datetime import datetime
from uuid import UUID

from .di import ToDoServiceDep

from domain import ToDoItem
from application.DTOs import ToDoDeleteDTO, ToDoFindDTO, ToDoInsertDTO, ToDoUpdateDTO
from api.rest.v1.schemas import ToDoAPIItem

v1_router = APIRouter(prefix="/todoitems")

@v1_router.get("/", tags=["todoitems"], response_model=list[ToDoItem])
async def get_to_do_items(service: ToDoServiceDep,
                    id: Annotated[UUID | None, Query()] = None,
                    name: Annotated[str | None, Query(max_length=256)] = None,
                    description: Annotated[str | None, Query(max_length=512)] = None,
                    created_at: Annotated[datetime | None, Query()] = None):
    result = await service.find(ToDoFindDTO(id=id, name=name, description=description, created_at=created_at))
    
    return [ToDoAPIItem.create(entity) for entity in result]

@v1_router.delete("/{id}", tags=["todoitems"])
async def delete_to_do_items(service: ToDoServiceDep,
                        id: Annotated[UUID, Path()]):
    await service.delete(ToDoDeleteDTO(id))

@v1_router.put("/{id}", tags=["todoitems"], response_model=ToDoItem)
async def put_to_do_items(service: ToDoServiceDep,
                    id: Annotated[UUID, Path()],
                    name: Annotated[str, Body(max_length=256)],
                    description: Annotated[str, Body(max_length=512)]):
    result = await service.update(ToDoUpdateDTO(id=id, name=name, description=description))
    
    return ToDoAPIItem.create(result)

@v1_router.post("/", tags=["todoitems"], response_model=ToDoItem, status_code=201)
async def post_to_do_items(service: ToDoServiceDep,
                    name: Annotated[str, Body(max_length=256)],
                    description: Annotated[str, Body(max_length=512)]):
    result = await service.insert(ToDoInsertDTO(name=name, description=description))

    return ToDoAPIItem.create(result)
