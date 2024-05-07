import random
from string import ascii_lowercase

import pytest

import argilla_sdk as rg
from argilla_sdk import Argilla, Dataset, Settings, TextField, Workspace, LabelQuestion


@pytest.fixture
def client() -> Argilla:
    return Argilla(api_url="http://localhost:6900", api_key="argilla.apikey")


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
def dataset_with_metadata(client: Argilla, workspace: Workspace) -> Dataset:
    name = "".join(random.choices(ascii_lowercase, k=16))
    settings = Settings(
        fields=[TextField(name="text")],
        questions=[LabelQuestion(name="label", labels=["positive", "negative"])],
        metadata=[
            rg.TermsMetadataProperty(name="category", options=["A", "B", "C"]),
        ],
    )
    dataset = Dataset(
        name=name,
        workspace=workspace.name,
        settings=settings,
        client=client,
    )
    dataset.publish()
    dataset.get()
    return dataset


def test_create_dataset_with_metadata(client: Argilla, workspace: Workspace) -> Dataset:
    name = "".join(random.choices(ascii_lowercase, k=16))
    settings = Settings(
        fields=[TextField(name="text")],
        questions=[LabelQuestion(name="label", labels=["positive", "negative"])],
        metadata=[
            rg.TermsMetadataProperty(name="category", options=["A", "B", "C"]),
        ],
    )
    dataset = Dataset(
        name=name,
        workspace=workspace.name,
        settings=settings,
        client=client,
    )
    dataset.publish()
    dataset.get()

    assert dataset.settings.metadata[0].name == "category"


def test_add_record_with_metadata(dataset_with_metadata: Dataset):
    records = [
        {"text": "text", "label": "positive", "category": "A"},
        {"text": "text", "label": "negative", "category": "B"},
    ]

    dataset_with_metadata.records.add(records)

    for idx, record in enumerate(dataset_with_metadata.records):
        assert record.metadata.category == records[idx]["category"]
        assert record.metadata["category"] == records[idx]["category"]
        assert len(record._model.metadata) == 1
        assert record._model.metadata[0].value == records[idx]["category"]
        assert record._model.metadata[0].name == "category"

def test_add_record_with_mapped_metadata(dataset_with_metadata: Dataset):
    records = [
        {"text": "text", "label": "positive", "my_category": "A"},
        {"text": "text", "label": "negative", "my_category": "B"},
    ]

    dataset_with_metadata.records.add(records, mapping={"my_category": "category"})

    for idx, record in enumerate(dataset_with_metadata.records):
        assert record.metadata.category == records[idx]["my_category"]
        assert record.metadata["category"] == records[idx]["my_category"]
        assert len(record._model.metadata) == 1
        assert record._model.metadata[0].value == records[idx]["my_category"]
        assert record._model.metadata[0].name == "category"
