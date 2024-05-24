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

from typing import Dict, List, TYPE_CHECKING, Union

from datasets import Dataset

from argilla_sdk.records._io._generic import GenericIO

if TYPE_CHECKING:
    from argilla_sdk import Record


class HFDatasetsIO:
    @staticmethod
    def to_datasets(records: List["Record"]) -> Dataset:
        """
        Export the records to a Hugging Face dataset.

        Returns:
            The dataset containing the records.

        """
        record_dicts = [GenericIO._record_to_dict(record=record, flatten=True) for record in records]
        dataset = Dataset.from_list(record_dicts)
        return dataset

    @staticmethod
    def _record_dicts_from_datasets(dataset: Dataset) -> List[Dict[str, Union[str, float, int, list]]]:
        """Creates a dictionaries from a HF dataset that can be passed to DatasetRecords.add or DatasetRecords.update.

        Parameters:
            dataset (Dataset): The dataset containing the records.

        Returns:
            Generator[Dict[str, Union[str, float, int, list]], None, None]: A generator of dictionaries to be passed to DatasetRecords.add or DatasetRecords.update.
        """
        record_dicts = []
        for example in dataset.to_iterable_dataset():
            record_dicts.append(example)
        return record_dicts
