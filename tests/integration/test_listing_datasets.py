from argilla_sdk import Argilla, Dataset, Settings, TextField, TextQuestion, Workspace


class TestDatasetsList:

    def test_list_datasets(self, client: Argilla):
        workspace = Workspace(name="test_workspace", client=client)
        workspace.create()

        dataset = Dataset(
            name="test_dataset",
            workspace=workspace.name,
            settings=Settings(fields=[TextField(name="text")], questions=[TextQuestion(name="text_question")]),
            client=client,
        )
        dataset.create()
        datasets = client.datasets
        assert len(datasets) > 0, "No datasets were found"

        for ds in datasets:
            if ds.name == "test_dataset":
                assert ds == dataset, "The dataset was not loaded properly"
