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

from enum import Enum
from typing import Optional

from pydantic import field_validator

from argilla_sdk._models import ResourceModel

__all__ = ["UserModel", "Role"]


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

    @field_validator("first_name")
    def validate_first_name(cls, value: str, values) -> str:
        """Set first name to user name if not provided."""
        return value or values.data["username"]
