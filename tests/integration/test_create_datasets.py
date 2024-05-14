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

import pytest

from argilla_sdk import Argilla, Dataset, Settings, TextField, RatingQuestion


@pytest.fixture(scope="session", autouse=True)
def clean_datasets(client: Argilla):
    datasets = client.datasets
    for dataset in datasets:
        if dataset.name.startswith("test_"):
            dataset.delete()
    yield


class TestCreateDatasets:

    def test_create_dataset(self, client: Argilla):
        dataset = Dataset(
            name="test_dataset",
            settings=Settings(
                fields=[TextField(name="test_field")],
                questions=[RatingQuestion(name="test_question", values=[1, 2, 3, 4, 5])],
            ),
        )
        client.datasets.add(dataset)

        assert dataset in client.datasets
        assert dataset.exists()

        created_dataset = client.datasets(name="test_dataset")
        assert created_dataset.settings == dataset.settings
