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
from typing import List, Optional
from uuid import UUID

import httpx

import argilla_sdk
from argilla_sdk import _helpers
from argilla_sdk._api import _http

__all__ = ["Workspace"]


@dataclass
class Workspace:
    name: str

    id: Optional[UUID] = None
    inserted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    client: Optional[httpx.Client] = field(default=None, repr=False, compare=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "inserted_at": self.inserted_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Workspace":
        return _helpers.dataclass_instance_from_dict(cls, data)

    @classmethod
    def list(cls) -> List["Workspace"]:
        client = argilla_sdk.get_default_http_client()

        response = client.get("/api/v1/me/workspaces")
        _http.raise_for_status(response)

        response_json = response.json()
        return [cls._create_from_json(client, json_workspace) for json_workspace in response_json["items"]]

    @classmethod
    def get(cls, workspace_id: UUID) -> "Workspace":
        client = argilla_sdk.get_default_http_client()

        response = client.get(f"/api/v1/workspaces/{workspace_id}")
        _http.raise_for_status(response)

        return cls._create_from_json(client, response.json())

    @classmethod
    def get_by_name(cls, name: str) -> Optional["Workspace"]:
        for workspace in cls.list():
            if workspace.name == name:
                return workspace
        return None

    def create(self) -> "Workspace":
        self.client = argilla_sdk.get_default_http_client()

        # TODO: Unify API endpoint
        response = self.client.post("/api/workspaces", json={"name": self.name})
        _http.raise_for_status(response)

        return self._update_from_api_response(response)

    def delete(self) -> "Workspace":
        self.client = argilla_sdk.get_default_http_client()

        response = self.client.delete(f"/api/v1/workspaces/{self.id}")
        _http.raise_for_status(response)

        return self._update_from_api_response(response)

    @classmethod
    def _create_from_json(cls, client, json):
        return cls.from_dict(dict(**json, client=client))

    def _update_from_api_response(self, response: httpx.Response) -> "Workspace":
        new_instance = self.from_dict(dict(**response.json(), client=self.client))
        self.__dict__.update(new_instance.__dict__)

        return self
