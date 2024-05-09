import random

import pytest

import argilla_sdk as rg


@pytest.fixture
def client() -> rg.Argilla:
    client = rg.Argilla(api_url="http://localhost:6900", api_key="argilla.apikey")
    return client


@pytest.fixture
def dataset(client: rg.Argilla):
    ws = client.workspaces[0]
    settings = rg.Settings(
        guidelines=f"my_dataset_{random.randint(1, 100)}",
        fields=[rg.TextField(name="text", required=True, title="Text")],
        questions=[
            rg.LabelQuestion(name="label", title="Label", labels=["positive", "negative"]),
            rg.RankingQuestion(name="ranking", title="Ranking", values=["1", "2", "3"]),
        ],
    )

    ds = rg.Dataset(
        name=f"my_dataset_{random.randint(1, 100)}",
        settings=settings,
        client=client,
        workspace=ws,
    )
    ds.publish()
    yield ds
    ds.delete()


def test_ranking_question_with_suggestions(dataset: rg.Dataset):
    dataset.records.add(
        [
            {"text": "This is a test text", "label": "positive", "ranking": ["2", "1", "3"]},
        ],
    )
    assert next(iter(dataset.records(with_suggestions=True))).suggestions.ranking.value == ["2", "1", "3"]


def test_ranking_question_with_responses(dataset: rg.Dataset):
    dataset.records.add(
        [
            {"text": "This is a test text", "label": "positive", "ranking_": ["2"]},
        ],
        mapping={"ranking_": "ranking.response"},
    )
    assert next(iter(dataset.records(with_responses=True))).responses.ranking[0].value == ["2"]
