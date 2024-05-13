import pytest

import argilla_sdk as rg


@pytest.fixture(scope="session")
def client() -> rg.Argilla:
    client = rg.Argilla()
    yield client


@pytest.fixture(autouse=True)
def cleanup(client: rg.Argilla):
    for workspace in client.workspaces:
        if workspace.name.startswith("test_"):
            for dataset in workspace.datasets:
                dataset.delete()
            workspace.delete()

    for user in client.users:
        if user.username.startswith("test_"):
            user.delete()
