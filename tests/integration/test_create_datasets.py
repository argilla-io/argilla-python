import pytest

from argilla_sdk import Argilla, Dataset, Settings, TextField, RatingQuestion


@pytest.fixture(scope="session", autouse=True)
def clean_datasets(client: Argilla):
    datasets = client.datasets
    for dataset in datasets:
        if dataset.name.startswith("test_"):
            dataset.delete()
    yield


class TestCreateDatasets:

    def test_create_dataset(self, client: Argilla):
        dataset = Dataset(
            name="test_dataset",
            settings=Settings(
                fields=[TextField(name="test_field")],
                questions=[RatingQuestion(name="test_question", values=[1, 2, 3, 4, 5])],
            ),
        )
        client.datasets.add(dataset)

        assert dataset in client.datasets
        assert dataset.exists()

        created_dataset = client.datasets(name="test_dataset")
        assert created_dataset.settings == dataset.settings
