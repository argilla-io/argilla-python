from argilla_sdk import Argilla, Dataset, Settings, TextField, TextQuestion


class TestDatasetsList:

    def test_list_datasets(self, client: Argilla):
        dataset = Dataset(
            name="test_dataset",
            workspace="test_workspace",
            settings=Settings(fields=[TextField(name="text")], questions=[TextQuestion(name="text_question")]),
            client=client,
        )
        dataset_ = client.datasets(dataset.name)
        if dataset_.exists():
            dataset_.delete()

        dataset.create()
        datasets = client.datasets
        assert len(datasets) > 0, "No datasets were found"

        for ds in datasets:
            if ds.name == "test_dataset":
                assert ds == dataset, "The dataset was not loaded properly"
