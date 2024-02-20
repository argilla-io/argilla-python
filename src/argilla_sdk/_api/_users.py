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

from typing import List, Union
from uuid import UUID

import httpx

from argilla_sdk._api import _http
from argilla_sdk._api._base import ResourceAPI
from argilla_sdk._models import UserModel

__all__ = ["UsersAPI"]


class UsersAPI(ResourceAPI):
    """Manage users via the API"""

    http_client: httpx.Client

    ################
    # CRUD methods #
    ################

    def create(self, user: UserModel) -> "UserModel":
        json_body = user.model_dump()
        response = self.http_client.post(
            "/api/users",
            json=json_body,
        )
        _http.raise_for_status(response=response)
        user = self._model_from_json(json_user=response.json())
        self.log(message=f"Created user {user.username}")
        return user

    def get(self, user_id: Union[UUID, str]) -> "UserModel":
        response = self.http_client.get(url=f"/api/users/{user_id}")
        _http.raise_for_status(response=response)
        response_json = response.json()
        user = self._model_from_json(json_user=response_json)
        self.log(message=f"Got user {user.username}")
        return user

    def delete(self, user_id: Union[UUID, str]) -> None:
        response = self.http_client.delete(url=f"/api/users/{user_id}")
        _http.raise_for_status(response=response)
        self.log(message=f"Deleted user {id}")

    ####################
    # Utility methods #
    ####################

    def list(self) -> List["UserModel"]:
        response = self.http_client.get(url="/api/users")
        _http.raise_for_status(response=response)
        response_json = response.json()
        users = self._model_from_jsons(json_users=response_json)
        self.log(message=f"Listed {len(users)} users")
        return users

    def list_by_workspace_id(self, workspace_id: UUID) -> List["UserModel"]:
        response = self.http_client.get(url=f"/api/workspaces/{workspace_id}/users")
        _http.raise_for_status(response=response)
        response_json = response.json()["items"]
        users = self._model_from_jsons(json_users=response_json)
        self.log(message=f"Listed {len(users)} users")
        return users

    def get_me(self) -> "UserModel":
        response = self.http_client.get("/api/me")
        _http.raise_for_status(response=response)
        user = self._model_from_json(json_user=response.json())
        self.log(message=f"Got user {user.username}")
        return user

    def add_to_workspace(self, workspace_id: UUID, user_id: UUID) -> None:
        response = self.http_client.post(url=f"/api/workspaces/{workspace_id}/users/{user_id}")
        _http.raise_for_status(response=response)
        self.log(message=f"Added user {user_id} to workspace {workspace_id}")

    def delete_from_workspace(self, workspace_id: UUID, user_id: UUID) -> None:
        response = self.http_client.delete(url=f"/api/workspaces/{workspace_id}/users/{user_id}")
        _http.raise_for_status(response=response)
        self.log(message=f"Deleted user {user_id} from workspace {workspace_id}")

    ####################
    # Private methods #
    ####################

    def _model_from_json(self, json_user) -> "UserModel":
        return UserModel(
            id=json_user["id"],
            username=json_user["username"],
            first_name=json_user["first_name"],
            last_name=json_user["last_name"],
            role=json_user["role"],
            inserted_at=self._date_from_iso_format(date=json_user["inserted_at"]),
            updated_at=self._date_from_iso_format(date=json_user["updated_at"]),
        )

    def _model_from_jsons(self, json_users) -> List["UserModel"]:
        return list(map(self._model_from_json, json_users))
