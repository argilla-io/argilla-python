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
from collections.abc import Sequence
from abc import abstractmethod
from typing import TYPE_CHECKING, overload

from argilla_sdk import _api

if TYPE_CHECKING:
    from argilla_sdk import Workspace
    from argilla_sdk import Dataset
    from argilla_sdk import User

__all__ = ["Argilla"]


class Argilla(_api.APIClient):
    @property
    def workspaces(self) -> "Workspaces":
        return Workspaces(client=self)

    @property
    def datasets(self) -> "Datasets":
        return Datasets(client=self)

    @property
    def users(self) -> "Users":
        return Users(client=self)

    @property
    def me(self) -> "User":
        return User(client=self, _model=self._users.get_me())


class Users(Sequence):
    """A collection of users. It can be used to create a new user or to get an existing one."""

    def __init__(self, client: "Argilla") -> None:
        self._client = client
        self._api = _api.UsersAPI(http_client=client.http_client)

    def __call__(self, username: str, **kwargs) -> "User":
        from argilla_sdk.users._resource import User

        user_models = self._api.list()
        for model in user_models:
            if model.username == username:
                return User(_model=model, client=self._client)

        return User(username=username, client=self._client, **kwargs)

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> "User": ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence["User"]: ...

    def __getitem__(self, index):
        from argilla_sdk.users._resource import User

        model = self._api.list()[index]
        return User(client=self._client, _model=model)

    def __len__(self) -> int:
        return len(self._api.list())


class Workspaces(Sequence):
    """A collection of workspaces. It can be used to create a new workspace or to get an existing one."""

    def __init__(self, client: "Argilla") -> None:
        self._client = client
        self._api = _api.WorkspacesAPI(http_client=client.http_client)

    def __call__(self, name: str, **kwargs) -> "Workspace":
        from argilla_sdk.workspaces._resource import Workspace

        workspace_models = self._api.list()

        for model in workspace_models:
            if model.name == name:
                return Workspace(_model=model, client=self._client)

        return Workspace(name=name, client=self._client, **kwargs)

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> "Workspace": ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence["Workspace"]: ...

    def __getitem__(self, index: int) -> "Workspace":
        from argilla_sdk.workspaces._resource import Workspace

        model = self._api.list()[index]
        return Workspace(client=self._client, _model=model)

    def __len__(self) -> int:
        return len(self._api.list())


class Datasets(Sequence):
    """A collection of datasets. It can be used to create a new dataset or to get an existing one."""

    def __init__(self, client: "Argilla") -> None:
        self._client = client
        self._api = _api.DatasetsAPI(http_client=client.http_client)

    def __call__(self, name: str, workspace: "Workspace", **kwargs) -> "Dataset":
        from argilla_sdk.datasets._resource import Dataset

        workspace_id = workspace.id
        dataset_models = self._api.list(workspace_id=workspace_id)

        for model in dataset_models:
            if model.name == name:
                return Dataset(_model=model, client=self._client)

        return Dataset(name=name, workspace_id=workspace_id, client=self._client, **kwargs)

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> "Dataset": ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence["Dataset"]: ...

    def __getitem__(self, index) -> "Dataset":
        from argilla_sdk.datasets._resource import Dataset

        model = self._api.list()[index]
        return Dataset(client=self._client, _model=model)

    def __len__(self) -> int:
        return len(self._api.list())
