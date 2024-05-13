# `rg.Dataset`

`Dataset` is a class that represents a collection of records. It is used to store and manage records in Argilla.

## Usage Examples

### Creating a Dataset

To create a new dataset you need to define its name and settings.

```python
dataset = rg.Dataset(
    name="my_dataset",
    settings=rg.Settings(
        fields=[
            rg.TextField(name="text"),
        ],
        questions=[
            rg.TextQuestion(name="response"),
        ],
    ),
)
```

For a detail guide of the dataset creation and publication process, see the [Dataset how to guide](/argilla-python/how_to_guides/dataset).

### Retrieving an existing Dataset


To retrieve an existing dataset, use `client.datasets("my_dataset")` instead.

```python
dataset = client.datasets("my_dataset")
```

---

## Class Reference

### `rg.Dataset`

::: argilla_sdk.datasets.Dataset
    options: 
        heading_level: 3