import uuid

import pytest

from argilla_sdk import Dataset, Settings, TextField, LabelQuestion, Argilla, VectorField, FloatMetadataProperty


@pytest.fixture
def dataset():
    return Dataset(
        name=f"test_dataset_{uuid.uuid4().int}",
        settings=Settings(
            fields=[TextField(name="text", use_markdown=False)],
            questions=[LabelQuestion(name="label", labels=["a", "b", "c"])],
        ),
    ).create()


class TestUpdateDatasetFields:

    def test_update_settings(self, client: Argilla, dataset: Dataset):
        settings = dataset.settings

        settings.schema["text"].use_markdown = True
        dataset.settings.vectors.append(VectorField(name="vector", dimensions=10))
        dataset.settings.metadata.append(FloatMetadataProperty(name="metadata"))
        dataset.settings.update()

        dataset = client.datasets(dataset.name)
        assert dataset.schema["text"].use_markdown is True
        assert dataset.schema["vector"].dimensions == 10
        assert isinstance(dataset.schema["metadata"], FloatMetadataProperty)

        settings = dataset.settings
        settings.schema["vector"].title = "A new title for vector"

        settings.update()
        dataset = client.datasets(dataset.name)
        assert dataset.schema["vector"].title == "A new title for vector"
