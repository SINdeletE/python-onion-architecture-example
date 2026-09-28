from fastapi import APIRouter, Query, Path, Body, Depends

from typing import Annotated, Iterable
from datetime import datetime
from uuid import UUID

from di import ToDoServiceDep

from domain import ToDoItem
from application.DTOs import *

v1_router = APIRouter(prefix="/todoitems")

@v1_router.get("/", tags=["todoitems"], response_model=Iterable[ToDoItem])
async def get_to_do_items(service: ToDoServiceDep,
                    id: Annotated[UUID | None, Query()] = None,
                    name: Annotated[str | None, Query(max_length=256)] = None,
                    description: Annotated[str | None, Query(max_length=512)] = None,
                    created_at: Annotated[datetime | None, Query()] = None):
    return await service.find(ToDoFindDTO(id=id, name=name, description=description, created_at=created_at))

@v1_router.delete("/{id}", tags=["todoitems"], response_model=None)
async def delete_to_do_items(service: ToDoServiceDep,
                        id: Annotated[UUID, Path()]):
    await service.delete(ToDoDeleteDTO(id))

@v1_router.put("/{id}", tags=["todoitems"], response_model=ToDoItem)
async def put_to_do_items(service: ToDoServiceDep,
                    id: Annotated[UUID, Path()],
                    name: Annotated[str, Body(max_length=256)],
                    description: Annotated[str, Body(max_length=512)]):
    return await service.update(ToDoUpdateDTO(id=id, name=name, description=description))

@v1_router.delete("/{id}", tags=["todoitems"], response_model=ToDoItem)
async def post_to_do_items(service: ToDoServiceDep,
                    name: Annotated[str, Body(max_length=256)],
                    description: Annotated[str, Body(max_length=512)]):
    return await service.insert(ToDoInsertDTO(name=name, description=description))
