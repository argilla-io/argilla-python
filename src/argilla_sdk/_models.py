# Copyright 2024-present, Argilla, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from typing import Literal
from enum import Enum

from pydantic import BaseModel, field_serializer

__all__ = ["DatasetModel", "WorkspaceModel", "UserModel", "Role"]


class ResourceModel(BaseModel):
    id: UUID = uuid4()
    inserted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_serializer("inserted_at", "updated_at", when_used="unless-none")
    def serialize_datetime(self, value: datetime) -> str:
        return value.isoformat()

    @field_serializer("id", when_used="unless-none")
    def serialize_id(self, value: UUID) -> str:
        return str(value.hex)


class DatasetModel(ResourceModel):
    name: str
    status: Literal["draft", "ready"] = "draft"
    allow_extra_metadata: bool = False

    workspace_id: Optional[UUID] = None
    last_activity_at: Optional[datetime] = None
    api: object = None
    url: Optional[str] = None

    @field_serializer("last_activity_at", when_used="unless-none")
    def serialize_last_activity_at(self, value: datetime) -> str:
        return value.isoformat()

    @field_serializer("workspace_id", when_used="unless-none")
    def serialize_workspace_id(self, value: UUID) -> str:
        return str(value.hex)


class Role(str, Enum):
    annotator = "annotator"
    admin = "admin"
    owner = "owner"


class UserModel(ResourceModel):
    username: str
    first_name: str
    role: str = Role.annotator

    last_name: Optional[str] = None
    password: Optional[str] = None


class WorkspaceModel(ResourceModel):
    name: str
