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
from typing import Optional, Literal
from uuid import UUID, uuid4

from argilla_sdk.client import Argilla
from argilla_sdk._models import DatasetModel
from argilla_sdk._resource import Resource
from argilla_sdk.datasets._dataset_records import DatasetRecords
from argilla_sdk.datasets._exceptions import DatasetNotPublished
from argilla_sdk.settings import Settings
from argilla_sdk._models import DatasetModel


if TYPE_CHECKING:
    from argilla_sdk._api._datasets import DatasetsAPI

__all__ = ["Dataset"]


class Dataset(Resource):
    """Class for interacting with Argilla Datasets"""

    def __init__(
        self,
        name: Optional[str] = None,
        status: Literal["draft", "ready"] = "draft",
        workspace_id: Optional[UUID] = None,
        settings: Settings = Settings(),
        client: Optional["Argilla"] = Argilla(),
        id: Optional[UUID] = uuid4(),
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
                workspace_id=workspace_id,
                id=id,
            )
        else:
            self._model = _model
        self._sync(model=self._model)
        self.__define_settings(settings=settings)
        self.__published = False

    @property
    def records(self) -> "DatasetRecords":
        if not self.__published:
            raise DatasetNotPublished("Cannot access records before publishing the dataset. Call `publish` first.")
        return self.__records

    @records.setter
    def records(self, value: "DatasetRecords") -> None:
        self.__records = value

    def __define_settings(
        self,
        settings: Settings,
    ) -> None:
        """ Populate the dataset object with settings"""
        self._settings = settings
        self.guidelines = settings.guidelines
        self.fields = settings.fields
        self.questions = settings.questions
        self.allow_extra_metadata = settings.allow_extra_metadata

    def publish(self) -> None:
        self.__create()
        self.__update_remote_fields()
        self.__update_remote_questions()
        self.__publish()
        self.records = DatasetRecords(
            client=self._client,
            dataset_id=self._model.id,
            question_name_map=self.__get_remote_question_id_map(),
        )

    def get(self, **kwargs) -> "Dataset":
        self.__update_local_properties()
        self.__update_local_fields()
        self.__update_local_questions()
        return self

    #####################
    #  Utility methods  #
    #####################

    def __create(self) -> None:
        response_model = self._api.create(dataset=self._model)
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
        return question_name_map
