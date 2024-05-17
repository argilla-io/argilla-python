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
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Optional, Tuple, Union, Iterable
from uuid import UUID, uuid4

from argilla_sdk._models import (
    MetadataModel,
    RecordModel,
    UserResponseModel,
    SuggestionModel,
    VectorModel,
    MetadataValue,
)
from argilla_sdk._resource import Resource
from argilla_sdk.responses import Response, UserResponse
from argilla_sdk.settings import QuestionType, VectorField, TextField, MetadataType
from argilla_sdk.suggestions import Suggestion
from argilla_sdk.vectors import Vector

if TYPE_CHECKING:
    from argilla_sdk.datasets import Dataset


class Record(Resource):
    """The class for interacting with Argilla Records. A `Record` is a single sample
    in a dataset. Records receives feedback in the form of responses and suggestions.
    Records contain fields, metadata, and vectors.

    Attributes:
        fields (RecordFields): The fields of the record.
        metadata (RecordMetadata): The metadata of the record.
        vectors (RecordVectors): The vectors of the record.
        responses (RecordResponses): The responses of the record.
        suggestions (RecordSuggestions): The suggestions of the record.
        external_id (str): The external id of the record.
        id (str): The id of the record.
        dataset (Dataset): The dataset to which the record belongs.
    """

    _model: RecordModel

    def __init__(
        self,
        fields: Dict[str, Union[str, None]] = None,
        metadata: Optional[Dict[str, MetadataValue]] = None,
        vectors: Optional[List[Vector]] = None,
        responses: Optional[List[Response]] = None,
        suggestions: Optional[List[Suggestion]] = None,
        external_id: Optional[str] = None,
        id: Optional[UUID] = None,
        _dataset: Optional["Dataset"] = None,
    ):
        """Initializes a Record with fields, metadata, vectors, responses, suggestions, external_id, and id.
        Records are typically defined as flat dictionary objects with fields, metadata, vectors, responses, and suggestions
        and passed to Dataset.DatasetRecords.add() as a list of dictionaries.

        Args:
            fields: A dictionary of fields for the record.
            metadata: A dictionary of metadata for the record.
            vectors: A dictionary of vectors for the record.
            responses: A list of Response objects for the record.
            suggestions: A list of Suggestion objects for the record.
            external_id: An external id for the record.
            id: An id for the record.
            _dataset: The dataset object to which the record belongs.
        """
        self._dataset = _dataset

        self._model = RecordModel(
            fields=fields,
            external_id=external_id or uuid4(),
            id=id,
        )
        # TODO: All this code blocks could be define as property setters
        # Initialize the fields
        self.__fields = RecordFields(fields=self._model.fields)
        # Initialize the vectors
        self.__vectors = RecordVectors(vectors=vectors, record=self)
        # Initialize the metadata
        self.__metadata = RecordMetadata(metadata=metadata)
        self.__responses = RecordResponses(responses=responses, record=self)
        self.__suggestions = RecordSuggestions(suggestions=suggestions, record=self)

    def __repr__(self) -> str:
        return (
            f"Record(id={self.id},fields={self.fields},metadata={self.metadata},"
            f"suggestions={self.suggestions},responses={self.responses})"
        )

    ############################
    # Properties
    ############################

    @property
    def dataset(self) -> "Dataset":
        return self._dataset

    @dataset.setter
    def dataset(self, value: "Dataset") -> None:
        self._dataset = value

    @property
    def external_id(self) -> str:
        return self._model.external_id

    @external_id.setter
    def external_id(self, value: str) -> None:
        self._model.external_id = str(value)

    @property
    def fields(self) -> "RecordFields":
        return self.__fields

    @property
    def responses(self) -> "RecordResponses":
        return self.__responses

    @property
    def suggestions(self) -> "RecordSuggestions":
        return self.__suggestions

    @property
    def metadata(self) -> "RecordMetadata":
        return self.__metadata

    @property
    def vectors(self) -> "RecordVectors":
        return self.__vectors

    ############################
    # Public methods
    ############################

    def api_model(self) -> RecordModel:
        return RecordModel(
            id=self.id,
            external_id=self.external_id,
            fields=self.fields.to_dict(),
            metadata=self.metadata.models,
            vectors=self.vectors.models,
            responses=self.responses.api_models(),
            suggestions=self.suggestions.api_models(),
        )

    def serialize(self) -> Dict[str, Any]:
        """Serializes the Record to a dictionary for interaction with the API"""
        serialized_model = self._model.model_dump()
        serialized_suggestions = [suggestion.serialize() for suggestion in self.__suggestions]
        serialized_responses = [response.serialize() for response in self.__responses]
        serialized_model["responses"] = serialized_responses
        serialized_model["suggestions"] = serialized_suggestions
        return serialized_model

    @classmethod
    def from_dict(
        cls,
        dataset: "Dataset",
        data: dict,
        mapping: Optional[Dict[str, str]] = None,
        user_id: Optional[UUID] = None,
    ) -> "Record":
        """Converts a record dictionary to a Record object.
        Args:
            dataset: The dataset object to which the record belongs.
            data: A dictionary representing the record.
            mapping: A dictionary mapping source data keys to Argilla fields, questions, and ids.
            user_id: The user id to associate with the record responses.
        Returns:
            A Record object.
        """
        fields: Dict[str, str] = {}
        responses: List[Response] = []
        record_id: Optional[str] = None
        suggestion_values = defaultdict(dict)
        vectors: List[Vector] = []
        metadata: Dict[str, MetadataValue] = {}

        schema = dataset.schema

        for attribute, value in data.items():
            schema_item = schema.get(attribute)
            attribute_type = None
            sub_attribute = None

            # Map source data keys using the mapping
            if mapping and attribute in mapping:
                attribute_mapping = mapping.get(attribute)
                attribute_mapping = attribute_mapping.split(".")
                attribute = attribute_mapping[0]
                schema_item = schema.get(attribute)
                if len(attribute_mapping) > 1:
                    attribute_type = attribute_mapping[1]
                if len(attribute_mapping) > 2:
                    sub_attribute = attribute_mapping[2]
            elif schema_item is mapping is None and attribute != "id":
                warnings.warn(
                    message=f"""Record attribute {attribute} is not in the schema so skipping. 
                        Define a mapping to map source data fields to Argilla Fields, Questions, and ids
                        """
                )
                continue

            if attribute == "id":
                record_id = value
                continue

            # Add suggestion values to the suggestions
            if attribute_type == "suggestion":
                if sub_attribute in ["score", "agent"]:
                    suggestion_values[attribute][sub_attribute] = value

                elif sub_attribute is None:
                    suggestion_values[attribute].update(
                        {"value": value, "question_name": attribute, "question_id": schema_item.id}
                    )
                else:
                    warnings.warn(
                        message=f"Record attribute {sub_attribute} is not a valid suggestion sub_attribute so skipping."
                    )
                continue

            # Assign the value to question, field, or response based on schema item
            if isinstance(schema_item, TextField):
                fields[attribute] = value
            elif isinstance(schema_item, QuestionType) and attribute_type == "response":
                responses.append(Response(question_name=attribute, value=value, user_id=user_id))
            elif isinstance(schema_item, QuestionType) and attribute_type is None:
                suggestion_values[attribute].update(
                    {"value": value, "question_name": attribute, "question_id": schema_item.id}
                )
            elif isinstance(schema_item, VectorField):
                vectors.append(Vector(name=attribute, values=value))
            elif isinstance(schema_item, MetadataType):
                metadata[attribute] = value
            else:
                warnings.warn(message=f"""Record attribute {attribute} is not in the schema or mapping so skipping.""")
                continue

        suggestions = [Suggestion(**suggestion_dict) for suggestion_dict in suggestion_values.values()]

        return cls(
            id=record_id,
            fields=fields,
            suggestions=suggestions,
            responses=responses,
            vectors=vectors,
            metadata=metadata,
            external_id=data.get("external_id") or record_id,
            _dataset=dataset,
        )

    def to_dict(self) -> Dict[str, Dict]:
        """Converts a Record object to a dictionary for export.
        Returns:
            A dictionary representing the record where the keys are "fields",
            "metadata", "suggestions", and "responses". Each field and question is
            represented as a key-value pair in the dictionary of the respective key. i.e.
            `{"fields": {"prompt": "...", "response": "..."}, "responses": {"rating": "..."},
        """
        fields = self.fields.to_dict()
        metadata = self.metadata
        suggestions = self.suggestions.to_dict()
        responses = self.responses.to_dict()
        record_dict = {
            "fields": fields,
            "metadata": metadata,
            "suggestions": suggestions,
            "responses": responses,
            "external_id": self.external_id,
        }
        return record_dict

    @classmethod
    def from_model(cls, model: RecordModel, dataset: "Dataset") -> "Record":
        """Converts a RecordModel object to a Record object.
        Args:
            model: A RecordModel object.
            dataset: The dataset object to which the record belongs.
        Returns:
            A Record object.
        """
        return cls(
            id=model.id,
            external_id=model.external_id,
            fields=model.fields,
            metadata={meta.name: meta.value for meta in model.metadata},
            vectors=[Vector.from_model(model=vector) for vector in model.vectors],
            # Responses and their models are not aligned 1-1.
            responses=[
                response
                for response_model in model.responses
                for response in UserResponse.from_model(response_model, dataset=dataset)
            ],
            suggestions=[Suggestion.from_model(model=suggestion, dataset=dataset) for suggestion in model.suggestions],
            _dataset=dataset,
        )


