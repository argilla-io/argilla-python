import warnings
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union, Tuple
from uuid import uuid4

from argilla_sdk._models import RecordModel, SuggestionModel, ResponseModel
from argilla_sdk._resource import Resource
from argilla_sdk.response import Response
from argilla_sdk.settings import FieldType, QuestionType
from argilla_sdk.suggestion import Suggestion


if TYPE_CHECKING:
    from argilla_sdk.datasets import Dataset


class Record(Resource):
    """This is the class for interacting with Argilla Records."""

    _model: RecordModel

    # TODO: Once the RecordsAPI is implemented, this class could
    # be adapted to extend a Resource class and
    # provide mechanisms to update and delete single records.
    # This record would be used for fetching records in a custom schema.
    # Let's see this when we tackle the fetch records endpoint

    def __init__(
        self,
        fields: Dict[str, Union[str, None]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        vectors: Optional[Dict[str, List[float]]] = None,
        responses: Optional[List[Response]] = None,
        suggestions: Optional[Union[Tuple[Suggestion], List[Suggestion]]] = None,
        external_id: Optional[str] = None,
        id: Optional[str] = None,
        dataset: Optional["Dataset"] = None,
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
            dataset: The dataset object to which the record belongs.
        """
        self._model = RecordModel(
            fields=fields,
            metadata=metadata,
            vectors=vectors,
            external_id=external_id or uuid4(),
            id=id or uuid4(),
        )
        self.__responses = RecordResponses(responses=responses, dataset=dataset)
        self.__suggestions = RecordSuggestions(suggestions=suggestions, dataset=dataset)
        self._model.responses = self.__responses.models
        self._model.suggestions = self.__suggestions.models
        # TODO: This should be done in the RecordModel class as above
        self.__fields = RecordFields(fields=self._model.fields)

    def __repr__(self):
        record_body = ",".join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"<Record {record_body}>"

    ############################
    # Properties
    ############################

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

    ############################
    # Public methods
    ############################

    def serialize(self) -> Dict[str, Any]:
        serialized_model = self._model.model_dump()
        serialized_suggestions = [suggestion.model_dump() for suggestion in self.__suggestions.models]
        serialized_responses = [response.model_dump() for response in self.__responses.models]
        serialized_model["responses"] = serialized_responses
        serialized_model["suggestions"] = serialized_suggestions
        return serialized_model

    @classmethod
    def from_dict(cls, dataset: "Dataset", record_as_dict: Dict) -> "Record":
        """Converts a record dictionary to a Record object.
        Args:
            dataset: The dataset object to which the record belongs.
            record_as_dict: A dictionary representing the record.
        Returns:
            A Record object.
        """
        model = cls.__flat_dict_to_record_model(data=record_as_dict, schema=dataset.schema)
        return cls.from_model(model=model)

    @classmethod
    def from_model(cls, model: RecordModel, dataset: Optional["Dataset"] = None) -> "Record":
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
            metadata=model.metadata,
            vectors=model.vectors,
            responses=[Response.from_model(model=response) for response in model.responses],
            suggestions=[Suggestion.from_model(model=suggestion) for suggestion in model.suggestions],
            dataset=dataset,
        )

    ############################
    # Utility methods
    ############################

    @staticmethod
    def __flat_dict_to_record_model(data: dict, schema: Dict[str, Any]) -> RecordModel:
        """Converts a flat Record-like dictionary object to a RecordModel.
        Args:
            data: A dictionary representing the record with flat attributes.
            schema: The schema of the dataset to which the record belongs.
        Returns:
            A RecordModel object.
        """

        fields = {}
        suggestions = []

        for attribute, value in data.items():
            if attribute not in schema:
                warnings.warn(f"Record attribute {attribute} is not in the schema. Skipping.")
                continue

            schema_item = schema.get(attribute)
            if isinstance(schema_item, FieldType):
                fields[attribute] = value
            elif isinstance(schema_item, QuestionType):
                suggestion = SuggestionModel(value=value, question_id=schema_item.id, question_name=attribute)
                suggestions.append(suggestion.model_dump())
            else:
                warnings.warn(f"Property {attribute} is not a valid schema item. Skipping.")

        return RecordModel(
            id=data.get("id") or str(uuid4()),
            fields=fields,
            suggestions=suggestions,
            external_id=data.get("external_id"),
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

    def __repr__(self):
        return f"<RecordFields {self.__fields}>"


class RecordResponses:
    """This is a container class for the responses of a Record.
    It allows for accessing responses by attribute and iterating over them.
    """

    def __init__(self, responses: List[Response], dataset: Optional["Dataset"] = None) -> None:
        self.__responses = responses or []
        for response in self.__responses:
            if dataset is None:
                continue
            question_name = dataset.settings.question_by_id(response.question_id).name
            setattr(self, question_name, response.value)

    @property
    def models(self) -> List[ResponseModel]:
        return [response._model for response in self.__responses]

    def __iter__(self):
        return iter(self.__responses)

    def __getitem__(self, index):
        return self.__responses[index]


class RecordSuggestions:
    """This is a container class for the suggestions of a Record.
    It allows for accessing suggestions by attribute and iterating over them.
    """

    def __init__(self, suggestions: List[Suggestion], dataset: Optional["Dataset"] = None) -> None:
        self.__suggestions = suggestions or []
        for suggestion in self.__suggestions:
            if suggestion.question_name is None and dataset is None:
                continue
            question_name = dataset.settings.question_by_id(suggestion.question_id).name
            setattr(self, question_name, suggestion.value)

    @property
    def models(self) -> List[SuggestionModel]:
        return [suggestion._model for suggestion in self.__suggestions]

    def __iter__(self):
        return iter(self.__suggestions)

    def __getitem__(self, index):
        return self.__suggestions[index]
