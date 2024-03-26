import warnings
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union, Sequence, Tuple
from uuid import UUID, uuid4

from argilla_sdk._models import RecordModel, SuggestionModel
from argilla_sdk._resource import Resource
from argilla_sdk.client import Argilla
from argilla_sdk.settings import FieldType, QuestionType

if TYPE_CHECKING:
    from argilla_sdk.datasets import Dataset


class Record:
    """
    This record would be used for fetching records in a custom schema.
    Let's see this when tackle the fetch records endpoint
    """

    # TODO: Once the RecordsAPI is implemented, this class could be adapted to extend a Resource class and
    #  provide mechanisms to update and delete single records.

    id: Optional[UUID]
    external_id: Optional[str]

    _model: RecordModel

    def __init__(self, model, **kwargs):
        self.id = None
        self.external_id = None
        self.__dict__.update(kwargs)
        self._model = model
        self.suggestions = self._model.suggestions

    def __repr__(self):
        record_body = ",".join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"<Record {record_body}>"


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
        records = self.__client.api.records.list(
            self.__dataset.id,
            limit=self.__batch_size,
            offset=self.__offset,
            with_responses=False,
            with_suggestions=self.__with_suggestions,
        )
        for record in records:
            yield _record_model_to_record(self.__dataset, record)


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
        records = _cast_return_records(records)
        record_schema = self.__dataset.schema
        serialized_records = [_dict_to_record_model(r, record_schema).model_dump() for r in records]

        self.__client.api.records.create_many(dataset_id=self.__dataset.id, records=serialized_records)

    def update(self, records):
        """Update records in a dataset"""
        records = _cast_return_records(records)
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
        self.__records = [_record_model_to_record(self.__dataset, record) for record in records]
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


def _cast_return_records(records: Union[dict, List[dict]]) -> List[dict]:
    single_record = isinstance(records, dict)
    if single_record:
        records = [records]
    return records


def _record_model_to_record(dataset: "Dataset", model: RecordModel) -> Record:
    """
    Converts a record dictionary to a Record object.

    Dataset is used to map the question ids to question names. In the future, this could be done in the record resource
    by passing the linked dataset to the record object, or fetching question names from the API.
    """
    kwargs = {
        **model.fields,
        **model.metadata,
        **{
            dataset.settings.question_by_id(suggestion.question_id).name: suggestion.value
            for suggestion in model.suggestions
        },
    }
    return Record(id=model.id, external_id=model.external_id, model=model, **kwargs)


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
