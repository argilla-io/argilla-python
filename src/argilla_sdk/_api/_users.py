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

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

import httpx

import argilla_sdk
from argilla_sdk._api import _http

__all__ = ["Role", "User"]


class Role(str, Enum):
    annotator = "annotator"
    admin = "admin"
    owner = "owner"


@dataclass
class User:
    username: str
    first_name: str
    role: Role = Role.annotator
    last_name: Optional[str] = None
    password: Optional[str] = None

    id: Optional[UUID] = None
    api_key: Optional[str] = None
    inserted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    client: Optional[httpx.Client] = field(default=None, repr=False, compare=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "api_key": self.api_key,
            "inserted_at": self.inserted_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        role = data.get("role")
        if role is not None:
            data["role"] = Role(role)

        return cls(**data)

    @classmethod
    def list(cls) -> List["User"]:
        client = argilla_sdk.get_default_http_client()

        response = client.get("/api/users")
        _http.raise_for_status(response)

        return [cls._create_from_json(user_json, client) for user_json in response.json()]

    @classmethod
    def list_by_workspace_id(cls, workspace_id: UUID) -> List["User"]:
        client = argilla_sdk.get_default_http_client()

        response = client.get(f"/api/workspaces/{workspace_id}/users")
        _http.raise_for_status(response)

        return [cls._create_from_json(user_json, client) for user_json in response.json()]

    @classmethod
    def get_me(cls):
        client = argilla_sdk.get_default_http_client()

        response = client.get("/api/me")
        _http.raise_for_status(response)

        return cls._create_from_json(response.json(), client)

    def create(self) -> "User":
        response = self.client.post(
            "/api/users",
            json={
                "username": self.username,
                "password": self.password,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "role": self.role,
            },
        )
        _http.raise_for_status(response)

        return self._update_from_api_response(response)

    def add_to_workspace(self, workspace_id: UUID) -> "User":
        response = self.client.post(f"/api/workspaces/{workspace_id}/users/{self.id}")
        _http.raise_for_status(response)

        return self._update_from_api_response(response)

    def delete_from_workspace(self, workspace_id: UUID) -> "User":
        response = self.client.delete(f"/api/workspaces/{workspace_id}/users/{self.id}")
        _http.raise_for_status(response)

        return self._update_from_api_response(response)

    def delete(self) -> "User":
        response = self.client.delete(f"/api/users/{self.id}")
        _http.raise_for_status(response)

        return self._update_from_api_response(response)

    @classmethod
    def _create_from_json(cls, json: dict, client: httpx.Client) -> "User":
        return cls.from_dict(dict(**json, client=client))

    def _update_from_api_response(self, response: httpx.Response) -> "User":
        new_instance = self.from_dict(dict(**response.json(), client=self.client))
        self.__dict__.update(new_instance.__dict__)

        return self
