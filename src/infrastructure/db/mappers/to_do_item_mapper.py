from infrastructure.db.models import ToDoItemModel
from domain import ToDoItem

class ToDoItemMapper:
    @staticmethod
    def to_entity(model: ToDoItemModel) -> ToDoItem:
        return ToDoItem(
            id=model.id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(entity: ToDoItem) -> ToDoItemModel:
        return ToDoItemModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
        )