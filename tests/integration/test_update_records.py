import random
import uuid
from datetime import datetime

import pytest

import argilla_sdk as rg
from argilla_sdk import Argilla


@pytest.fixture
def client() -> rg.Argilla:
    client = rg.Argilla(api_url="http://localhost:6900")
    return client


def test_update_records_seperately(client):
    workspace_id = client.workspaces[0].id
    mock_dataset_name = f"test_add_records{datetime.now().strftime('%Y%m%d%H%M%S')}"
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
        workspace_id=workspace_id,
        settings=settings,
        client=client,
    )
    dataset.publish()
    dataset.records.add(records=mock_data)
    dataset.records.update(records=updated_mock_data)
    dataset_records = list(dataset.records)

    assert dataset.name == mock_dataset_name
    assert dataset_records[0].external_id == str(mock_data[0]["external_id"])
    assert dataset_records[1].external_id == str(mock_data[1]["external_id"])
    assert dataset_records[2].external_id == str(mock_data[2]["external_id"])
    for record in dataset.records(with_suggestions=True):
        assert record.suggestions[0].value == "positive"


def test_update_records_partially(client):
    workspace_id = client.workspaces[0].id
    mock_dataset_name = f"test_add_records{datetime.now().strftime('%Y%m%d%H%M%S')}"
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
        workspace_id=workspace_id,
        settings=settings,
        client=client,
    )
    dataset.publish()
    dataset.records.add(records=mock_data)
    dataset.records.update(records=updated_mock_data)
    for i, record in enumerate(dataset.records(with_suggestions=True)):
        assert record.suggestions[0].value == updated_mock_data[i]["label"]
    