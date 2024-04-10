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
    assert dataset_records[0].fields.text == mock_data[0]["text"]
    assert dataset_records[1].fields.text == mock_data[1]["text"]
    assert dataset_records[2].fields.text == mock_data[2]["text"]


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
        assert record.fields.text == data["text"]
        assert "label" not in record.__dict__

    for record, data in zip(ds.records(batch_size=1, with_suggestions=True), mock_data):
        assert record.external_id == data["external_id"]
        assert record.suggestions.label == data["label"]


def test_add_single_record(client: Argilla):
    new_ws = client.workspaces("new_ws")
    if not new_ws.exists():
        new_ws.create()

    ds = client.datasets("new_ds", workspace=new_ws)
    if ds.exists():
        ds.delete()

    ds.settings = rg.Settings(
        fields=[rg.TextField(name="text")],
        questions=[rg.TextQuestion(name="label")],
    )

    ds.publish()

    data = {
        "text": "Hello World, how are you?",
        "label": "positive",
        "external_id": "1",
    }

    # Now the dataset is published and is ready for annotate
    ds.records.add(data)

    records = list(ds.records)
    assert len(records) == 1

    record = records[0]
    assert record.id
    assert record.external_id == data["external_id"]
    assert record.fields.text == data["text"]


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
    assert dataset_records[1].fields.text == mock_data[1]["text"]
    assert dataset_records[2].suggestions.comment == "I'm doing great, thank you!"


def test_add_records_with_responses(client) -> None:
    workspace_id = client.workspaces[0].id
    mock_dataset_name = f"test_modify_record_responses_locally {uuid.uuid4()}"
    mock_data = [
        {
            "text": "Hello World, how are you?",
            "my_label": "positive",
            "external_id": uuid.uuid4(),
        },
        {
            "text": "Hello World, how are you?",
            "my_label": "positive",
            "external_id": uuid.uuid4(),
        },
        {
            "text": "Hello World, how are you?",
            "my_label": "negative",
            "external_id": uuid.uuid4(),
        },
    ]
    settings = rg.Settings(
        fields=[
            rg.TextField(name="text"),
        ],
        questions=[
            rg.LabelQuestion(name="label", labels=["positive", "negative"]),
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
        records=mock_data,
        user_id=user.id,
        mapping={
            "my_label": "label.response",
        },
    )
    assert dataset.name == mock_dataset_name

    dataset_records = list(dataset.records(with_responses=True))

    for record, mock_record in zip(dataset_records, mock_data):
        assert record.external_id == str(mock_record["external_id"])
        assert record.fields.text == mock_record["text"]
        assert record.responses.label[0].value == mock_record["my_label"]
        assert record.responses.label[0].user_id == user.id 


def test_add_records_with_responses_and_suggestions(client) -> None:
    workspace_id = client.workspaces[0].id
    mock_dataset_name = f"test_modify_record_responses_locally {uuid.uuid4()}"
    mock_data = [
        {
            "text": "Hello World, how are you?",
            "my_label": "negative",
            "my_guess": "positive",
            "external_id": uuid.uuid4(),
        },
        {
            "text": "Hello World, how are you?",
            "my_label": "negative",
            "my_guess": "positive",
            "external_id": uuid.uuid4(),
        },
        {
            "text": "Hello World, how are you?",
            "my_label": "negative",
            "my_guess": "positive",
            "external_id": uuid.uuid4(),
        },
    ]
    settings = rg.Settings(
        fields=[
            rg.TextField(name="text"),
        ],
        questions=[
            rg.LabelQuestion(name="label", labels=["positive", "negative"]),
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
        records=mock_data,
        user_id=user.id,
        mapping={
            "my_label": "label.response",
            "my_guess": "label.suggestion",
        },
    )
    assert dataset.name == mock_dataset_name

    dataset_records = list(dataset.records(with_suggestions=True))

    assert dataset_records[0].external_id == str(mock_data[0]["external_id"])
    assert dataset_records[1].fields.text == mock_data[1]["text"]
    assert dataset_records[2].suggestions.label == "positive"
    assert dataset_records[2].responses.label[0].value == "negative"
    assert dataset_records[2].responses.label[0].user_id == user.id


def test_add_records_with_fields_mapped(client) -> None:
    workspace_id = client.workspaces[0].id
    mock_dataset_name = f"test_modify_record_responses_locally {uuid.uuid4()}"
    mock_data = [
        {
            "x": "Hello World, how are you?",
            "my_label": "negative",
            "my_guess": "positive",
            "external_id": uuid.uuid4(),
        },
        {
            "x": "Hello World, how are you?",
            "my_label": "negative",
            "my_guess": "positive",
            "external_id": uuid.uuid4(),
        },
        {
            "x": "Hello World, how are you?",
            "my_label": "negative",
            "my_guess": "positive",
            "external_id": uuid.uuid4(),
        },
    ]
    settings = rg.Settings(
        fields=[
            rg.TextField(name="text"),
        ],
        questions=[
            rg.LabelQuestion(name="label", labels=["positive", "negative"]),
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
        records=mock_data,
        user_id=user.id,
        mapping={
            "my_label": "label.response",
            "my_guess": "label.suggestion",
            "x": "text"
        },
    )
    assert dataset.name == mock_dataset_name

    dataset_records = list(dataset.records(with_suggestions=True))

    assert dataset_records[0].external_id == str(mock_data[0]["external_id"])
    assert dataset_records[1].fields.text == mock_data[1]["x"]
    assert dataset_records[2].suggestions.label == "positive"
    assert dataset_records[2].responses.label[0].value == "negative"
    assert dataset_records[2].responses.label[0].user_id == user.id
