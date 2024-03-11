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
from enum import Enum
from pydantic import field_validator

from argilla_sdk._models import ResourceModel

__all__ = ["UserModel", "Role"]


class Role(str, Enum):
    annotator = "annotator"
    admin = "admin"
    owner = "owner"


class UserModel(ResourceModel):
    username: str
    role: str = Role.annotator

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None

    @field_validator("first_name")
    def __validate_first_name(cls, v, values):
        """Set first_name to username if not provided"""
        return v or values["username"]

    @field_validator("username", mode="before")
    def __validate_username(cls, username):
        """Ensure that the username is not empty"""
        if not username:
            raise ValueError("Username cannot be empty")
        return username
