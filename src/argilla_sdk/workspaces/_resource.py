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
    from argilla_sdk import Dataset, User
    from argilla_sdk._api import WorkspacesAPI


__all__ = ["Workspace"]


class Workspace(Resource):
    """Class for interacting with Argilla workspaces"""

    name: Optional[str]

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

    # TODO: Make this method private
    def list_datasets(self) -> List["Dataset"]:
        from argilla_sdk.datasets import Dataset

        datasets = self._client.api.datasets.list(self.id)
        self.log(f"Got {len(datasets)} datasets for workspace {self.id}")
        return [Dataset.from_model(model=dataset, client=self._client) for dataset in datasets]

    def exists(self) -> bool:
        return self._api.exists(self.id)

    def __len__(self) -> int:
        return len(self.datasets)

    ############################
    # Properties
    ############################

    @property
    def name(self) -> Optional[str]:
        return self._model.name

    @name.setter
    def name(self, value: str) -> None:
        self._model.name = value

    @property
    def datasets(self) -> List["Dataset"]:
        return self.list_datasets()

    @property
    def users(self) -> List["User"]:
        return self._list_users()

    ############################
    # Private methods
    ############################

    def _list_users(self) -> List["User"]:
        users = self._client.users.list(workspace=self)
        self.log(f"Got {len(users)} users for workspace {self.id}")
        return users

    def _remove_user_by_username(self, username: str) -> "User":
        user = self._client.users(username=username)
        if not user.exists():
            raise ValueError(f"User {username} does not exist")
        return user.remove_from_workspace(workspace=self)

    def _add_user_by_username(self, username: str) -> "User":
        username = self._client.users(username=username)
        if not username.exists():
            raise ValueError(f"User {username} does not exist")
        return username.add_to_workspace(workspace=self)
