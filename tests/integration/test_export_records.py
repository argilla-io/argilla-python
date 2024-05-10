import random
import uuid
from datetime import datetime
from string import ascii_lowercase

import pytest

import argilla_sdk as rg
from argilla_sdk import Argilla


@pytest.fixture
def dataset(client) -> rg.Dataset:
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
        settings=settings,
        client=client,
    )
    dataset.publish()
    yield dataset
    dataset.delete()


def test_export_records_dict_flattened(client: Argilla, dataset: rg.Dataset):
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
    dataset.records.add(records=mock_data)
    exported_records = dataset.records.to_dict(flatten=True)
    assert len(exported_records) == 5
    assert isinstance(exported_records, dict)
    assert isinstance(exported_records["external_id"], list)
    assert isinstance(exported_records["text"], list)
    assert isinstance(exported_records["label.suggestion"], list)
    assert exported_records["text"] == ["Hello World, how are you?"] * 3


def test_export_records_list_flattened(client: Argilla, dataset: rg.Dataset):
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
    dataset.records.add(records=mock_data)
    exported_records = dataset.records.to_list(flatten=True)
    assert len(exported_records) == len(mock_data)
    assert isinstance(exported_records, list)
    assert isinstance(exported_records[0], dict)
    assert isinstance(exported_records[0]["external_id"], str)
    assert isinstance(exported_records[0]["text"], str)
    assert isinstance(exported_records[0]["label.suggestion"], str)
    assert exported_records[0]["text"] == "Hello World, how are you?"
    assert exported_records[0]["label.suggestion"] == "positive"
    assert exported_records[0]["label.suggestion.score"] is None


def test_export_records_list_nested(client: Argilla, dataset: rg.Dataset):
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
    dataset.records.add(records=mock_data)
    exported_records = dataset.records.to_list(flatten=False)
    assert len(exported_records) == len(mock_data)
    assert exported_records[0]["fields"]["text"] == "Hello World, how are you?"
    assert exported_records[0]["suggestions"]["label"]["value"] == "positive"
    assert exported_records[0]["suggestions"]["label"]["score"] is None


def test_export_records_dict_nested(client: Argilla, dataset: rg.Dataset):
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

    dataset.records.add(records=mock_data)
    exported_records = dataset.records.to_dict(flatten=False)
    assert isinstance(exported_records, dict)
    assert exported_records["fields"][0]["text"] == "Hello World, how are you?"
    assert exported_records["suggestions"][0]["label"]["value"] == "positive"


def test_export_records_dict_nested_orient_index(client: Argilla, dataset: rg.Dataset):
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
    dataset.records.add(records=mock_data)
    exported_records = dataset.records.to_dict(flatten=False, orient="index")
    assert isinstance(exported_records, dict)
    for mock_record, (id_, exported_record) in zip(mock_data, exported_records.items()):
        assert id_ == exported_record["external_id"]
        assert exported_record["fields"]["text"] == mock_record["text"]
        assert exported_record["suggestions"]["label"]["value"] == mock_record["label"]
        assert exported_record["external_id"] == str(mock_record["external_id"])
