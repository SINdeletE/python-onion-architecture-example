from infrastructure.db.models import Base
from uuid import UUID
from datetime import datetime
from sqlalchemy import Uuid, DateTime, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class ToDoItemModel(Base):
    __tablename__ = "to_do_item"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
