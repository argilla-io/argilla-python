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

from typing import List, Optional
from uuid import UUID

from argilla_sdk import Workspace
from argilla_sdk._api import _http
from argilla_sdk._api._base import ResourceBase

__all__ = ["WorkspacesAPI"]


class WorkspacesAPI(ResourceBase):
    ################
    # CRUD methods #
    ################

    def create(self, workspace: Workspace) -> None:
        # TODO: Unify API endpoint
        response = self.http_client.post("/api/workspaces", json={"name": workspace.name})
        _http.raise_for_status(response)

    def update(self, workspace: Workspace) -> None:
        response = self.http_client.put(f"/api/v1/workspaces/{workspace.id}", json={"name": workspace.name})
        _http.raise_for_status(response)

    def get(self, id: UUID) -> Workspace:
        response = self.http_client.get(f"/api/v1/workspaces/{id}")
        _http.raise_for_status(response)
        response_json = response.json()
        workspace = self._model_from_json(response_json)
        return workspace

    def delete(self, id: UUID) -> None:
        response = self.http_client.delete(f"/api/v1/workspaces/{id}")
        _http.raise_for_status(response)

    ####################
    # Utility methods #
    ####################

    def list(self) -> List[Workspace]:
        response = self.http_client.get("/api/v1/me/workspaces")
        _http.raise_for_status(response)
        response_jsons = response.json()["items"]
        workspaces = self._model_from_jsons(response_jsons)
        self.log(f"Got {len(workspaces)} workspaces")
        return workspaces

    def list_by_user_id(self, user_id: UUID) -> List[Workspace]:
        response = self.http_client.get(f"/api/v1/users/{user_id}/workspaces")
        _http.raise_for_status(response)
        response_jsons = response.json()["items"]
        workspaces = self._model_from_jsons(response_jsons)
        self.log(f"Got {len(workspaces)} workspaces")
        return workspaces

    def list_current_user_workspaces(self) -> List[Workspace]:
        response = self.http_client.get("/api/v1/me/workspaces")
        _http.raise_for_status(response)
        response_jsons = response.json()["items"]
        workspaces = self._model_from_jsons(response_jsons)
        self.log(f"Got {len(workspaces)} workspaces")
        return workspaces

    def get_by_name(self, name: str) -> Optional[Workspace]:
        for workspace in self.list():
            if workspace.name == name:
                self.log(f"Got workspace {workspace.name}")
                return workspace
        return None

    def list_datasets(self, workspace_id: UUID) -> List["Dataset"]:
        response = self.http_client.get(f"/api/v1/workspaces/{workspace_id}/datasets")
        _http.raise_for_status(response)
        response_jsons = response.json()["items"]
        datasets = self._model_from_jsons(response_jsons)
        self.log(f"Got {len(datasets)} datasets")
        return datasets

    def add_user(self, workspace_id: UUID, user_id: UUID) -> None:
        response = self.http_client.post(f"/api/v1/workspaces/{workspace_id}/users/{user_id}")
        _http.raise_for_status(response)
        self.log(f"Added user {user_id} to workspace {workspace_id}")

    def remove_user(self, workspace_id: UUID, user_id: UUID) -> None:
        response = self.http_client.delete(f"/api/v1/workspaces/{workspace_id}/users/{user_id}")
        _http.raise_for_status(response)
        self.log(f"Removed user {user_id} from workspace {workspace_id}")

    ####################
    # Private methods #
    ####################

    def _model_from_json(self, json_workspace) -> Workspace:
        return Workspace(
            id=UUID(json_workspace["id"]),
            name=json_workspace["name"],
            inserted_at=self._date_from_iso_format(json_workspace["inserted_at"]),
            updated_at=self._date_from_iso_format(json_workspace["updated_at"]),
        )

    def _model_from_jsons(self, json_workspaces) -> List[Workspace]:
        return list(map(self._model_from_json, json_workspaces))
