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


class TestDatasets:
    def test_serialize(self):
        ds = rg.Dataset(
            name="test-workspace",
            id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            guidelines="Test guidelines",
            inserted_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        assert ds.name == ds.serialize()["name"]

    def test_serialize_with_extra_arguments(self):
        ds = rg.Dataset(
            name="test-dataset",
            id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            guidelines="Test guidelines",
            inserted_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            extra_argument="extra",
        )
        assert "extra_argument" not in ds.serialize()

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
            assert datasets[0].allow_extra_metadata == mock_return_value["items"][0]["allow_extra_metadata"]

    def test_get_dataset(self, httpx_mock: HTTPXMock):
        mock_return_value = {
            "id": str(uuid.uuid4()),
            "name": "dataset-01",
            "status": "ready",
            "allow_extra_metadata": False,
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"{api_url}/api/v1/datasets/{mock_return_value['id']}",
            method="GET",
            status_code=200,
        )
        with httpx.Client():
            client = rg.Argilla(api_url)
            dataset = rg.Dataset(id=mock_return_value["id"])
            dataset = client.get(dataset)
            assert str(dataset.id) == mock_return_value["id"]
            assert dataset.name == mock_return_value["name"]
            assert dataset.status == mock_return_value["status"]
            assert dataset.allow_extra_metadata == mock_return_value["allow_extra_metadata"]

    def test_get_by_name_and_workspace(self, httpx_mock: HTTPXMock):
        mock_workspace_id = uuid.uuid4()
        mock_dataset_id = uuid.uuid4()
        mock_return_value = {
            "items": [
                {
                    "id": str(mock_dataset_id),
                    "name": "dataset-01",
                    "status": "ready",
                    "allow_extra_metadata": False,
                    "inserted_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                    "workspace_id": str(mock_workspace_id),
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
            assert str(dataset.id) == mock_return_value["items"][0]["id"]
            assert dataset.name == mock_return_value["items"][0]["name"]
            assert dataset.status == mock_return_value["items"][0]["status"]
            assert dataset.id == mock_dataset_id
            assert dataset.workspace_id == mock_workspace_id

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
            client.create(
                rg.Dataset(
                    name="dataset-01",
                    workspace_id=str(uuid.uuid4()),
                    guidelines="Test guidelines",
                    allow_extra_metadata=False,
                    id=str(mock_dataset_id),
                )
            )

    def test_get_dataset(self, httpx_mock: HTTPXMock):
        mock_dataset_id = uuid.uuid4().hex
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
            dataset = rg.Dataset(
                name="dataset-01",
                workspace_id=uuid.uuid4(),
                guidelines="Test guidelines",
                allow_extra_metadata=False,
                id=str(mock_dataset_id),
            )
            dataset = client.create(dataset)
            dataset = client.get(dataset)
            assert dataset.id.hex == mock_return_value["id"]
            assert dataset.name == mock_return_value["name"]
            assert dataset.status == mock_return_value["status"]
            assert dataset.allow_extra_metadata == mock_return_value["allow_extra_metadata"]

    def test_update_dataset(self, httpx_mock: HTTPXMock):
        mock_dataset_id = uuid.uuid4().hex
        mock_workspace_id = uuid.uuid4().hex
        mock_return_value = {
            "id": mock_dataset_id,
            "name": "dataset-01",
            "workspace_id": str(mock_workspace_id),
            "guidelines": "guidelines",
            "allow_extra_metadata": False,
            "last_activity_at": datetime.utcnow().isoformat(),
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"http://test_url/api/v1/datasets/{mock_dataset_id}",
            method="PATCH",
            status_code=200,
        )
        httpx_mock.add_response(
            json=mock_return_value,
            url=f"http://test_url/api/v1/datasets/{mock_dataset_id}",
            method="GET",
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
            dataset = rg.Dataset(
                id=mock_return_value["id"],
                name=mock_return_value["name"],
                workspace_id=mock_return_value["workspace_id"],
                guidelines=mock_return_value["guidelines"],
            )
            client = rg.Argilla("http://test_url")
            client.create(dataset)
            dataset.guidelines = "new guidelines"
            updated_dataset = client.update(dataset)
            gotten_dataset = client.get(updated_dataset)
            assert dataset.id == gotten_dataset.id
            assert dataset.name == gotten_dataset.name

    def test_delete_dataset(self, httpx_mock: HTTPXMock):
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
                    "id": str(mock_dataset_id),
                    "name": "dataset-01",
                    "status": "ready",
                    "allow_extra_metadata": False,
                    "inserted_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                    "workspace_id": str(mock_workspace_id),
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
            assert str(dataset.id) == mock_return_value["items"][0]["id"]
            assert dataset.name == mock_return_value["items"][0]["name"]
            assert dataset.status == mock_return_value["items"][0]["status"]
            assert dataset.id == mock_dataset_id
            assert dataset.workspace_id == mock_workspace_id
