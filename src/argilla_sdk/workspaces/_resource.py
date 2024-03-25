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

from typing import List, TYPE_CHECKING, Optional
from uuid import UUID

from argilla_sdk._api._workspaces import WorkspacesAPI
from argilla_sdk._models import WorkspaceModel
from argilla_sdk._resource import Resource
from argilla_sdk.client import Argilla

if TYPE_CHECKING:
    from argilla_sdk._models import DatasetModel
    from argilla_sdk._api._workspaces import WorkspacesAPI


__all__ = ["Workspace"]


class Workspace(Resource):
    """Class for interacting with Argilla workspaces"""

    name: Optional[str]
    id: Optional[UUID]

    _api: "WorkspacesAPI"

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[UUID] = None,
        client: Optional["Argilla"] = Argilla(),
        _model: Optional[WorkspaceModel] = None,
    ) -> None:
        """Initializes a Workspace object with a client and a name or id
        Args:
            client (Argilla): The client used to interact with Argilla
            name (str): The name of the workspace
            id (UUID): The id of the workspace
            _model (WorkspaceModel): The internal Pydantic model of the workspace from/to the server
        Returns:
            Workspace: The initialized workspace object
        """
        super().__init__(client=client, api=client.api.workspaces)
        self._sync(model=WorkspaceModel(name=name, id=id) if not _model else _model)

    def list_datasets(self) -> List["DatasetModel"]:
        datasets = self._client.api.datasets.list(self.id)
        self.log(f"Got {len(datasets)} datasets for workspace {self.id}")
        return datasets

    def exists(self) -> bool:
        return self._api.exists(self.id)
