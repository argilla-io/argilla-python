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

from typing import TYPE_CHECKING, List

from argilla_sdk import _api
import argilla_sdk as rg

if TYPE_CHECKING:
    from argilla_sdk import Workspace
    from argilla_sdk import Dataset
    from argilla_sdk import User

__all__ = ["Argilla"]


class Argilla(_api.APIClient):
    @property
    def me(self) -> "UserModel":
        return rg.User(client=self, _model=self._users.get_me())

    @property
    def workspaces(self) -> List["Workspace"]:
        return [rg.Workspace(client=self, _model=model) for model in self._workspaces.list()]

    @property
    def datasets(self) -> List["Dataset"]:
        return [rg.Dataset(client=self, _model=model) for model in self._datasets.list()]

    @property
    def users(self) -> List["User"]:
        return [rg.User(client=self, _model=model) for model in self._users.list()]
