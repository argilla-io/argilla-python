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

from typing import List, Optional, TYPE_CHECKING

from argilla_sdk import _api
from argilla_sdk._helpers import GenericIterator  # noqa

if TYPE_CHECKING:
    from argilla_sdk import Workspace

__all__ = ["Dataset", "WorkspaceDatasets"]


class Dataset(_api.Dataset):
    @property
    def workspace(self) -> Optional["Workspace"]:
        from argilla_sdk.workspaces import Workspace

        if self.workspace_id:
            return Workspace.get(self.workspace_id)

    @workspace.setter
    def workspace(self, workspace: "Workspace") -> None:
        self.workspace_id = workspace.id

    @classmethod
    def get_by_name_and_workspace(cls, name: str, workspace: "Workspace") -> Optional["Dataset"]:
        return cls.get_by_name_and_workspace_id(name, workspace.id)


DatasetsIterator = GenericIterator["Dataset"]


class WorkspaceDatasets:
    def __init__(self, workspace: "Workspace"):
        self.workspace = workspace

    def list(self) -> List["Dataset"]:
        from argilla_sdk import Dataset

        return Dataset.list(workspace_id=self.workspace.id)

    def add(self, dataset: "Dataset") -> "Dataset":
        dataset.workspace_id = self.workspace.id
        return dataset.create()

    def get_by_name(self, name: str) -> "Dataset":
        return Dataset.get_by_name_and_workspace(name=name, workspace=self.workspace)

    def __iter__(self):
        return DatasetsIterator(self.list())
