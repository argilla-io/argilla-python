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
from typing import List, TYPE_CHECKING, Union

from argilla_sdk import _api
from argilla_sdk._helpers._iterator import GenericIterator  # noqa

if TYPE_CHECKING:
    from argilla_sdk import Dataset

__all__ = ["Workspace"]


class Workspace(_api.Workspace):
    @property
    def datasets(self) -> "WorkspaceDatasets":
        return WorkspaceDatasets(self)


DatasetsIterator = GenericIterator["Dataset"]


class WorkspaceDatasets:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace

    def list(self) -> List["Dataset"]:
        from argilla_sdk import Dataset

        return Dataset.list(workspace_id=self.workspace.id)

    def add(self, dataset: "Dataset") -> "Dataset":
        dataset.workspace_id = self.workspace.id
        return dataset.create()

    def get_by_name(self, name: str) -> "Dataset":
        from argilla_sdk import Dataset

        return Dataset.get_by_name_and_workspace(name=name, workspace=self.workspace)

    def __getitem__(self, key: Union[str, int]) -> "Dataset":
        if isinstance(key, int):
            return self.list()[key]
        else:
            return self.get_by_name(key)

    def __iter__(self):
        return DatasetsIterator(self.list())
