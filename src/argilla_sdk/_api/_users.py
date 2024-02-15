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

from typing import List
from uuid import UUID

import httpx

from argilla_sdk._api import _http
from argilla_sdk._api._base import ResourceBase
from argilla_sdk.users import User

__all__ = ["UsersAPI"]


class UsersAPI(ResourceBase):
    """Manage users via the API"""

    ################
    # CRUD methods #
    ################

    def create(self, user) -> None:
        json_body = {
            "username": user.username,
            "password": user.password,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
        }
        response = self.http_client.post(
            "/api/users",
            json=json_body,
        )
        _http.raise_for_status(response)
        self.log(f"Created user {user.username}")

    def get(self, id: UUID) -> User:
        response = self.http_client.get(f"/api/users/{id}")
        _http.raise_for_status(response)
        response_json = response.json()
        user = self._model_from_json(response_json)
        self.log(f"Got user {user.username}")
        return user

    def update(self, user: User) -> None:
        raise NotImplementedError("Updating users is not supported")

    def delete(self, id: UUID) -> None:
        response = self.http_client.delete(f"/api/users/{id}")
        _http.raise_for_status(response)
        self.log(f"Deleted user {id}")

    ####################
    # Utility methods #
    ####################

    def list(self) -> List["User"]:
        response = self.http_client.get("/api/users")
        _http.raise_for_status(response)
        response_json = response.json()
        users = self._model_from_jsons(response_json)
        self.log(f"Listed {len(users)} users")
        return users

    def list_by_workspace_id(self, workspace_id: UUID) -> List["User"]:
        response = self.http_client.get(f"/api/workspaces/{workspace_id}/users")
        _http.raise_for_status(response)
        response_json = response.json()["items"]
        users = self._model_from_jsons(response_json)
        self.log(f"Listed {len(users)} users")
        return users

    def get_me(self):
        response = self.http_client.get("/api/me")
        _http.raise_for_status(response)
        user = self._model_from_json(response.json())
        self.log(f"Got user {user.username}")
        return user

    def add_to_workspace(self, workspace_id: UUID, user_id: UUID) -> None:
        response = self.http_client.post(f"/api/workspaces/{workspace_id}/users/{user_id}")
        _http.raise_for_status(response)
        self.log(f"Added user {user_id} to workspace {workspace_id}")

    def delete_from_workspace(self, workspace_id: UUID, user_id: UUID) -> None:
        response = self.http_client.delete(f"/api/workspaces/{workspace_id}/users/{user_id}")
        _http.raise_for_status(response)
        self.log(f"Deleted user {user_id} from workspace {workspace_id}")

    def get_me(self):
        response = self.http_client.get("/api/me")
        _http.raise_for_status(response)
        user = self._model_from_json(response.json())
        self.log(f"Got user {user.username}")
        return user

    ####################
    # Private methods #
    ####################

    def _model_from_json(self, json_user) -> User:
        return User(
            id=json_user["id"],
            username=json_user["username"],
            first_name=json_user["first_name"],
            last_name=json_user["last_name"],
            role=json_user["role"],
            inserted_at=self._date_from_iso_format(json_user["inserted_at"]),
            updated_at=self._date_from_iso_format(json_user["updated_at"]),
        )

    def _model_from_jsons(self, json_users) -> List[User]:
        return list(map(self._model_from_json, json_users))
