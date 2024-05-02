import random

import pytest

import argilla_sdk as rg


@pytest.fixture
def client() -> rg.Argilla:
    client = rg.Argilla(api_url="http://localhost:6900", api_key="owner.apikey")
    return client


def test_dataset_with_workspace_id(client: rg.Argilla):
    workspace_id = client.workspaces[0].id
    dataset = rg.Dataset(
        name=f"test_{random.randint(0, 1000)}",
        settings=rg.Settings(
            fields=[
                rg.TextField(name="text"),
            ],
            questions=[
                rg.TextQuestion(name="response"),
            ],
        ),
        workspace_id=workspace_id,
        client=client,
    )
    dataset.publish()
    assert dataset.id is not None
    assert dataset.exists()
    assert dataset.is_published
    assert dataset.workspace_id == workspace_id


def test_dataset_with_workspace(client: rg.Argilla):
    ws = client.workspaces[0]
    dataset = rg.Dataset(
        name=f"test_{random.randint(0, 1000)}",
        settings=rg.Settings(
            fields=[
                rg.TextField(name="text"),
            ],
            questions=[
                rg.TextQuestion(name="response"),
            ],
        ),
        workspace=ws,
        client=client,
    )
    dataset.publish()
    assert dataset.id is not None
    assert dataset.exists()
    assert dataset.is_published
    assert dataset.workspace_id == ws.id


def test_dataset_with_default_workspace(client: rg.Argilla):
    dataset = rg.Dataset(
        name=f"test_{random.randint(0, 1000)}",
        settings=rg.Settings(
            fields=[
                rg.TextField(name="text"),
            ],
            questions=[
                rg.TextQuestion(name="response"),
            ],
        ),
        client=client,
    )
    dataset.publish()
    assert dataset.id is not None
    assert dataset.exists()
    assert dataset.is_published
    assert dataset.workspace_id == client.workspaces[0].id
