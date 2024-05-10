import pytest

from argilla_sdk import Argilla, Dataset


@pytest.fixture
def client() -> Argilla:
    return Argilla()


class TestDatasetsList:

    def test_list_datasets(self, client: Argilla):
        dataset = client.datasets("test_dataset")
        if dataset.exists():
            dataset.delete()
        dataset.create()

        datasets = client.datasets
        assert len(datasets) > 0, "No datasets were found"

        for ds in datasets:
            if ds.name == "test_dataset":
                assert ds == dataset, "The dataset was not loaded properly"
