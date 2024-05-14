# `rg.Settings`

`rg.Settings` is used to define the setttings of an Argilla `Dataset`. The settings can be used to configure the
behavior of the dataset, such as the fields, questions, guidelines, metadata, and vectors. The `Settings` class is
passed to the `Dataset` class and used to create the dataset on the server. Once created, the settings of a dataset
cannot be changed.

## Usage Examples

### Creating a new dataset with settings

To create a new dataset with settings, instantiate the `Settings` class and pass it to the `Dataset` class.

```python
import argilla_sdk as rg

settings = rg.Settings(
    guidelines="Select the sentiment of the prompt.",
    fields=[rg.TextField(name="prompt", use_markdown=True)],
    questions=[rg.LabelQuestion(name="sentiment", labels=["positive", "negative"])],
)

dataset = rg.Dataset(name="sentiment_analysis", settings=settings)

# Create the dataset on the server
dataset.create()

```

### Creating multiple datasets with the same settings

To create multiple datasets with the same settings, define the settings once and pass it to each dataset.

```python
import argilla_sdk as rg

settings = rg.Settings(
    guidelines="Select the sentiment of the prompt.",
    fields=[rg.TextField(name="prompt", use_markdown=True)],
    questions=[rg.LabelQuestion(name="sentiment", labels=["positive", "negative"])],
)

dataset1 = rg.Dataset(name="sentiment_analysis_1", settings=settings)
dataset2 = rg.Dataset(name="sentiment_analysis_2", settings=settings)

# Create the datasets on the server
dataset1.create()
dataset2.create()

```

### Creating a dataset with settings from an existing dataset

To create a new dataset with settings from an existing dataset, get the settings from the existing dataset and pass it
to the new dataset.

```python
import argilla_sdk as rg

# Get the settings from an existing dataset
existing_dataset = client.datasets("sentiment_analysis")

# Create a new dataset with the same settings
dataset = rg.Dataset(name="sentiment_analysis_copy", settings=existing_dataset.settings)

# Create the dataset on the server
dataset.create()

```

> To define the settings for fields, questions, metadata, or vectors, refer to the [`rg.TextField`](fields.md), [`rg.LabelQuestion`](questions.md), [`rg.TermsMetadataProperty`](metadata_property.md), and [`rg.VectorField`](vectors.md) class documentation.

---

## Class Reference

### `rg.Settings`

::: argilla_sdk.settings.Settings
    options: 
        heading_level: 3