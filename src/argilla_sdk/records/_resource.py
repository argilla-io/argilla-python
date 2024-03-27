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

    def __init__(
        self,
        fields: Dict[str, Union[str, None]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        vectors: Optional[Dict[str, List[float]]] = None,
        responses: Optional[List[Response]] = None,
        suggestions: Optional[Union[Tuple[Suggestion], List[Suggestion]]] = None,
        external_id: Optional[str] = None,
        id: Optional[str] = None,
    ):
        self._model = RecordModel(
            fields=fields,
            metadata=metadata,
            vectors=vectors,
            external_id=external_id or uuid4(),
            id=id or uuid4(),
        )
        self.__responses = RecordResponses(responses=responses)
        self.__suggestions = RecordSuggestions(suggestions=suggestions)
        self._model.responses = self.__responses.models
        self._model.suggestions = self.__suggestions.models

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
    def responses(self) -> "RecordResponses":
        return self.__responses

    @property
    def suggestions(self) -> "RecordSuggestions":
        return self.__suggestions

    ############################
    # Public methods
    ############################

    def serialize(self) -> RecordModel:
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
    def from_model(cls, model: RecordModel) -> "Record":
        return cls(
            id=model.id,
            external_id=model.external_id,
            fields=model.fields,
            metadata=model.metadata,
            vectors=model.vectors,
            responses=[Response.from_model(response) for response in model.responses],
            suggestions=[Suggestion.from_model(suggestion) for suggestion in model.suggestions],
        )


class RecordResponses:
    def __init__(self, responses: List[Response]) -> None:
        self.__responses = responses or []

    @property
    def models(self) -> List[ResponseModel]:
        return [response._model for response in self.__responses]

    def __iter__(self):
        return iter(self.__responses)

    def __getitem__(self, index):
        return self.__responses[index]


class RecordSuggestions:
    def __init__(self, suggestions: List[Suggestion]) -> None:
        self.__suggestions = suggestions or []

    @property
    def models(self) -> List[SuggestionModel]:
        return [suggestion._model for suggestion in self.__suggestions]

    def __iter__(self):
        return iter(self.__suggestions)

    def __getitem__(self, index):
        return self.__suggestions[index]
