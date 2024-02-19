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

import httpx

from argilla_sdk._models import WorkspaceModel
from argilla_sdk._api import _http
from argilla_sdk._api._base import ResourceAPI

__all__ = ["WorkspacesAPI"]


class WorkspacesAPI(ResourceAPI):
    http_client: httpx.Client

    ################
    # CRUD methods #
    ################

    def create(self, workspace: WorkspaceModel) -> "WorkspaceModel":
        # TODO: Unify API endpoint
        response = self.http_client.post(url="/api/workspaces", json={"name": workspace.name})
        _http.raise_for_status(response=response)
        workspace = self._model_from_json(json_workspace=response.json())
        self.log(message=f"Created workspace {workspace.name}")
        return workspace

    def update(self, workspace: WorkspaceModel) -> "WorkspaceModel":
        response = self.http_client.put(f"/api/v1/workspaces/{workspace.id}", json={"name": workspace.name})
        _http.raise_for_status(response=response)
        self.log(message=f"Updated workspace {workspace.name}")
        workspace = self.get(workspace.id)
        return workspace

    def get(self, id: UUID) -> WorkspaceModel:
        response = self.http_client.get(url=f"/api/v1/workspaces/{id}")
        _http.raise_for_status(response=response)
        response_json = response.json()
        workspace = self._model_from_json(json_workspace=response_json)
        return workspace

    def delete(self, id: UUID) -> None:
        response = self.http_client.delete(url=f"/api/v1/workspaces/{id}")
        _http.raise_for_status(response=response)

    ####################
    # Utility methods #
    ####################

    def list(self) -> List[WorkspaceModel]:
        response = self.http_client.get(url="/api/v1/me/workspaces")
        _http.raise_for_status(response=response)
        response_jsons = response.json()["items"]
        workspaces = self._model_from_jsons(json_workspaces=response_jsons)
        self.log(message=f"Got {len(workspaces)} workspaces")
        return workspaces

    def list_by_user_id(self, user_id: UUID) -> List[WorkspaceModel]:
        response = self.http_client.get(f"/api/v1/users/{user_id}/workspaces")
        _http.raise_for_status(response=response)
        response_jsons = response.json()["items"]
        workspaces = self._model_from_jsons(json_workspaces=response_jsons)
        self.log(message=f"Got {len(workspaces)} workspaces")
        return workspaces

    def list_current_user_workspaces(self) -> List[WorkspaceModel]:
        response = self.http_client.get(url="/api/v1/me/workspaces")
        _http.raise_for_status(response=response)
        response_jsons = response.json()["items"]
        workspaces = self._model_from_jsons(json_workspaces=response_jsons)
        self.log(message=f"Got {len(workspaces)} workspaces")
        return workspaces

    def get_by_name(self, name: str) -> Optional[WorkspaceModel]:
        for workspace in self.list():
            if workspace.name == name:
                self.log(message=f"Got workspace {workspace.name}")
                return workspace
        return None

    def add_user(self, workspace_id: UUID, user_id: UUID) -> None:
        response = self.http_client.post(f"/api/v1/workspaces/{workspace_id}/users/{user_id}")
        _http.raise_for_status(response=response)
        self.log(message=f"Added user {user_id} to workspace {workspace_id}")

    def remove_user(self, workspace_id: UUID, user_id: UUID) -> None:
        response = self.http_client.delete(f"/api/v1/workspaces/{workspace_id}/users/{user_id}")
        _http.raise_for_status(response=response)
        self.log(message=f"Removed user {user_id} from workspace {workspace_id}")

    ####################
    # Private methods #
    ####################

    def _model_from_json(self, json_workspace) -> WorkspaceModel:
        return WorkspaceModel(
            id=UUID(json_workspace["id"]),
            name=json_workspace["name"],
            inserted_at=self._date_from_iso_format(date=json_workspace["inserted_at"]),
            updated_at=self._date_from_iso_format(date=json_workspace["updated_at"]),
        )

    def _model_from_jsons(self, json_workspaces) -> List[WorkspaceModel]:
        return list(map(self._model_from_json, json_workspaces))
