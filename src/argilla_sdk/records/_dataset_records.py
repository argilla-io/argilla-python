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

from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union, Sequence, Tuple
from uuid import UUID

from argilla_sdk._models import RecordModel
from argilla_sdk._resource import Resource
from argilla_sdk.client import Argilla
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


class DatasetRecords(Resource):
    """
    This class is used to work with records from a dataset.

    The responsibility of this class is to provide an interface to interact with records in a dataset,
    by adding, updating, fetching, querying, and deleting records.

    """

    def __init__(self, client: "Argilla", dataset: "Dataset"):
        """Initializes a DatasetRecords object with a client and a dataset.
        Args:
            client: An Argilla client object.
            dataset: A Dataset object.
        """
        self.__client = client
        self.__dataset = dataset

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
        self, records: Union[dict, List[dict]], mapping: Optional[Dict[str, str]] = None, user_id: Optional[UUID] = None
    ) -> None:
        """
        Add new records to a dataset on the server.
        Args:
            records: A dictionary or a list of dictionaries representing the records
                     to be added to the dataset. Records are defined as dictionaries
                     with keys corresponding to the fields in the dataset schema.
        """
        # TODO: Once we have implemented the new records bulk endpoint, this method should use it
        # and return the response from the API.
        records_models = self.__ingest_records(records=records, mapping=mapping, user_id=user_id)
        self.__client.api.records.create_many(dataset_id=self.__dataset.id, records=records_models)
        self.log(
            message=f"Added {len(records_models)} records to dataset {self.__dataset.name}",
            level="info",
        )

    def update(
        self, records: Union[dict, List[dict]], mapping: Optional[Dict[str, str]] = None, user_id: Optional[UUID] = None
    ) -> None:
        """Update records in a dataset on the server using the provided records
            and matching based on the external_id or id.

        Args:
            records: A dictionary or a list of dictionaries representing the records
                     to be updated in the dataset. Records are defined as dictionaries
                     with keys corresponding to the fields in the dataset schema. Ids or
                     external_ids should be provided to identify the records to be updated.
        """
        record_models = self.__ingest_records(records=records, mapping=mapping, user_id=user_id)
        records_to_update, records_to_add = self.__align_split_records(record_models)
        if len(records_to_update) > 0:
            self.__client.api.records.update_many(dataset_id=self.__dataset.id, records=records_to_update)
            self.__create_record_responses(records=records_to_update)
        else:
            message = """
            No existing records founds to update. 
            If you want to add new records, you should use the `Dataset.records.add` method.
            """
            self.log(message=message, level="warning")
        if len(records_to_add) > 0:
            self.__client.api.records.create_many(dataset_id=self.__dataset.id, records=records_to_add)
        records = self.__list_records_from_server()
        self.__records = [Record.from_model(model=record, dataset=self.__dataset) for record in records]
        self.log(
            message=f"Updated {len(records_to_update)} records and added {len(records_to_add)} records to dataset {self.__dataset.name}",
            level="info",
        )

    ############################
    # Utility methods
    ############################

    def __list_records_from_server(self):
        """Get records from the server"""
        return self.__client.api.records.list(dataset_id=self.__dataset.id, with_suggestions=True, with_responses=True)

    def __create_record_responses(self, records):
        """Create record responses in the server on a per record basis."""
        for record in records:
            self.__client.api.records.create_record_responses(record)

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
                "Records should be a dictionary, a list of dictionaries, a Record instance, or a list of Record instances."
            )
        return record_models

    def __align_split_records(self, records) -> Tuple[List[RecordModel], List[RecordModel]]:
        """Align records with server ids and external_ids and split them into two lists: records to update and records to add."""
        server_records = self.__list_records_from_server()
        server_records_map = {str(record.external_id): str(record.id) for record in server_records}
        records_to_update = []
        records_to_add = []
        for record in records:
            external_id = str(record.external_id) if record.external_id is not None else None
            record_id = str(record.id) if record.id is not None else None
            if record_id is None and external_id is None:
                # the record is new and doesn't have an external_id
                records_to_add.append(record)
            elif external_id in server_records_map:
                # the record has an external_id and is already in the server
                record.id = server_records_map.get(external_id)
                records_to_update.append(record)
            elif record_id in server_records_map.values():
                # the record is already in the server but we don't have the external_id
                records_to_update.append(record)
        self.log(message=f"Updating {len(records_to_update)} records.")
        self.log(message=f"Adding {len(records_to_add)} records.")
        return records_to_update, records_to_add
