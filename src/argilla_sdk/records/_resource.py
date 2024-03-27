from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union, Tuple
from uuid import uuid4

from argilla_sdk._models import RecordModel, SuggestionModel, ResponseModel
from argilla_sdk._resource import Resource
from argilla_sdk.response import Response
from argilla_sdk.suggestion import Suggestion
from argilla_sdk.records._utils import dict_to_record_model

if TYPE_CHECKING:
    from argilla_sdk.datasets import Dataset


class Record(Resource):
    """
    This record would be used for fetching records in a custom schema.
    Let's see this when we tackle the fetch records endpoint
    """

    # TODO: Once the RecordsAPI is implemented, this class could be adapted to extend a Resource class and
    #  provide mechanisms to update and delete single records.

    _model: RecordModel

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
        """
        Converts a record dictionary to a Record object.

        Dataset is used to map the question ids to question names. In the future, this could be done in the record resource
        by passing the linked dataset to the record object, or fetching question names from the API.
        """
        model = dict_to_record_model(data=record_as_dict, schema=dataset.schema)
        return cls.from_model(model=model)

    @classmethod
    def from_model(cls, model: RecordModel, dataset: Optional["Dataset"] = None) -> "Record":
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


class RecordFields:
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
