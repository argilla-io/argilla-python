import random
import uuid
from datetime import datetime

import pytest

import argilla_sdk as rg
from argilla_sdk import Argilla


@pytest.fixture
def client() -> rg.Argilla:
    client = rg.Argilla(api_url="http://localhost:6900", api_key="owner.apikey")
    return client


def test_create_dataset(client):
    workspace_id = client.workspaces[0].id
    mock_dataset_name = f"test_create_dataset{datetime.now().strftime('%Y%m%d%H%M%S')}"
    dataset = rg.Dataset(
        name=mock_dataset_name,
        workspace_id=workspace_id,
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
    gotten_dataset = dataset.get()
    assert dataset.id == gotten_dataset.id
    assert dataset.name == mock_dataset_name


def test_add_records(client):
    workspace_id = client.workspaces[0].id
    mock_dataset_name = f"test_add_records{datetime.now().strftime('%Y%m%d%H%M%S')}"
    mock_data = [
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": uuid.uuid4(),
        },
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "external_id": uuid.uuid4(),
        },
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": uuid.uuid4(),
        },
    ]
    settings = rg.Settings(
        fields=[
            rg.TextField(name="text"),
        ],
        questions=[
            rg.TextQuestion(name="comment", use_markdown=False),
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

    dataset_records = list(dataset.records)

    assert dataset.name == mock_dataset_name
    assert dataset_records[0].external_id == str(mock_data[0]["external_id"])
    assert dataset_records[1].external_id == str(mock_data[1]["external_id"])
    assert dataset_records[2].external_id == str(mock_data[2]["external_id"])
    assert dataset_records[0].text == mock_data[0]["text"]
    assert dataset_records[1].text == mock_data[1]["text"]
    assert dataset_records[2].text == mock_data[2]["text"]


def test_add_dict_records(client: Argilla):
    ws = client.workspaces("argilla")

    new_ws = client.workspaces("new_ws")
    if not new_ws.exists():
        new_ws.create()

    ds = client.datasets("new_ds", workspace=ws)
    if ds.exists():
        ds.delete()

    ds.settings = rg.Settings(
        fields=[rg.TextField(name="text")],
        questions=[rg.TextQuestion(name="label")],
    )

    ds.publish()

    mock_data = [
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": "1",
        },
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "external_id": "2",
        },
        {"text": "Hello World, how are you?", "label": "negative", "external_id": "3"},
    ]

    # Now the dataset is published and is ready for annotate
    ds.records.add(mock_data)

    for record, data in zip(ds.records, mock_data):
        assert record.id
        assert record.external_id == data["external_id"]
        assert record.text == data["text"]
        assert "label" not in record.__dict__

    for record, data in zip(ds.records(batch_size=1, with_suggestions=True), mock_data):
        assert record.external_id == data["external_id"]
        assert record.label == data["label"]


def test_add_records_with_suggestions(client) -> None:
    workspace_id = client.workspaces[0].id
    mock_dataset_name = f"test_add_record_with_suggestions {datetime.now().strftime('%Y%m%d%H%M%S')}"
    mock_data = [
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": uuid.uuid4(),
            "comment": "I'm doing great, thank you!",
        },
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "external_id": uuid.uuid4(),
            "comment": "I'm doing great, thank you!",
        },
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": uuid.uuid4(),
            "comment": "I'm doing great, thank you!",
        },
    ]
    settings = rg.Settings(
        fields=[
            rg.TextField(name="text"),
        ],
        questions=[
            rg.TextQuestion(name="comment", use_markdown=False),
        ],
    )
    dataset = rg.Dataset(
        name=mock_dataset_name,
        workspace_id=workspace_id,
        settings=settings,
        client=client,
    )
    dataset.publish()
    dataset.records.add(mock_data)
    assert dataset.name == mock_dataset_name

    dataset_records = list(dataset.records(with_suggestions=True))

    assert dataset_records[0].external_id == str(mock_data[0]["external_id"])
    assert dataset_records[1].text == mock_data[1]["text"]
    assert dataset_records[2].comment == "I'm doing great, thank you!"


@pytest.mark.skip("Responses are not supported yet")
def test_add_records_with_responses(client) -> None:
    workspace_id = client.workspaces[0].id
    mock_dataset_name = f"test_modify_record_responses_locally {uuid.uuid4()}"
    mock_data = [
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": uuid.uuid4(),
        },
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "external_id": uuid.uuid4(),
        },
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": uuid.uuid4(),
        },
    ]
    settings = rg.Settings(
        fields=[
            rg.TextField(name="text"),
        ],
        questions=[
            rg.TextQuestion(name="text", use_markdown=False),
        ],
    )
    dataset = rg.Dataset(
        name=mock_dataset_name,
        workspace_id=workspace_id,
        settings=settings,
        client=client,
    )
    user = rg.User(
        username=f"test_{random.randint(0, 1000)}",
        first_name="test",
        password="testtesttest",
        client=client,
    )
    user.create()
    dataset.publish()
    dataset.records.add(
        records=[
            rg.Record(
                fields={
                    "text": _record["text"],
                },
                external_id=_record["external_id"],
                responses=[rg.Response(question_name="text", value=_record["label"], user_id=user.id, status="draft")],
            )
            for _record in mock_data
        ]
    )
    assert dataset.name == mock_dataset_name
    assert dataset.records[0].external_id == mock_data[0]["external_id"]
    assert dataset.records[1].fields["text"] == mock_data[1]["text"]
    assert dataset.records[2].responses[0].values["text"]["value"] == "positive"
