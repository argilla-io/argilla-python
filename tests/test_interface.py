import pytest

import argilla_sdk as rg


def test_default_client():
    client = rg.Client(api_rul="http://localhost:6900", api_key="admin.apikey")
    assert client.api_url == "http://localhost:6900"
    assert client.api_key == "admin.apikey"
    assert client.workspace is "argilla"


def test_default_client_create_workspace():
    client = rg.Client(api_rul="http://localhost:6900", api_key="admin.apikey")
    workspace = rg.Workspace(name="MyWorkspace")
    client.workspace.create(workspace)
    assert client.workspace.get(name="MyWorkspace") == workspace
    assert client.workspace.get(name="MyWorkspace") == workspace


def test_default_client_create_user():
    client = rg.Client(api_rul="http://localhost, 6900", api_key="admin.apikey")
    user = rg.User(name="John Doe", role="admin", workspace=workspace.name)
    client.user.create(user)
    assert client.user.get(name="John Doe", workspace=workspace.name) == user
    assert client.user.get(name="John Doe") == user


def test_multiple_clients():
    local_client = rg.Client(api_rul="http://localhost:6900", api_key="admin.apikey")
    production_client = rg.Client(api_rul="http://argilla.production.net", api_key="admin.apikey")
    assert local_client.api_url == "http://localhost:6900"


def test_multiple_clients_create_workspace():
    local_client = rg.Client(api_rul="http://localhost:6900", api_key="admin.apikey")
    production_client = rg.Client(api_rul="http://argilla.production.net", api_key="admin.apikey")
    # Creating a workspace
    workspace = rg.Workspace(name="MyWorkspace")
    local_client.workspace.create(workspace)
    production_client.workspace.create(workspace)
    assert local_client.workspace.get(name="MyWorkspace") == workspace


def test_multiple_clients_create_user():
    local_client = rg.Client(api_rul="http://localhost:6900", api_key="admin.apikey")
    production_client = rg.Client(api_rul="http://argilla.production.net", api_key="admin.apikey")
    user = rg.User(name="John Doe", role="admin", workspace=workspace.name)
    client.user.create(user)
    user_from_local = client.user.get(name="John Doe", workspace=local_client.workspace.name)
    production_client.user.create(user_from_local)
    assert production_client.user.get(name="John Doe", workspace=production_client.workspace.name) == user_from_local
    assert production_client.user.get(name="John Doe") == user_from_local
    