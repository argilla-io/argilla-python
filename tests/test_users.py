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


class TestUserSerialization:
    def test_serialize(self):
        user = rg.User(
            id=uuid.uuid4(),
            username="test-user",
            first_name="Test",
            last_name="User",
            inserted_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        assert user.username == user.serialize()["username"]

    def test_serialize_with_extra_arguments(self):
        user = rg.User(
            id=uuid.uuid4(),
            username="test-user",
            password="test-password",
            first_name="Test",
            last_name="User",
            role="admin",
            extra_argument="extra-argument",
            another_extra_argument="another-extra-argument",
        )

        assert user.serialize() == {
            "id": user.id,
            "username": "test-user",
            "first_name": "Test",
            "last_name": "User",
            "role": "admin",
            "inserted_at": user.inserted_at,
            "updated_at": user.updated_at,
            "password": "test-password",
        }

    def test_json_serialize(self):
        user = rg.User(
            id=uuid.uuid4(),
            username="test-user",
            first_name="Test",
            last_name="User",
            inserted_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        user_from_json = json.loads(user.serialize_json())
        assert user.username == user_from_json["username"]
        assert user.id == user_from_json["id"]
        assert user.inserted_at == user_from_json["inserted_at"]
        assert user.updated_at == user_from_json["updated_at"]

    def test_model_from_json(self):
        user_id = uuid.uuid4().hex
        user_json = {
            "id": user_id,
            "username": "test-user",
            "first_name": "Test",
            "last_name": "User",
            "role": "admin",
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        user = rg.User(**user_json)
        assert user.username == user_json["username"]
        assert user.id == user_json["id"]
        assert user.inserted_at == user_json["inserted_at"]
        assert user.updated_at == user_json["updated_at"]

class TestUsers:

    def test_create_user(self, httpx_mock: HTTPXMock):
        user_id = uuid.uuid4().hex
        mock_return_value = {
            "id": str(user_id),
            "username": "test-user",
            "password": "test-password",
            "first_name": "Test",
            "last_name": "User",
            "role": "admin",
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        api_url = "http://test_url"
        httpx_mock.add_response(json=mock_return_value, url=f"{api_url}/api/users", method="POST")
        with httpx.Client():
            client = rg.Argilla(api_url=api_url, api_key="admin.apikey")
            user = rg.User(**mock_return_value)
            client.create(user)

    def test_get_user(self, httpx_mock: HTTPXMock):
        user_id = uuid.uuid4().hex
        mock_return_value = {
            "id": user_id,
            "username": "test-user",
            "password": "test-password",
            "first_name": "Test",
            "last_name": "User",
            "role": "admin",
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        api_url = "http://test_url"
        httpx_mock.add_response(json=mock_return_value, url=f"{api_url}/api/users", method="POST")
        httpx_mock.add_response(json=mock_return_value, url=f"{api_url}/api/users/{user_id}")
        with httpx.Client():
            client = rg.Argilla(api_url=api_url, api_key="admin.apikey")
            user = rg.User(**mock_return_value)
            client.create(user)
            gotten_user = client.get(user)
            assert user.username == gotten_user.username
            assert user.id == gotten_user.id

    def test_list_users(self, httpx_mock: HTTPXMock):
        mock_return_value = [
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
                "role": "annotator",
                "first_name": "First",
                "last_name": "Last",
                "inserted_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            },
        ]
        api_url = "http://test_url"
        httpx_mock.add_response(json=mock_return_value, url=f"{api_url}/api/users")
        with httpx.Client():
            client = rg.Argilla(api_url="http://test_url", api_key="admin.apikey")
            users = client.list(rg.User)
            assert len(users) == 2
            for i in range(len(users)):
                assert users[i].username == mock_return_value[i]["username"]
                assert users[i].role == mock_return_value[i]["role"]
                assert users[i].id == uuid.UUID(mock_return_value[i]["id"])


class TestUsersAPI:
    def test_get_me(self, httpx_mock: HTTPXMock):
        mock_return_value = {
            "id": str(uuid.uuid4()),
            "username": "test-user",
            "first_name": "Test",
            "last_name": "User",
            "role": "admin",
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        api_url = "http://test_url"
        httpx_mock.add_response(json=mock_return_value, url=f"{api_url}/api/me")
        with httpx.Client():
            client = rg.Argilla(api_url=api_url, api_key="admin.apikey")
            user = client._users.get_me()
            assert user.username == mock_return_value["username"]
            assert user.id == uuid.UUID(mock_return_value["id"])
            assert user.role == mock_return_value["role"]

    def test_add_user_to_workspace(self, httpx_mock: HTTPXMock):
        user_id = uuid.uuid4().hex
        workspace_id = uuid.uuid4().hex
        mock_workspace_user_return_value = {
            "id": str(user_id),
            "username": "test-user",
            "password": "test-password",
            "first_name": "Test",
            "last_name": "User",
            "role": "admin",
            "inserted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        httpx_mock.add_response(
            json=mock_workspace_user_return_value, url=f"http://test_url/api/users/{user_id}", method="GET"
        )
        httpx_mock.add_response(url=f"http://test_url/api/v1/workspaces/{workspace_id}/users/{user_id}", method="POST")
        with httpx.Client():
            client = rg.Argilla(api_url="http://test_url", api_key="admin.apikey")
            user = rg.User(**mock_workspace_user_return_value)
            client._workspaces.add_user(workspace_id, user_id)
            gotten_user = client.get(user)
            assert user.username == gotten_user.username
            assert user.id == gotten_user.id
    
    def test_remove_user_from_workspace(self, httpx_mock: HTTPXMock):
        user_id = uuid.uuid4()
        workspace_id = uuid.uuid4()
        httpx_mock.add_response(
            url=f"http://test_url/api/v1/workspaces/{workspace_id}/users/{user_id}", method="DELETE"
        )
        with httpx.Client():
            client = rg.Argilla(api_url="http://test_url", api_key="admin.apikey")
            client._workspaces.remove_user(workspace_id, user_id)

    def test_delete_user(self, httpx_mock: HTTPXMock):
        user_id = uuid.uuid4()
        httpx_mock.add_response(url=f"http://test_url/api/users/{user_id}", method="DELETE")
        with httpx.Client():
            client = rg.Argilla(api_url="http://test_url", api_key="admin.apikey")
            client._users.delete(user_id)

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