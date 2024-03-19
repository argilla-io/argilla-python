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
from argilla_sdk.datasets._dataset_records import DatasetRecords
from argilla_sdk.datasets._exceptions import DatasetNotPublished
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
        settings: Settings = Settings(),
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
        if _model is None:
            self._model = DatasetModel(
                name=name,
                status=status,
                workspace_id=self._convert_optional_uuid(uuid=workspace_id),
                id=self._convert_optional_uuid(uuid=id),
            )
        else:
            self._model = _model
        self._sync(model=self._model)
        self.__define_settings(settings=settings)
        self.__published = False
        self.question_name_map = {}

    @property
    def records(self) -> "DatasetRecords":
        if not self.is_published:
            raise DatasetNotPublished("Cannot access records before publishing the dataset. Call `publish` first.")
        return self.__records

    @records.setter
    def records(self, value: "DatasetRecords") -> None:
        self.__records = value

    @property
    def is_published(self) -> bool:
        return self._model.status == "ready"

    def exists(self) -> bool:
        """Check if the dataset exists on the server."""
        return self._api.exists(dataset_id=self.id)

    def publish(self, settings: Union[Settings, None] = None) -> "Dataset":
        return self._configure(settings=settings or self._settings,publish=True)

    def get(self, **kwargs) -> "Dataset":
        self.__update_local_properties()
        self.__update_local_fields()
        self.__update_local_questions()
        return self

    #####################
    #  Utility methods  #
    #####################

    # we leave this method as private for now and we use the `ds.publish` one
    def _configure(self, settings: Settings, publish: bool = False) -> "Dataset":
        if not self.exists():
            self.__create()

        self.__define_settings(settings=settings)
        self.__update_remote_fields()
        self.__update_remote_questions()

        if publish:
            self.__publish()
            # This may be done in the __init__ method
            self.records = DatasetRecords(client=self._client, dataset=self)

        return self.get()

    def __define_settings(
        self,
        settings: Settings,
    ) -> None:
        """Populate the dataset object with settings"""
        self._settings = settings
        self.guidelines = settings.guidelines
        self.fields = settings.fields
        self.questions = settings.questions
        self.allow_extra_metadata = settings.allow_extra_metadata

    def __create(self) -> None:
        response_model = self._api.create(self._model)
        self._sync(response_model)

    def __publish(self) -> None:
        if not self.__published:
            response_model = self._api.publish(dataset_id=self._model.id)
            self._sync(response_model)
            self.__published = True

    def __update_remote_fields(self) -> None:
        fields = [field.model_dump() for field in self.fields]
        self._api.create_fields(dataset_id=self._model.id, fields=fields)

    def __update_remote_questions(self) -> None:
        questions = [question.model_dump() for question in self.questions]
        self._api.create_questions(dataset_id=self._model.id, questions=questions)

    def __update_local_properties(self) -> None:
        self._model = self._api.get(dataset_id=self._model.id)
        self._sync(self._model)

    def __update_local_fields(self) -> None:
        self.fields = self._api.list_fields(dataset_id=self._model.id)

    def __update_local_questions(self) -> None:
        self.questions = self._api.list_questions(dataset_id=self._model.id)

    def __get_remote_question_id_map(self) -> Dict[str, str]:
        remote_questions = self._api.list_questions(dataset_id=self._model.id)
        question_name_map = {question["name"]: question["id"] for question in remote_questions}
        self.question_name_map = question_name_map

        return question_name_map
