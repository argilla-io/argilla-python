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
from unittest.mock import MagicMock

import httpx

from argilla_sdk import Dataset, Workspace


class TestSuiteDatasets:
    def test_serialize(self, mock_httpx_client: httpx.Client):
        ds = Dataset(
            name="test-workspace",
            id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            guidelines="Test guidelines",
            inserted_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            client=mock_httpx_client,
        )

        assert Dataset.from_dict(ds.to_dict()) == ds

    def test_list_datasets(self, mocker: MagicMock, mock_httpx_client: httpx.Client):
        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(return_value={"items": [{"id": uuid.uuid4(), "name": "dataset-01"}]})

        mock_httpx_client.get = mocker.MagicMock(return_value=mock_response)

        datasets = Dataset.list()
        mock_httpx_client.get.assert_called_once_with("/api/v1/me/datasets")

        for dataset, mock_dataset in zip(datasets, mock_response.json()["items"]):
            assert dataset.id == mock_dataset["id"]
            assert dataset.name == mock_dataset["name"]
            assert dataset.client == mock_httpx_client

    def test_get_dataset(self, mocker: MagicMock, mock_httpx_client: httpx.Client):
        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(return_value={"id": uuid.uuid4(), "name": "dataset-01"})

        mock_httpx_client.get = mocker.MagicMock(return_value=mock_response)

        dataset = Dataset.get(mock_response.json()["id"])
        mock_httpx_client.get.assert_called_once_with(f"/api/v1/datasets/{mock_response.json()['id']}")

        assert dataset.id == mock_response.json()["id"]
        assert dataset.name == mock_response.json()["name"]
        assert dataset.client == mock_httpx_client

    def test_get_by_name_and_workspace(self, mocker: MagicMock, mock_httpx_client: httpx.Client):
        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value={
                "items": [
                    {"id": uuid.uuid4(), "name": "dataset-01"},
                    {"id": uuid.uuid4(), "name": "dataset-02"},
                ]
            }
        )

        mock_httpx_client.get = mocker.MagicMock(return_value=mock_response)

        dataset = Dataset.get_by_name_and_workspace("dataset-01", Workspace(name="workspace-01"))
        mock_httpx_client.get.assert_called_once_with("/api/v1/me/datasets")

        items_json = mock_response.json()["items"]
        assert dataset.id == items_json[0]["id"]
        assert dataset.name == items_json[0]["name"]

        assert dataset.client == mock_httpx_client

    def test_create_dataset(self, mocker: MagicMock, mock_httpx_client: httpx.Client):
        dataset = Dataset(name="dataset-01", guidelines="Test guidelines", workspace_id=uuid.uuid4())

        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value={
                "id": uuid.uuid4(),
                "name": dataset.name,
                "workspace_id": dataset.workspace_id,
                "guidelines": dataset.guidelines,
                "allow_extra_metadata": dataset.allow_extra_metadata,
                "last_activity_at": datetime.utcnow(),
            }
        )

        mock_httpx_client.post = mocker.MagicMock(return_value=mock_response)

        dataset.create()

        mock_httpx_client.post.assert_called_once_with(
            "/api/v1/datasets",
            json={
                "name": dataset.name,
                "guidelines": dataset.guidelines,
                "workspace_id": dataset.workspace_id,
                "allow_extra_metadata": dataset.allow_extra_metadata,
            },
        )

        assert dataset.id == mock_response.json()["id"]
        assert dataset.name == mock_response.json()["name"]
        assert dataset.last_activity_at == mock_response.json()["last_activity_at"]
        assert dataset.client == mock_httpx_client

    def test_update_dataset(self, mocker: MagicMock, mock_httpx_client: httpx.Client):
        dataset = Dataset(
            id=uuid.uuid4(),
            name="dataset-01",
            guidelines="Test guidelines",
            workspace_id=uuid.uuid4(),
            client=mock_httpx_client,
        )

        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value={
                "id": dataset.id,
                "name": dataset.name,
                "workspace_id": dataset.workspace_id,
                "guidelines": dataset.guidelines,
                "allow_extra_metadata": dataset.allow_extra_metadata,
                "last_activity_at": datetime.utcnow(),
            }
        )

        mock_httpx_client.patch = mocker.MagicMock(return_value=mock_response)
        dataset.update()

        mock_httpx_client.patch.assert_called_once_with(
            f"/api/v1/datasets/{dataset.id}",
            json={
                "guidelines": dataset.guidelines,
                "allow_extra_metadata": dataset.allow_extra_metadata,
            },
        )

        assert dataset.id == mock_response.json()["id"]
        assert dataset.name == mock_response.json()["name"]
        assert dataset.last_activity_at == mock_response.json()["last_activity_at"]
        assert dataset.client == mock_httpx_client

    def test_delete_dataset(self, mocker: MagicMock, mock_httpx_client: httpx.Client):
        dataset = Dataset(
            id=uuid.uuid4(),
            name="dataset-01",
            guidelines="Test guidelines",
            workspace_id=uuid.uuid4(),
            client=mock_httpx_client,
        )

        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value={
                "id": dataset.id,
                "name": dataset.name,
                "workspace_id": dataset.workspace_id,
                "guidelines": dataset.guidelines,
                "allow_extra_metadata": dataset.allow_extra_metadata,
                "last_activity_at": datetime.utcnow(),
            }
        )

        mock_httpx_client.delete = mocker.MagicMock(return_value=mock_response)
        dataset.delete()

        mock_httpx_client.delete.assert_called_once_with(
            f"/api/v1/datasets/{dataset.id}",
        )

        assert dataset.id == mock_response.json()["id"]
        assert dataset.name == mock_response.json()["name"]
        assert dataset.last_activity_at == mock_response.json()["last_activity_at"]
        assert dataset.client == mock_httpx_client

    def test_publish_dataset(self, mocker: MagicMock, mock_httpx_client: httpx.Client):
        dataset = Dataset(
            id=uuid.uuid4(),
            name="dataset-01",
            guidelines="Test guidelines",
            workspace_id=uuid.uuid4(),
            client=mock_httpx_client,
        )

        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value={
                "id": dataset.id,
                "name": dataset.name,
                "workspace_id": dataset.workspace_id,
                "guidelines": dataset.guidelines,
                "allow_extra_metadata": dataset.allow_extra_metadata,
                "last_activity_at": datetime.utcnow(),
                "status": "ready",
            }
        )

        mock_httpx_client.put = mocker.MagicMock(return_value=mock_response)
        dataset.publish()

        mock_httpx_client.put.assert_called_once_with(
            f"/api/v1/datasets/{dataset.id}/publish",
        )

        assert dataset.id == mock_response.json()["id"]
        assert dataset.name == mock_response.json()["name"]
        assert dataset.last_activity_at == mock_response.json()["last_activity_at"]
        assert dataset.status == mock_response.json()["status"]
        assert dataset.client == mock_httpx_client

    def test_get_dataset_workspace(self, mocker: MagicMock, mock_httpx_client: httpx.Client):
        dataset = Dataset(
            id=uuid.uuid4(),
            name="dataset-01",
            guidelines="Test guidelines",
            workspace_id=uuid.uuid4(),
            client=mock_httpx_client,
        )

        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value={
                "id": dataset.workspace_id,
                "name": "workspace-01",
                "inserted_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        )

        mock_httpx_client.get = mocker.MagicMock(return_value=mock_response)
        workspace = dataset.workspace

        mock_httpx_client.get.assert_called_once_with(
            f"/api/v1/workspaces/{dataset.workspace_id}",
        )

        assert workspace.id == mock_response.json()["id"]
        assert workspace.name == mock_response.json()["name"]
        assert workspace.client == mock_httpx_client
