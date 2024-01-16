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
from pytest_mock import MockerFixture

from argilla_sdk import Workspace


class TestSuiteWorkspaces:
    def test_serialize_workspace(self, mock_httpx_client: httpx.Client):
        ws = Workspace(
            name="test-workspace",
            id=uuid.uuid4(),
            inserted_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            client=mock_httpx_client,
        )

        assert Workspace.from_dict(ws.to_dict()) == ws

    def test_list_workspaces(self, mocker: MockerFixture, mock_httpx_client: httpx.Client):
        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value={
                "items": [
                    {"id": uuid.uuid4(), "name": "test-workspace"},
                    {"id": uuid.uuid4(), "name": "another-test-workspace"},
                ]
            }
        )

        mock_httpx_client.get = mocker.MagicMock(return_value=mock_response)

        workspaces = Workspace.list()
        mock_httpx_client.get.assert_called_once_with("/api/v1/me/workspaces")

        assert len(workspaces) == 2
        items_json = mock_response.json()["items"]
        for i in range(len(workspaces)):
            assert workspaces[i].name == items_json[i]["name"]
            assert workspaces[i].id == items_json[i]["id"]
            assert workspaces[i].client == mock_httpx_client

    def test_get_workspace(self, mocker: MockerFixture, mock_httpx_client: httpx.Client):
        workspace_id = uuid.uuid4()

        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(return_value={"id": workspace_id, "name": "test-workspace"})

        mock_httpx_client.get = mocker.MagicMock(return_value=mock_response)

        ws = Workspace.get(workspace_id)
        mock_httpx_client.get.assert_called_once_with(f"/api/v1/workspaces/{workspace_id}")

        assert ws.name == mock_response.json()["name"]
        assert ws.id == mock_response.json()["id"]
        assert ws.client == mock_httpx_client

    def test_get_workspace_by_name(self, mocker: MockerFixture, mock_httpx_client: httpx.Client):
        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value={
                "items": [
                    {"id": uuid.uuid4(), "name": "test-workspace"},
                    {"id": uuid.uuid4(), "name": "other-workspace"},
                ]
            }
        )

        mock_httpx_client.get = mocker.MagicMock(return_value=mock_response)

        ws = Workspace.get_by_name("test-workspace")
        mock_httpx_client.get.assert_called_once_with("/api/v1/me/workspaces")

        items_json = mock_response.json()["items"]
        assert ws.name == items_json[0]["name"]
        assert ws.id == items_json[0]["id"]
        assert ws.client == mock_httpx_client

    def test_create_workspace(self, mocker: MockerFixture, mock_httpx_client: httpx.Client):
        ws = Workspace(name="test-workspace")

        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(return_value={"id": uuid.uuid4(), "name": ws.name})

        mock_httpx_client.post = mocker.MagicMock(return_value=mock_response)

        ws.create()
        mock_httpx_client.post.assert_called_once_with("/api/workspaces", json={"name": ws.name})

        assert ws.id == mock_response.json()["id"]
        assert ws.client == mock_httpx_client

    def test_delete_workspace(self, mocker: MockerFixture, mock_httpx_client: httpx.Client):
        workspace_id = uuid.uuid4()

        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(return_value={"id": workspace_id, "name": "test-workspace"})

        mock_httpx_client.delete = mocker.MagicMock(return_value=mock_response)

        ws = Workspace(name="test-workspace", id=workspace_id)
        ws.delete()
        mock_httpx_client.delete.assert_called_once_with(f"/api/v1/workspaces/{workspace_id}")

    def test_list_workspace_datasets(self, mocker: MockerFixture, mock_httpx_client: httpx.Client):
        workspace_id = uuid.uuid4()

        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value={
                "items": [
                    {"id": uuid.uuid4(), "name": "test-dataset", "workspace_id": workspace_id},
                    {"id": uuid.uuid4(), "name": "another-test-dataset", "workspace_id": workspace_id},
                    {"id": uuid.uuid4(), "name": "third-test-dataset", "workspace_id": uuid.uuid4()},
                ]
            }
        )

        mock_httpx_client.get = mocker.MagicMock(return_value=mock_response)

        datasets = Workspace(id=workspace_id, name="workspace-01").datasets.list()
        mock_httpx_client.get.assert_called_once_with("/api/v1/me/datasets")

        assert len(datasets) == 2
        items_json = mock_response.json()["items"]
        for i in range(len(datasets)):
            assert datasets[i].name == items_json[i]["name"]
            assert datasets[i].id == items_json[i]["id"]
            assert datasets[i].client == mock_httpx_client
