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

from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union, Sequence, Iterable
from uuid import UUID

from argilla_sdk._api import RecordsAPI
from argilla_sdk._helpers._mixins import LoggingMixin
from argilla_sdk._models import RecordModel
from argilla_sdk.client import Argilla
from argilla_sdk.records._io import RecordsIOMixin
from argilla_sdk.records._resource import Record
from argilla_sdk.records._search import Query

if TYPE_CHECKING:
    from argilla_sdk.datasets import Dataset


class DatasetRecordsIterator(RecordsIOMixin):
    """This class is used to iterate over records in a dataset"""

    def __init__(
        self,
        dataset: "Dataset",
        client: "Argilla",
        query: Optional[Query] = None,
        start_offset: int = 0,
        batch_size: Optional[int] = None,
        with_suggestions: bool = False,
        with_responses: bool = False,
        with_vectors: Optional[Union[str, List[str], bool]] = None,
    ):
        self.__dataset = dataset
        self.__client = client
        self.__query = query or Query()
        self.__offset = start_offset or 0
        self.__batch_size = batch_size or 100
        self.__with_suggestions = with_suggestions
        self.__with_responses = with_responses
        self.__with_vectors = with_vectors
        self.__records_batch = []

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
        for record_model in self._fetch_from_server():
            yield Record.from_model(model=record_model, dataset=self.__dataset)

    def _fetch_from_server(self) -> List[RecordModel]:
        if not self.__dataset.exists():
            raise ValueError(f"Dataset {self.__dataset.name} does not exist on the server.")
        if self._is_search_query():
            return self._fetch_from_server_with_search()
        return self._fetch_from_server_with_list()

    def _fetch_from_server_with_list(self) -> List[RecordModel]:
        return self.__client.api.records.list(
            dataset_id=self.__dataset.id,
            limit=self.__batch_size,
            offset=self.__offset,
            with_responses=self.__with_responses,
            with_suggestions=self.__with_suggestions,
            with_vectors=self.__with_vectors,
        )

    def _fetch_from_server_with_search(self) -> List[RecordModel]:
        search_items, total = self.__client.api.records.search(
            dataset_id=self.__dataset.id,
            query=self.__query.model,
            limit=self.__batch_size,
            offset=self.__offset,
            with_responses=self.__with_responses,
            with_suggestions=self.__with_suggestions,
        )
        return [record_model for record_model, _ in search_items]

    def _is_search_query(self) -> bool:
        return bool(self.__query and (self.__query.query or self.__query.filter))


