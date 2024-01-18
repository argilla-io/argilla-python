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

from argilla_sdk import Role, User, Workspace


class TestUsers:
    def test_serialize(self, mock_httpx_client: httpx.Client):
        user = User(
            id=uuid.uuid4(),
            username="test-user",
            first_name="Test",
            last_name="User",
            inserted_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            client=mock_httpx_client,
        )

        assert User.from_dict(user.to_dict()) == user

    def test_serialize_with_extra_arguments(self, mock_httpx_client: httpx.Client):
        user = User.from_dict(
            {
                "id": uuid.uuid4(),
                "username": "test-user",
                "password": "test-password",
                "first_name": "Test",
                "last_name": "User",
                "role": "admin",
                "client": mock_httpx_client,
                "extra_argument": "extra-argument",
                "another_extra_argument": "another-extra-argument",
            }
        )

        assert user.to_dict() == {
            "id": user.id,
            "username": "test-user",
            "api_key": None,
            "first_name": "Test",
            "last_name": "User",
            "role": "admin",
            "inserted_at": user.inserted_at,
            "updated_at": user.updated_at,
        }

    def test_list_users(self, mocker: MockerFixture, mock_httpx_client: httpx.Client):
        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value=[
                {
                    "id": uuid.uuid4(),
                    "username": "test-user",
                    "first_name": "Test",
                    "last_name": "User",
                    "role": "admin",
                },
                {
                    "id": uuid.uuid4(),
                    "username": "another-test-user",
                    "role": "annotator",
                    "first_name": "First",
                    "last_name": "Last",
                },
            ]
        )

        mock_httpx_client.get = mocker.MagicMock(return_value=mock_response)

        users = User.list()
        mock_httpx_client.get.assert_called_once_with("/api/users")

        assert len(users) == 2
        items_json = mock_response.json()
        for i in range(len(users)):
            assert users[i].username == items_json[i]["username"]
            assert users[i].id == items_json[i]["id"]
            assert users[i].role == items_json[i]["role"]
            assert users[i].client == mock_httpx_client

    def test_list_workspace_users(self, mocker: MockerFixture, mock_httpx_client: httpx.Client):
        workspace = Workspace(id=uuid.uuid4(), name="test-workspace", client=mock_httpx_client)

        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value=[
                {
                    "id": uuid.uuid4(),
                    "username": "test-user",
                    "first_name": "Test",
                    "last_name": "User",
                    "role": "admin",
                },
                {
                    "id": uuid.uuid4(),
                    "username": "another-test-user",
                    "role": "annotator",
                    "first_name": "First",
                    "last_name": "Last",
                },
            ]
        )

        mock_httpx_client.get = mocker.MagicMock(return_value=mock_response)

        users = workspace.users.list()
        mock_httpx_client.get.assert_called_once_with(f"/api/workspaces/{workspace.id}/users")

        assert len(users) == 2
        items_json = mock_response.json()
        for i in range(len(users)):
            assert users[i].username == items_json[i]["username"]
            assert users[i].id == items_json[i]["id"]
            assert users[i].role == items_json[i]["role"]
            assert users[i].client == mock_httpx_client

    def test_get_me(self, mocker: MockerFixture, mock_httpx_client: httpx.Client):
        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value={
                "id": uuid.uuid4(),
                "username": "test-user",
                "first_name": "Test",
                "last_name": "User",
                "role": "admin",
            }
        )

        mock_httpx_client.get = mocker.MagicMock(return_value=mock_response)

        user = User.get_me()
        mock_httpx_client.get.assert_called_once_with("/api/me")

        assert user.username == mock_response.json()["username"]
        assert user.id == mock_response.json()["id"]
        assert user.role == mock_response.json()["role"]
        assert user.client == mock_httpx_client

    def test_create_user(self, mocker: MockerFixture, mock_httpx_client: httpx.Client):
        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value={
                "id": uuid.uuid4(),
                "username": "test-user",
                "password": "test-password",
                "first_name": "Test",
                "last_name": "User",
                "role": "admin",
            }
        )

        mock_httpx_client.post = mocker.MagicMock(return_value=mock_response)

        user = User(
            username="test-user",
            password="test-password",
            first_name="Test",
            last_name="User",
            role=Role.admin,
            client=mock_httpx_client,
        )

        user.create()
        mock_httpx_client.post.assert_called_once_with(
            "/api/users",
            json={
                "username": "test-user",
                "password": "test-password",
                "first_name": "Test",
                "last_name": "User",
                "role": Role.admin,
            },
        )

        assert user.username == mock_response.json()["username"]
        assert user.id == mock_response.json()["id"]
        assert user.role == mock_response.json()["role"]
        assert user.client == mock_httpx_client

    def test_add_user_to_workspace(self, mocker: MockerFixture, mock_httpx_client: httpx.Client):
        workspace = Workspace(id=uuid.uuid4(), name="test-workspace", client=mock_httpx_client)
        user_id = uuid.uuid4()

        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value={
                "id": user_id,
                "username": "test-user",
                "password": "test-password",
                "first_name": "Test",
                "last_name": "User",
                "role": "admin",
            }
        )

        mock_httpx_client.post = mocker.MagicMock(return_value=mock_response)

        user = User(
            id=user_id,
            username="test-user",
            first_name="Test",
            last_name="User",
            role=Role.admin,
            client=mock_httpx_client,
        )

        workspace.users.add(user)
        mock_httpx_client.post.assert_called_once_with(f"/api/workspaces/{workspace.id}/users/{user_id}")

        assert user.username == mock_response.json()["username"]
        assert user.id == mock_response.json()["id"]
        assert user.role == mock_response.json()["role"]
        assert user.client == mock_httpx_client

    def test_delete_user_from_workspace(self, mocker: MockerFixture, mock_httpx_client: httpx.Client):
        workspace = Workspace(id=uuid.uuid4(), name="test-workspace", client=mock_httpx_client)
        user_id = uuid.uuid4()

        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value={
                "id": user_id,
                "username": "test-user",
                "password": "test-password",
                "first_name": "Test",
                "last_name": "User",
                "role": "admin",
            }
        )

        mock_httpx_client.delete = mocker.MagicMock(return_value=mock_response)

        user = User(
            id=user_id,
            username="test-user",
            first_name="Test",
            last_name="User",
            role=Role.admin,
            client=mock_httpx_client,
        )

        workspace.users.delete(user)
        mock_httpx_client.delete.assert_called_once_with(f"/api/workspaces/{workspace.id}/users/{user_id}")

        assert user.username == mock_response.json()["username"]
        assert user.id == mock_response.json()["id"]
        assert user.role == mock_response.json()["role"]
        assert user.client == mock_httpx_client

    def test_delete_user(self, mocker: MockerFixture, mock_httpx_client: httpx.Client):
        user_id = uuid.uuid4()

        mock_response = mocker.Mock(httpx.Response)
        mock_response.json = mocker.Mock(
            return_value={
                "id": user_id,
                "username": "test-user",
                "password": "test-password",
                "first_name": "Test",
                "last_name": "User",
                "role": "admin",
            }
        )

        mock_httpx_client.delete = mocker.MagicMock(return_value=mock_response)

        user = User(
            id=user_id,
            username="test-user",
            first_name="Test",
            last_name="User",
            role=Role.admin,
            client=mock_httpx_client,
        )

        user.delete()
        mock_httpx_client.delete.assert_called_once_with(f"/api/users/{user_id}")

        assert user.username == mock_response.json()["username"]
        assert user.id == mock_response.json()["id"]
        assert user.role == mock_response.json()["role"]
        assert user.client == mock_httpx_client
