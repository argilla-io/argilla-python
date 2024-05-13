import random
import uuid
from datetime import datetime
from string import ascii_lowercase

import pytest

import argilla_sdk as rg


@pytest.fixture
def dataset(client: rg.Argilla) -> rg.Dataset:
    workspace = client.workspaces[0]
    mock_dataset_name = "".join(random.choices(ascii_lowercase, k=16))
    settings = rg.Settings(
        fields=[
            rg.TextField(name="text"),
        ],
        questions=[
            rg.TextQuestion(name="label", use_markdown=False),
        ],
    )
    dataset = rg.Dataset(
        name=mock_dataset_name,
        workspace=workspace.name,
        settings=settings,
        client=client,
    )
    dataset.create()
    return dataset


def test_update_records_separately(client: rg.Argilla, dataset: rg.Dataset):
    mock_data = [
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "external_id": uuid.uuid4(),
        },
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "external_id": uuid.uuid4(),
        },
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "external_id": uuid.uuid4(),
        },
    ]
    updated_mock_data = [
        {
            "text": r["text"],
            "label": "positive",
            "external_id": r["external_id"],
        }
        for r in mock_data
    ]

    dataset.records.add(records=mock_data)
    dataset.records.update(records=updated_mock_data)
    dataset_records = list(dataset.records)

    assert dataset_records[0].external_id == str(mock_data[0]["external_id"])
    assert dataset_records[1].external_id == str(mock_data[1]["external_id"])
    assert dataset_records[2].external_id == str(mock_data[2]["external_id"])
    for record in dataset.records(with_suggestions=True):
        assert record.suggestions[0].value == "positive"


def test_update_records_partially(client: rg.Argilla, dataset: rg.Dataset):
    mock_data = [
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "external_id": uuid.uuid4(),
        },
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "external_id": uuid.uuid4(),
        },
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "external_id": uuid.uuid4(),
        },
    ]
    updated_mock_data = mock_data.copy()
    updated_mock_data[0]["label"] = "positive"
    dataset.records.add(records=mock_data)
    dataset.records.update(records=updated_mock_data)
    for i, record in enumerate(dataset.records(with_suggestions=True)):
        assert record.suggestions[0].value == updated_mock_data[i]["label"]
