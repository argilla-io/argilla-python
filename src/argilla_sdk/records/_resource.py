import warnings
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union, Sequence, Tuple
from uuid import UUID, uuid4

from argilla_sdk._models import RecordModel, SuggestionModel, ResponseModel
from argilla_sdk._resource import Resource
from argilla_sdk.response import Response
from argilla_sdk.suggestion import Suggestion
from argilla_sdk.client import Argilla
from argilla_sdk.settings import FieldType, QuestionType

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
        model = _dict_to_record_model(data=record_as_dict, schema=dataset.schema)
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


class DatasetRecordsIterator:
    """This class is used to iterate over records in a dataset"""

    def __init__(
        self,
        dataset: "Dataset",
        client: "Argilla",
        start_offset: int = 0,
        batch_size: Optional[int] = None,
        with_suggestions: bool = False,
    ):
        self.__dataset = dataset
        self.__client = client
        self.__records_batch = []
        self.__offset = start_offset or 0
        self.__batch_size = batch_size or 100
        self.__with_suggestions = with_suggestions

    def __iter__(self):
        return self

    def __next__(self) -> Record:
        if not self._has_local_records():
            self._fetch_next_batch()
            if not self._has_local_records():
                raise StopIteration()
        return self._next_record()

    def _next_record(self) -> Record:
        return self.__records_batch.pop(0)

    def _has_local_records(self) -> bool:
        return len(self.__records_batch) > 0

    def _fetch_next_batch(self) -> None:
        self.__records_batch = list(self._list())
        self.__offset += len(self.__records_batch)

    def _list(self) -> Sequence[Record]:
        record_models = self.__client.api.records.list(
            dataset_id=self.__dataset.id,
            limit=self.__batch_size,
            offset=self.__offset,
            with_responses=False,
            with_suggestions=self.__with_suggestions,
        )
        for record_model in record_models:
            yield Record.from_model(model=record_model)


class DatasetRecords(Resource):
    """
    This class is used to work with records from a dataset.

    The responsibility of this class is to provide an interface to interact with records in a dataset,
    by adding, updating, fetching, querying, and deleting records.

    """

    def __init__(self, client: "Argilla", dataset: "Dataset"):
        self.__client = client
        self.__dataset = dataset

    def __iter__(self):
        return DatasetRecordsIterator(self.__dataset, self.__client)

    def __call__(self, batch_size: Optional[int] = 100, start_offset: int = 0, with_suggestions: bool = True):
        return DatasetRecordsIterator(
            self.__dataset,
            self.__client,
            batch_size=batch_size,
            start_offset=start_offset,
            with_suggestions=with_suggestions,
        )

    def add(self, records: Union[dict, List[dict]]) -> None:
        """
        Add records to a dataset
        """

        # TODO: Once we have implemented the new records bulk endpoint, this method should use it
        #   and return the response from the API.
        records = self.__cast_return_records(records)
        record_schema = self.__dataset.schema
        serialized_records = [_dict_to_record_model(r, record_schema).model_dump() for r in records]

        self.__client.api.records.create_many(dataset_id=self.__dataset.id, records=serialized_records)

    def update(self, records):
        """Update records in a dataset"""
        records = self.__cast_return_records(records)
        record_schema = self.__dataset.schema
        serialized_records = [_dict_to_record_model(r, record_schema) for r in records]
        records_to_update, records_to_add = self.__align_split_records(serialized_records)
        self.log(f"Updating {len(records_to_update)} records.")
        self.log(f"Adding {len(records_to_add)} records.")
        if len(records_to_update) > 0:
            self.__client.api.records.update_many(dataset_id=self.__dataset.id, records=records_to_update)
            self.__update_record_responses(records=records_to_update)
        else:
            self.log("No existing records founds to update.")
        if len(records_to_add) > 0:
            self.__client.api.records.create_many(dataset_id=self.__dataset.id, records=records_to_add)
        records = self.__list_records_from_server()
        self.__records = [Record.from_model(model=record) for record in records]
        return self.__records

    def __list_records_from_server(self):
        """Get records from the server"""
        return self.__client.api.records.list(dataset_id=self.__dataset.id, with_suggestions=True, with_responses=True)

    def __align_split_records(self, records) -> Tuple[List[RecordModel], List[RecordModel]]:
        """Align records with server ids"""
        server_records = self.__list_records_from_server()
        server_records_map = {record.external_id: str(record.id) for record in server_records}
        records_to_update = []
        records_to_add = []
        for n, record in enumerate(records):
            record = record.model_dump()
            external_id = record.get("external_id")
            record_id = record.get("id")
            if external_id is not None and external_id in server_records_map:
                # the record has an external_id and is already in the server
                record["id"] = server_records_map.get(external_id)
                records_to_update.append(record)
            elif record_id in server_records_map.values():
                # the record is already in the server but we don't have the external_id
                records_to_update.append(record)
            else:
                # we don't have the record in the server
                records_to_add.append(record)
        return records_to_update, records_to_add

    def __update_record_responses(self, records):
        """Filter records with updated responses"""
        for record in records:
            self.__client.api.records.create_record_responses(record)

    def __cast_return_records(self, records: Union[dict, List[dict]]) -> List[dict]:
        """Cast the return records to a list of records"""
        single_record = isinstance(records, dict)
        if single_record:
            records = [records]
        return records


def _dict_to_record_model(data: dict, schema: Dict[str, Any]) -> RecordModel:
    """Converts a Record object to a record dictionary."""

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
