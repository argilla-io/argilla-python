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

import uuid
from datetime import datetime

import httpx
import pytest
from pytest_httpx import HTTPXMock

import argilla_sdk as rg


class TestDatasetSerialization:
    def test_serialize(self):
        ds = rg.Dataset(
            name="test-workspace",
            id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
        )

        assert ds.name == ds.serialize()["name"]

    def test_json_serialize_raise_typeerror(self):
        with pytest.raises(TypeError):
            user = rg.User(username="user", id=uuid.uuid4(), extra_arguments="testing")


class TestDatasets:
    def test_create_dataset(self, httpx_mock: HTTPXMock):
        mock_dataset_id = uuid.uuid4()
        mock_return_value = {
            "id": str(mock_dataset_id),
            "name": "dataset-01",
            "status": "draft",
            "allow_extra_metadata": False,
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets",
            method="POST",
            status_code=200,
        )
        with httpx.Client():
            client = rg.Argilla(api_url)
            dataset = rg.Dataset(
                name="dataset-01",
                workspace_id=str(uuid.uuid4()),
                id=str(mock_dataset_id),
                client=client,
            )
            dataset.create()

    def test_get_dataset(self, httpx_mock: HTTPXMock):
        mock_dataset_id = uuid.uuid4()
        mock_return_value = {
            "id": str(mock_dataset_id),
            "name": "dataset-01",
            "status": "draft",
            "allow_extra_metadata": False,
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value, url=f"{api_url}/api/v1/datasets", method="POST", status_code=200
        )
        httpx_mock.add_response(
            json=mock_return_value, url=f"{api_url}/api/v1/datasets/{mock_dataset_id}", method="GET", status_code=200
        )
        with httpx.Client():
            client = rg.Argilla(api_url)
            dataset = rg.Dataset(name="dataset-01", workspace_id=uuid.uuid4(), id=mock_dataset_id, client=client)
            dataset.create()
            gotten_dataset = dataset.get()
            assert gotten_dataset.id == dataset.id
            assert gotten_dataset.name == dataset.name
            assert gotten_dataset.status == dataset.status

    def test_list_datasets(self, httpx_mock: HTTPXMock):
        mock_return_value = {
            "items": [
                {
                    "id": str(uuid.uuid4()),
                    "name": "dataset-01",
                    "status": "ready",
                    "allow_extra_metadata": False,
                    "inserted_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                }
            ]
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value, url=f"{api_url}/api/v1/me/datasets", method="GET", status_code=200
        )
        with httpx.Client():
            client = rg.Argilla(api_url)
            datasets = client.datasets
            assert len(datasets) == 1
            assert str(datasets[0].id) == mock_return_value["items"][0]["id"]
            assert datasets[0].name == mock_return_value["items"][0]["name"]
            assert datasets[0].status == mock_return_value["items"][0]["status"]

    def test_list_datasets(self, httpx_mock: HTTPXMock):
        mock_return_value = {
            "items": [
                {
                    "id": str(uuid.uuid4()),
                    "name": "dataset-01",
                    "status": "ready",
                    "allow_extra_metadata": False,
                    "inserted_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                }
            ]
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value, url=f"{api_url}/api/v1/me/datasets", method="GET", status_code=200
        )
        with httpx.Client():
            client = rg.Argilla(api_url)
            datasets = client.list(rg.Dataset)
            assert len(datasets) == 1
            assert str(datasets[0].id) == mock_return_value["items"][0]["id"]
            assert datasets[0].name == mock_return_value["items"][0]["name"]
            assert datasets[0].status == mock_return_value["items"][0]["status"]

    def test_update_dataset(self, httpx_mock: HTTPXMock):
        mock_dataset_id = uuid.uuid4()
        mock_workspace_id = uuid.uuid4()
        mock_return_value = {
            "id": str(mock_dataset_id),
            "name": "dataset-01",
            "workspace_id": str(mock_workspace_id),
            "guidelines": "guidelines",
            "allow_extra_metadata": False,
            "last_activity_at": datetime.utcnow().isoformat(),
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        mock_patch_return_value = {
            "id": str(mock_dataset_id),
            "name": "new_name",
            "workspace_id": str(mock_workspace_id),
            "guidelines": "guidelines",
            "allow_extra_metadata": False,
            "last_activity_at": datetime.utcnow().isoformat(),
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        httpx_mock.add_response(
            json=mock_patch_return_value,
            url=f"http://test_url/api/v1/datasets/{mock_dataset_id}",
            method="PATCH",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"http://test_url/api/v1/datasets",
            method="POST",
            status_code=200,
            # match_json=mock_return_value,
        )
        with httpx.Client() as client:
            client = rg.Argilla("http://test_url")
            dataset = rg.Dataset(
                id=mock_dataset_id, name=mock_return_value["name"], workspace_id=mock_workspace_id, client=client
            )
            dataset.create()
            dataset = rg.Dataset(id=mock_dataset_id, name="new name", client=client)
            dataset = dataset.update()
            assert dataset.name == "new_name"


class TestDatasetsAPI:
    def test_delete_dataset(self, httpx_mock: HTTPXMock):
        # TODO: Add a test for the delete method in client
        mock_dataset_id = uuid.uuid4()
        mock_return_value = {
            "id": str(mock_dataset_id),
            "name": "dataset-01",
            "status": "draft",
            "allow_extra_metadata": False,
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"http://test_url/api/v1/datasets/{mock_dataset_id}",
            method="DELETE",
            status_code=200,
        )
        with httpx.Client() as client:
            client = rg.Argilla("http://test_url")
            client._datasets.delete(mock_dataset_id)
            pytest.raises(httpx.HTTPError, client._datasets.get, mock_dataset_id)

    def test_publish_dataset(self, httpx_mock: HTTPXMock):
        # TODO: Add a test for the publish method in client when dataset is finished
        mock_dataset_id = uuid.uuid4()
        mock_return_value = {
            "id": str(mock_dataset_id),
            "name": "dataset-01",
            "status": "ready",
            "allow_extra_metadata": False,
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"http://test_url/api/v1/datasets/{mock_dataset_id}/publish",
            method="PUT",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"http://test_url/api/v1/datasets/{mock_dataset_id}",
            method="GET",
            status_code=200,
        )
        with httpx.Client() as client:
            client = rg.Argilla("http://test_url")
            client._datasets.publish(mock_dataset_id)
            dataset = client._datasets.get(mock_dataset_id)
            assert dataset.status == "ready"
            assert dataset.id == mock_dataset_id
            assert dataset.name == "dataset-01"

    def test_get_by_name_and_workspace_id(self, httpx_mock: HTTPXMock):
        mock_workspace_id = uuid.uuid4()
        mock_dataset_id = uuid.uuid4()
        mock_return_value = {
            "items": [
                {
                    "id": mock_dataset_id.hex,
                    "name": "dataset-01",
                    "status": "ready",
                    "inserted_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                    "workspace_id": mock_workspace_id.hex,
                }
            ]
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value, url=f"{api_url}/api/v1/me/datasets", method="GET", status_code=200
        )
        with httpx.Client():
            client = rg.Argilla(api_url)
            dataset = client._datasets.get_by_name_and_workspace_id("dataset-01", mock_workspace_id)
            assert mock_dataset_id.hex == mock_return_value["items"][0]["id"]
            assert dataset.name == mock_return_value["items"][0]["name"]
            assert dataset.status == mock_return_value["items"][0]["status"]
            assert dataset.workspace_id.hex == mock_return_value["items"][0]["workspace_id"]
            assert dataset.inserted_at.isoformat() == mock_return_value["items"][0]["inserted_at"]
            assert dataset.updated_at.isoformat() == mock_return_value["items"][0]["updated_at"]


class TestRecords:
    def test_records_with_create(self, httpx_mock: HTTPXMock):
        mock_dataset_id = uuid.uuid4()
        mock_return_value = {
            "id": mock_dataset_id.hex,
            "name": "dataset-01",
            "status": "draft",
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id}/records",
            method="POST",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets",
            method="POST",
            status_code=200,
        )
        with httpx.Client() as client:
            list_of_records = [
                rg.Record(
                    fields={
                        "text": "Hello World, how are you?",
                    }
                )
            ]
            settings = rg.Settings(
                fields=[
                    rg.TextField(name="text"),
                ],
                questions=[
                    rg.LabelQuestion(name="label", labels=["positive", "negative"]),
                ],
            )
            client = rg.Argilla("http://test_url")
            dataset = rg.Dataset(
                id=mock_dataset_id,
                name=mock_return_value["name"],
                workspace_id=uuid.uuid4(),
                guidelines="Test guidelines",
                settings=settings,
            )
            dataset.records = list_of_records
            client.create(dataset)
            assert dataset.id == mock_dataset_id
            assert dataset.name == mock_return_value["name"]
            assert dataset.status == "draft"

    def test_records_with_get(self, httpx_mock: HTTPXMock):
        mock_dataset_id = uuid.uuid4()
        mock_return_value = {
            "id": mock_dataset_id.hex,
            "name": "dataset-01",
            "status": "draft",
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id}/records",
            method="POST",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets",
            method="POST",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id.hex}",
            method="PATCH",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id}",
            method="GET",
            status_code=200,
        )
        with httpx.Client() as client:
            list_of_records = [
                rg.Record(
                    fields={
                        "text": "Hello World, how are you?",
                    }
                )
            ]
            settings = rg.Settings(
                fields=[
                    rg.TextField(name="text"),
                ],
                questions=[
                    rg.LabelQuestion(name="label", labels=["positive", "negative"]),
                ],
            )
            client = rg.Argilla("http://test_url")
            dataset = rg.Dataset(
                id=mock_dataset_id,
                name=mock_return_value["name"],
                workspace_id=uuid.uuid4(),
                guidelines="Test guidelines",
                settings=settings,
            )
            client.create(dataset)
            dataset.records = list_of_records
            dataset = client.update(dataset)
            gotten_dataset = client.get(dataset)
            assert dataset.id == gotten_dataset.id
            assert dataset.name == gotten_dataset.name
            assert dataset.status == gotten_dataset.status

    def test_records_with_update(self, httpx_mock: HTTPXMock):
        mock_dataset_id = uuid.uuid4()
        mock_return_value = {
            "id": mock_dataset_id.hex,
            "name": "dataset-01",
            "status": "draft",
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id}/records",
            method="POST",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets",
            method="POST",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id.hex}",
            method="PATCH",
            status_code=200,
        )
        with httpx.Client() as client:
            list_of_records = [
                rg.Record(
                    fields={
                        "text": "Hello World, how are you?",
                    }
                )
            ]
            settings = rg.Settings(
                fields=[
                    rg.TextField(name="text"),
                ],
                questions=[
                    rg.LabelQuestion(name="label", labels=["positive", "negative"]),
                ],
            )
            client = rg.Argilla("http://test_url")
            dataset = rg.Dataset(
                id=mock_dataset_id,
                name=mock_return_value["name"],
                workspace_id=uuid.uuid4(),
                guidelines="Test guidelines",
                settings=settings,
            )
            client.create(dataset)
            dataset.records = list_of_records
            dataset = client.update(dataset)
            assert dataset.id == mock_dataset_id
            assert dataset.name == mock_return_value["name"]
            assert dataset.status == "draft"

    def test_records_duplicates(self, httpx_mock: HTTPXMock):
        mock_dataset_id = uuid.uuid4()
        mock_return_value = {
            "id": mock_dataset_id.hex,
            "name": "dataset-01",
            "status": "draft",
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id}/records",
            method="POST",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets",
            method="POST",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id.hex}",
            method="PATCH",
            status_code=200,
        )
        with httpx.Client() as client:
            list_of_records = [
                rg.Record(
                    fields={
                        "text": "Hello World, how are you?",
                    }
                )
            ]
            settings = rg.Settings(
                fields=[
                    rg.TextField(name="text"),
                ],
                questions=[
                    rg.LabelQuestion(name="label", labels=["positive", "negative"]),
                ],
            )
            client = rg.Argilla("http://test_url")
            dataset = rg.Dataset(
                id=mock_dataset_id,
                name=mock_return_value["name"],
                workspace_id=uuid.uuid4(),
                guidelines="Test guidelines",
                settings=settings,
            )
            client.create(dataset)
            dataset.records = list_of_records
            dataset = client.update(dataset)
            dataset.records = list_of_records
            dataset = client.update(dataset)
            assert len(dataset.records) == 1

    def test_records_deleted(self, httpx_mock: HTTPXMock):
        mock_dataset_id = uuid.uuid4()
        mock_return_value = {
            "id": mock_dataset_id.hex,
            "name": "dataset-01",
            "status": "draft",
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id}/records",
            method="POST",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets",
            method="POST",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id.hex}",
            method="PATCH",
            status_code=200,
        )
        with httpx.Client() as client:
            list_of_records = [
                rg.Record(
                    fields={
                        "text": "Hello World, how are you?",
                    }
                )
            ]
            settings = rg.Settings(
                fields=[
                    rg.TextField(name="text"),
                ],
                questions=[
                    rg.LabelQuestion(name="label", labels=["positive", "negative"]),
                ],
            )
            client = rg.Argilla("http://test_url")
            dataset = rg.Dataset(
                id=mock_dataset_id,
                name=mock_return_value["name"],
                workspace_id=uuid.uuid4(),
                guidelines="Test guidelines",
                settings=settings,
            )
            client.create(dataset)
            dataset.records = list_of_records
            dataset = client.update(dataset)
            dataset.records = []
            dataset = client.update(dataset)
            assert len(dataset.records) == 0
    
    def test_records_suggestions(self, httpx_mock: HTTPXMock):
        mock_dataset_id = uuid.uuid4()
        mock_return_value = {
            "id": mock_dataset_id.hex,
            "name": "dataset-01",
            "status": "draft",
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id}/records",
            method="POST",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets",
            method="POST",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_dataset_id.hex}",
            method="PATCH",
            status_code=200,
        )
        with httpx.Client() as client:
            list_of_records = [
                rg.Record(
                    fields={
                        "text": "Hello World, how are you?",
                    }
                )
            ]
            settings = rg.Settings(
                fields=[
                    rg.TextField(name="text"),
                ],
                questions=[
                    rg.LabelQuestion(name="label", labels=["positive", "negative"]),
                ],
            )
            client = rg.Argilla("http://test_url")
            dataset = rg.Dataset(
                id=mock_dataset_id,
                name=mock_return_value["name"],
                workspace_id=uuid.uuid4(),
                guidelines="Test guidelines",
                settings=settings,
            )
            client.create(dataset)
            dataset.records = list_of_records
            dataset = client.update(dataset)
            for record in dataset.records:
                record.suggestions = rg.Suggestion(
                    question_name="label",
                    value="positive",
                )