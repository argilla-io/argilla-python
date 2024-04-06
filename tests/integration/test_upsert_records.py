import uuid
from datetime import datetime

import pytest

import argilla_sdk as rg


@pytest.fixture
def client() -> rg.Argilla:
    return rg.Argilla()


def test_upsert_records(client):
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
        fields=[rg.TextField(name="text")],
        questions=[rg.TextQuestion(name="label", use_markdown=False)],
    )
    dataset = rg.Dataset(
        name=mock_dataset_name,
        workspace_id=workspace_id,
        settings=settings,
        client=client,
    )
    dataset.publish()
    created_records = dataset.records.upsert(records=mock_data)
    assert len(created_records) == len(list(dataset.records))
    for created_record, mock_record in zip(created_records, mock_data):
        assert created_record.external_id == str(mock_record["external_id"])
        assert created_record.fields["text"] == mock_record["text"]
        assert created_record.suggestions[0].value == mock_record["label"]

    dataset.records.upsert(records=updated_mock_data)
    dataset_records = list(dataset.records)

    assert dataset.name == mock_dataset_name
    assert dataset_records[0].external_id == str(mock_data[0]["external_id"])
    assert dataset_records[1].external_id == str(mock_data[1]["external_id"])
    assert dataset_records[2].external_id == str(mock_data[2]["external_id"])
    for record in dataset.records(with_suggestions=True):
        assert record.suggestions[0].value == "positive"
