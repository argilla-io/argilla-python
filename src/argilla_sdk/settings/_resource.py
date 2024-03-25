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
from functools import cached_property
from typing import List, Optional, TYPE_CHECKING, Dict, Union
from uuid import UUID

from argilla_sdk._models import TextFieldModel, TextQuestionModel
from argilla_sdk.client import Argilla
from argilla_sdk.settings._field import FieldType
from argilla_sdk.settings._question import QuestionType

if TYPE_CHECKING:
    from argilla_sdk.datasets import Dataset


__all__ = ["Settings"]


class Settings:
    """Settings class for Argilla Datasets. This class is used to define the representation of a Dataset within the UI."""

    def __init__(
        self,
        fields: Optional[List[FieldType]] = None,
        questions: Optional[List[QuestionType]] = None,
        guidelines: Optional[str] = None,
        allow_extra_metadata: bool = False,
        client: Argilla = Argilla(),
        _dataset: Optional["Dataset"] = None,
    ) -> None:
        """
        Args:
            guidelines (str): A string containing the guidelines for the Dataset.
            fields (List[TextField]): A list of TextField objects that represent the fields in the Dataset.
            questions (List[Union[LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion, RatingQuestion]]): A list of Question objects that represent the questions in the Dataset.
            allow_extra_metadata (bool): A boolean that determines whether or not extra metadata is allowed in the Dataset. Defaults to False.
        """
        if fields is None:
            fields = []
        if questions is None:
            questions = []

        self.__guidelines = self.__process_guidelines(guidelines)
        self.__allow_extra_metadata = allow_extra_metadata
        self.__questions = questions
        self.__fields = fields
        self._dataset = _dataset

        self.__client = client

    #####################
    # Properties        #
    #####################

    @property
    def fields(self) -> List[FieldType]:
        return self.__fields

    @fields.setter
    def fields(self, fields: List[FieldType]):
        self.__fields = fields

    @property
    def questions(self) -> List[QuestionType]:
        return self.__questions

    @questions.setter
    def questions(self, questions: List[QuestionType]):
        self.__questions = questions

    @property
    def guidelines(self) -> str:
        return self.__guidelines

    @guidelines.setter
    def guidelines(self, guidelines: str):
        self.__guidelines = self.__process_guidelines(guidelines)
        if self._dataset:
            self._dataset._model.guidelines = guidelines

    @property
    def allow_extra_metadata(self) -> bool:
        return self.__allow_extra_metadata

    @allow_extra_metadata.setter
    def allow_extra_metadata(self, value: bool):
        self.__allow_extra_metadata = value
        if self._dataset:
            self._dataset._model.allow_extra_metadata = value

    @property
    def dataset(self) -> "Dataset":
        return self._dataset

    @dataset.setter
    def dataset(self, dataset: "Dataset"):
        self._dataset = dataset
        self.__allow_extra_metadata = dataset._model.allow_extra_metadata
        self.__guidelines = dataset._model.guidelines

    @cached_property
    def schema(self) -> dict:
        schema_dict = {}

        for field in self.fields:
            schema_dict[field.name] = field

        for question in self.questions:
            schema_dict[question.name] = question

        return schema_dict

    @cached_property
    def schema_by_id(self) -> Dict[UUID, Union[FieldType, QuestionType]]:
        return {
            v.id: v
            for v in self.schema.values()
        }

    #####################
    #  Public methods   #
    #####################

    def create(self) -> "Settings":
        self.__upsert_fields()
        self.__upsert_questions()
        self.__update_dataset_related_attributes()
        return self

    def question_by_id(self, question_id: UUID) -> QuestionType:
        property = self.schema_by_id.get(question_id)
        if isinstance(property, QuestionType):
            return property
        raise ValueError(f"Question with id {question_id} not found")

    def __update_dataset_related_attributes(self):
        # This flow may be a bit weird, but it's the only way to update the dataset related attributes
        # Everything is point that we should have several settings-related endpoints in the API to handle this.
        # POST /api/v1/datasets/{dataset_id}/settings
        # {
        #   "guidelines": ....,
        #   "allow_extra_metadata": ....,
        # }
        # But this is not implemented yet, so we need to update the dataset model directly
        ds_model = self._dataset._model

        ds_model.guidelines = self.guidelines
        ds_model.allow_extra_metadata = self.allow_extra_metadata

    def __upsert_questions(self) -> None:
        for question in self.__questions:
            question_model = self.__client.api.questions.create(dataset_id=self._dataset.id, question=question._model)
            question._model = question_model

    def __upsert_fields(self) -> None:
        for field in self.__fields:
            field_model = self.__client.api.fields.create(dataset_id=self._dataset.id, field=field._model)
            field._model = field_model

    def serialize(self):
        return {
            "guidelines": self.guidelines,
            "fields": self.__serialize_fields(fields=self.fields),
            "questions": self.__serialize_questions(questions=self.questions),
            "allow_extra_metadata": self.allow_extra_metadata,
        }

    def _set_dataset(self, dataset: "Dataset"):
        self._dataset = dataset
        self.__client = dataset._client

    #####################
    #  Utility methods  #
    #####################

    def __process_fields(self, fields: List[FieldType]) -> List["TextFieldModel"]:
        # TODO: Implement error handling for invalid fields
        processed_fields = [field._model for field in fields]
        return processed_fields

    def __process_questions(self, questions: List[QuestionType]) -> List["TextQuestionModel"]:
        # TODO: Implement error handling for invalid questions
        processed_questions = [question._model for question in questions]
        return processed_questions

    def __process_guidelines(self, guidelines):
        # TODO: process guidelines to be of type str or load str from file
        return guidelines

    def __serialize_fields(self, fields):
        return [field.serialize() for field in fields]

    def __serialize_questions(self, questions):
        return [question.serialize() for question in questions]
