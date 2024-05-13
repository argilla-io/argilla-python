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
    """Class for interacting with Argilla Datasets

    Attributes:
        records (DatasetRecords): The records object
        is_published (bool): True if the dataset is published, False otherwise
        settings (Settings): The settings object
        fields (list): The fields of the dataset
        questions (list): The questions of the dataset
        guidelines (str): The guidelines of the dataset
        allow_extra_metadata (bool): True if extra metadata is allowed, False otherwise
        schema: The schema of the dataset
    """

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
        client: Optional["Argilla"] = None,
        _model: Optional[DatasetModel] = None,
    ) -> None:
        """Initalizes a new Argilla Dataset object with the given parameters.

        Parameters:
            name (str): Name of the dataset. Replaced by random UUID if not assigned.
            workspace (UUID): Workspace of the dataset. Default is the first workspace found in the client.
            settings (Settings): Settings class to be used to configure the dataset.
            client (Argilla): Instance of Argilla to connect with the server.
        """
        client = client or Argilla._get_default()
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

    #####################
    #  Properties       #
    #####################

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

    #####################
    #  Core methods     #
    #####################

    def exists(self) -> bool:
        """Checks if the dataset exists on the server
        Returns:
            bool: True if the dataset exists, False otherwise
        """
        return self.id and self._api.exists(self.id)

    def create(self) -> None:
        """ Creates the dataset on the server with the `Settings` configuration and sets the dataset status to `ready`.
        Returns:
            None
        """
        super().create()
        try:
            self._publish()
        except Exception as e:
            self.log(message=f"Error creating dataset: {e}", level="error")
            self.__rollback_dataset_creation()
            raise SettingsError from e

    @classmethod
    def from_model(cls, model: DatasetModel, client: "Argilla") -> "Dataset":
        return cls(client=client, _model=model)

    #####################
    #  CRUD operations  #
    #####################

    def create(self) -> "Dataset":
        """Creates a new dataset on the server without `Settings` configuration and without publishing
        Returns:
            Dataset: The created dataset object
        Examples:
        """
        return super().create()

    def get(self) -> "Dataset":
        """Retrieves the dataset from the server
        Returns:
            Dataset: The retrieved dataset object
        """
        return super().get()

    def update(self) -> "Dataset":
        """Updates the dataset on the server
        Returns:
            Dataset: The updated dataset object
        Examples:
        ```python
        dataset = rg.Dataset(name="my_dataset")
        dataset.create()
        # do something to the dataset configuration locally
        dataset.update()
        ```
        """
        return super().update()

    def delete(self) -> None:
        """Deletes the dataset from the server"""
        return super().delete()

    #####################
    #  Utility methods  #
    #####################

    def _sync(self, model: "DatasetModel") -> "Dataset":
        # We only need to update the model. Maybe in the future the
        # _sync method makes less sense for those resources defining getter/setters
        self._model = model
        return self

    def _publish(self) -> "Dataset":

        self.settings.validate()
        self._settings.create()
        self._api.publish(dataset_id=self._model.id)

        return self.get()  # type: ignore

    def __configure_settings_for_dataset(
        self,
        settings: Optional[Settings] = None,
    ) -> Settings:
        if settings is None:
            settings = Settings(_dataset=self)
            warnings.warn(
                message="Settings not provided. Using empty settings for the dataset. \
                    Define the settings before creating the dataset.",
                stacklevel=2,
            )
        else:
            settings.dataset = self
        return settings

    def __workspace_id_from_name(self, workspace: Optional[Union["Workspace", str]]) -> UUID:

        if workspace is None:
            available_workspaces = self._client.workspaces
            ws = available_workspaces[0]  # type: ignore
            warnings.warn(f"Workspace not provided. Using default workspace: {ws.name} id: {ws.id}")
        elif isinstance(workspace, str):
            available_workspace_names = [ws.name for ws in self._client.workspaces]
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

    def __rollback_dataset_creation(self):
        if self.exists() and not self.__is_published():
            self.delete()

    def __is_published(self) -> bool:
        return self.exists() and self._model.status == "ready"
