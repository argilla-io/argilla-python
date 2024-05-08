import random

import pytest

import argilla_sdk as rg
from argilla_sdk._exceptions import NotFoundError


@pytest.fixture
def client() -> rg.Argilla:
    client = rg.Argilla(api_url="http://localhost:6900", api_key="argilla.apikey")
    return client


@pytest.fixture
def dataset(client: rg.Argilla):
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
    yield dataset
    dataset.delete()


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


def test_dataset_with_workspace_name(client: rg.Argilla):
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
        workspace=ws.name,
        client=client,
    )
    dataset.publish()
    assert dataset.id is not None
    assert dataset.exists()
    assert dataset.is_published
    assert dataset.workspace_id == ws.id


def test_dataset_with_incorrect_workspace_name(client: rg.Argilla):
    with pytest.raises(expected_exception=NotFoundError):
        rg.Dataset(
            name=f"test_{random.randint(0, 1000)}",
            settings=rg.Settings(
                fields=[
                    rg.TextField(name="text"),
                ],
                questions=[
                    rg.TextQuestion(name="response"),
                ],
            ),
            workspace=f"non_existing_workspace_{random.randint(0, 1000)}",
            client=client,
        )


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


def test_retrieving_dataset(client: rg.Argilla, dataset: rg.Dataset):
    ws = client.workspaces[0]
    dataset = client.datasets(dataset.name, workspace=ws)
    assert dataset.exists()


def test_retrieving_dataset_on_name(client: rg.Argilla, dataset: rg.Dataset):
    ws = client.workspaces[0]
    dataset = client.datasets(dataset.name, workspace=ws.name)
    assert dataset.exists()


def test_retrieving_dataset_on_default(client: rg.Argilla, dataset: rg.Dataset):
    ws = client.workspaces[0]
    dataset = client.datasets(dataset.name)
    assert dataset.exists()    
