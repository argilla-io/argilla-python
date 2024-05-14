import random
import uuid
from datetime import datetime
from string import ascii_lowercase

import pytest

import argilla_sdk as rg

@pytest.fixture
def dataset(client: rg.Argilla) -> rg.Dataset:
    workspace = client.workspaces[0]
    mock_dataset_name = f"test_add_records{datetime.now().strftime('%Y%m%d%H%M%S')}"
    settings = rg.Settings(
        fields=[
            rg.TextField(name="text"),
        ],
        questions=[
            rg.LabelQuestion(name="label", labels=["positive", "negative"]),
        ],
        vectors=[
            rg.VectorField(name="vector", dimensions=10),
        ],
    )
    dataset = rg.Dataset(
        name=mock_dataset_name,
        workspace=workspace,
        settings=settings,
        client=client,
    )
    dataset.create()
    yield dataset
    dataset.delete()


def test_vectors(client: rg.Argilla, dataset: rg.Dataset):
    mock_data = [
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": uuid.uuid4(),
            "vector": [random.random() for _ in range(10)],
        },
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "external_id": uuid.uuid4(),
            "vector": [random.random() for _ in range(10)],
        },
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": uuid.uuid4(),
            "vector": [random.random() for _ in range(10)],
        },
    ]
    dataset.records.add(records=mock_data)

    dataset_records = list(dataset.records(with_responses=True, with_suggestions=True, with_vectors=["vector"]))
    assert dataset_records[0].external_id == str(mock_data[0]["external_id"])
    assert dataset_records[1].external_id == str(mock_data[1]["external_id"])
    assert dataset_records[2].external_id == str(mock_data[2]["external_id"])
    assert dataset_records[0].vectors.vector == mock_data[0]["vector"]
    assert dataset_records[1].vectors.vector == mock_data[1]["vector"]
    assert dataset_records[2].vectors.vector == mock_data[2]["vector"]


def test_vectors_return_with_bool(client: rg.Argilla, dataset: rg.Dataset):
    mock_data = [
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": uuid.uuid4(),
            "vector": [random.random() for _ in range(10)],
        },
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "external_id": uuid.uuid4(),
            "vector": [random.random() for _ in range(10)],
        },
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": uuid.uuid4(),
            "vector": [random.random() for _ in range(10)],
        },
    ]
    dataset.records.add(records=mock_data)

    dataset_records = list(dataset.records(with_responses=True, with_suggestions=True, with_vectors=True))
    assert dataset_records[0].external_id == str(mock_data[0]["external_id"])
    assert dataset_records[1].external_id == str(mock_data[1]["external_id"])
    assert dataset_records[2].external_id == str(mock_data[2]["external_id"])
    assert dataset_records[0].vectors.vector == mock_data[0]["vector"]
    assert dataset_records[1].vectors.vector == mock_data[1]["vector"]
    assert dataset_records[2].vectors.vector == mock_data[2]["vector"]


def test_vectors_return_with_name(client: rg.Argilla, dataset: rg.Dataset):
    mock_data = [
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": uuid.uuid4(),
            "vector": [random.random() for _ in range(10)],
        },
        {
            "text": "Hello World, how are you?",
            "label": "negative",
            "external_id": uuid.uuid4(),
            "vector": [random.random() for _ in range(10)],
        },
        {
            "text": "Hello World, how are you?",
            "label": "positive",
            "external_id": uuid.uuid4(),
            "vector": [random.random() for _ in range(10)],
        },
    ]
    dataset.records.add(records=mock_data)

    dataset_records = list(dataset.records(with_responses=True, with_suggestions=True, with_vectors="vector"))
    assert dataset_records[0].external_id == str(mock_data[0]["external_id"])
    assert dataset_records[1].external_id == str(mock_data[1]["external_id"])
    assert dataset_records[2].external_id == str(mock_data[2]["external_id"])
    assert dataset_records[0].vectors.vector == mock_data[0]["vector"]
    assert dataset_records[1].vectors.vector == mock_data[1]["vector"]
    assert dataset_records[2].vectors.vector == mock_data[2]["vector"]
