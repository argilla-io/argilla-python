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
        external_id=str(uuid.uuid4()),
    )


def test_export_to_dict(record):
    record_dict = GenericExportMixin._record_to_dict(record)
    imported_record = _dict_to_record(record_dict)

    assert record.responses[0].value == imported_record.responses[0].value
    assert record.suggestions[0].value == imported_record.suggestions[0].value
    for key, value in record.metadata.to_dict().items():
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
    for key, value in record.metadata.to_dict().items():
        assert imported_record.metadata[key] == value
    assert record.fields.text == imported_record.fields.text
    assert record.vectors.text == imported_record.vectors.text