class DatasetRecords(Iterable[Record], LoggingMixin):
    """This class is used to work with records from a dataset and is accessed via `Dataset.records`.
    The responsibility of this class is to provide an interface to interact with records in a dataset,
    by adding, updating, fetching, querying, deleting, and exporting records.

    Attributes:
        client (Argilla): The Argilla client object.
        dataset (Dataset): The dataset object.
    """

    _api: RecordsAPI

    DEFAULT_BATCH_SIZE = 256

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
        query: Optional[Union[str, Query]] = None,
        batch_size: Optional[int] = DEFAULT_BATCH_SIZE,
        start_offset: int = 0,
        with_suggestions: bool = True,
        with_responses: bool = True,
        with_vectors: Optional[Union[List, bool, str]] = None,
    ):
        """Returns an iterator over the records in the dataset on the server.

        Parameters:
            query: A string or a Query object to filter the records.
            batch_size: The number of records to fetch in each batch. The default is 256.
            start_offset: The offset from which to start fetching records. The default is 0.
            with_suggestions: Whether to include suggestions in the records. The default is True.
            with_responses: Whether to include responses in the records. The default is True.
            with_vectors: A list of vector names to include in the records. The default is None.
                If a list is provided, only the specified vectors will be included.
                If True is provided, all vectors will be included.

        Returns:
            An iterator over the records in the dataset on the server.

        """
        if query and isinstance(query, str):
            query = Query(query=query)

        if with_vectors:
            self._validate_vector_names(vector_names=with_vectors)

        return DatasetRecordsIterator(
            self.__dataset,
            self.__client,
            query=query,
            batch_size=batch_size,
            start_offset=start_offset,
            with_suggestions=with_suggestions,
            with_responses=with_responses,
            with_vectors=with_vectors,
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dataset})"

    ############################
    # Public methods
    ############################

    def add(
        self,
        records: Union[dict, List[dict], Record, List[Record]],
        mapping: Optional[Dict[str, str]] = None,
        user_id: Optional[UUID] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> List[Record]:
        """
        Add new records to a dataset on the server.

        Parameters:
            records: A dictionary or a list of dictionaries representing the records
                     to be added to the dataset. Records are defined as dictionaries
                     with keys corresponding to the fields in the dataset schema.
            mapping: A dictionary that maps the keys in the records to the fields in the dataset schema.
            user_id: The user id to be associated with the records. If not provided, the current user id is used.
            batch_size: The number of records to send in each batch. The default is 256.

        Returns:
            A list of Record objects representing the added records.

        Examples:

        Add generic records to a dataset as dictionaries:

        """
        record_models = self._ingest_records(records=records, mapping=mapping, user_id=user_id or self.__client.me.id)

        batch_size = self._normalize_batch_size(
            batch_size=batch_size,
            records_length=len(record_models),
            max_value=self._api.MAX_RECORDS_PER_CREATE_BULK,
        )

        created_records = []
        for batch in range(0, len(record_models), batch_size):
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
        records: Union[dict, List[dict], Record, List[Record]],
        mapping: Optional[Dict[str, str]] = None,
        user_id: Optional[UUID] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> List[Record]:
        """Update records in a dataset on the server using the provided records
            and matching based on the external_id or id.

        Parameters:
            records: A dictionary or a list of dictionaries representing the records
                     to be updated in the dataset. Records are defined as dictionaries
                     with keys corresponding to the fields in the dataset schema. Ids or
                     external_ids should be provided to identify the records to be updated.
            mapping: A dictionary that maps the keys in the records to the fields in the dataset schema.
            user_id: The user id to be associated with the records. If not provided, the current user id is used.
            batch_size: The number of records to send in each batch. The default is 256.

        Returns:
            A list of Record objects representing the updated records.

        """
        record_models = self._ingest_records(records=records, mapping=mapping, user_id=user_id or self.__client.me.id)
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

        return created_or_updated

    def to_dict(self, flatten: bool = False, orient: str = "names") -> Dict[str, Any]:
        """
        Return the records as a dictionary. This is a convenient shortcut for dataset.records(...).to_dict().

        Parameters:
            flatten (bool): Whether to flatten the dictionary and use dot notation for nested keys like suggestions and responses.
            orient (str): The structure of the exported dictionary.

        Returns:
            A dictionary of records.

        """
        return self(with_suggestions=True, with_responses=True).to_dict(flatten=flatten, orient=orient)

    def to_list(self, flatten: bool = False) -> List[Dict[str, Any]]:
        """
        Return the records as a list of dictionaries. This is a convenient shortcut for dataset.records(...).to_list().

        Parameters:
            flatten (bool): Whether to flatten the dictionary and use dot notation for nested keys like suggestions and responses.

        Returns:
            A list of dictionaries of records.
        """
        return self(with_suggestions=True, with_responses=True).to_list(flatten=flatten)

    def to_json(self, path: Union[Path, str]) -> Path:
        """
        Export the records to a file on disk. This is a convenient shortcut for dataset.records(...).to_disk().

        Parameters:
            path (str): The path to the file to save the records.
            orient (str): The structure of the exported dictionary.

        Returns:
            The path to the file where the records were saved.

        """
        return self(with_suggestions=True, with_responses=True).to_json(path=path)
    
    def from_json(self, path: Union[Path, str]) -> "DatasetRecords":
        """Creates a DatasetRecords object from a disk path.

        Args:
            path (str): The path to the file containing the records.

        Returns:
            DatasetRecords: The DatasetRecords object created from the disk path.

        """
        records = self().from_json(path=path)
        self.update(records)
        return self
    
    ############################
    # Private methods
    ############################

    def _ingest_records(
        self,
        records: Union[List[Dict[str, Any]], Dict[str, Any], List[Record], Record],
        mapping: Optional[Dict[str, str]] = None,
        user_id: Optional[UUID] = None,
    ) -> List[RecordModel]:
        if isinstance(records, (Record, dict)):
            records = [records]

        if all(map(lambda r: isinstance(r, dict), records)):
            # Records as flat dicts of values to be matched to questions as suggestion or response
            records = [
                Record.from_dict(data=r, mapping=mapping, dataset=self.__dataset, user_id=user_id) for r in records
            ]  # type: ignore
        elif all(map(lambda r: isinstance(r, Record), records)):
            for record in records:
                record.dataset = self.__dataset
        else:
            raise ValueError(
                "Records should be a dictionary, a list of dictionaries, a Record instance, "
                "or a list of Record instances."
            )
        return [record.api_model() for record in records]

    def _normalize_batch_size(self, batch_size: int, records_length, max_value: int):
        norm_batch_size = min(batch_size, records_length, max_value)

        if batch_size != norm_batch_size:
            self.log(
                message=f"The provided batch size {batch_size} was normalized. Using value {norm_batch_size}.",
                level="warning",
            )

        return norm_batch_size

    def _validate_vector_names(self, vector_names: Union[List[str], str]) -> None:
        if not isinstance(vector_names, list):
            vector_names = [vector_names]
        for vector_name in vector_names:
            if isinstance(vector_name, bool):
                continue
            if vector_name not in self.__dataset.schema:
                raise ValueError(f"Vector field {vector_name} not found in dataset schema.")
