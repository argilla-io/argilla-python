import warnings
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union, Sequence
from uuid import UUID

from argilla_sdk._models import RecordModel, SuggestionModel
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

    def __init__(self, **kwargs):
        self.id = None
        self.external_id = None
        self.__dict__.update(kwargs)

    def __repr__(self):
        record_body = ",".join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"<Record {record_body}>"


class DatasetRecordsIterator:
    """This class is used to iterate over records in a dataset"""

    def __init__(self, dataset: "Dataset", batch_size: Optional[int] = None):
        self.__dataset = dataset
        self.__api = dataset._client._datasets
        self.__records_batch = []
        self.__offset = 0
        self.__size = batch_size or 100

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
        self.__records_batch = list(self._list(size=self.__size, offset=self.__offset))
        self.__offset += len(self.__records_batch)

    def _list(self, size: int, offset: int) -> Sequence[Record]:
        records = self.__api.list_records(
            self.__dataset.id,
            with_responses=False,  # We skip this for now
            with_suggestions=False,  # We skip this for now
            limit=size,
            offset=offset,
        )
        for record in records:
            yield _record_model_to_record(record)


class DatasetRecords:
    """
    This class is similar to the DatasetRecords class and normally should be replaced if we validate this approach.
    The class naming is optional and just to do not break the existing code.

    The class should be renamed to DatasetRecords and the old class should be removed.

    """

    def __init__(self, client: "Argilla", dataset: "Dataset"):
        self.__client = client
        self.__dataset = dataset
        self.__datasets_api = client._datasets

    def __iter__(self):
        return DatasetRecordsIterator(self.__dataset)

    def __call__(self, batch_size: Optional[int] = 100):
        return DatasetRecordsIterator(self.__dataset, batch_size=batch_size)

    def add(self, records: Union[dict, List[dict]]) -> None:
        """
        Add records to a dataset
        """

        # TODO: Once we have implemented the new records bulk endpoint, this method should use it
        #   and return the response from the API.

        single_record = isinstance(records, dict)
        if single_record:
            records = [records]

        record_schema = self.__dataset.schema
        serialized_records = [_dict_to_record_model(r, record_schema).model_dump() for r in records]

        self.__datasets_api.create_records(dataset_id=self.__dataset.id, records=serialized_records)


def _record_model_to_record(model: RecordModel) -> Record:
    """Converts a record dictionary to a Record object."""
    kwargs = {
        **model.fields,
        **model.metadata,
        **{suggestion.question_name: suggestion.value for suggestion in model.suggestions},
    }

    return Record(id=model.id, external_id=model.external_id, **kwargs)


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
        id=data.get("id"),
        fields=fields,
        suggestions=suggestions,
        external_id=data.get("external_id"),
    )