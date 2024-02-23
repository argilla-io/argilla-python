from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, field_serializer


class ResourceModel(BaseModel):
    """Base model for all resources (DatasetModel, WorkspaceModel, UserModel, etc.)"""

    id: UUID = uuid4()
    inserted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_serializer("inserted_at", "updated_at", when_used="unless-none")
    def serialize_datetime(self, value: datetime) -> str:
        return value.isoformat()

    @field_serializer("id", when_used="unless-none")
    def serialize_id(self, value: UUID) -> str:
        return str(value.hex)

    def __hash__(self) -> int:
        return hash(self.model_dump_json())
