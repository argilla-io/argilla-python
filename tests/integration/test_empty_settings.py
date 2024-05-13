import random
from string import ascii_lowercase

import pytest

from argilla_sdk import Argilla, Dataset, Settings, Workspace, TextQuestion, TextField
from argilla_sdk._exceptions import SettingsError

@pytest.fixture
def workspace(client: Argilla) -> Workspace:
    workspace = client.workspaces("test-workspace")
    if not workspace.exists():
        workspace.create()
    yield workspace

    for dataset in workspace.list_datasets():
        client.api.datasets.delete(dataset.id)

    workspace.delete()

    
def test_dataset_empty_settings(client: Argilla, workspace: Workspace) -> Dataset:
    name = "".join(random.choices(ascii_lowercase, k=16))
    settings = Settings()
    dataset = Dataset(
        name=name,
        workspace=workspace.name,
        settings=settings,
        client=client,
    )
    with pytest.raises(expected_exception=SettingsError):
        dataset.publish()


def test_dataset_no_fields(client: Argilla, workspace: Workspace) -> Dataset:
    name = "".join(random.choices(ascii_lowercase, k=16))
    settings = Settings(
        questions=[
            TextQuestion(name="text_question"),
        ],
    )
    dataset = Dataset(
        name=name,
        workspace=workspace.name,
        settings=settings,
        client=client,
    )
    with pytest.raises(expected_exception=SettingsError):
        dataset.publish()
    

def test_dataset_no_questions(client: Argilla, workspace: Workspace) -> Dataset:
    name = "".join(random.choices(ascii_lowercase, k=16))
    settings = Settings(
        fields=[
            TextField(name="text_field"),
        ],
    )
    dataset = Dataset(
        name=name,
        workspace=workspace.name,
        settings=settings,
        client=client,
    )
    with pytest.raises(expected_exception=SettingsError):
        dataset.publish()