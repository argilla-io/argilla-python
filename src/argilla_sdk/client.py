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
from typing import TYPE_CHECKING, List, Union

from argilla_sdk import _api
from argilla_sdk.datasets import Dataset
from argilla_sdk.users import User
from argilla_sdk.workspaces import Workspace

if TYPE_CHECKING:
    from argilla_sdk._models import UserModel, WorkspaceModel

__all__ = ["Argilla"]


class Argilla(_api.APIClient):
    @property
    def default_workspace(self) -> "WorkspaceModel":
        return self.workspaces.list_current_user_workspaces()[0]

    @property
    def default_user(self) -> "UserModel":
        return self.users.get_me()

    def create(self, entity: Union[Workspace, User, Dataset]) -> Union[Workspace, User, Dataset]:
        """Create a new entity in the API. For example, a new workspace, user, or dataset.
        Args:
            entity: Union[Workspace, User, Dataset] - The entity to create
        Returns:
            Union[Workspace, User, Dataset] - The created entity
        """
        resource_api = self._which_resource_api(entity)
        response_model = resource_api.create(entity.model)  # type: ignore
        entity = entity.update(api=self, model=response_model)
        return entity

    def get(self, entity: Union[Workspace, User, Dataset]) -> Union[Workspace, User, Dataset]:
        """Get an entity from the API. For example, a workspace, user, or dataset.
        Args:
            entity: Union[Workspace, User, Dataset] - The entity to get
        Returns:
            Union[Workspace, User, Dataset] - The requested entity
        """
        resource_api = self._which_resource_api(entity)
        response_model = resource_api.get(entity.id)
        entity = entity.update(api=self, model=response_model)
        return entity

    def list(self, entity: Union[Workspace, User, Dataset]) -> List[Union[Workspace, User, Dataset]]:
        """List entities from the API. For example, workspaces, users, or datasets.
        Args:
            entity: Union[Workspace, User, Dataset] - The entity to list
        Returns:
            Union[Workspace, User, Dataset] - The requested entities
        """
        resource_api = self._which_resource_api(entity)
        response_models = resource_api.list()
        entities = [entity.update(api=self, model=model) for model in response_models]
        return entities

    def update(self, entity: Union[Workspace, User, Dataset]) -> Union[Workspace, User, Dataset, None]:
        """Update an entity in the API. For example, a workspace, user, or dataset.
        Args:
            entity: Union[Workspace, User, Dataset] - The entity to update
        Returns:
            Union[Workspace, User, Dataset] - The updated entity
        """
        resource_api = self._which_resource_api(entity)
        response_model = resource_api.update(entity.model) # type: ignore
        entity = entity.update(api=self, model=response_model)
        return entity

    def delete(self, entity: Union[Workspace, User, Dataset]) -> None:
        """Delete an entity from the API. For example, a workspace, user, or dataset.
        Args:
            entity: Union[Workspace, User, Dataset] - The entity to delete
        """
        resource_api = self._which_resource_api(entity)
        resource_api.delete(entity.id)

    def _which_resource_api(
        self, entity: Union[Workspace, User, Dataset]
    ) -> Union[_api.WorkspacesAPI, _api.UsersAPI, _api.DatasetsAPI]:
        """Determine which resource to use based on the entity type."""
        if isinstance(entity, Workspace):
            return self.workspaces
        elif isinstance(entity, User):
            return self.users
        elif isinstance(entity, Dataset):
            return self.datasets
        else:
            raise ValueError("Invalid entity type: must be a Workspace, User, or Dataset.")
