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

from abc import abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING, overload, List, Optional, Union
import warnings

from argilla_sdk import _api
from argilla_sdk._helpers import GenericIterator
from argilla_sdk._helpers._resource_repr import ResourceHTMLReprMixin
from argilla_sdk._models import UserModel, WorkspaceModel, DatasetModel

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
        from argilla_sdk import User

        return User(client=self, _model=self.api.users.get_me())


class Users(Sequence["User"], ResourceHTMLReprMixin):
    """A collection of users. It can be used to create a new user or to get an existing one."""

    class _Iterator(GenericIterator["User"]):
        pass

    def __init__(self, client: "Argilla") -> None:
        self._client = client
        self._api = client.api.users

    def __call__(self, username: str, **kwargs) -> "User":
        from argilla_sdk.users._resource import User

        user_models = self._api.list()
        for model in user_models:
            if model.username == username:
                return User(_model=model, client=self._client)
        warnings.warn(f"User {username} not found. Creating a new user. Do `user.create()` to create the user.")
        return User(username=username, client=self._client, **kwargs)

    def __iter__(self):
        return self._Iterator(self.list())

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> "User": ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence["User"]: ...

    def __getitem__(self, index):
        model = self._api.list()[index]
        return self._from_model(model)

    def __len__(self) -> int:
        return len(self._api.list())

    def list(self) -> List["User"]:
        """List all users."""
        return [self._from_model(model) for model in self._api.list()]

    def _repr_html_(self) -> "HTML":
        return self._represent_as_html(resources=self.list())

    def _from_model(self, model: UserModel) -> "User":
        from argilla_sdk.users._resource import User

        return User(client=self._client, _model=model)


class Workspaces(Sequence["Workspace"], ResourceHTMLReprMixin):
    """A collection of workspaces. It can be used to create a new workspace or to get an existing one."""

    class _Iterator(GenericIterator["Workspace"]):
        pass

    def __init__(self, client: "Argilla") -> None:
        self._client = client
        self._api = client.api.workspaces

    def __call__(self, name: str, **kwargs) -> "Workspace":
        from argilla_sdk.workspaces._resource import Workspace

        workspace_models = self._api.list()

        for model in workspace_models:
            if model.name == name:
                return Workspace(_model=model, client=self._client)
        warnings.warn(
            f"Workspace {name} not found. Creating a new workspace. Do `workspace.create()` to create the workspace."
        )
        return Workspace(name=name, client=self._client, **kwargs)

    def __iter__(self):
        return self._Iterator(self.list())

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> "Workspace": ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence["Workspace"]: ...

    def __getitem__(self, index) -> "Workspace":
        model = self._api.list()[index]
        return self._from_model(model)

    def __len__(self) -> int:
        return len(self._api.list())

    def list(self) -> List["Workspace"]:
        return [self._from_model(model) for model in self._api.list()]

    def _repr_html_(self) -> "HTML":
        return self._represent_as_html(resources=self.list())

    def _from_model(self, model: WorkspaceModel) -> "Workspace":
        from argilla_sdk.workspaces._resource import Workspace

        return Workspace(client=self._client, _model=model)


class Datasets(Sequence["Dataset"], ResourceHTMLReprMixin):
    """A collection of datasets. It can be used to create a new dataset or to get an existing one."""

    class _Iterator(GenericIterator["Dataset"]):
        pass

    def __init__(self, client: "Argilla") -> None:
        self._client = client
        self._api = client.api.datasets

    def __call__(self, name: str, workspace: Optional[Union["Workspace", str]] = None, **kwargs) -> "Dataset":
        from argilla_sdk.datasets._resource import Dataset

        if isinstance(workspace, str):
            workspace = self._client.workspaces(workspace)
        elif workspace is None:
            workspace = self._client.workspaces[0]

        for dataset in workspace.datasets:
            if dataset.name == name:
                return Dataset(_model=dataset, client=self._client)
        warnings.warn(f"Dataset {name} not found. Creating a new dataset. Do `dataset.create()` to create the dataset.")
        return Dataset(name=name, workspace=workspace, client=self._client, **kwargs)

    def __iter__(self):
        return self._Iterator(self.list())

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> "Dataset": ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence["Dataset"]: ...

    def __getitem__(self, index) -> "Dataset":
        model = self._api.list()[index]
        return self._from_model(model)

    def __len__(self) -> int:
        return len(self._api.list())

    def list(self) -> List["Dataset"]:
        return [self._from_model(model) for model in self._api.list()]

    def _repr_html_(self) -> "HTML":
        return self._represent_as_html(resources=self.list())

    def _from_model(self, model: DatasetModel) -> "Dataset":
        from argilla_sdk.datasets._resource import Dataset

        return Dataset(client=self._client, _model=model)