class RecordFields:
    """This is a container class for the fields of a Record.
    It allows for accessing fields by attribute and iterating over them.
    """

    def __init__(self, fields: Dict[str, Union[str, None]]) -> None:
        self.__fields = fields or {}
        for key, value in self.__fields.items():
            setattr(self, key, value)

    def __getitem__(self, key: str) -> Optional[str]:
        return self.__fields.get(key)

    def __iter__(self):
        return iter(self.__fields)

    def to_dict(self) -> Dict[str, Union[str, None]]:
        return self.__fields

    def __repr__(self) -> str:
        return self.to_dict().__repr__()


class RecordResponses(Iterable[Response]):
    """This is a container class for the responses of a Record.
    It allows for accessing responses by attribute and iterating over them.
    A record can have multiple responses per question so we set the response
    in a list default dictionary with the question name as the key.
    """

    def __init__(self, responses: List[Response], record: Record) -> None:
        self.record = record
        self.__responses_by_question_name = defaultdict(list)

        self.__responses = responses or []
        for response in self.__responses:
            response.record = self.record
            self.__responses_by_question_name[response.question_name].append(response)

    def api_models(self) -> List[UserResponseModel]:
        """Returns a list of ResponseModel objects."""

        responses_by_user_id = defaultdict(list)
        for response in self.__responses:
            responses_by_user_id[response.user_id].append(response)

        return [
            UserResponse(user_id=user_id, answers=responses, _record=self.record).api_model()
            for user_id, responses in responses_by_user_id.items()
        ]

    def __iter__(self):
        return iter(self.__responses)

    def __getitem__(self, index: int):
        return self.__responses[index]

    def __getattr__(self, name) -> List[Response]:
        return self.__responses_by_question_name[name]

    def to_dict(self) -> Dict[str, List[Dict]]:
        """Converts the responses to a dictionary.
        Returns:
            A dictionary of responses.
        """
        response_dict = defaultdict(list)
        for response in self.__responses:
            response_dict[response.question_name].append({"value": response.value, "user_id": response.user_id})
        return response_dict

    def __repr__(self) -> str:
        return {k: [{"value": v["value"]} for v in values] for k, values in self.to_dict().items()}.__repr__()


