import random
import uuid
from datetime import datetime

import pytest

import argilla_sdk as rg


@pytest.fixture
def client() -> rg.Argilla:
    client = rg.Argilla(api_url="http://localhost:6900", api_key="argilla.apikey")
    return client


def test_create_dataset(client):
    workspace_id = client._workspaces.get_by_name(name="argilla").id
    mock_dataset_name = f"test_create_dataset{datetime.now().strftime('%Y%m%d%H%M%S')}"
    dataset = rg.Dataset(
        name=mock_dataset_name,
        workspace_id=workspace_id,
        guidelines="Test guidelines",
        settings=rg.Settings(
            fields=[
                rg.TextField(name="text"),
            ],
            questions=[
                rg.TextQuestion(name="response"),
            ],
        ),
    )
    dataset.publish()
    gotten_dataset = dataset.get()
    assert dataset.id == gotten_dataset.id
    assert dataset.name == mock_dataset_name


def test_add_records(client):
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
            rg.TextQuestion(name="text", use_markdown=False),
        ],
    )
    dataset = rg.Dataset(
        name=mock_dataset_name,
        workspace_id="3b8416c6-ad6f-4641-8567-de6f5a7343ba",
        guidelines="Test guidelines",
        settings=settings,
        client=client,
    )
    dataset.publish()
    records = [
        rg.Record(
            fields={
                "text": record["text"],
            },
            external_id=record["external_id"],
        )
        for record in mock_data
    ]
    dataset.records.add(records=records)
    assert dataset.name == mock_dataset_name
    assert dataset.records[0].external_id == mock_data[0]["external_id"]
    assert dataset.records[1].external_id == mock_data[1]["external_id"]
    assert dataset.records[2].external_id == mock_data[2]["external_id"]
    assert dataset.records[0].fields["text"] == mock_data[0]["text"]
    assert dataset.records[1].fields["text"] == mock_data[1]["text"]
    assert dataset.records[2].fields["text"] == mock_data[2]["text"]


def test_add_records_with_suggestions(client) -> None:
    mock_dataset_name = f"test_add_record_with_suggestions {datetime.now().strftime('%Y%m%d%H%M%S')}"
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
        workspace_id="3b8416c6-ad6f-4641-8567-de6f5a7343ba",
        guidelines="Test guidelines",
        settings=settings,
    )
    dataset.publish()
    dataset.records.add(
        records=[
            rg.Record(
                fields={
                    "text": _record["text"],
                },
                external_id=_record["external_id"],
                suggestions=[
                    rg.Suggestion(
                        question_name="text",
                        value="I'm doing great, thank you!",
                        agent="DaveLLM",
                    )
                ],
            )
            for _record in mock_data
        ]
    )
    assert dataset.name == mock_dataset_name
    assert dataset.records[0].external_id == mock_data[0]["external_id"]
    assert dataset.records[1].fields["text"] == mock_data[1]["text"]
    assert dataset.records[2].suggestions[0].value == "I'm doing great, thank you!"
    assert dataset.records[2].suggestions[0].agent == "DaveLLM"


def test_add_records_with_responses(client) -> None:
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
        workspace_id="3b8416c6-ad6f-4641-8567-de6f5a7343ba",
        guidelines="Test guidelines",
        settings=settings,
    )
    user = rg.User(
        username=f"test_{random.randint(0, 1000)}",
        first_name="test",
        password="testtesttest",
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
