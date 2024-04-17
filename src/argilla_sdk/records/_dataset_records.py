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

from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union, Sequence
from uuid import UUID

from argilla_sdk._api import RecordsAPI
from argilla_sdk._models import RecordModel
from argilla_sdk._resource import Resource
from argilla_sdk.client import Argilla
from argilla_sdk.records._export import GenericExportMixin
from argilla_sdk.records._resource import Record

if TYPE_CHECKING:
    from argilla_sdk.datasets import Dataset


class DatasetRecordsIterator:
    """This class is used to iterate over records in a dataset"""

    def __init__(
        self,
        dataset: "Dataset",
        client: "Argilla",
        start_offset: int = 0,
        batch_size: Optional[int] = None,
        with_suggestions: bool = False,
        with_responses: bool = False,
    ):
        self.__dataset = dataset
        self.__client = client
        self.__records_batch = []
        self.__offset = start_offset or 0
        self.__batch_size = batch_size or 100
        self.__with_suggestions = with_suggestions
        self.__with_responses = with_responses

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
            with_responses=self.__with_responses,
            with_suggestions=self.__with_suggestions,
        )
        for record_model in record_models:
            yield Record.from_model(model=record_model, dataset=self.__dataset)


class DatasetRecords(Resource, GenericExportMixin):
    """
    This class is used to work with records from a dataset.

    The responsibility of this class is to provide an interface to interact with records in a dataset,
    by adding, updating, fetching, querying, and deleting records.

    """

    _api: RecordsAPI

    def __init__(self, client: "Argilla", dataset: "Dataset"):
        """Initializes a DatasetRecords object with a client and a dataset.
        Args:
            client: An Argilla client object.
            dataset: A Dataset object.
        """
        self.__client = client
        self.__dataset = dataset
        self._api = self.__client.api.records

    def __iter__(self):
        return DatasetRecordsIterator(self.__dataset, self.__client)

    def __call__(
        self,
        batch_size: Optional[int] = 100,
        start_offset: int = 0,
        with_suggestions: bool = True,
        with_responses: bool = True,
    ):
        return DatasetRecordsIterator(
            self.__dataset,
            self.__client,
            batch_size=batch_size,
            start_offset=start_offset,
            with_suggestions=with_suggestions,
            with_responses=with_responses,
        )

    ############################
    # Public methods
    ############################

    def add(
        self,
        records: Union[dict, List[dict]],
        mapping: Optional[Dict[str, str]] = None,
        user_id: Optional[UUID] = None,
        batch_size: int = 256,
    ) -> List[Record]:
        """
        Add new records to a dataset on the server.
        Args:
            records: A dictionary or a list of dictionaries representing the records
                     to be added to the dataset. Records are defined as dictionaries
                     with keys corresponding to the fields in the dataset schema.
        """
        record_models = self.__ingest_records(records=records, mapping=mapping, user_id=user_id)

        batch_size = self._normalize_batch_size(
            batch_size=batch_size,
            records_length=len(record_models),
            max_value=self._api.MAX_RECORDS_PER_CREATE_BULK,
        )

        created_records = []
        for batch in range(0, len(records), batch_size):
            self.log(message=f"Sending records from {batch} to {batch + batch_size}.")
            batch_records = record_models[batch : batch + batch_size]
            models = self._api.bulk_create(dataset_id=self.__dataset.id, records=batch_records)
            created_records.extend([Record.from_model(model=model, dataset=self.__dataset) for model in models])

        self.log(
            message=f"Added {len(created_records)} records to dataset {self.__dataset.name}",
            level="info",
        )

        return created_records

    def update(
        self,
        records: Union[dict, List[dict]],
        mapping: Optional[Dict[str, str]] = None,
        user_id: Optional[UUID] = None,
        batch_size: int = 256,
    ) -> List[Record]:
        """Update records in a dataset on the server using the provided records
            and matching based on the external_id or id.

        Args:
            records: A dictionary or a list of dictionaries representing the records
                     to be updated in the dataset. Records are defined as dictionaries
                     with keys corresponding to the fields in the dataset schema. Ids or
                     external_ids should be provided to identify the records to be updated.
        """
        record_models = self.__ingest_records(records=records, mapping=mapping, user_id=user_id)
        batch_size = self._normalize_batch_size(
            batch_size=batch_size,
            records_length=len(record_models),
            max_value=self._api.MAX_RECORDS_PER_UPSERT_BULK,
        )

        created_or_updated = []
        records_updated = 0
        for batch in range(0, len(records), batch_size):
            self.log(message=f"Sending records from {batch} to {batch + batch_size}.")
            batch_records = record_models[batch : batch + batch_size]
            models, updated = self._api.bulk_upsert(dataset_id=self.__dataset.id, records=batch_records)
            created_or_updated.extend([Record.from_model(model=model, dataset=self.__dataset) for model in models])
            records_updated += updated

        records_created = len(created_or_updated) - records_updated
        self.log(
            message=f"Updated {records_updated} records and added {records_created} records to dataset {self.__dataset.name}",
            level="info",
        )

    def to_dict(self, flatten: bool = True, orient: str = "names") -> Dict[str, Any]:
        """Return the records as a dictionary."""
        records = self.__pull_records_from_server()
        return self._export_to_dict(records=records, flatten=flatten, orient=orient)

    def to_list(self, flatten: bool = True) -> List[Dict[str, Any]]:
        """Return the records as a list of dictionaries."""
        records = self.__pull_records_from_server()
        return self._export_to_list(records=records, flatten=flatten)

    ############################
    # Utility methods
    ############################

    def __pull_records_from_server(self):
        """Get records from the server"""
        return list(self(with_suggestions=True, with_responses=True))

    def __ingest_records(
        self,
        records: Union[List[Dict[str, Any]], Dict[str, Any], List[Record], Record],
        mapping: Optional[Dict[str, str]] = None,
        user_id: Optional[UUID] = None,
    ) -> List[RecordModel]:
        """Ingest records as dictionaries and return a list of RecordModel instances."""
        if isinstance(records, dict) or isinstance(records, Record):
            records = [records]
        if all(map(lambda r: isinstance(r, dict), records)):
            # Records as flat dicts of values to be matched to questions as suggestion or response
            record_models = [
                Record._dict_to_record_model(data=r, schema=self.__dataset.schema, mapping=mapping, user_id=user_id)
                for r in records
            ]  # type: ignore
        elif all(map(lambda r: isinstance(r, Record), records)):
            # Pre-constructed Record instances with suggestions and responses declared
            record_models = [r._model for r in records]  # type: ignore
        else:
            raise ValueError(
                "Records should be a dictionary, a list of dictionaries, a Record instance, "
                "or a list of Record instances."
            )
        return record_models

    def _normalize_batch_size(self, batch_size: int, records_length, max_value: int):
        norm_batch_size = min(batch_size, records_length, max_value)

        if batch_size != norm_batch_size:
            self.log(
                message=f"The provided batch size {batch_size} was normalized. Using value {norm_batch_size}.",
                level="warning",
            )

        return norm_batch_size