class RecordSuggestions(Iterable[Suggestion]):
    """This is a container class for the suggestions of a Record.
    It allows for accessing suggestions by attribute and iterating over them.
    """

    def __init__(self, suggestions: List[Suggestion], record: Record) -> None:
        self.record = record

        self.__suggestions = suggestions or []
        for suggestion in self.__suggestions:
            suggestion.record = self.record
            setattr(self, suggestion.question_name, suggestion)

    def api_models(self) -> List[SuggestionModel]:
        return [suggestion.api_model() for suggestion in self.__suggestions]

    def __iter__(self):
        return iter(self.__suggestions)

    def __getitem__(self, index: int):
        return self.__suggestions[index]

    def to_dict(self) -> Dict[str, List[str]]:
        """Converts the suggestions to a dictionary.
        Returns:
            A dictionary of suggestions.
        """
        suggestion_dict: dict = {}
        for suggestion in self.__suggestions:
            suggestion_dict[suggestion.question_name] = {
                "value": suggestion.value,
                "score": suggestion.score,
                "agent": suggestion.agent,
            }
        return suggestion_dict

    def __repr__(self) -> str:
        return self.to_dict().__repr__()


class RecordVectors:
    """This is a container class for the vectors of a Record.
    It allows for accessing suggestions by attribute and iterating over them.
    """

    def __init__(self, vectors: List[Vector], record: Record) -> None:
        self.__vectors = vectors or []
        self.record = record
        for vector in self.__vectors:
            setattr(self, vector.name, vector.values)

    @property
    def models(self) -> List[VectorModel]:
        return [vector.api_model() for vector in self.__vectors]

    def to_dict(self) -> Dict[str, List[float]]:
        """Converts the vectors to a dictionary.
        Returns:
            A dictionary of vectors.
        """
        return {vector.name: vector.values for vector in self.__vectors}

    def __repr__(self) -> str:
        return {vector.name: f"{len(vector.values)}" for vector in self.__vectors}.__repr__()


class RecordMetadata:
    """This is a container class for the metadata of a Record."""

    __metadata_map: Dict[str, MetadataValue]
    __metadata_models: List[MetadataModel]

    def __init__(self, metadata: Optional[Dict[str, MetadataValue]] = None) -> None:
        self.__metadata_map = metadata or {}
        for key, value in self.__metadata_map.items():
            setattr(self, key, value)
        self.__metadata_models = [MetadataModel(name=key, value=value) for key, value in self.__metadata_map.items()]

    @property
    def models(self) -> List[MetadataModel]:
        return self.__metadata_models

    def to_dict(self) -> Dict[str, MetadataValue]:
        return {meta.name: meta.value for meta in self.__metadata_models}

    def __iter__(self) -> Iterable[MetadataModel]:
        return iter(self.__metadata_models)

    def __getitem__(self, key: str) -> MetadataValue:
        return self.__metadata_map[key]

    def __len__(self) -> int:
        return len(self.__metadata_models)

    def __repr__(self) -> Generator:
        return self.to_dict().__repr__()
