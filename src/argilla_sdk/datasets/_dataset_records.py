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
from typing import TYPE_CHECKING

from argilla_sdk.datasets._record import Record
from argilla_sdk._models import RecordModel

if TYPE_CHECKING:
    from argilla_sdk import Dataset
    from argilla_sdk.client import Argilla


class DatasetRecords:
    def __init__(self, client: "Argilla", dataset: "Dataset"):
        self.client = client
        self.dataset_id = dataset.id
        self.question_name_map = dataset.question_name_map

    def add(self, records):
        """Add records to a dataset"""
        records = self.__normalize_records(records)
        records = self.__add_records_to_server(records)
        records = self.__list_records_from_server()
        self.__records = records
        return records

    def list(self):
        """Get records from a dataset"""
        self.__records = self.__list_records_from_server()
        return self.__records

    def update(self, records):
        """Update records in a dataset"""
        raise NotImplementedError("Update records is not implemented yet")

    def __add_records_to_server(self, records):
        """Add records to a dataset"""
        serialized_records = self.__serialize_records(records)
        return self.client._datasets.create_records(dataset_id=self.dataset_id, records=serialized_records)

    def __list_records_from_server(self):
        """Get records from the server"""
        return self.client._datasets.list_records(
            dataset_id=self.dataset_id, with_suggestions=True, with_responses=True
        )

    def __update_records_on_server(self, records):
        raise NotImplementedError("Update records is not implemented yet")

    #####################
    # Container methods #
    #####################

    def __getitem__(self, key):
        return self.__records[key]

    def __len__(self):
        return len(self.__records)

    def __iter__(self):
        return iter(self.__records)

    ###################
    # Utility methods #
    ###################

    def __normalize_records(self, records):
        """Normalize records to a list of `Record` instances"""
        normalized_records = []
        for record in records:
            if isinstance(record, dict):
                record = Record(question_name_map=self.question_name_map, **record)
            elif isinstance(record, RecordModel):
                record = Record(question_name_map=self.question_name_map, **record.model_dump())
            elif isinstance(record, Record):
                pass
            else:
                raise ValueError(f"Invalid record type: {type(record)}")
            normalized_records.append(record)
        return normalized_records

    def __serialize_records(self, records):
        """Serialize records to a list of dictionaries"""
        serialized_records = []
        for record in records:
            dumped_model = record.serialize()
            for suggestion in dumped_model["suggestions"]:
                suggestion["question_id"] = self.question_name_map[suggestion["question_name"]]
            serialized_records.append(dumped_model)
        return serialized_records
