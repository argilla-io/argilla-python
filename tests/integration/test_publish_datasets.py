# Copyright 2024-present, Argilla, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from argilla_sdk import Argilla, Settings, TextField, TextQuestion


@pytest.fixture
def client() -> Argilla:
    client = Argilla(api_url="http://localhost:6900", api_key="owner.apikey")
    return client


def test_publish_datasets(client: "Argilla"):
    ws = client.workspaces("admin")

    new_ws = client.workspaces("new_ws")
    if not new_ws.exists():
        new_ws.create()

    assert new_ws.exists(), "The workspace was not created"

    ds = client.datasets("new_ds", workspace=ws)
    if ds.exists():
        ds.delete()

    assert not ds.exists(), "The dataset was not deleted"

    settings = Settings(
        fields=[TextField(name="text-field")],
        questions=[TextQuestion(name="text-question")],
    )

    ds.configure(settings=settings)
    
    ds.publish()

    assert ds.published(), "The dataset was not published"
