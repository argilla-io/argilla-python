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

from typing import Optional, Literal, Union
from uuid import UUID, uuid4

from argilla_sdk._api import DatasetsAPI
from argilla_sdk._models import DatasetModel
from argilla_sdk._resource import Resource
from argilla_sdk.client import Argilla
from argilla_sdk.records import DatasetRecords
from argilla_sdk.settings import Settings

__all__ = ["Dataset"]


class Dataset(Resource):
    """Class for defining and interacting with Argilla Datasets

    Attributes:
        name (str): Name of the dataset.
        id (UUID): Unique identifier of the dataset.
        status (Literal["draft", "ready"]): Status of the dataset.
        records (DatasetRecords): Records of the dataset.
        settings (Settings): Settings of the dataset.
        fields (list): Fields of the dataset.
        questions (list): Questions of the dataset.
        guidelines (str): Guidelines of the dataset.
        allow_extra_metadata (bool): Allow extra metadata for the dataset.

    Examples:
    ```python
    import argilla_sdk as rg

    dataset = rg.Dataset(name="My Dataset")

    ```
    """

    name: str
    id: Optional[UUID]
    status: Literal["draft", "ready"]

    _api: "DatasetsAPI"
    _model: "DatasetModel"

    def __init__(
        self,
        name: Optional[str] = None,
        status: Literal["draft", "ready"] = "draft",
        workspace_id: Optional[Union[UUID, str]] = None,
        settings: Optional[Settings] = None,
        client: Optional["Argilla"] = Argilla(),
        id: Optional[Union[UUID, str]] = uuid4(),
        _model: Optional[DatasetModel] = None,
    ) -> None:
        """Initalizes a Dataset object with the given parameters.

        Attributes:
            name (str): Name of the dataset. Replaced by random UUID if not assigned.
            status ["draft", "ready"]: Status of the dataset
            workspace_id (UUID): Workspace_id of the dataset
            settings (Settings): Settings class to be used to configure the dataset.
            client (Argilla): Instance of Argilla to connect with the server.
            id: (UUID): To predefine dataset_id or to reference existing datasets.
                Random UUID is used if not assigned.
        """
        super().__init__(client=client, api=client.api.datasets)
        if name is None:
            name = str(id)
            self.log(f"Settings dataset name to unique UUID: {id}")
        if workspace_id is None:
            workspace_id = client.workspaces[0].id
        _model = _model or DatasetModel(
            name=name,
            status=status,
            workspace_id=self._convert_optional_uuid(uuid=workspace_id),
            id=self._convert_optional_uuid(uuid=id),
        )
        self._model = _model
        self._settings = self.__configure_settings_for_dataset(settings=settings)
        self.__records = DatasetRecords(client=self._client, dataset=self)
        self._sync(model=self._model)

    @property
    def records(self) -> "DatasetRecords":
        """Returns the records of the dataset as a `DatasetRecords` object."""
        return self.__records

    @property
    def is_published(self) -> bool:
        """Returns True if the dataset is published on the server, False otherwise."""
        return self._model.status == "ready"

    @property
    def settings(self) -> Settings:
        if self.is_published and self._settings.is_outdated:
            self._settings.get()
        return self._settings

    @settings.setter
    def settings(self, value: Settings) -> None:
        self._settings = self.__configure_settings_for_dataset(settings=value)

    @property
    def fields(self) -> list:
        """Returns the fields of the dataset as a list."""
        return self._settings.fields

    @property
    def questions(self) -> list:
        """Returns the questions of the dataset as a list of `Question` objects."""
        return self._settings.questions

    @property
    def guidelines(self) -> str:
        """Returns the guidelines of the dataset as a string."""
        return self._settings.guidelines

    @guidelines.setter
    def guidelines(self, value: str) -> None:
        self._settings.guidelines = value

    @property
    def allow_extra_metadata(self) -> bool:
        """Returns True if the dataset allows extra metadata, False otherwise."""
        return self._settings.allow_extra_metadata

    @allow_extra_metadata.setter
    def allow_extra_metadata(self, value: bool) -> None:
        self._settings.allow_extra_metadata = value

    @property
    def schema(self):
        return self._settings.schema

    def exists(self) -> bool:
        return self._api.exists(self.id)

    def publish(self) -> None:
        self._configure(settings=self._settings, publish=True)

    #####################
    #  Utility methods  #
    #####################

    # we leave this method as private for now and we use the `ds.publish` one
    def _configure(self, settings: Settings, publish: bool = False) -> "Dataset":
        if not self.exists():
            self.__create()

        self._settings = self.__configure_settings_for_dataset(settings=settings)
        self._settings.create()

        if publish:
            self.__publish()

        return self.get()  # type: ignore

    def __configure_settings_for_dataset(
        self,
        settings: Optional[Settings] = None,
    ) -> Settings:
        settings = settings or Settings()
        settings.dataset = self
        return settings

    def __create(self) -> None:
        response_model = self._api.create(self._model)
        self._sync(response_model)

    def __publish(self) -> None:
        if not self.is_published:
            response_model = self._api.publish(dataset_id=self._model.id)
            self._sync(response_model)
