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

from abc import ABC, abstractmethod
import json
import logging
import os
from pathlib import Path
import warnings
from typing import Optional, Union, TYPE_CHECKING, Tuple
from uuid import uuid4

from argilla_sdk._models import DatasetModel
from argilla_sdk.client import Argilla
from argilla_sdk.settings import Settings
from argilla_sdk.workspaces._resource import Workspace


if TYPE_CHECKING:
    from argilla_sdk import Dataset
    from argilla_sdk.records import DatasetRecords


class DiskImportExportMixin(ABC):
    """A mixin for exporting and importing datasets to and from disk."""

    _model: DatasetModel
    _default_settings_path = "settings.json"
    _default_records_path = "records.json"
    _default_dataset_path = "dataset.json"

    def to_disk(self, path: str) -> str:
        """Exports the dataset to disk in the given path.

        Args:
            path (str): The path to export the dataset to.
        """

        dir_path, dataset_path, settings_path, records_path = self._define_child_paths(path=path)
        os.makedirs(path, exist_ok=True)

        with open(dataset_path, "w") as f:
            json.dump(self._model.model_dump(), f)

        self.settings.to_json(path=settings_path)

        if self.exists():
            self.records.to_json(path=records_path)

        return dir_path

    @classmethod
    def from_disk(
        cls,
        path: str,
        target_workspace: Optional[Union["Workspace", str]] = None,
        target_name: Optional[str] = None,
        client: Optional["Argilla"] = None,
    ) -> "Dataset":
        client = client or Argilla._get_default()

        path, dataset_path, settings_path, records_path = cls._define_child_paths(path=path)

        with open(dataset_path, "r") as f:
            dataset_model = json.load(f)
            dataset_model = DatasetModel(**dataset_model)

        if isinstance(target_workspace, str):
            workspace_id = client.workspaces(target_workspace).id
        elif isinstance(target_workspace, Workspace):
            workspace_id = target_workspace.id
        else:
            warnings.warn("Workspace not provided. Using default workspace.")
            workspace_id = client.workspaces.default.id
        dataset_model.workspace_id = workspace_id

        if target_name:
            logging.warning(f"Changing dataset name from {dataset_model.name} to {target_name}")
            dataset_model.name = target_name
        elif client.api.datasets.name_exists(name=dataset_model.name, workspace_id=workspace_id):
            logging.warning(f"Loaded dataset name {dataset_model.name} already exists. Changing to unique UUID.")
            dataset_model.name = f"{dataset_model.name}_{uuid4()}"

        dataset = cls.from_model(model=dataset_model, client=client)

        dataset.settings = Settings.from_json(path=settings_path)

        if os.path.exists(records_path):
            dataset.records.from_json(path=records_path)
        return dataset

    ############################
    # Utility methods
    ############################

    @classmethod
    def _define_child_paths(cls, path: Union[Path, str]) -> Tuple[Path, Path, Path, Path]:
        path = Path(path)
        dataset_path = path / cls._default_dataset_path
        settings_path = path / cls._default_settings_path
        records_path = path / cls._default_records_path
        return path, dataset_path, settings_path, records_path

    ############################
    # Abstracted Dataset Methods
    ############################

    @property
    @abstractmethod
    def records(self) -> "DatasetRecords":
        ...

    @property
    @abstractmethod
    def settings(self) -> Settings:
        ...

    @settings.setter
    @abstractmethod
    def settings(self, value: Settings):
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def create(self) -> "Dataset":
        ...

    @abstractmethod
    def exists(self) -> bool:
        ...

    @classmethod
    @abstractmethod
    def from_model(cls, model: DatasetModel, client: Argilla) -> "Dataset":
        ...
