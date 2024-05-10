import pytest

import argilla_sdk as rg


@pytest.fixture
def client() -> rg.Argilla:
    client = rg.Argilla()
    yield client
