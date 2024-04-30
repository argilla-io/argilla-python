import random
from string import ascii_lowercase

import pytest

from argilla_sdk import Argilla, Dataset, Settings, TextField, TextQuestion, Workspace


@pytest.fixture
def client() -> Argilla:
    return Argilla(api_url="http://localhost:6900")


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
def dataset(client: Argilla, workspace: Workspace) -> Dataset:
    name = "".join(random.choices(ascii_lowercase, k=16))
    settings = Settings(
        fields=[TextField(name="text")],
        questions=[TextQuestion(name="comment", use_markdown=False)],
    )
    dataset = Dataset(
        name=name,
        workspace_id=workspace.id,
        settings=settings,
        client=client,
    )
    dataset.publish()
    yield dataset
    dataset.delete()


def test_list_records_with_start_offset(client: Argilla, dataset: Dataset):
    dataset.records.add(
        [
            {"text": "The record text field", "external_id": 1},
            {"text": "The record text field", "external_id": 2},
        ]
    )

    records = list(dataset.records(start_offset=1))
    assert len(records) == 1
