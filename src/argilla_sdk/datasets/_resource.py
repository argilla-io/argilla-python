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

import warnings
from typing import Optional, Literal, Union
from uuid import UUID, uuid4

from argilla_sdk._api import DatasetsAPI
from argilla_sdk._exceptions import NotFoundError, SettingsError
from argilla_sdk._models import DatasetModel
from argilla_sdk._resource import Resource
from argilla_sdk.client import Argilla
from argilla_sdk.records import DatasetRecords
from argilla_sdk.settings import Settings
from argilla_sdk.workspaces._resource import Workspace

__all__ = ["Dataset"]


class Dataset(Resource):
    """Class for interacting with Argilla Datasets"""

    name: str
    id: Optional[UUID]
    status: Literal["draft", "ready"]

    _api: "DatasetsAPI"
    _model: "DatasetModel"

    def __init__(
        self,
        name: Optional[str] = None,
        workspace: Optional[Union["Workspace", str]] = None,
        settings: Optional[Settings] = None,
        client: Optional["Argilla"] = Argilla(),
        _model: Optional[DatasetModel] = None,
    ) -> None:
        """Initalizes a Dataset with a client and model
        Args:
            name (str): Name of the dataset. Replaced by random UUID if not assigned.
            workspace (UUID): Workspace of the dataset. Default is the first workspace found in the client.
            settings (Settings): Settings class to be used to configure the dataset.
            client (Argilla): Instance of Argilla to connect with the server.
        """
        super().__init__(client=client, api=client.api.datasets)
        if name is None:
            name = f"dataset_{uuid4()}"
            self.log(f"Settings dataset name to unique UUID: {name}")

        self.workspace_id = (
            _model.workspace_id
            if _model and _model.workspace_id
            else self.__workspace_id_from_name(workspace=workspace)
        )
        self._model = _model or DatasetModel(
            name=name,
            workspace_id=self._convert_optional_uuid(uuid=self.workspace_id),
        )
        self._settings = self.__configure_settings_for_dataset(settings=settings)
        self.__records = DatasetRecords(client=self._client, dataset=self)

    @property
    def name(self) -> str:
        return self._model.name

    @name.setter
    def name(self, value: str) -> None:
        self._model.name = value

    @property
    def records(self) -> "DatasetRecords":
        return self.__records

    @property
    def settings(self) -> Settings:
        if self.__is_published() and self._settings.is_outdated:
            self._settings.get()
        return self._settings

    @settings.setter
    def settings(self, value: Settings) -> None:
        self._settings = self.__configure_settings_for_dataset(settings=value)

    @property
    def fields(self) -> list:
        return self.settings.fields

    @property
    def questions(self) -> list:
        return self.settings.questions

    @property
    def guidelines(self) -> str:
        return self.settings.guidelines

    @guidelines.setter
    def guidelines(self, value: str) -> None:
        self.settings.guidelines = value

    @property
    def allow_extra_metadata(self) -> bool:
        return self.settings.allow_extra_metadata

    @allow_extra_metadata.setter
    def allow_extra_metadata(self, value: bool) -> None:
        self.settings.allow_extra_metadata = value

    @property
    def schema(self):
        return self.settings.schema

    def exists(self) -> bool:
        return self.id and self._api.exists(self.id)

    def create(self) -> None:
        super().create()
        try:
            self._configure(settings=self._settings, publish=True)
        except Exception as e:
            self.log(message=f"Error creating dataset: {e}", level="error")
            self.__rollback_dataset_creation()
            raise SettingsError from e

    @classmethod
    def from_model(cls, model: DatasetModel, client: "Argilla") -> "Dataset":
        return cls(client=client, _model=model)

    #####################
    #  Utility methods  #
    #####################

    # we leave this method as private for now and we use the `ds.publish` one
    def _configure(self, settings: Settings, publish: bool = False) -> "Dataset":
        self._settings = self.__configure_settings_for_dataset(settings=settings)
        self.settings.validate()
        self._settings.create()

        if publish:
            self.__publish()

        return self.get()  # type: ignore

    def __configure_settings_for_dataset(
        self,
        settings: Optional[Settings] = None,
    ) -> Settings:
        """Populate the dataset object with settings"""
        if settings is None:
            settings = Settings(_dataset=self)
            warnings.warn(
                message="Settings not provided. Using empty settings for the dataset. \
                    Define the settings before publishing the dataset.",
                stacklevel=2,
            )
        else:
            settings.dataset = self
        return settings

    def __workspace_id_from_name(self, workspace: Optional[Union["Workspace", str]]) -> UUID:
        available_workspaces = self._client.workspaces
        available_workspace_names = [ws.name for ws in available_workspaces]
        if workspace is None:
            ws = available_workspaces[0]  # type: ignore
            warnings.warn(f"Workspace not provided. Using default workspace: {ws.name} id: {ws.id}")
        elif isinstance(workspace, str):
            ws = self._client.workspaces(workspace)
            if not ws.exists():
                self.log(
                    message=f"Workspace with name {workspace} not found. \
                        Available workspaces: {available_workspace_names}",
                    level="error",
                )
                raise NotFoundError()
        else:
            ws = workspace
        return ws.id

    def __create(self) -> None:
        response_model = self._api.create(self._model)
        self._sync(response_model)

    def __publish(self) -> None:
        response_model = self._api.publish(dataset_id=self._model.id)
        self._sync(response_model)

    def __rollback_dataset_creation(self):
        if self.exists():
            self.delete()

    def __is_published(self) -> bool:
        return self.exists() and self._model.status == "ready"
