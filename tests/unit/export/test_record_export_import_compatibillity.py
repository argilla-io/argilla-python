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

import json
import uuid

import pytest

import argilla_sdk as rg
from argilla_sdk.records._export._generic import GenericExportMixin
from argilla_sdk.records._helpers import _dict_to_record


@pytest.fixture
def user_id():
    return str(uuid.uuid4())


@pytest.fixture
def record(user_id):
    return rg.Record(
        fields={"text": "Hello World, how are you?"},
        suggestions=[
            rg.Suggestion("label", "positive", score=0.9),
            rg.Suggestion("topics", ["topic1", "topic2"], score=[0.9, 0.8]),
        ],
        responses=[rg.Response("label", "positive", user_id=user_id)],
        metadata={"source": "twitter", "language": "en"},
        vectors=[rg.Vector("text", [0, 0, 0])],
        id=str(uuid.uuid4()),
    )


def test_export_to_dict(record):
    record_dict = GenericExportMixin._record_to_dict(record)
    imported_record = _dict_to_record(record_dict)

    assert record.responses[0].value == imported_record.responses[0].value
    assert record.suggestions[0].value == imported_record.suggestions[0].value
    for key, value in record.metadata.items():
        assert imported_record.metadata[key] == value
    assert record.fields.text == imported_record.fields.text
    assert record.vectors.text == imported_record.vectors.text


def test_export_to_dict_json(record):
    record_dict = GenericExportMixin._record_to_dict(record)
    record_dict = json.dumps(record_dict)
    record_dict = json.loads(record_dict)
    imported_record = _dict_to_record(record_dict)

    assert record.responses[0].value == imported_record.responses[0].value
    assert record.suggestions[0].value == imported_record.suggestions[0].value
    for key, value in record.metadata.items():
        assert imported_record.metadata[key] == value
    assert record.fields.text == imported_record.fields.text
    assert record.vectors.text == imported_record.vectors.text
