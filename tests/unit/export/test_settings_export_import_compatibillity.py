import pytest
import uuid
from datetime import datetime
from tempfile import NamedTemporaryFile, TemporaryDirectory

import httpx
from pytest_httpx import HTTPXMock

import argilla_sdk as rg


@pytest.fixture
def settings():
    settings = rg.Settings(
        fields=[
            rg.TextField(name="text", title="text"),
        ],
        metadata=[
            rg.FloatMetadataProperty("source"),
        ],
        questions=[
            rg.LabelQuestion(name="label", title="text", labels=["positive", "negative"]),
        ],
        vectors=[rg.VectorField(name="text_vector", dimensions=3)],
    )
    return settings


@pytest.fixture
def dataset(httpx_mock: HTTPXMock, settings) -> rg.Dataset:
    api_url = "http://test_url"
    client = rg.Argilla(api_url)
    workspace_id = uuid.uuid4()
    workspace_name = "workspace-01"
    mock_workspace = {
        "id": str(workspace_id),
        "name": workspace_name,
        "inserted_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    httpx_mock.add_response(
        json={"items": [mock_workspace]},
        url=f"{api_url}/api/v1/me/workspaces",
        method="GET",
        status_code=200,
    )

    httpx_mock.add_response(
        url=f"{api_url}/api/v1/workspaces/{workspace_id}",
        method="GET",
        status_code=200,
        json=mock_workspace,
    )

    with httpx.Client():
        dataset = rg.Dataset(
            client=client,
            name=f"dataset_{uuid.uuid4()}",
            settings=settings,
            workspace=workspace_name,
        )
        yield dataset


def test_export_settings_to_disk(settings):
    with NamedTemporaryFile() as f:
        settings.to_disk(f.name)
        loaded_settings = rg.Settings.from_disk(f.name)

    assert settings == loaded_settings


def test_export_dataset_to_disk(dataset):
    with TemporaryDirectory(ignore_cleanup_errors=True) as f:
        directory_path = dataset.to_disk(f)
        loaded_dataset = rg.Dataset.from_disk(directory_path)

    assert dataset == loaded_dataset
