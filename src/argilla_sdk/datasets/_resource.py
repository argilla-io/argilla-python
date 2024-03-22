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
from typing import Optional, Literal, Union, Dict
from uuid import UUID, uuid4

from argilla_sdk._api import DatasetsAPI
from argilla_sdk._models import DatasetModel
from argilla_sdk._resource import Resource
from argilla_sdk.client import Argilla
from argilla_sdk.datasets._exceptions import DatasetNotPublished
from argilla_sdk.records import DatasetRecords
from argilla_sdk.settings import Settings

__all__ = ["Dataset"]


class Dataset(Resource):
    """Class for interacting with Argilla Datasets"""

    name: str
    id: UUID
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
        """Initalizes a Dataset with a client and model
        Args:
            name (str): Name of the dataset. Replaced by random UUID if not assigned.
            status ["draft", "ready"]: Status of the dataset
            workspace_id (UUID): Workspace_id of the dataset
            settings (Settings): Settings class to be used to configure the dataset.
            client (Argilla): Instance of Argilla to connect with the server.
            id: (UUID): To predefine dataset_id or to reference existing datasets.
                Random UUID is used if not assigned.
        """
        super().__init__(client=client, api=client._datasets)
        if name is None:
            name = str(id)
            self.log(f"Settings dataset name to unique UUID: {id}")

        _model = _model or DatasetModel(
            name=name,
            status=status,
            workspace_id=self._convert_optional_uuid(uuid=workspace_id),
            id=self._convert_optional_uuid(uuid=id),
        )
        self._model = _model
        self.__define_settings(settings=settings or Settings())
        self.question_name_map = {}
        self.__records = DatasetRecords(client=self._client, dataset=self)
        self._sync(model=self._model)

    @property
    def records(self) -> "DatasetRecords":
        if not self.is_published:
            raise DatasetNotPublished("Cannot access records before publishing the dataset. Call `publish` first.")
        return self.__records

    @property
    def is_published(self) -> bool:
        return self._model.status == "ready"

    @property
    def settings(self) -> Settings:
        return self._settings

    @settings.setter
    def settings(self, value: Settings) -> None:
        self.__define_settings(settings=value)

    @property
    def fields(self) -> list:
        return self._settings.fields

    @property
    def questions(self) -> list:
        return self._settings.questions

    @property
    def guidelines(self) -> str:
        return self._settings.guidelines

    @guidelines.setter
    def guidelines(self, value: str) -> None:
        self._settings.guidelines = value

    @property
    def allow_extra_metadata(self) -> bool:
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

        self.__define_settings(settings=settings)
        settings.create()

        if publish:
            self.__publish()

        return self.get()

    def __define_settings(
        self,
        settings: Settings,
    ) -> None:
        """Populate the dataset object with settings"""
        settings._dataset = self
        self._settings = settings

    def __create(self) -> None:
        response_model = self._api.create(self._model)
        self._sync(response_model)

    def __publish(self) -> None:
        if not self.is_published:
            response_model = self._api.publish(dataset_id=self._model.id)
            self._sync(response_model)
