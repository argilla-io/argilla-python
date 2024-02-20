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

import json
import uuid
from datetime import datetime

import httpx
from pytest_httpx import HTTPXMock
import argilla_sdk as rg


class TestWorkspaces:
    def test_serialize(self):
        ws = rg.Workspace(
            name="test-workspace",
            id=uuid.uuid4(),
            inserted_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        assert ws.name == ws.serialize()["name"]

    def test_serialize_with_extra_arguments(self):
        ws = rg.Workspace(
            name="test-workspace",
            id=uuid.uuid4(),
            inserted_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            extra="extra",
        )
        assert ws.name == ws.serialize()["name"]
        assert "extra" not in ws.serialize()

    def test_json_serialize(self):
        ws = rg.Workspace(
            name="test-workspace",
            id=uuid.uuid4(),
            inserted_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        ws_from_json = json.loads(ws.serialize_json())
        assert ws.name == ws_from_json["name"]
        assert ws.id == uuid.UUID(ws_from_json["id"])
        assert ws.inserted_at == datetime.fromisoformat(ws_from_json["inserted_at"])
        assert ws.updated_at == datetime.fromisoformat(ws_from_json["updated_at"])

    def test_list_workspaces(self, httpx_mock: HTTPXMock):
        mock_return_value = {
            "items": [
                {
                    "id": str(uuid.uuid4()),
                    "name": "test-workspace",
                    "inserted_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "another-test-workspace",
                    "inserted_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                },
            ]
        }
        api_url = "http://test_url"
        httpx_mock.add_response(json=mock_return_value, url=f"{api_url}/api/v1/me/workspaces")
        with httpx.Client():
            client = rg.Argilla(api_url="http://test_url", api_key="admin.apikey")
            workspaces = client.list(rg.Workspace)
        assert len(workspaces) == 2
        for i in range(len(workspaces)):
            assert workspaces[i].name == mock_return_value["items"][i]["name"]
            assert workspaces[i].id == uuid.UUID(mock_return_value["items"][i]["id"])

    def test_get_workspace(self, httpx_mock: HTTPXMock):
        workspace_id = uuid.uuid4()
        mock_return_value = {
            "id": str(workspace_id),
            "name": "test-workspace",
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(json=mock_return_value, url=f"{api_url}/api/v1/workspaces/{workspace_id}")
        with httpx.Client():
            client = rg.Argilla(api_url="http://test_url", api_key="admin.apikey")
            workspace = client._workspaces.get(workspace_id)
            assert workspace.name == mock_return_value["name"]
            assert workspace.id == workspace_id

    def test_get_workspace_by_name(self, httpx_mock: HTTPXMock):
        mock_return_value = {
            "items": [
                {
                    "id": str(uuid.uuid4()),
                    "name": "test-workspace",
                    "inserted_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "other-workspace",
                    "inserted_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                },
            ]
        }
        api_url = "http://test_url"
        httpx_mock.add_response(json=mock_return_value, url=f"{api_url}/api/v1/me/workspaces")
        with httpx.Client():
            client = rg.Argilla(api_url=api_url, api_key="admin.apikey")
            ws = client._workspaces.get_by_name("test-workspace")
            assert ws is not None
            assert ws.name == "test-workspace"
            assert ws.id == uuid.UUID(mock_return_value["items"][0]["id"])

    def test_create_workspace(self, httpx_mock: HTTPXMock):
        ws = rg.Workspace(name="test-workspace", id=uuid.uuid4())

        mock_return_value = {
            "id": str(uuid.uuid4()),
            "name": ws.name,
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        api_url = "http://test_url"
        httpx_mock.add_response(json=mock_return_value, url=f"{api_url}/api/workspaces")
        with httpx.Client():
            client = rg.Argilla(api_url=api_url, api_key="admin.apikey")
            created_workspace = client.create(ws)
            assert created_workspace.name == ws.name
            assert created_workspace.id == ws.id

    def test_multiple_clients_create_workspace(self, httpx_mock: HTTPXMock):
        mock_uuid = str(uuid.uuid4())
        mock_name = "local-test-workspace"
        mock_return = {
            "id": mock_uuid,
            "name": mock_name,
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        httpx_mock.add_response(
            url="http://localhost:6900/api/workspaces",
            json=mock_return,
        )
        httpx_mock.add_response(
            url="http://argilla.production.net/api/workspaces",
            json=mock_return,
        )
        with httpx.Client():
            local_client = rg.Argilla(api_url="http://localhost:6900", api_key="admin.apikey")
            remote_client = rg.Argilla(api_url="http://argilla.production.net", api_key="admin.apikey")
            assert local_client.api_url == "http://localhost:6900"
            assert remote_client.api_url == "http://argilla.production.net"
            workspace = rg.Workspace(name="local-test-workspace")
            local_client.create(workspace)
            remote_client.create(workspace)

    def test_delete_workspace(self, httpx_mock: HTTPXMock):
        workspace_id = uuid.uuid4()
        api_url = "http://test_url"
        httpx_mock.add_response(url=f"{api_url}/api/v1/workspaces/{workspace_id}", status_code=204)
        with httpx.Client():
            client = rg.Argilla(api_url=api_url, api_key="admin.apikey")
            client._workspaces.delete(workspace_id)

    def test_list_workspace_datasets(self, httpx_mock: HTTPXMock):
        workspace_id = uuid.uuid4()
        mock_return_value = {
            "items": [
                {
                    "id": str(uuid.uuid4()),
                    "name": "test-dataset",
                    "status": "ready",
                    "guidelines": "test-guidelines",
                    "allow_extra_metadata": True,
                    "workspace_id": str(workspace_id),
                    "inserted_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "another-test-dataset",
                    "status": "ready",
                    "guidelines": "test-guidelines",
                    "allow_extra_metadata": True,
                    "workspace_id": str(workspace_id),
                    "inserted_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                },
            ]
        }
        api_url = "http://test_url"
        httpx_mock.add_response(json=mock_return_value, url=f"{api_url}/api/v1/me/datasets")
        with httpx.Client():
            client = rg.Argilla(api_url=api_url, api_key="admin.apikey")
            datasets = client._datasets.list(workspace_id)
            assert len(datasets) == 2
            for i in range(len(datasets)):
                assert datasets[i].name == mock_return_value["items"][i]["name"]
                assert datasets[i].id == uuid.UUID(mock_return_value["items"][i]["id"])

    def test_list_workspace_users(self, httpx_mock: HTTPXMock):
        workspace_id = uuid.uuid4()
        mock_return_value = {
            "items": [
                {
                    "id": str(uuid.uuid4()),
                    "username": "test-user",
                    "first_name": "Test",
                    "last_name": "User",
                    "role": "admin",
                    "inserted_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                },
                {
                    "id": str(uuid.uuid4()),
                    "username": "another-test-user",
                    "first_name": "Another",
                    "last_name": "User",
                    "role": "admin",
                    "inserted_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                },
            ]
        }
        api_url = "http://test_url"
        httpx_mock.add_response(json=mock_return_value, url=f"{api_url}/api/workspaces/{workspace_id}/users")
        with httpx.Client():
            client = rg.Argilla(api_url=api_url, api_key="admin.apikey")
            users = client._users.list_by_workspace_id(workspace_id)
            assert len(users) == 2
            for i in range(len(users)):
                assert users[i].username == mock_return_value["items"][i]["username"]
                assert users[i].id == uuid.UUID(mock_return_value["items"][i]["id"])
