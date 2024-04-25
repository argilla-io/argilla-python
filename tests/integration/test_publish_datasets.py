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

from argilla_sdk import Argilla, Settings, TextField, TextQuestion, SpanQuestion


@pytest.fixture
def client() -> Argilla:
    return Argilla(api_url="http://localhost:6900")


def test_publish_dataset(client: "Argilla"):
    new_ws = client.workspaces("new_ws")
    if not new_ws.exists():
        new_ws.create()

    assert new_ws.exists(), "The workspace was not created"

    ds = client.datasets("new_ds", workspace=new_ws)
    if ds.exists():
        ds.delete()

    assert not ds.exists(), "The dataset was not deleted"

    ds.settings = Settings(
        fields=[TextField(name="text-field")],
        questions=[
            TextQuestion(name="text-question"),
            SpanQuestion(name="span-question", field="text-field", labels=["label1", "label2"]),
        ],
    )

    ds.publish()
    assert ds.is_published, "The dataset was not published"

    published_ds = client.datasets(name=ds.name, workspace=new_ws)
    assert published_ds.exists(), "The dataset was not found"
    assert published_ds.settings == ds.settings, "The settings were not saved"
