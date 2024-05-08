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
from email import message
import os
from functools import cached_property
from typing import List, Optional, TYPE_CHECKING, Dict, Union
from uuid import UUID

from argilla_sdk._exceptions import SettingsError, ArgillaAPIError, ArgillaSerializeError
from argilla_sdk._models import TextFieldModel, TextQuestionModel, DatasetModel
from argilla_sdk._resource import Resource
from argilla_sdk.settings._field import FieldType, TextField, VectorField, field_from_model
from argilla_sdk.settings._metadata import MetadataType
from argilla_sdk.settings._question import QuestionType, question_from_model

if TYPE_CHECKING:
    from argilla_sdk.datasets import Dataset


__all__ = ["Settings"]


class Settings(Resource):
    """
    Settings class for Argilla Datasets.

    This class is used to define the representation of a Dataset within the UI.
    """

    def __init__(
        self,
        fields: Optional[List[FieldType]] = None,
        questions: Optional[List[QuestionType]] = None,
        vectors: Optional[List[VectorField]] = None,
        metadata: Optional[List[MetadataType]] = None,
        guidelines: Optional[str] = None,
        allow_extra_metadata: bool = False,
        _dataset: Optional["Dataset"] = None,
    ) -> None:
        """
        Args:
            fields (List[TextField]): A list of TextField objects that represent the fields in the Dataset.
            questions (List[Union[LabelQuestion, MultiLabelQuestion, RankingQuestion, TextQuestion, RatingQuestion]]): A list of Question objects that represent the questions in the Dataset.
            vectors (List[VectorField]): A list of VectorField objects that represent the vectors in the Dataset.
            metadata (List[MetadataField]): A list of MetadataField objects that represent the metadata in the Dataset.
            guidelines (str): A string containing the guidelines for the Dataset.
            allow_extra_metadata (bool): A boolean that determines whether or not extra metadata is allowed in the Dataset. Defaults to False.
        """
        super().__init__(client=_dataset._client if _dataset else None)

        self.__questions = questions or []
        self.__fields = fields or []
        self.__vectors = vectors or []
        self.__metadata = metadata or []

        self.__guidelines = self.__process_guidelines(guidelines)
        self.__allow_extra_metadata = allow_extra_metadata

        self._dataset = _dataset

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

    @property
    def vectors(self) -> List[VectorField]:
        return self.__vectors

    @vectors.setter
    def vectors(self, vectors: List[VectorField]):
        self.__vectors = vectors

    @property
    def metadata(self) -> List[MetadataType]:
        return self.__metadata

    @metadata.setter
    def metadata(self, metadata: List[MetadataType]):
        self.__metadata = metadata

    @property
    def allow_extra_metadata(self) -> bool:
        return self.__allow_extra_metadata

    @allow_extra_metadata.setter
    def allow_extra_metadata(self, value: bool):
        self.__allow_extra_metadata = value

    @property
    def dataset(self) -> "Dataset":
        return self._dataset

    @dataset.setter
    def dataset(self, dataset: "Dataset"):
        self._dataset = dataset
        self._client = dataset._client

    @cached_property
    def schema(self) -> dict:
        schema_dict = {}

        for field in self.fields:
            schema_dict[field.name] = field

        for question in self.questions:
            schema_dict[question.name] = question

        for vector in self.vectors:
            schema_dict[vector.name] = vector

        for metadata in self.metadata:
            schema_dict[metadata.name] = metadata

        return schema_dict

    @cached_property
    def schema_by_id(self) -> Dict[UUID, Union[FieldType, QuestionType]]:
        return {v.id: v for v in self.schema.values()}

    def validate(self) -> None:
        if not all([self.fields, self.questions]):
            message = "Fields and questions are required"
            raise SettingsError(message=message)

    #####################
    #  Public methods   #
    #####################

    def get(self) -> "Settings":
        self.__fetch_fields()
        self.__fetch_questions()
        self.__fetch_vectors()
        self.__fetch_metadata()
        self.__get_dataset_related_attributes()

        self._update_last_api_call()
        return self

    def create(self) -> "Settings":
        self.__upsert_fields()
        self.__upsert_questions()
        self.__upsert_vectors()
        self.__upsert_metadata()
        self.__update_dataset_related_attributes()

        self._update_last_api_call()
        return self

    def question_by_id(self, question_id: UUID) -> QuestionType:
        property = self.schema_by_id.get(question_id)
        if isinstance(property, QuestionType):
            return property
        raise ValueError(f"Question with id {question_id} not found")

    def __fetch_fields(self) -> List[FieldType]:
        models = self._client.api.fields.list(dataset_id=self._dataset.id)
        self.__fields = [field_from_model(model) for model in models]

        return self.__fields

    def __fetch_questions(self) -> List[QuestionType]:
        models = self._client.api.questions.list(dataset_id=self._dataset.id)
        self.__questions = [question_from_model(model) for model in models]

        return self.__questions

    def __fetch_vectors(self) -> List[VectorField]:
        models = self._client.api.vectors.list(dataset_id=self._dataset.id)
        self.__vectors = [field_from_model(model) for model in models]

        return self.__vectors

    def __fetch_metadata(self) -> List[MetadataType]:
        models = self._client.api.metadata.list(dataset_id=self._dataset.id)
        self.__metadata = [field_from_model(model) for model in models]

        return self.__metadata

    def __get_dataset_related_attributes(self):
        # This flow may be a bit weird, but it's the only way to update the dataset related attributes
        # Everything is point that we should have several settings-related endpoints in the API to handle this.
        # POST /api/v1/datasets/{dataset_id}/settings
        # {
        #   "guidelines": ....,
        #   "allow_extra_metadata": ....,
        # }
        # But this is not implemented yet, so we need to update the dataset model directly
        dataset_model = self._client.api.datasets.get(self._dataset.id)

        self.guidelines = dataset_model.guidelines
        self.allow_extra_metadata = dataset_model.allow_extra_metadata

    def __update_dataset_related_attributes(self):
        # This flow may be a bit weird, but it's the only way to update the dataset related attributes
        # Everything is point that we should have several settings-related endpoints in the API to handle this.
        # POST /api/v1/datasets/{dataset_id}/settings
        # {
        #   "guidelines": ....,
        #   "allow_extra_metadata": ....,
        # }
        # But this is not implemented yet, so we need to update the dataset model directly
        dataset_model = DatasetModel(
            id=self._dataset.id,
            name=self._dataset.name,
            guidelines=self.guidelines,
            allow_extra_metadata=self.allow_extra_metadata,
        )
        self._client.api.datasets.update(dataset_model)

    def __upsert_questions(self) -> None:
        for question in self.__questions:
            try:
                question_model = self._client.api.questions.create(
                    dataset_id=self._dataset.id, question=question._model
                )
                question._model = question_model
            except ArgillaAPIError as e:
                raise SettingsError(f"Failed to create question {question.name}") from e

    def __upsert_fields(self) -> None:
        for field in self.__fields:
            try:
                field_model = self._client.api.fields.create(dataset_id=self._dataset.id, field=field._model)
                field._model = field_model
            except ArgillaAPIError as e:
                raise SettingsError(f"Failed to create field {field.name}") from e

    def __upsert_vectors(self) -> None:
        for vector in self.__vectors:
            try:
                vector_model = self._client.api.vectors.create(dataset_id=self._dataset.id, vector=vector._model)
                vector._model = vector_model
            except ArgillaAPIError as e:
                raise SettingsError(f"Failed to create vector {vector.name}") from e

    def __upsert_metadata(self) -> None:
        for metadata in self.__metadata:
            metadata_model = self._client.api.metadata.create(
                dataset_id=self._dataset.id, metadata_field=metadata._model
            )
            metadata._model = metadata_model

    def serialize(self):
        try:
            return {
                "guidelines": self.guidelines,
                "fields": self.__serialize_fields(fields=self.fields),
                "questions": self.__serialize_questions(questions=self.questions),
                "allow_extra_metadata": self.allow_extra_metadata,
            }
        except Exception as e:
            raise ArgillaSerializeError(f"Failed to serialize the settings. {e.__class__.__name__}") from e

    #####################
    #  Utility methods  #
    #####################

    def __eq__(self, other: "Settings") -> bool:
        return self.serialize() == other.serialize()  # TODO: Create proper __eq__ methods for fields and questions

    def __process_fields(self, fields: List[FieldType]) -> List["TextFieldModel"]:
        processed_fields = []
        for field in fields:
            try:
                processed_field = field._model
            except Exception as e:
                raise SettingsError(f"Failed to process field {field.name}") from e
            processed_fields.append(processed_field)
        return processed_fields

    def __process_questions(self, questions: List[QuestionType]) -> List["TextQuestionModel"]:
        processed_questions = []
        for question in questions:
            try:
                processed_question = question._model
            except Exception as e:
                raise SettingsError(f"Failed to process question {question.name}") from e
            processed_questions.append(processed_question)
        return processed_questions

    def __process_guidelines(self, guidelines):
        """Process the guidelines, either by reading them from a file or returning the string"""

        if guidelines is None:
            return guidelines

        if not isinstance(guidelines, str):
            raise SettingsError("Guidelines must be a string or a path to a file")

        if os.path.exists(guidelines):
            with open(guidelines, "r") as file:
                return file.read()

        return guidelines

    def __serialize_fields(self, fields):
        return [field.serialize() for field in fields]

    def __serialize_questions(self, questions):
        return [question.serialize() for question in questions]

    #####################
    #  Repr Methods     #
    #####################

    def __repr__(self) -> str:
        yield "guidelines", self.guidelines
        yield "allow_extra_metadata", self.allow_extra_metadata
        yield "fields", self.fields
        yield "questions", self.questions
        yield "vectors", self.vectors
        yield "metadata", self.metadata
