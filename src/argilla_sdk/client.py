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

from tkinter import W
from typing import TYPE_CHECKING, Union

from argilla_sdk import _api
from argilla_sdk.datasets import *  # noqa
from argilla_sdk.workspaces import *  # noqa
from argilla_sdk.users import *  # noqa

if TYPE_CHECKING:
    from argilla_sdk.workspaces import Workspace
    from argilla_sdk.users import User
    from argilla_sdk.datasets import Dataset


__all__ = ["Client"]


class Client(_api.Client):
    @property
    def default_workspace(self) -> Workspace:
        return self.workspaces.list_current_user_workspaces()[0]

    @property
    def default_user(self) -> User:
        return self.users.get_me()

    def create(self, entity: Union[Workspace, User, Dataset]) -> Union[Workspace, User, Dataset]:
        module, Model = self._is_entity(entity)
        return Model(**module.create(entity))

    def get(self, entity: Union[Workspace, User, Dataset]) -> Union[Workspace, User, Dataset]:
        module, Model = self._is_entity(entity)
        return Model(**module.get(entity.id))

    def list(self, entity: Union[Workspace, User, Dataset]) -> Union[Workspace, User, Dataset]:
        module, Model = self._is_entity(entity)
        return module.list()

    def update(self, entity: Union[Workspace, User, Dataset]) -> Union[Workspace, User, Dataset]:
        module, Model = self._is_entity(entity)
        return module.update(entity)

    def _is_entity(self, entity: Union[Workspace, User, Dataset]) -> Union[Workspace, User, Dataset]:
        if isinstance(entity, Workspace):
            return self.workspaces, Workspace
        elif isinstance(entity, User):
            return self.users, User
        elif isinstance(entity, Dataset):
            return self.datasets, Dataset
        else:
            raise ValueError("Invalid entity type")
