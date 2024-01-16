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

from typing import List, TYPE_CHECKING

from argilla_sdk import _api
from argilla_sdk._helpers._iterator import GenericIterator  # noqa

if TYPE_CHECKING:
    from argilla_sdk.workspaces import Workspace

__all__ = ["User", "WorkspaceUsers"]


class User(_api.User):
    @property
    def workspaces(self) -> List["Workspace"]:
        return Workspace.list_by_user_id(self.id)


UsersIterator = GenericIterator[User]


class WorkspaceUsers:
    def __init__(self, workspace: "Workspace"):
        self.workspace = workspace

    def list(self) -> List[User]:
        return User.list_by_workspace_id(self.workspace.id)

    def add(self, user: User) -> User:
        return user.add_to_workspace(self.workspace.id)

    def delete(self, user: User) -> User:
        return user.delete_from_workspace(self.workspace.id)

    def __iter__(self):
        return UsersIterator(self.list())
