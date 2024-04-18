import random
import uuid
from datetime import datetime

import pytest

import argilla_sdk as rg


@pytest.fixture
def client() -> rg.Argilla:
    client = rg.Argilla(api_url="http://localhost:6900", api_key="argilla.apikey")
    return client


def test_vectors(client):
    workspace_id = client.workspaces[0].id
    mock_dataset_name = f"test_add_records{datetime.now().strftime('%Y%m%d%H%M%S')}"
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
        workspace_id=workspace_id,
        settings=settings,
        client=client,
    )
    dataset.publish()
    dataset.records.add(records=mock_data)

    dataset_records = list(dataset.records(with_responses=True, with_suggestions=True, with_vectors=True))

    assert dataset.name == mock_dataset_name
    assert dataset_records[0].external_id == str(mock_data[0]["external_id"])
    assert dataset_records[1].external_id == str(mock_data[1]["external_id"])
    assert dataset_records[2].external_id == str(mock_data[2]["external_id"])
    assert dataset_records[0].vectors.vector == mock_data[0]["vector"]
    assert dataset_records[1].vectors.vector == mock_data[1]["vector"]
    assert dataset_records[2].vectors.vector == mock_data[2]["vector"]
