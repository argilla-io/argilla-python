import uuid

from unittest import mock
import argilla_sdk as rg


def test_default_client():
    with mock.patch("argilla_sdk.Client") as mock_client:
        mock_client.return_value.api_url = "http://localhost:6900"
        mock_client.return_value.api_key = "admin.apikey"
        mock_client.return_value.workspace = "argilla"

        client = rg.Client(api_url="http://localhost:6900", api_key="admin.apikey")
        assert client.api_url == "http://localhost:6900"
        assert client.api_key == "admin.apikey"
        assert client.workspace == "argilla"


def test_default_client_create_workspace():
    mock_uuid = uuid.uuid4()
    mock_name = "test-workspace"
    mock_return = {"id": mock_uuid, "name": mock_name}
    with mock.patch("argilla_sdk.client._api.Workspace.create") as patch:
        patch.return_value = mock_return
        client = rg.Client(api_url="http://test_url", api_key="admin.apikey")
        workspace = rg.Workspace(name=mock_name, id=mock_uuid)
        client.workspaces.create(workspace)
        patch.assert_called_once_with(workspace)


def test_default_client_create_workspace_then_get():
    mock_uuid = uuid.uuid4()
    mock_name = "test-workspace"
    mock_return = {"id": mock_uuid, "name": mock_name}
    with mock.patch("argilla_sdk.client._api.Workspace.create"):
        with mock.patch("argilla_sdk.client._api.Workspace.get") as patch:
            patch.return_value = mock_return
            client = rg.Client(api_url="http://test_url", api_key="admin.apikey")
            workspace = rg.Workspace(name=mock_name, id=mock_uuid)
            client.workspaces.create(workspace)
            gotten_workspace = client.get(workspace)
            patch.assert_called_once_with(workspace.id)
            assert gotten_workspace == workspace


def test_default_client_create_user():
    with mock.patch("argilla_sdk.Client") as mock_client:
        client = mock_client.return_value
        user = mock.Mock()
        client.user.create.return_value = user

        client = rg.Client(api_rul="http://localhost, 6900", api_key="admin.apikey")
        client.user.create(user)
        assert client.user.get(name="John Doe", workspace=workspace.name) == user
        assert client.user.get(name="John Doe") == user


def test_multiple_clients():
    with mock.patch("argilla_sdk.Client") as mock_client:
        client = mock_client.return_value
        client.api_url = "http://localhost:6900"

        local_client = rg.Client(api_rul="http://localhost:6900", api_key="admin.apikey")
        assert local_client.api_url == "http://localhost:6900"


def test_multiple_clients_create_workspace():
    with mock.patch("argilla_sdk.Client") as mock_client:
        client = mock_client.return_value
        workspace = mock.Mock()
        client.workspace.create.return_value = workspace

        local_client = rg.Client(api_rul="http://localhost:6900", api_key="admin.apikey")
        production_client = rg.Client(api_rul="http://argilla.production.net", api_key="admin.apikey")
        local_client.workspace.create(workspace)
        production_client.workspace.create(workspace)
        assert local_client.workspace.get(name="MyWorkspace") == workspace


def test_multiple_clients_create_user():
    with mock.patch("argilla_sdk.Client") as mock_client:
        client = mock_client.return_value
        user = mock.Mock()
        client.user.create.return_value = user

        local_client = rg.Client(api_rul="http://localhost:6900", api_key="admin.apikey")
        production_client = rg.Client(api_rul="http://argilla.production.net", api_key="admin.apikey")
        client.user.create(user)
        user_from_local = client.user.get(name="John Doe", workspace=local_client.workspace.name)
        production_client.user.create(user_from_local)
        assert (
            production_client.user.get(name="John Doe", workspace=production_client.workspace.name) == user_from_local
        )
        assert production_client.user.get(name="John Doe") == user_from_local
