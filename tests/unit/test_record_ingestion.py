from uuid import uuid4

import pytest

import argilla_sdk as rg
from argilla_sdk.records._resource import _ingest_record_from_dict


@pytest.fixture
def dataset():
    settings = rg.Settings(
        fields=[rg.TextField(name="prompt")],
        questions=[rg.LabelQuestion(name="label", labels=["negative", "positive"])],
        metadata=[rg.FloatMetadataProperty(name="score")],
        vectors=[rg.VectorField(name="vector", dimensions=3)],
    )

    return rg.Dataset(
        name="test_dataset",
        settings=settings,
    )


def test_ingest_record_from_dict(dataset):
    record = _ingest_record_from_dict(
        dataset=dataset,
        data={
            "prompt": "What is the capital of France?",
            "label": "positive",
        },
    )

    assert record.fields.prompt == "What is the capital of France?"
    assert record.suggestions.label.value == "positive"


def test_ingest_record_from_dict_with_mapping(dataset):
    record = _ingest_record_from_dict(
        dataset=dataset,
        data={
            "my_prompt": "What is the capital of France?",
            "label": "positive",
        },
        mapping={
            "my_prompt": "prompt",
        },
    )

    assert record.fields.prompt == "What is the capital of France?"
    assert record.suggestions.label.value == "positive"


def test_ingest_record_from_dict_with_suggestions(dataset):
    record = _ingest_record_from_dict(
        dataset=dataset,
        data={
            "prompt": "Hello World, how are you?",
            "label": "negative",
        },
    )

    assert record.fields.prompt == "Hello World, how are you?"
    assert record.suggestions.label.value == "negative"


def test_ingest_record_from_dict_with_suggestions_scores(dataset):
    record = _ingest_record_from_dict(
        dataset=dataset,
        data={
            "prompt": "Hello World, how are you?",
            "label": "negative",
            "score": 0.9,
            "model": "model_name",
        },
        mapping={
            "score": "label.suggestion.score",
            "model": "label.suggestion.agent",
        },
    )

    assert record.fields.prompt == "Hello World, how are you?"
    assert record.suggestions.label.value == "negative"
    assert record.suggestions.label.score == 0.9
    assert record.suggestions.label.agent == "model_name"


def test_ingest_record_from_dict_with_suggestions_scores_and_agent(dataset):
    record = _ingest_record_from_dict(
        dataset=dataset,
        data={
            "prompt": "Hello World, how are you?",
            "label": "negative",
            "score": 0.9,
            "model": "model_name",
        },
        mapping={
            "score": "label.suggestion.score",
            "model": "label.suggestion.agent",
        },
    )

    assert record.fields.prompt == "Hello World, how are you?"
    assert record.suggestions.label.value == "negative"
    assert record.suggestions.label.score == 0.9
    assert record.suggestions.label.agent == "model_name"


def test_ingest_record_from_dict_with_responses(dataset):
    user_id = uuid4()
    record = _ingest_record_from_dict(
        dataset=dataset,
        data={
            "prompt": "Hello World, how are you?",
            "label": "negative",
        },
        mapping={
            "label": "label.response",
        },
        user_id=user_id,
    )

    assert record.fields.prompt == "Hello World, how are you?"
    assert record.responses.label[0].value == "negative"
    assert record.responses.label[0].user_id == user_id


def test_ingest_record_from_dict_with_id_as_id(dataset):
    record_id = uuid4()
    record = _ingest_record_from_dict(
        dataset=dataset,
        data={
            "prompt": "Hello World, how are you?",
            "label": "negative",
            "id": record_id,
        },
    )

    assert record.fields.prompt == "Hello World, how are you?"
    assert record.id == record_id


def test_ingest_record_from_dict_with_id_and_mapping(dataset):
    record_id = uuid4()
    record = _ingest_record_from_dict(
        dataset=dataset,
        data={
            "prompt": "Hello World, how are you?",
            "label": "negative",
            "test_id": record_id,
        },
        mapping={
            "test_id": "id",
        },
    )

    assert record.fields.prompt == "Hello World, how are you?"
    assert record.id == record_id


def test_ingest_record_from_dict_with_metadata(dataset):
    record = _ingest_record_from_dict(
        dataset=dataset,
        data={
            "prompt": "Hello World, how are you?",
            "label": "negative",
            "score": 0.9,
        },
    )

    assert record.fields.prompt == "Hello World, how are you?"
    assert record.suggestions.label.value == "negative"
    assert record.metadata["score"] == 0.9


def test_ingest_record_from_dict_with_metadata_and_mapping(dataset):
    record = _ingest_record_from_dict(
        dataset=dataset,
        data={
            "prompt": "Hello World, how are you?",
            "label": "negative",
            "test_score": 0.9,
        },
        mapping={
            "test_score": "score",
        },
    )

    assert record.fields.prompt == "Hello World, how are you?"
    assert record.suggestions.label.value == "negative"
    assert record.metadata["score"] == 0.9


def test_ingest_record_from_dict_with_vectors(dataset):
    record = _ingest_record_from_dict(
        dataset=dataset,
        data={
            "prompt": "Hello World, how are you?",
            "label": "negative",
            "vector": [1, 2, 3],
        },
    )

    assert record.fields.prompt == "Hello World, how are you?"
    assert record.suggestions.label.value == "negative"
    assert record.vectors.vector == [1, 2, 3]


def test_ingest_record_from_dict_with_vectors_and_mapping(dataset):
    record = _ingest_record_from_dict(
        dataset=dataset,
        data={
            "prompt": "Hello World, how are you?",
            "label": "negative",
            "test_vector": [1, 2, 3],
        },
        mapping={
            "test_vector": "vector",
        },
    )

    assert record.fields.prompt == "Hello World, how are you?"
    assert record.suggestions.label.value == "negative"
    assert record.vectors.vector == [1, 2, 3]
