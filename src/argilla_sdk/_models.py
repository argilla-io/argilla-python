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

from pydantic import BaseModel

__all__ = ["DatasetModel", "WorkspaceModel", "UserModel", "Role"]


class DatasetModel(BaseModel):
    name: str
    status: Literal["draft", "ready"] = "draft"
    allow_extra_metadata: bool = True
    id: UUID = uuid4()

    guidelines: Optional[str] = None
    workspace_id: Optional[UUID] = None
    inserted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_activity_at: Optional[datetime] = None
    api: object = None


class Role(str, Enum):
    annotator = "annotator"
    admin = "admin"
    owner = "owner"


class UserModel(BaseModel):
    username: str
    first_name: str
    role: str = Role.annotator
    
    id: UUID = uuid4()
    last_name: Optional[str] = None
    password: Optional[str] = None
    inserted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class WorkspaceModel(BaseModel):
    name: str
    id: UUID = uuid4()
    inserted_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
