import uuid

from unittest import mock

import argilla_sdk as rg


def test_default_client():
    with mock.patch("argilla_sdk.Argilla") as mock_client:
        mock_client.return_value.api_url = "http://localhost:6900"
        mock_client.return_value.api_key = "admin.apikey"
        mock_client.return_value.workspace = "argilla"

        client = rg.Argilla(api_url="http://localhost:6900", api_key="admin.apikey")
        assert client.api_url == "http://localhost:6900"
        assert client.api_key == "admin.apikey"


def test_create_workspace():
    mock_uuid = uuid.uuid4()
    mock_name = "test-workspace"
    mock_return = {"id": mock_uuid, "name": mock_name}
    with mock.patch("argilla_sdk.client._api.WorkspacesAPI.create") as patch:
        patch.return_value = mock_return
        client = rg.Argilla(api_url="http://test_url", api_key="admin.apikey")
        workspace = rg.Workspace(name=mock_name, id=mock_uuid)
        client.create(workspace)
        patch.assert_called_once_with(workspace)


def test_get_workspace():
    mock_uuid = uuid.uuid4()
    mock_name = "test-workspace"
    mock_return = mock.Mock(id=mock_uuid, name=mock_name)
    with mock.patch("argilla_sdk.client._api.WorkspacesAPI.create"):
        with mock.patch("argilla_sdk.client._api.WorkspacesAPI.get") as patch:
            patch.return_value = mock_return
            client = rg.Argilla(api_url="http://test_url", api_key="admin.apikey")
            workspace = rg.Workspace(name=mock_name, id=mock_uuid)
            client.workspaces.create(workspace)
            gotten_workspace = client.get(workspace)
            patch.assert_called_once_with(workspace.id)
            assert gotten_workspace.id == mock_uuid


def test_create_user():
    """
    Test creating a user with the default client.
    """
    mock_username = "john.doe"
    mock_first_name = "John"
    mock_role = "admin"
    mock_last_name = "Doe"
    mock_password = "password"
    mock_inserted_at = "2021-01-01T00:00:00"
    mock_updated_at = "2021-01-01T00:00:00"
    mock_user = rg.User(
        username=mock_username,
        first_name=mock_first_name,
        role=mock_role,
        last_name=mock_last_name,
        password=mock_password,
        inserted_at=mock_inserted_at,
        updated_at=mock_updated_at,
    )
    with mock.patch("argilla_sdk.client._api.UsersAPI.create") as mock_client:
        client = rg.Argilla(api_url="http://localhost:6900", api_key="admin.apikey")
        client.create(mock_user)
        mock_client.assert_called_once_with(mock_user)


def test_multiple_clients():
    with mock.patch("argilla_sdk.client._api.APIClient.http_client") as mock_client:
        local_client = rg.Argilla(api_url="http://localhost:6900", api_key="admin.apikey")
        remote_client = rg.Argilla(api_url="http://argilla.production.net", api_key="admin.apikey")
        assert local_client.api_url == "http://localhost:6900"
        assert remote_client.api_url == "http://argilla.production.net"
