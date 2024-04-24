import random
from string import ascii_lowercase

import pytest

import argilla_sdk as rg
from argilla_sdk import Argilla, Dataset, Settings, TextField, Workspace, LabelQuestion


@pytest.fixture
def client() -> Argilla:
    return Argilla()


@pytest.fixture
def workspace(client: Argilla) -> Workspace:
    workspace = client.workspaces("test-workspace")
    if not workspace.exists():
        workspace.create()
    yield workspace

    for dataset in workspace.list_datasets():
        client.api.datasets.delete(dataset.id)

    workspace.delete()


@pytest.fixture
def dataset(client: Argilla, workspace: Workspace) -> Dataset:
    name = "".join(random.choices(ascii_lowercase, k=16))
    settings = Settings(
        fields=[TextField(name="text")],
        questions=[LabelQuestion(name="label", labels=["positive", "negative"])],
    )
    dataset = Dataset(
        name=name,
        workspace_id=workspace.id,
        settings=settings,
        client=client,
    )
    dataset.publish()
    yield dataset
    dataset.delete()


def test_query_records_by_text(client: Argilla, dataset: Dataset):
    dataset.records.add(
        [
            {"text": "First record", "external_id": 1},
            {"text": "Second record", "external_id": 2},
        ]
    )

    records = list(dataset.records(query="first"))

    assert len(records) == 1
    assert records[0].external_id == "1"
    assert records[0].fields.text == "First record"

    records = list(dataset.records(query="second"))
    assert len(records) == 1
    assert records[0].external_id == "2"
    assert records[0].fields.text == "Second record"

    records = list(dataset.records(query="record"))
    assert len(records) == 2


def test_query_records_by_suggestion_value(client: Argilla, dataset: Dataset):
    data = [
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": 1,
        },
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "external_id": 2,
        },
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": 3,
        },
    ]

    dataset.records.add(data)

    query = rg.Query(filter=rg.Filter([("label", "==", "positive")]))
    records = list(dataset.records(query=query))

    assert len(records) == 2
    assert records[0].external_id == "1"
    assert records[1].external_id == "3"

    query = rg.Query(filter=rg.Filter(("label", "==", "negative")))
    records = list(dataset.records(query=query))

    assert len(records) == 1
    assert records[0].external_id == "2"

    query = rg.Query(filter=rg.Filter(("label", "in", ["positive", "negative"])))
    records = list(dataset.records(query=query))
    assert len(records) == 3

    test_filter = rg.Filter([("label", "==", "positive"), ("label", "==", "negative")])
    query = rg.Query(filter=test_filter)
    records = list(dataset.records(query=query))
    assert len(records) == 0
