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
from typing import TYPE_CHECKING, List, Union, Type

from argilla_sdk import _api
from argilla_sdk.datasets import Dataset
from argilla_sdk.users import User
from argilla_sdk.workspaces import Workspace

if TYPE_CHECKING:
    from argilla_sdk._models import UserModel

__all__ = ["Argilla"]


class Argilla(_api.APIClient):
    @property
    def default_user(self) -> "UserModel":
        return self.users.get_me()

    def create(self, resource: Union[Workspace, User, Dataset]) -> Union[Workspace, User, Dataset]:
        """Create a new resource in the API. For example, a new workspace, user, or dataset.
        Args:
            resource: Union[Workspace, User, Dataset] - The resource to create
        Returns:
            Union[Workspace, User, Dataset] - The created resource
        """
        resource_api = self._which_resource_api(resource)
        response_model = resource_api.create(resource._model)  # type: ignore
        resource = resource._update(api=self, model=response_model)
        return resource

    def get(self, resource: Union[Workspace, User, Dataset]) -> Union[Workspace, User, Dataset]:
        """Get an resource from the API. For example, a workspace, user, or dataset.
        Args:
            resource: Union[Workspace, User, Dataset] - The resource to get
        Returns:
            Union[Workspace, User, Dataset] - The requested resource
        """
        resource_api = self._which_resource_api(resource)
        response_model = resource_api.get(resource.id.hex)
        resource = resource._update(api=self, model=response_model)
        return resource

    def list(self, resource_type: Type[Union[Workspace, User, Dataset]]) -> List[Union[Workspace, User, Dataset]]:
        """List entities from the API. For example, workspaces, users, or datasets.
        Args:
            resource: Union[Workspace, User, Dataset] - The resource to list
        Returns:
            Union[Workspace, User, Dataset] - The requested entities
        """
        resource_api = self._which_resource_api(resource_type)
        response_models = resource_api.list()
        return response_models

    def update(self, resource: Union[Workspace, User, Dataset]) -> Union[Workspace, User, Dataset, None]:
        """Update an resource in the API. For example, a workspace, user, or dataset.
        Args:
            resource: Union[Workspace, User, Dataset] - The resource to update
        Returns:
            Union[Workspace, User, Dataset] - The updated resource
        """
        resource_api = self._which_resource_api(resource)
        response_model = resource_api.update(resource._model)  # type: ignore
        resource = resource._update(api=self, model=response_model)
        return resource

    def delete(self, resource: Union[Workspace, User, Dataset]) -> None:
        """Delete an resource from the API. For example, a workspace, user, or dataset.
        Args:
            resource: Union[Workspace, User, Dataset] - The resource to delete
        """
        resource_api = self._which_resource_api(resource)
        resource_api.delete(resource.id)

    def _which_resource_api(
        self, resource: Union[Workspace, User, Dataset]
    ) -> Union[Union[_api.WorkspacesAPI, _api.UsersAPI, _api.DatasetsAPI], Type[Union[Workspace, User, Dataset]]]:
        """Determine which resource to use based on the resource type."""
        if isinstance(resource, Workspace) or resource == Workspace:
            return self._workspaces
        elif isinstance(resource, User) or resource == User:
            return self._users
        elif isinstance(resource, Dataset) or resource == Dataset:
            return self._datasets
        else:
            raise ValueError("Invalid resource type: must be a Workspace, User, or Dataset.")
