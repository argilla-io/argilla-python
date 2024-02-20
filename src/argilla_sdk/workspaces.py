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

from typing import List
from uuid import UUID

from argilla_sdk._resource import Resource
from argilla_sdk._models import WorkspaceModel, DatasetModel

__all__ = ["Workspace"]


class Workspace(Resource):
    def __init__(self, **kwargs) -> None:
        self._model = WorkspaceModel(**kwargs)
        self.name = self._model.name
        self.id = self._model.id
        self.inserted_at = self._model.inserted_at
        self.updated_at = self._model.updated_at

    def list_datasets(self, workspace_id: UUID) -> List["DatasetModel"]:
        datasets = self.api._datasets.list(workspace_id)
        self.log(f"Got {len(datasets)} datasets for workspace {workspace_id}")
        return datasets
